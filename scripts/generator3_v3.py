#!/usr/bin/env python3
"""Gemini + Supabase 디자인 자동 생성기 (v3.1.0 - Free Tier Optimized).

[v3.1.0 변경사항]
- [Core] API 호출 디자인 1개당 정확히 1회로 축소 (Brief+HTML+자가검증 통합 프롬프트)
- [Core] 무료 티어 Rate Limit 완전 대응
    · RPM 5 → 요청 간 최소 13초 강제 대기 (여유 1초 포함)
    · RPD 100 → 일일 호출 횟수 카운터 + 한도 초과 시 자동 중단
    · 429 에러 → Retry-After 헤더 파싱 후 정확한 시간만큼 대기
- [Core] AI 자가 품질 검증 내장 (별도 API 호출 0회)
    · 응답 JSON에 self_review 키 포함 → 35점 미만 시 해당 결과 저장 안 함
- [Fix] 모든 Supabase 호출 asyncio.to_thread 래핑
- [Fix] ensure_unique_slug 무한루프 방어 (100회 + UUID 폴백)
- [Fix] httpx.AsyncClient 알림 전송
- [Fix] 지수 백오프 재시도
- [Fix] 스크린샷 폰트/이미지 완전 로딩 대기

무료 티어 기준 (2025-12 이후):
- Gemini 2.5 Pro: 5 RPM / 100 RPD
- 디자인 1개 = API 1회 → 하루 최대 100개 생성 가능
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

# ---------------------------------------------------------------------------
# Rate Limit 상수 (무료 티어 기준)
# ---------------------------------------------------------------------------
RPM_LIMIT = 5                        # 분당 최대 요청 수
RPD_LIMIT = int(os.getenv("GEMINI_RPD_LIMIT", "100"))  # 일일 최대 요청 수
MIN_REQUEST_INTERVAL = 60 / RPM_LIMIT + 1  # 13초 (12초 + 여유 1초)
MAX_RETRY_ATTEMPTS = 3               # 에러 시 최대 재시도 횟수

# ---------------------------------------------------------------------------
# 클라이언트 지연 초기화
# ---------------------------------------------------------------------------
_supabase_client: Optional[Client] = None
_gemini_client: Optional[genai.Client] = None


def get_supabase() -> Client:
    global _supabase_client
    if _supabase_client is None:
        if not all([SUPABASE_URL, SUPABASE_KEY]):
            raise RuntimeError("SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY가 필요합니다.")
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client


def get_gemini() -> genai.Client:
    global _gemini_client
    if _gemini_client is None:
        if not GEMINI_API_KEY:
            raise RuntimeError("GEMINI_API_KEY가 필요합니다.")
        _gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    return _gemini_client


# ---------------------------------------------------------------------------
# Rate Limiter (RPM + RPD 동시 관리)
# ---------------------------------------------------------------------------
class RateLimiter:
    """무료 티어 RPM/RPD 제한을 관리하는 토큰 버킷."""

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
            log.info("[RateLimit] 날짜 변경 → 일일 카운터 초기화 (%d → 0)", self._daily_count)
            self._daily_count = 0
            self._day_start = today

    def is_daily_limit_reached(self) -> bool:
        self._reset_if_new_day()
        return self._daily_count >= self.rpd

    async def acquire(self) -> None:
        """요청 전 반드시 호출. 필요한 경우 자동 대기."""
        self._reset_if_new_day()

        if self._daily_count >= self.rpd:
            raise RuntimeError(
                f"일일 요청 한도 {self.rpd}회 도달. 자정(태평양 시간) 이후 재시작하세요."
            )

        elapsed = time.monotonic() - self._last_request_time
        if elapsed < self.min_interval:
            wait = self.min_interval - elapsed
            log.info("[RateLimit] RPM 대기 중... %.1f초", wait)
            await asyncio.sleep(wait)

        self._last_request_time = time.monotonic()
        self._daily_count += 1
        log.info("[RateLimit] API 호출 %d/%d (일일)", self._daily_count, self.rpd)

    async def wait_for_retry_after(self, retry_after_seconds: float) -> None:
        """429 응답의 Retry-After만큼 정확히 대기."""
        wait = max(retry_after_seconds, self.min_interval)
        log.warning("[RateLimit] 429 수신 → %.0f초 대기 후 재시도", wait)
        await asyncio.sleep(wait)
        self._last_request_time = time.monotonic()


# 전역 Rate Limiter
rate_limiter = RateLimiter(rpm=RPM_LIMIT, rpd=RPD_LIMIT, min_interval=MIN_REQUEST_INTERVAL)

# ---------------------------------------------------------------------------
# 데이터 상수
# ---------------------------------------------------------------------------
CATEGORIES = ["Landing Page", "Dashboard", "E-commerce", "Portfolio", "Blog", "Component"]

STYLE_STRUCTURE_AFFINITY: Dict[str, list[str]] = {
    "Apple-inspired Minimal White": [
        "Hero with Center Call-to-Action",
        "Minimalist Article Feed",
        "Split Screen Feature Display",
        "Step-by-step Onboarding Flow",
        "Centered Newsletter Subscription",
    ],
    "Vercel-style Developer Minimal": [
        "Bento Grid Dashboard",
        "Multi-column Technical Documentation",
        "Tabbed Dashboard Interface",
        "Stat-heavy Admin Panel",
        "Command Palette Quick Search",
    ],
    "Stripe-inspired Fintech Clean": [
        "Three-tier Pricing Table",
        "Hero with Center Call-to-Action",
        "Floating Interactive Cards",
        "Data-rich Table with Pagination",
        "Footer with Sitemap and Newsletter",
    ],
    "Linear App Dark Mode Elegance": [
        "Sticky Sidebar Navigation",
        "Expandable Sidebar with Tooltips",
        "Draggable Kanban Board",
        "Settings Page with Toggle Buttons",
        "Notification Center List",
    ],
    "Notion-like Clean Typography": [
        "Minimalist Article Feed",
        "Multi-column Technical Documentation",
        "Accordion FAQ List",
        "Vertical Timeline of Events",
        "Profile Header with Stats",
    ],
    "Glassmorphism Frosted": [
        "Floating Interactive Cards",
        "Hero with Center Call-to-Action",
        "Layered Overlay Components",
        "Full-page Video Background",
        "Stat-heavy Admin Panel",
    ],
    "Cyberpunk Neon Pink & Blue": [
        "Bento Grid Dashboard",
        "Full-page Video Background",
        "Radial Progress Dashboard",
        "Interactive Heatmap Dashboard",
        "Marquee-based Logo Wall",
    ],
    "Neo-Brutalism High Contrast": [
        "Hero with Center Call-to-Action",
        "Masonry Gallery Layout",
        "E-commerce Product Showcase with Filter",
        "Project Portfolio Masonry",
        "Floating Interactive Cards",
    ],
    "Luxury Gold & Deep Black": [
        "Hero with Center Call-to-Action",
        "E-commerce Product Showcase with Filter",
        "Team Member Circle Grid",
        "Testimonial Slider Grid",
        "Split Screen Feature Display",
    ],
    "Soft Pastel Gradient": [
        "Centered Newsletter Subscription",
        "Step-by-step Onboarding Flow",
        "Multi-step Interactive Quiz",
        "Profile Header with Stats",
        "Testimonial Slider Grid",
    ],
    "Deep Ocean Dark Mode": [
        "Bento Grid Dashboard",
        "Tabbed Dashboard Interface",
        "Live Activity Feed Sidebar",
        "Radial Progress Dashboard",
        "Data-rich Table with Pagination",
    ],
    "Enterprise Professional Blue": [
        "Stat-heavy Admin Panel",
        "Data-rich Table with Pagination",
        "Three-tier Pricing Table",
        "Multi-column Technical Documentation",
        "Settings Page with Toggle Buttons",
    ],
    "Japanese Zen Minimal": [
        "Minimalist Article Feed",
        "Hero with Center Call-to-Action",
        "Clean Contact Form with Map",
        "Centered Newsletter Subscription",
        "Vertical Timeline of Events",
    ],
    "Claymorphism Soft 3D": [
        "Floating Interactive Cards",
        "Step-by-step Onboarding Flow",
        "Multi-step Interactive Quiz",
        "Bento Grid Dashboard",
        "Three-tier Pricing Table",
    ],
    "Modern Swiss Typographic": [
        "Hero with Center Call-to-Action",
        "Minimalist Article Feed",
        "Masonry Gallery Layout",
        "Project Portfolio Masonry",
        "Multi-column Technical Documentation",
    ],
    "Retro 80s Synthwave": [
        "Full-page Video Background",
        "Marquee-based Logo Wall",
        "Hero with Center Call-to-Action",
        "Masonry Gallery Layout",
        "Horizontal Scroll Feature List",
    ],
}


def pick_compatible_style_structure() -> tuple[str, str]:
    style = random.choice(list(STYLE_STRUCTURE_AFFINITY.keys()))
    structure = random.choice(STYLE_STRUCTURE_AFFINITY[style])
    return style, structure


# ---------------------------------------------------------------------------
# 통합 프롬프트 (API 1회 = 설계 + 구현 + 자가검증)
# ---------------------------------------------------------------------------

UNIFIED_PROMPT_TEMPLATE = """\
You are the lead designer who shipped Linear.app's 2024 redesign AND the senior frontend engineer who built Stripe's checkout flow.
Your task: design AND implement a production-ready UI component in a single response.

