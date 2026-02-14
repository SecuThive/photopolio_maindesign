#!/usr/bin/env python3
"""Gemini + Supabase 디자인 자동 생성기 (최적화 버전 v2.1).

- [v2.1 Fix] 프리뷰 이미지 세로 여백 버그 완벽 수정 (min-h-screen 강제 제거 및 타이트 캡처)
- React(JSX) 코드 동시 생성
- 애드센스 승인을 위한 텍스트 설명(Features, Usage) 보강
- 원본 STRUCTURES, STYLES, CATEGORIES 100% 보존
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
from typing import Any, Dict

from dotenv import load_dotenv
from google import genai
from playwright.async_api import async_playwright, Browser
from supabase import Client, create_client

# --- 환경 변수 로드 ---
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-latest") 
STORAGE_BUCKET = os.getenv("SUPABASE_DESIGNS_BUCKET", "designs-bucket")
STORAGE_FOLDER = os.getenv("SUPABASE_DESIGNS_FOLDER", "designs")

if not all([SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY]):
    raise RuntimeError("SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, GEMINI_API_KEY가 필요합니다.")

# --- 클라이언트 초기화 ---
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

# --- 데이터 상수 (구조 및 스타일) ---
STRUCTURES = [
    "Hero with Center Call-to-Action", "Split Screen Feature Display", "Bento Grid Dashboard",
    "Sticky Sidebar Navigation", "Multi-column Technical Documentation", "Floating Interactive Cards",
    "Minimalist Article Feed", "E-commerce Product Showcase with Filter", "Full-page Video Background",
    "Three-tier Pricing Table", "Testimonial Slider Grid", "Vertical Timeline of Events",
    "Data-rich Table with Pagination", "Tabbed Dashboard Interface", "Profile Header with Stats",
    "Horizontal Scroll Feature List", "Masonry Gallery Layout", "Layered Overlay Components",
    "Step-by-step Onboarding Flow", "Notification Center List", "Search-focused Hero Section",
    "Footer with Sitemap and Newsletter", "Accordion FAQ List", "Stat-heavy Admin Panel",
    "Centered Newsletter Subscription", "Team Member Circle Grid", "Project Portfolio Masonry",
    "Clean Contact Form with Map", "Live Activity Feed Sidebar", "Settings Page with Toggle Buttons",
    "Marquee-based Logo Wall", "Comparison Slider (Before/After)", "Draggable Kanban Board",
    "Segmented Control Navigation", "Infinite Scroll Feed with Skeleton Loader", "Floating Action Button (FAB) Menu",
    "Interactive Heatmap Dashboard", "Command Palette Quick Search", "Radial Progress Dashboard",
    "Fixed Footer Mobile Bottom Bar", "Multi-step Interactive Quiz", "Expandable Sidebar with Tooltips"
]

STYLES = [
    "Apple-inspired Minimal White", "Cyberpunk Neon Pink & Blue", "Glassmorphism Frosted",
    "Neo-Brutalism High Contrast", "Luxury Gold & Deep Black", "Soft Pastel Gradient",
    "Enterprise Professional Blue", "Retro 80s Synthwave", "Deep Ocean Dark Mode",
    "Eco-friendly Nature Green", "Nordic Arctic Clean", "Industrial Raw Concrete",
    "Futuristic Holographic", "Modern Swiss Typographic", "Bauhaus Primary Colors",
    "Matte Material Design", "Vintage Paper Texture", "Vibrant Memphis Pop",
    "Stealth All-Black Aesthetic", "Cozy Coffee Shop Warmth", "Midnight Aurora Borealis",
    "Clinical Scientific Clean", "Gaming Razer Green & Black", "Royal Velvet Purple",
    "Sunset Orange & Red", "Space Exploration Dark Grey", "Organic Earth Tones",
    "Sketch Style Hand-drawn", "High-tech Wireframe", "Pixel Art 16-bit Style",
    "Claymorphism Soft 3D", "Monochromatic Deep Sea Blue", "Acid Graphic Techno",
    "Solarized Eye-care Dark", "Japanese Zen Minimal", "Dotted Blueprint Grid",
    "Liquid Gradient Flow", "Grainy Retro Film", "Cyber-Security Matrix Green",
    "Flat Illustration Pop", "Skeuomorphic Modern Leather", "High-Gloss Plastic Candy"
]

CATEGORIES = [
    "Landing Page", "Dashboard", "E-commerce", "Portfolio", "Blog", "Component"
]

# --- 헬퍼 함수 ---

def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "design"

def clean_json_text(text: str) -> str:
    text = text.strip()
    pattern = r"^```(?:json)?\s*(.*)\s*```$"
    match = re.search(pattern, text, re.DOTALL)
    if match:
        return match.group(1)
    return text

def build_prompt(category: str, structure: str, style: str) -> str:
    """텍스트 비중을 높이고 React(JSX) 코드까지 요구하는 프롬프트"""
    return (
        "Act as a senior UI engineer and expert visual designer. "
        f"Create a modern '{category}' web design using the '{structure}' layout structure and '{style}' art direction. "
        "\n\n"
        "Requirements:\n"
        "1. Output MUST be valid JSON only. Do not wrap in markdown.\n"
        "2. JSON Keys:\n"
        "   - 'title': Catchy, SEO-friendly title (3-6 words).\n"
        "   - 'description': A detailed 2-3 sentence overview of the design intent and visual hierarchy.\n"
        "   - 'features': An array of 3 bullet points explaining the key UI features.\n"
        "   - 'usage': A short sentence on where this component is best used (e.g., 'Perfect for SaaS admin panels').\n"
        "   - 'html_code': Single-file HTML5 with Tailwind CSS classes. Use semantic tags and clean spacing.\n"
        "   - 'react_code': The exact same UI, but converted to a React functional component with `className` and self-closing tags.\n"
        "   - 'colors': Array of 5 hex color codes used.\n"
        "3. Images: Use reliable placeholder URLs (e.g., 'https://images.unsplash.com/photo-1498050108023-c5249f4df085') with descriptive alt text.\n"
        "4. The UI must be production-ready and fully responsive.\n"
        "5. CRITICAL LAYOUT RULE: Do NOT wrap the component in a `min-h-screen`, `h-screen`, or full-height container unless it is strictly a full dashboard layout. The outermost element MUST shrink to fit its content tightly to prevent excessive vertical white space."
    )

def parse_gemini_json(response: Any) -> Dict[str, Any]:
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        parts = getattr(getattr(candidate, "content", None), "parts", [])
        for part in parts:
            text = getattr(part, "text", "").strip()
            if not text:
                continue
            try:
                cleaned_text = clean_json_text(text)
                return json.loads(cleaned_text)
            except json.JSONDecodeError:
                print(f"[debug] JSON 파싱 실패 (일부 텍스트): {text[:50]}...")
                continue
    raise ValueError("Gemini가 유효한 JSON을 반환하지 않았습니다.")

def wrap_html_if_needed(html: str) -> str:
    """여백 문제를 원천 차단하기 위해 타이트한 캡처 전용 박스(#capture-box)로 감쌉니다."""
    if "<html" in html.lower():
        return html
    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\" />\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
        "  <script src=\"https://cdn.tailwindcss.com\"></script>\n"
        "  <title>Preview</title>\n"
        "</head>\n"
        "<body class=\"bg-gray-50 text-gray-900 antialiased m-0 p-0 flex justify-center\">\n"
        f"  <div id=\"capture-box\" class=\"w-full max-w-[1400px] flow-root\">\n"
        f"    {html}\n"
        f"  </div>\n"
        "</body>\n"
        "</html>"
    )

