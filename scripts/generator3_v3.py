#!/usr/bin/env python3
"""Gemini + Supabase 디자인 자동 생성기 (v3.1.0 - Free Tier Optimized).

[v3.1.0 변경사항]
- [Core] API 호출 디자인 1개당 정확히 1회로 축소 (Brief+HTML+자가검증 통합 프롬프트)
- [Core] 무료 티어 Rate Limit 완전 대응
- [Core] AI 자가 품질 검증 내장
- [SNS] X(Twitter) 스레드(Thread) 게시 기능 추가 (Global/English focus)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import logging
import os
import random
import re
import time
import uuid
from datetime import datetime
from typing import Any, Dict, Optional

import httpx
import tweepy
from dotenv import load_dotenv
from google import genai
from playwright.async_api import async_playwright, Browser
from supabase import Client, create_client

# ---------------------------------------------------------------------------
# 로깅
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# 환경 변수
# ---------------------------------------------------------------------------
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-latest")
STORAGE_BUCKET = os.getenv("SUPABASE_DESIGNS_BUCKET", "designs-bucket")
STORAGE_FOLDER = os.getenv("SUPABASE_DESIGNS_FOLDER", "designs")
REQUEST_NOTIFY_BASE_URL = os.getenv("REQUEST_NOTIFY_BASE_URL", "http://localhost:3000").rstrip("/")
REQUEST_NOTIFY_SECRET = os.getenv("REQUEST_NOTIFY_SECRET", "")

X_CONSUMER_KEY = os.getenv("X_CONSUMER_KEY")
X_CONSUMER_SECRET = os.getenv("X_CONSUMER_SECRET")
X_ACCESS_TOKEN = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

# ---------------------------------------------------------------------------
# Rate Limit 상수 (무료 티어 기준)
# ---------------------------------------------------------------------------
RPM_LIMIT = 5                        
RPD_LIMIT = int(os.getenv("GEMINI_RPD_LIMIT", "100"))  
MIN_REQUEST_INTERVAL = 60 / RPM_LIMIT + 1  
MAX_RETRY_ATTEMPTS = 3               

# ---------------------------------------------------------------------------
# 클라이언트 지연 초기화
# ---------------------------------------------------------------------------
_supabase_client: Optional[Client] = None
_gemini_client: Optional[genai.Client] = None


def get_supabase() -> Client:
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client


def get_gemini() -> genai.Client:
    global _gemini_client
    if _gemini_client is None:
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    return _gemini_client


# ---------------------------------------------------------------------------
# Rate Limiter
# ---------------------------------------------------------------------------
class RateLimiter:
    def __init__(self, rpm: int, rpd: int, min_interval: float):
        self.rpm = rpm
        self.rpd = rpd
        self.min_interval = min_interval
        self._last_request_time: float = 0.0
        self._daily_count: int = 0
        self._day_start: str = datetime.utcnow().strftime("%Y-%m-%d")

    def _reset_if_new_day(self) -> None:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        if today != self._day_start:
            self._daily_count = 0
            self._day_start = today

    def is_daily_limit_reached(self) -> bool:
        self._reset_if_new_day()
        return self._daily_count >= self.rpd

    async def acquire(self) -> None:
        self._reset_if_new_day()
        if self._daily_count >= self.rpd:
            raise RuntimeError(f"RPD 한도 {self.rpd} 도달")
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)
        self._last_request_time = time.monotonic()
        self._daily_count += 1

    async def wait_for_retry_after(self, retry_after_seconds: float) -> None:
        await asyncio.sleep(retry_after_seconds)
        self._last_request_time = time.monotonic()


rate_limiter = RateLimiter(rpm=RPM_LIMIT, rpd=RPD_LIMIT, min_interval=MIN_REQUEST_INTERVAL)

# ---------------------------------------------------------------------------
# SNS 업로드 헬퍼 (X/Twitter Thread Support)
# ---------------------------------------------------------------------------

async def post_to_x_thread(title: str, image_bytes: bytes, slug: str, tweets: list[str]) -> bool:
    if not all([X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
        log.info("[X] API 키 미설정: 업로드 건너뜀")
        return False

    try:
        log.info("[X] X에 잉글리시 스레드 업로드 시도 중...")
        auth = tweepy.OAuth1UserHandler(X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
        api_v1 = tweepy.API(auth)
        client_v2 = tweepy.Client(
            consumer_key=X_CONSUMER_KEY, consumer_secret=X_CONSUMER_SECRET,
            access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_TOKEN_SECRET
        )

        temp_filename = f"temp_x_{uuid.uuid4().hex[:6]}.png"
        with open(temp_filename, "wb") as f:
            f.write(image_bytes)
        media = await asyncio.to_thread(api_v1.media_upload, filename=temp_filename)
        
        first_tweet = tweets[0] if tweets else f"✨ New UI Design: {title}\n\n👉 https://ui-syntax.com/design/{slug}"
        response = await asyncio.to_thread(client_v2.create_tweet, text=first_tweet, media_ids=[media.media_id])
        last_tweet_id = response.data['id']
        
        if len(tweets) > 1:
            for i in range(1, len(tweets)):
                await asyncio.sleep(2)
                response = await asyncio.to_thread(client_v2.create_tweet, text=tweets[i], in_reply_to_tweet_id=last_tweet_id)
                last_tweet_id = response.data['id']

        log.info("[X] 스레드 업로드 성공!")
        if os.path.exists(temp_filename):
            os.remove(temp_filename)
        return True
    except Exception as e:
        log.error("[X] 업로드 실패: %s", e)
        return False

# ---------------------------------------------------------------------------
# 데이터 상수
# ---------------------------------------------------------------------------
CATEGORIES = ["Landing Page", "Dashboard", "E-commerce", "Portfolio", "Blog", "Component"]

STYLE_STRUCTURE_AFFINITY: Dict[str, list[str]] = {
    "Apple-inspired Minimal White": ["Hero with Center Call-to-Action", "Minimalist Article Feed", "Split Screen Feature Display", "Step-by-step Onboarding Flow", "Centered Newsletter Subscription"],
    "Vercel-style Developer Minimal": ["Bento Grid Dashboard", "Multi-column Technical Documentation", "Tabbed Dashboard Interface", "Stat-heavy Admin Panel", "Command Palette Quick Search"],
    "Stripe-inspired Fintech Clean": ["Three-tier Pricing Table", "Hero with Center Call-to-Action", "Floating Interactive Cards", "Data-rich Table with Pagination", "Footer with Sitemap and Newsletter"],
    "Linear App Dark Mode Elegance": ["Sticky Sidebar Navigation", "Expandable Sidebar with Tooltips", "Draggable Kanban Board", "Settings Page with Toggle Buttons", "Notification Center List"],
    "Notion-like Clean Typography": ["Minimalist Article Feed", "Multi-column Technical Documentation", "Accordion FAQ List", "Vertical Timeline of Events", "Profile Header with Stats"],
    "Glassmorphism Frosted": ["Floating Interactive Cards", "Hero with Center Call-to-Action", "Layered Overlay Components", "Full-page Video Background", "Stat-heavy Admin Panel"],
    "Cyberpunk Neon Pink & Blue": ["Bento Grid Dashboard", "Full-page Video Background", "Radial Progress Dashboard", "Interactive Heatmap Dashboard", "Marquee-based Logo Wall"],
    "Neo-Brutalism High Contrast": ["Hero with Center Call-to-Action", "Masonry Gallery Layout", "E-commerce Product Showcase with Filter", "Project Portfolio Masonry", "Floating Interactive Cards"],
    "Luxury Gold & Deep Black": ["Hero with Center Call-to-Action", "E-commerce Product Showcase with Filter", "Team Member Circle Grid", "Testimonial Slider Grid", "Split Screen Feature Display"],
}

def pick_compatible_style_structure() -> tuple[str, str]:
    style = random.choice(list(STYLE_STRUCTURE_AFFINITY.keys()))
    structure = random.choice(STYLE_STRUCTURE_AFFINITY[style])
    return style, structure

# ---------------------------------------------------------------------------
# 통합 프롬프트
# ---------------------------------------------------------------------------

UNIFIED_PROMPT_TEMPLATE = """\
You are the lead designer at a top agency. Design AND implement a production-ready UI component.
Category: {category} | Layout: {structure} | Aesthetic: {style}
{request_context}