=== TASK ===
Category : {category}
Layout   : {structure}
Aesthetic: {style}
{request_context}

=== OUTPUT FORMAT ===
Return a SINGLE valid JSON object with ALL keys listed below, in THIS EXACT ORDER.
Writing keys in order forces you to design before you code — do not skip or reorder keys.

{{
  "title": "Specific, memorable product name — not generic",

  "concept": "One sentence: design philosophy for THIS exact combination",

  "color_palette": [
    {{"name": "Primary",        "hex": "#...", "usage": "CTAs, key highlights"}},
    {{"name": "Secondary",      "hex": "#...", "usage": "Supporting elements"}},
    {{"name": "Background",     "hex": "#...", "usage": "Page/section bg"}},
    {{"name": "Surface",        "hex": "#...", "usage": "Cards, panels"}},
    {{"name": "Border",         "hex": "#...", "usage": "Subtle dividers"}},
    {{"name": "Text Primary",   "hex": "#...", "usage": "Headings, main text"}},
    {{"name": "Text Secondary", "hex": "#...", "usage": "Subtext, captions"}},
    {{"name": "Accent",         "hex": "#...", "usage": "Badges, tags, icons"}}
  ],

  "typography": {{
    "heading_font": "Google Fonts name",
    "body_font": "Google Fonts name",
    "scale": {{
      "hero"    : "72px / 900 weight / 1.05 line-height",
      "h1"      : "48px / 800 / 1.1",
      "h2"      : "32px / 700 / 1.2",
      "h3"      : "24px / 600 / 1.3",
      "body_lg" : "18px / 400 / 1.6",
      "body"    : "16px / 400 / 1.6",
      "caption" : "12px / 500 / 1.4 uppercase tracking-widest"
    }}
  }},

  "content_strategy": {{
    "headline"         : "Actual compelling headline — NO lorem ipsum, domain-specific",
    "subheadline"      : "Supporting copy",
    "cta_primary"      : "Primary button label",
    "cta_secondary"    : "Secondary button label",
    "realistic_content": ["5 domain-specific, realistic content items or data points"]
  }},

  "self_review": {{
    "visual_hierarchy" : <1-10>,
    "color_harmony"    : <1-10>,
    "typography"       : <1-10>,
    "spacing_balance"  : <1-10>,
    "content_realism"  : <1-10>,
    "total"            : <sum, max 50>,
    "weakest_area"     : "lowest score dimension name",
    "fix_applied"      : "What you mentally revised before finalizing html_code"
  }},

  "features"   : ["4-6 key feature/design highlight descriptions"],
  "description": "2-3 sentence gallery description",
  "usage"      : "When and how to use this in a real product",

  "html_code"  : "<FULL self-contained HTML — see rules below>",
  "react_code" : "<React/JSX equivalent using Tailwind>",
  "colors"     : ["#hex1", "#hex2", "... all palette hex values"]
}}