async def capture_screenshot(browser: Browser, html: str) -> bytes:
    """가장 핵심적인 여백 제거 로직 포함"""
    page = await browser.new_page(viewport={"width": 1400, "height": 800})
    try:
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(1500)
        
        # [방어벽] AI가 강제로 생성한 'min-h-screen' 클래스를 DOM에서 강제로 삭제하여 
        # 내용물이 본래 높이(타이트하게)로 줄어들도록 조작합니다.
        await page.evaluate('''
            const captureBox = document.getElementById('capture-box');
            if (captureBox) {
                // capture-box 내부의 최상단 엘리먼트들 검사
                Array.from(captureBox.children).forEach(el => {
                    if (el.classList.contains('min-h-screen') || el.classList.contains('h-screen')) {
                        el.classList.remove('min-h-screen', 'h-screen');
                        el.style.minHeight = 'auto';
                        el.style.height = 'auto';
                    }
                });
            }
        ''')
        
        # 화면 전체(빈 여백 포함)가 아닌, 내용물이 꽉 찬 #capture-box 만 캡처합니다.
        target = await page.query_selector('#capture-box') or await page.query_selector('body')
        screenshot = await target.screenshot()
        
    finally:
        await page.close()
        
    return screenshot

def upload_image(image_bytes: bytes, category: str) -> str:
    filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{slugify(category)}_{uuid.uuid4().hex[:6]}.png"
    object_path = f"{STORAGE_FOLDER}/{filename}"
    supabase.storage.from_(STORAGE_BUCKET).upload(object_path, image_bytes, {"content-type": "image/png"})
    return supabase.storage.from_(STORAGE_BUCKET).get_public_url(object_path)

