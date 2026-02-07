#!/usr/bin/env python3
"""Gemini + Supabase 디자인 자동 생성기 (최적화 버전).

- 기본 실행 시 디자인 3개 생성 (저품질 방지 및 꾸준한 업로드용)
- Playwright 브라우저 인스턴스 재사용으로 속도 향상
- Gemini JSON 응답 전처리로 에러 방지
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List

from dotenv import load_dotenv
from google import genai
from playwright.async_api import async_playwright, Browser
from supabase import Client, create_client

# --- 환경 변수 로드 ---
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash") # 모델 버전에 맞게 수정 가능
STORAGE_BUCKET = os.getenv("SUPABASE_DESIGNS_BUCKET", "designs-bucket")
STORAGE_FOLDER = os.getenv("SUPABASE_DESIGNS_FOLDER", "designs")

if not all([SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY]):
    raise RuntimeError("SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, GEMINI_API_KEY가 필요합니다.")

# --- 클라이언트 초기화 ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# --- 데이터 상수 (구조 및 스타일) ---
STRUCTURES = [
    "Hero with Center Call-to-Action",
    "Split Screen Feature Display",
    "Bento Grid Dashboard",
    "Sticky Sidebar Navigation",
    "Multi-column Technical Documentation",
    "Floating Interactive Cards",
    "Minimalist Article Feed",
    "E-commerce Product Showcase with Filter",
    "Full-page Video Background",
    "Three-tier Pricing Table",
    "Testimonial Slider Grid",
    "Vertical Timeline of Events",
    "Data-rich Table with Pagination",
    "Tabbed Dashboard Interface",
    "Profile Header with Stats",
    "Horizontal Scroll Feature List",
    "Masonry Gallery Layout",
    "Layered Overlay Components",
    "Step-by-step Onboarding Flow",
    "Notification Center List",
    "Search-focused Hero Section",
    "Footer with Sitemap and Newsletter",
    "Accordion FAQ List",
    "Stat-heavy Admin Panel",
    "Centered Newsletter Subscription",
    "Team Member Circle Grid",
    "Project Portfolio Masonry",
    "Clean Contact Form with Map",
    "Live Activity Feed Sidebar",
    "Settings Page with Toggle Buttons",
    "Marquee-based Logo Wall",
    "Comparison Slider (Before/After)",
    "Draggable Kanban Board",
    "Segmented Control Navigation",
    "Infinite Scroll Feed with Skeleton Loader",
    "Floating Action Button (FAB) Menu",
    "Interactive Heatmap Dashboard",
    "Command Palette Quick Search",
    "Radial Progress Dashboard",
    "Fixed Footer Mobile Bottom Bar",
    "Multi-step Interactive Quiz",
    "Expandable Sidebar with Tooltips"
]

STYLES = [
    "Apple-inspired Minimal White",
    "Cyberpunk Neon Pink & Blue",
    "Glassmorphism Frosted",
    "Neo-Brutalism High Contrast",
    "Luxury Gold & Deep Black",
    "Soft Pastel Gradient",
    "Enterprise Professional Blue",
    "Retro 80s Synthwave",
    "Deep Ocean Dark Mode",
    "Eco-friendly Nature Green",
    "Nordic Arctic Clean",
    "Industrial Raw Concrete",
    "Futuristic Holographic",
    "Modern Swiss Typographic",
    "Bauhaus Primary Colors",
    "Matte Material Design",
    "Vintage Paper Texture",
    "Vibrant Memphis Pop",
    "Stealth All-Black Aesthetic",
    "Cozy Coffee Shop Warmth",
    "Midnight Aurora Borealis",
    "Clinical Scientific Clean",
    "Gaming Razer Green & Black",
    "Royal Velvet Purple",
    "Sunset Orange & Red",
    "Space Exploration Dark Grey",
    "Organic Earth Tones",
    "Sketch Style Hand-drawn",
    "High-tech Wireframe",
    "Pixel Art 16-bit Style",
    "Claymorphism Soft 3D",
    "Monochromatic Deep Sea Blue",
    "Acid Graphic Techno",
    "Solarized Eye-care Dark",
    "Japanese Zen Minimal",
    "Dotted Blueprint Grid",
    "Liquid Gradient Flow",
    "Grainy Retro Film",
    "Cyber-Security Matrix Green",
    "Flat Illustration Pop",
    "Skeuomorphic Modern Leather",
    "High-Gloss Plastic Candy"
]

CATEGORIES = [
    "Landing Page",
    "Dashboard",
    "E-commerce",
    "Portfolio",
    "Blog",
    "Component",
]


# --- 헬퍼 함수 ---

def slugify(value: str) -> str:
    """제목을 URL 친화적인 슬러그로 변환"""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "design"


def clean_json_text(text: str) -> str:
    """마크다운 코드 블록(```json ... ```)을 제거하여 순수 JSON만 추출"""
    text = text.strip()
    pattern = r"^```(?:json)?\s*(.*)\s*```$"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return text


def build_prompt(category: str, structure: str, style: str) -> str:
    """디자인 중심의 프롬프트 생성"""
    return (
        "Act as a senior UI engineer and expert visual designer. "
        f"Create a modern '{category}' web design using the '{structure}' layout structure and '{style}' art direction. "
        "\n\n"
        "Requirements:\n"
        "1. Output must be valid JSON only. Do not include markdown formatting.\n"
        "2. JSON Keys:\n"
        "   - 'title': Catchy, SEO-friendly title (3-6 words, include function keyword e.g., 'Dashboard', 'UI').\n"
        "   - 'description': 150-200 chars. Focus on visual hierarchy, color psychology, and UX intent. Mention the style used.\n"
        "   - 'code': Single-file HTML5 with Tailwind CSS (via CDN). Use semantic tags. Ensure high contrast and accessibility.\n"
        "   - 'colors': Array of 5 hex color codes used in the design.\n"
        "3. Images: Use reliable placeholder URLs (e.g., 'https://placehold.co/600x400' or similar) with descriptive alt text.\n"
        "4. The UI must be production-ready, fully responsive (mobile-first), and aesthetically pleasing."
    )


def parse_gemini_json(response: Any) -> Dict[str, Any]:
    """Gemini 응답에서 JSON 파싱 (안정성 강화)"""
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        parts = getattr(getattr(candidate, "content", None), "parts", [])
        for part in parts:
            text = getattr(part, "text", "").strip()
            if not text:
                continue
            try:
                # 마크다운 제거 후 파싱
                cleaned_text = clean_json_text(text)
                return json.loads(cleaned_text)
            except json.JSONDecodeError:
                print(f"[debug] JSON 파싱 실패 (일부 텍스트): {text[:50]}...")
                continue
    raise ValueError("Gemini가 유효한 JSON을 반환하지 않았습니다.")


def ensure_payload_shape(payload: Dict[str, Any]) -> Dict[str, Any]:
    """필수 필드 검증"""
    missing = [key for key in ("title", "description", "code", "colors") if key not in payload]
    if missing:
        raise ValueError(f"누락된 필드: {', '.join(missing)}")

    title = str(payload["title"]).strip() or "Untitled Design"
    description = str(payload["description"]).strip()
    code = str(payload["code"]).strip()
    colors_raw = payload.get("colors")
    if not isinstance(colors_raw, list):
        colors = []
    else:
        colors = [str(color).strip() for color in colors_raw if isinstance(color, str)]

    return {
        "title": title,
        "description": description,
        "code": code,
        "colors": colors[:6],
    }


def combination_key(structure: str, style: str) -> str:
    return f"{structure}__{style}".lower().replace(" ", "_")


def is_combination_used(combo_key: str) -> bool:
    """이미 생성된 조합인지 확인"""
    response = supabase.table("designs").select("id", count="exact").eq("prompt", combo_key).limit(1).execute()
    return bool(response.data)


def ensure_unique_slug(base_title: str) -> str:
    """중복되지 않는 슬러그 생성"""
    base = slugify(base_title)
    candidate = base
    suffix = 2
    while True:
        response = supabase.table("designs").select("id").eq("slug", candidate).limit(1).execute()
        if not response.data:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1


def wrap_html_if_needed(html: str) -> str:
    """HTML 완전한 구조로 감싸기"""
    if "<html" in html.lower():
        return html
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\" />\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
        "  <script src=\"https://cdn.tailwindcss.com\"></script>\n"
        "  <title>AI Design</title>\n"
        "</head>\n"
        "<body class=\"min-h-screen bg-gray-50 flex items-center justify-center p-4 sm:p-10\">\n"
        f"{html}\n"
        "</body>\n"
        "</html>"
    )


async def capture_screenshot(browser: Browser, html: str) -> bytes:
    """전달받은 브라우저 인스턴스 사용 (속도 향상)"""
    # 새 페이지(탭)만 열었다 닫음 -> 훨씬 빠름
    page = await browser.new_page(viewport={"width": 1400, "height": 900})
    try:
        await page.set_content(html, wait_until="networkidle")
        # 렌더링 안정화를 위해 잠시 대기 (1초)
        await page.wait_for_timeout(1000)
        screenshot = await page.screenshot(full_page=True, type="png")
    finally:
        await page.close()
    return screenshot


def upload_image(image_bytes: bytes, category: str) -> str:
    """Supabase Storage에 이미지 업로드"""
    filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{category.replace(' ', '_')}_{uuid.uuid4().hex[:6]}.png"
    object_path = f"{STORAGE_FOLDER}/{filename}"
    storage = supabase.storage.from_(STORAGE_BUCKET)
    storage.upload(object_path, image_bytes, {"content-type": "image/png"})
    return storage.get_public_url(object_path)


async def generate_single_design(browser: Browser, max_attempts: int = 3) -> bool:
    """단일 디자인 생성 (재시도 로직 포함)"""
    for attempt in range(1, max_attempts + 1):
        category = random.choice(CATEGORIES)
        structure = random.choice(STRUCTURES)
        style = random.choice(STYLES)
        combo_key = combination_key(structure, style)

        if is_combination_used(combo_key):
            print(f"[skip] 이미 생성된 조합: {combo_key}")
            continue

        prompt = build_prompt(category, structure, style)
        print(f"[request] {category} | {structure} | {style}")

        try:
            # 1. Gemini로 코드 생성
            response = await asyncio.to_thread(
                gemini_client.models.generate_content,
                model=GEMINI_MODEL,
                config={"response_mime_type": "application/json"},
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
            )
            
            # 2. 파싱 및 전처리
            payload = ensure_payload_shape(parse_gemini_json(response))
            html = wrap_html_if_needed(payload["code"])
            
            # 3. 스크린샷 (브라우저 인스턴스 재사용)
            screenshot = await capture_screenshot(browser, html)
            
            # 4. 이미지 업로드
            image_url = upload_image(screenshot, category)
            slug = ensure_unique_slug(payload["title"])

            # 5. DB 저장
            record = {
                "id": str(uuid.uuid4()),
                "title": payload["title"],
                "description": payload["description"],
                "image_url": image_url,
                "category": category,
                "code": html,
                "prompt": combo_key,
                "colors": payload["colors"],
                "slug": slug,
                "likes": 0,
                "created_at": datetime.utcnow().isoformat(),
                "updated_at": datetime.utcnow().isoformat(),
            }

            supabase.table("designs").insert(record).execute()
            print(f"[success] 저장 완료: {payload['title']} ({slug})")
            return True

        except Exception as exc:
            message = str(exc)
            if "429" in message or "quota" in message.lower():
                print("[error] Gemini API 할당량 초과. 잠시 대기하거나 중단합니다.")
                return False
            print(f"[retry] 에러 발생 (시도 {attempt}/{max_attempts}): {exc}")
            await asyncio.sleep(2) # 재시도 전 짧은 대기

    return False


async def run_batch(count: int) -> None:
    """브라우저 생명주기 관리 및 배치 실행"""
    successes = 0
    
    print(f"[system] 디자인 {count}개 생성을 시작합니다...")
    
    # 브라우저를 한 번만 실행 (Context Manager)
    async with async_playwright() as p:
        print("[system] 브라우저 엔진 초기화 중...")
        browser = await p.chromium.launch()
        
        for i in range(count):
            print(f"\n--- 작업 진행 ({i+1}/{count}) ---")
            created = await generate_single_design(browser)
            
            if created:
                successes += 1
                # 너무 빠른 요청 방지 (API 보호) & 안정적인 생성 텀
                await asyncio.sleep(2)
        
        await browser.close()
        print("[system] 브라우저 종료.")

    print(f"\n[결과] 총 {successes}/{count}개 생성 완료")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gemini 기반 디자인 생성기")
    # [수정됨] 기본값을 3으로 변경
    parser.add_argument("--count", type=int, default=3, help="생성할 디자인 수 (기본값: 3)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run_batch(args.count))
    except KeyboardInterrupt:
        print("\n[stop] 사용자에 의해 중단되었습니다.")