=== HTML IMPLEMENTATION RULES ===
Apply these AFTER completing all preceding keys (they encode your design decisions):

1.  Fonts       : Load heading_font + body_font from Google Fonts. Apply as CSS variables on :root.
2.  Colors      : Use ONLY hex values from color_palette. Zero external colors.
3.  Hierarchy   : L1=Hero(largest/highest contrast), L2=Support(medium/secondary), L3=Meta(small/muted/uppercase).
4.  Spacing     : 8pt grid (8/16/24/32/48/64/96px). Generous whitespace. Minimum 24px between sections.
5.  Interactions: ALL buttons: transition-all duration-200 ease-in-out.
                  Cards: hover:-translate-y-1 hover:shadow-xl transition-all duration-300.
                  CTA: hover:opacity-90 active:scale-95.
6.  Content     : Use exact text from content_strategy. Expand realistically — no placeholders.
7.  Images      : https://images.unsplash.com/photo-[thematically-appropriate-id]?w=800&auto=format&fit=crop
8.  Layout      : Outermost element shrinks to content. NO min-h-screen unless full dashboard.
9.  Script      : Use addEventListener — no inline onclick/onchange handlers.
10. Custom CSS  : Include a <style> block for gradients, keyframe animations, custom properties.

=== QUALITY GATE ===
self_review.total MUST be >= 35 before you write html_code.
If your mental draft scores < 35, revise it and record the fix in fix_applied.
NEVER use "Lorem ipsum", "User 1", "Product A", or any placeholder text.
Output valid JSON ONLY — no markdown fences, no text before or after.
"""


def build_unified_prompt(
    category: str,
    structure: str,
    style: str,
    request_title: Optional[str] = None,
    request_description: Optional[str] = None,
    target_audience: Optional[str] = None,
    reference_notes: Optional[str] = None,
) -> str:
    ctx_lines: list[str] = []
    if request_title:
        ctx_lines += [
            "\n=== REQUEST CONTEXT (highest priority) ===",
            f"Requested title   : {request_title}",
        ]
        if request_description:
            ctx_lines.append(f"Requested details : {request_description}")
        if target_audience:
            ctx_lines.append(f"Target audience   : {target_audience}")
        if reference_notes:
            ctx_lines.append(f"Reference / notes : {reference_notes}")
        ctx_lines.append("Follow the request while preserving production-ready quality.")

    return UNIFIED_PROMPT_TEMPLATE.format(
        category=category,
        structure=structure,
        style=style,
        request_context="\n".join(ctx_lines),
    )


# ---------------------------------------------------------------------------
# Gemini 호출 (Rate Limiter 내장)
# ---------------------------------------------------------------------------

async def call_gemini_with_rate_limit(prompt: str) -> Any:
    for attempt in range(1, MAX_RETRY_ATTEMPTS + 1):
        await rate_limiter.acquire()
        try:
            return await asyncio.to_thread(
                get_gemini().models.generate_content,
                model=GEMINI_MODEL,
                config={"response_mime_type": "application/json"},
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
            )
        except Exception as exc:
            msg = str(exc)
            is_quota = "429" in msg or "quota" in msg.lower() or "ResourceExhausted" in type(exc).__name__

            if is_quota:
                retry_after = _parse_retry_after(exc)
                if attempt < MAX_RETRY_ATTEMPTS:
                    await rate_limiter.wait_for_retry_after(retry_after)
                    continue
                log.error("[Gemini] 429 최대 재시도 초과.")
                raise RuntimeError("QUOTA_EXHAUSTED") from exc

            if attempt < MAX_RETRY_ATTEMPTS:
                wait = 2 ** attempt
                log.warning("[Gemini] 에러 (시도 %d/%d), %ds 후 재시도: %s", attempt, MAX_RETRY_ATTEMPTS, wait, msg[:120])
                await asyncio.sleep(wait)
            else:
                raise

    raise RuntimeError("Gemini 호출 실패: 최대 재시도 초과")


def _parse_retry_after(exc: Exception) -> float:
    match = re.search(r"retry.after[:\s]+(\d+)", str(exc), re.IGNORECASE)
    return float(match.group(1)) if match else 60.0


# ---------------------------------------------------------------------------
# JSON 파싱
# ---------------------------------------------------------------------------

def clean_json_text(text: str) -> str:
    text = text.strip()
    match = re.search(r"^```(?:json)?\s*(.*)\s*```$", text, re.DOTALL)
    return match.group(1) if match else text


def parse_gemini_json(response: Any) -> Dict[str, Any]:
    for candidate in (getattr(response, "candidates", None) or []):
        for part in getattr(getattr(candidate, "content", None), "parts", []):
            text = getattr(part, "text", "").strip()
            if not text:
                continue
            try:
                return json.loads(clean_json_text(text))
            except json.JSONDecodeError as e:
                log.debug("JSON 파싱 실패 (pos %s): %s...", e.pos, text[:120])
    raise ValueError("Gemini가 유효한 JSON을 반환하지 않았습니다.")


# ---------------------------------------------------------------------------
# HTML 래퍼
# ---------------------------------------------------------------------------

def wrap_html_if_needed(html: str) -> str:
    stripped = re.sub(r"<!--.*?-->", "", html, flags=re.DOTALL)
    if re.search(r"<html[\s>]", stripped, re.IGNORECASE):
        return html
    return (
        "<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n"
        "  <meta charset=\"UTF-8\" />\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
        "  <script src=\"https://cdn.tailwindcss.com\"></script>\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
        "  <link href=\"https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900&display=swap\" rel=\"stylesheet\">\n"
        "  <style>*, *::before, *::after{box-sizing:border-box} body{font-family:'Inter',sans-serif;margin:0;padding:0}</style>\n"
        "  <title>Preview</title>\n</head>\n"
        "<body class=\"bg-gray-50 text-slate-900 antialiased\">\n"
        "  <div id=\"capture-box\" class=\"w-full max-w-[1400px] mx-auto flow-root\">\n"
        f"    {html}\n"
        "  </div>\n</body>\n</html>"
    )


# ---------------------------------------------------------------------------
# 스크린샷
# ---------------------------------------------------------------------------

async def capture_screenshot(browser: Browser, html: str) -> bytes:
    page = await browser.new_page(viewport={"width": 1400, "height": 900})
    try:
        try:
            await page.set_content(html, wait_until="load", timeout=20000)
        except Exception as e:
            log.warning("페이지 로딩 지연 (캡처 진행): %s", e)

        try:
            await page.evaluate("document.fonts.ready")
        except Exception:
            pass

        try:
            await page.wait_for_function(
                "() => [...document.images].every(img => img.complete)",
                timeout=8000,
            )
        except Exception:
            log.debug("이미지 로딩 타임아웃")

        try:
            await page.wait_for_load_state("networkidle", timeout=5000)
        except Exception:
            pass

        await page.wait_for_timeout(500)

        await page.evaluate("""
            (() => {
              const root = document.getElementById('capture-box') || document.body;
              root.querySelectorAll('*').forEach(el => {
                el.classList.remove('min-h-screen','h-screen','min-h-[100vh]','h-[100vh]');
                const s = el.style;
                if (s.minHeight?.includes('100vh')) s.minHeight = 'auto';
                if (s.height?.includes('100vh'))    s.height    = 'auto';
              });
              document.documentElement.style.cssText += ';margin:0;padding:0;';
              document.body.style.cssText            += ';margin:0;padding:0;';
            })();
        """)
        await page.wait_for_timeout(200)

        dims = await page.evaluate("""
            (() => {
              const el = document.getElementById('capture-box') || document.body;
              return { height: Math.ceil(el.scrollHeight || el.getBoundingClientRect().height || 900) };
            })();
        """)
        height = max(900, min(int(dims.get("height", 900)) + 60, 6000))
        await page.set_viewport_size({"width": 1400, "height": height})
        await page.wait_for_timeout(200)

        target = await page.query_selector("#capture-box") or await page.query_selector("body")
        return await target.screenshot(type="png")
    except Exception as e:
        log.error("캡처 에러 → body 대체: %s", e)
        return await (await page.query_selector("body")).screenshot(type="png")
    finally:
        await page.close()


# ---------------------------------------------------------------------------
# Supabase 헬퍼
# ---------------------------------------------------------------------------

def _slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "design"


async def upload_image(image_bytes: bytes, category: str) -> str:
    filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{_slugify(category)}_{uuid.uuid4().hex[:6]}.png"
    object_path = f"{STORAGE_FOLDER}/{filename}"
    sb = get_supabase()
    await asyncio.to_thread(
        sb.storage.from_(STORAGE_BUCKET).upload,
        object_path, image_bytes, {"content-type": "image/png"},
    )
    return await asyncio.to_thread(sb.storage.from_(STORAGE_BUCKET).get_public_url, object_path)


async def ensure_unique_slug(base_title: str) -> str:
    base = _slugify(base_title)
    candidate, suffix, sb = base, 2, get_supabase()
    for _ in range(100):
        res = await asyncio.to_thread(
            lambda c=candidate: sb.table("designs").select("id").eq("slug", c).limit(1).execute()
        )
        if not res.data:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1
    return f"{base}-{uuid.uuid4().hex[:6]}"


async def insert_design(record: Dict[str, Any]) -> None:
    sb = get_supabase()
    await asyncio.to_thread(sb.table("designs").insert(record).execute)


async def fetch_next_pending_request() -> Optional[Dict[str, Any]]:
    try:
        sb = get_supabase()
        res = await asyncio.to_thread(
            sb.table("design_requests")
            .select("id,title,description,category,target_audience,reference_notes,vote_count")
            .eq("status", "pending")
            .order("vote_count", desc=True)
            .order("created_at", desc=False)
            .limit(1)
            .execute
        )
        rows = res.data or []
        return rows[0] if rows else None
    except Exception as exc:
        log.warning("신청 테이블 조회 실패 (랜덤 모드): %s", exc)
        return None


async def update_request_status(
    request_id: str, status: str, linked_design_id: Optional[str] = None
) -> None:
    payload: Dict[str, Any] = {"status": status}
    if linked_design_id:
        payload["linked_design_id"] = linked_design_id
    sb = get_supabase()
    await asyncio.to_thread(
        sb.table("design_requests").update(payload).eq("id", request_id).execute
    )


# ---------------------------------------------------------------------------
# 알림
# ---------------------------------------------------------------------------

async def notify_request_completion(request_id: str, design_id: str) -> None:
    if not REQUEST_NOTIFY_SECRET:
        log.info("REQUEST_NOTIFY_SECRET 미설정: 알림 건너뜀")
        return
    endpoint = f"{REQUEST_NOTIFY_BASE_URL}/api/design-requests/notify"
    try:
        async with httpx.AsyncClient(timeout=12.0) as client:
            res = await client.post(
                endpoint,
                json={"requestId": request_id, "designId": design_id},
                headers={"Authorization": f"Bearer {REQUEST_NOTIFY_SECRET}"},
            )
            res.raise_for_status()
            log.info("알림 완료 (status=%d)", res.status_code)
    except httpx.HTTPStatusError as exc:
        log.warning("알림 HTTP 에러: %s", exc.response.status_code)
    except Exception as exc:
        log.warning("알림 호출 실패: %s", exc)


# ---------------------------------------------------------------------------
# 카테고리 정규화
# ---------------------------------------------------------------------------

def normalize_request_category(value: Optional[str]) -> str:
    if not value:
        return random.choice(CATEGORIES)
    mapping = {
        "landing page": "Landing Page", "dashboard": "Dashboard",
        "e-commerce": "E-commerce",     "ecommerce": "E-commerce",
        "portfolio": "Portfolio",        "blog": "Blog",
        "component": "Component",        "components": "Component",
    }
    return mapping.get(value.strip().lower(), "Landing Page")


# ---------------------------------------------------------------------------
# 메인 생성 로직 (API 1회)
# ---------------------------------------------------------------------------

async def generate_single_design(
    browser: Browser,
    source_request: Optional[Dict[str, Any]] = None,
) -> tuple[bool, Optional[str]]:
    """디자인 1개를 생성합니다. Gemini API 호출은 정확히 1회."""

    category = (
        normalize_request_category(source_request.get("category"))
        if source_request else random.choice(CATEGORIES)
    )
    style, structure = pick_compatible_style_structure()
    combo_key = f"{structure}_{style}".lower().replace(" ", "_")

    log.info(
        "[생성] %s | %s | %s%s",
        category, structure, style,
        f" | 신청: {source_request.get('title')}" if source_request else " | 랜덤",
    )

    prompt = build_unified_prompt(
        category=category, structure=structure, style=style,
        request_title=source_request.get("title") if source_request else None,
        request_description=source_request.get("description") if source_request else None,
        target_audience=source_request.get("target_audience") if source_request else None,
        reference_notes=source_request.get("reference_notes") if source_request else None,
    )

    # --- Gemini 호출 (1회) ---
    try:
        response = await call_gemini_with_rate_limit(prompt)
        payload = parse_gemini_json(response)
    except RuntimeError as exc:
        if "QUOTA_EXHAUSTED" in str(exc):
            raise
        log.error("[생성] Gemini 호출 실패: %s", exc)
        return False, None
    except Exception as exc:
        log.error("[생성] 예외: %s", exc)
        return False, None

    # --- 자가 품질 검증 (추가 API 호출 없음) ---
    review = payload.get("self_review", {})
    score = review.get("total", -1)
    if isinstance(score, (int, float)) and 0 < score < 35:
        log.warning(
            "[품질 미달] self_review.total=%d/50 (기준: 35) | 취약: %s | 이번 결과 저장 안 함",
            score, review.get("weakest_area", "?"),
        )
        return False, None

    log.info(
        "[품질 OK] %d/50 | 취약: %s | 수정 내용: %s",
        score, review.get("weakest_area", "?"), review.get("fix_applied", ""),
    )

    # --- colors 정규화 ---
    raw = payload.get("colors", [])
    if isinstance(raw, list):
        safe_colors = [str(c) for c in raw]
    elif isinstance(raw, dict):
        safe_colors = list(raw.values())
    elif isinstance(raw, str):
        safe_colors = [raw]
    else:
        safe_colors = [p.get("hex", "") for p in payload.get("color_palette", []) if p.get("hex")]

    # --- 스크린샷 캡처 & 저장 ---
    try:
        html_code: str = payload.get("html_code", payload.get("code", ""))
        react_code: str = payload.get("react_code", "")

        screenshot = await capture_screenshot(browser, wrap_html_if_needed(html_code))
        image_url = await upload_image(screenshot, category)
        slug = await ensure_unique_slug(payload.get("title", "Untitled Design"))
        design_id = str(uuid.uuid4())

        record = {
            "id": design_id,
            "title": payload.get("title", "Untitled Design"),
            "description": payload.get("description", ""),
            "features": payload.get("features", []),
            "usage": payload.get("usage", ""),
            "image_url": image_url,
            "category": category,
            "code": html_code,
            "code_react": react_code,
            "prompt": combo_key,
            "colors": safe_colors,
            "slug": slug,
            "status": "published",
            "sns_promoted": False,
            "pinterest_promoted": False,
            "created_at": datetime.utcnow().isoformat(),
        }

        await insert_design(record)
        log.info("[성공] %s (%s) | 품질: %d/50", record["title"], slug, score)
        return True, design_id

    except Exception as exc:
        log.error("[저장/캡처 실패] %s", exc)
        return False, None


# ---------------------------------------------------------------------------
# 배치 실행
# ---------------------------------------------------------------------------

async def run_batch(count: int, use_requests: bool, requests_only: bool) -> None:
    mode = "신청 우선" if use_requests else "랜덤"
    log.info("=== 디자인 %d개 생성 시작 (모드: %s) ===", count, mode)
    log.info(
        "Rate Limit: %d RPM / %d RPD → 요청 간 최소 %.0f초 대기",
        RPM_LIMIT, RPD_LIMIT, MIN_REQUEST_INTERVAL,
    )

    successes = failures = 0

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        try:
            for i in range(count):
                if rate_limiter.is_daily_limit_reached():
                    log.warning("일일 API 한도 %d회 도달. 배치 조기 종료.", RPD_LIMIT)
                    break

                log.info("--- 작업 %d/%d ---", i + 1, count)
                source_request: Optional[Dict[str, Any]] = None

                if use_requests:
                    source_request = await fetch_next_pending_request()
                    if source_request:
                        try:
                            await update_request_status(source_request["id"], "in_progress")
                        except Exception as exc:
                            log.warning("신청 상태 업데이트 실패: %s", exc)
                    elif requests_only:
                        log.info("처리할 pending 신청 없음. 종료.")
                        break

                try:
                    ok, design_id = await generate_single_design(browser, source_request)
                except RuntimeError as exc:
                    if "QUOTA_EXHAUSTED" in str(exc):
                        log.error("할당량 초과 → 배치 종료.")
                        break
                    raise

                if ok:
                    successes += 1
                    if source_request and design_id:
                        try:
                            await update_request_status(
                                source_request["id"], "completed", linked_design_id=design_id
                            )
                            await notify_request_completion(source_request["id"], design_id)
                        except Exception as exc:
                            log.warning("신청 완료 업데이트 실패: %s", exc)
                else:
                    failures += 1
                    if source_request:
                        try:
                            await update_request_status(source_request["id"], "pending")
                        except Exception as exc:
                            log.warning("신청 재대기 실패: %s", exc)

        finally:
            await browser.close()

    log.info("=== 완료: 성공 %d / 실패 %d / 총 %d ===", successes, failures, successes + failures)
    log.info("오늘 남은 API 호출 가능: %d회", max(0, RPD_LIMIT - rate_limiter._daily_count))


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Gemini 기반 디자인 생성기 v3.1 (무료 티어 최적화)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
무료 티어 예상 소요 시간 (Gemini 2.5 Pro, API 대기 포함):
  5개  →  약  1분 5초
  10개 →  약  2분 10초
  50개 →  약 10분 50초
  100개→  약 21분 40초 (일일 최대)

환경변수:
  GEMINI_RPD_LIMIT  일일 호출 한도 오버라이드 (기본: 100)
        """,
    )
    parser.add_argument("--count", type=int, default=1, help="생성할 디자인 수 (기본값: 1)")
    parser.add_argument("--use-requests", action="store_true", help="pending 신청 우선 처리")
    parser.add_argument("--requests-only", action="store_true", help="pending 신청만 처리 후 종료")
    parser.add_argument(
        "--rpd-limit", type=int, default=RPD_LIMIT,
        help=f"일일 API 한도 오버라이드 (기본: {RPD_LIMIT})",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    if args.rpd_limit != RPD_LIMIT:
        rate_limiter.rpd = args.rpd_limit
        log.info("일일 한도 오버라이드: %d", args.rpd_limit)

    try:
        asyncio.run(
            run_batch(
                count=args.count,
                use_requests=(args.use_requests or args.requests_only),
                requests_only=args.requests_only,
            )
        )
    except KeyboardInterrupt:
        log.info("사용자에 의해 중단되었습니다.")