def ensure_unique_slug(base_title: str) -> str:
    base = slugify(base_title)
    candidate = base
    suffix = 2
    while True:
        response = supabase.table("designs").select("id").eq("slug", candidate).limit(1).execute()
        if not response.data:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1

async def generate_single_design(browser: Browser, max_attempts: int = 3) -> bool:
    for attempt in range(1, max_attempts + 1):
        category = random.choice(CATEGORIES)
        structure = random.choice(STRUCTURES)
        style = random.choice(STYLES)
        combo_key = f"{structure}_{style}".lower().replace(" ", "_")

        prompt = build_prompt(category, structure, style)
        print(f"[request] {category} | {structure} | {style}")

        try:
            response = await asyncio.to_thread(
                gemini_client.models.generate_content,
                model=GEMINI_MODEL,
                config={"response_mime_type": "application/json"},
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
            )
            
            payload = parse_gemini_json(response)
            
            html_code = payload.get("html_code", payload.get("code", "")) 
            react_code = payload.get("react_code", "")
            wrapped_html = wrap_html_if_needed(html_code)
            
            screenshot = await capture_screenshot(browser, wrapped_html)
            image_url = upload_image(screenshot, category)
            slug = ensure_unique_slug(payload.get("title", "Untitled Design"))

            record = {
                "id": str(uuid.uuid4()),
                "title": payload.get("title", "Untitled Design"),
                "description": payload.get("description", ""),
                "features": payload.get("features", []),  
                "usage": payload.get("usage", ""),
                "image_url": image_url,
                "category": category,
                "code": html_code,         
                "code_react": react_code,
                "prompt": combo_key,
                "colors": payload.get("colors", []),
                "slug": slug,
                "status": "published",   
                "sns_promoted": False,   
                "pinterest_promoted": False, 
                "created_at": datetime.utcnow().isoformat(),
            }

            supabase.table("designs").insert(record).execute()
            print(f"[success] 저장 완료: {record['title']} ({slug})")
            return True

        except Exception as exc:
            message = str(exc)
            if "429" in message or "quota" in message.lower():
                print("[error] Gemini API 할당량 초과. 잠시 대기하거나 중단합니다.")
                return False
            print(f"[retry] 에러 발생 (시도 {attempt}/{max_attempts}): {exc}")
            await asyncio.sleep(2)

    return False

async def run_batch(count: int) -> None:
    successes = 0
    print(f"[system] 디자인 {count}개 생성을 시작합니다...")
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i in range(count):
            print(f"\n--- 작업 진행 ({i+1}/{count}) ---")
            if await generate_single_design(browser):
                successes += 1
            await asyncio.sleep(3) 
        await browser.close()

    print(f"\n[결과] 총 {successes}/{count}개 생성 완료")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gemini 기반 디자인 생성기")
    parser.add_argument("--count", type=int, default=3, help="생성할 디자인 수 (기본값: 3)")
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(run_batch(args.count))
    except KeyboardInterrupt:
        print("\n[stop] 사용자에 의해 중단되었습니다.")