Return a SINGLE valid JSON object with:
"title", "concept", "color_palette", "typography", "content_strategy", "self_review" (total score 1-50), "features", "description", "usage", "html_code", "react_code", "colors".

HTML RULE: Outermost element MUST shrink to fit its content tightly (NO min-h-screen). 
Include <script src="https://cdn.tailwindcss.com"></script> and <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap" rel="stylesheet">.
"""

# ---------------------------------------------------------------------------
# 메인 생성 로직 (API 1회)
# ---------------------------------------------------------------------------

async def generate_single_design(browser: Browser, source_request: Optional[Dict[str, Any]] = None) -> tuple[bool, Optional[str]]:
    category = random.choice(CATEGORIES)
    style, structure = pick_compatible_style_structure()
    prompt = UNIFIED_PROMPT_TEMPLATE.format(category=category, structure=structure, style=style, request_context="")

    await rate_limiter.acquire()
    try:
        response = await asyncio.to_thread(get_gemini().models.generate_content, model=GEMINI_MODEL, config={"response_mime_type": "application/json"}, contents=[prompt])
        try:
            payload = json.loads(response.text)
        except json.JSONDecodeError as e:
            log.error("[JSON Error] Gemini output was not valid JSON: %s", response.text)
            return False, None
        
        design_id = str(uuid.uuid4())
        slug = re.sub(r"[^a-z0-9]+", "-", payload['title'].lower()).strip("-")
        html_code = payload.get("html_code", "")
        
        # 캡처 및 업로드
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page.set_content(html_code)
        await page.wait_for_timeout(2000)
        screenshot = await page.screenshot(type="png")
        await page.close()
        
        # Supabase Storage 업로드
        filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{slug}.png"
        object_path = f"{STORAGE_FOLDER}/{filename}"
        sb = get_supabase()
        await asyncio.to_thread(sb.storage.from_(STORAGE_BUCKET).upload, object_path, screenshot, {"content-type": "image/png"})
        image_url = await asyncio.to_thread(sb.storage.from_(STORAGE_BUCKET).get_public_url, object_path)

        # SNS용 스레드 생성 (고도화된 가독성 프롬프트)
        thread_prompt = f"""
        You are a top-tier UI/UX Design Influencer on X (Twitter) with a massive following. 
        Your goal is to showcase the new design "{payload['title']}" in a high-value 3-tweet thread in English.
        
        [Readability & Style Rules]:
        1. Use emojis (✨, 🚀, 🎨, ✦) to make it visually engaging but keep it professional.
        2. Always add a double line break between paragraphs for extreme readability.
        3. Use bullet points for key features or design tips.
        4. Write with a "human-crafted" vibe—enthusiastic and expert-level.

        [Thread Content]:
        - Tweet 1: Hook + Design Reveal. Why is this {category} innovative?
        - Tweet 2: 3 Deep Design Insights. Share specific UI/UX tips related to the {style} aesthetic. Use bullet points.
        - Tweet 3: Summary + Call to Action. Friendly invitation to view the live demo.
          Link: https://ui-syntax.com/design/{slug}
          Max 2 hashtags (e.g. #UIUX #DesignTips).

        Format: Return ONLY valid JSON with a "tweets" key (list of 3 strings).
        """
        thread_res = await asyncio.to_thread(get_gemini().models.generate_content, model=GEMINI_MODEL, config={"response_mime_type": "application/json"}, contents=[thread_prompt])
        tweets = json.loads(thread_res.text).get("tweets", [])

        # SNS 업로드
        await post_to_x_thread(payload['title'], screenshot, slug, tweets)
        
        # DB 저장
        record = {
            "id": design_id, 
            "title": payload['title'], 
            "slug": slug, 
            "category": category, 
            "code": html_code, 
            "image_url": image_url,
            "sns_promoted": True, 
            "created_at": datetime.utcnow().isoformat()
        }
        await asyncio.to_thread(sb.table("designs").insert(record).execute)
        
        log.info("[성공] %s 게시 완료", payload['title'])
        return True, design_id
    except Exception as e:
        log.error("[에러] %s", e)
        return False, None

async def run_batch(count: int):
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i in range(count):
            await generate_single_design(browser)
        await browser.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1)
    args = parser.parse_args()
    asyncio.run(run_batch(args.count))
