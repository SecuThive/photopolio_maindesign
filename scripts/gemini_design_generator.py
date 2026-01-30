#!/usr/bin/env python3
"""Gemini + Supabase 디자인 자동 생성기.

- Gemini 3.0 Flash JSON 모드로 HTML/Tailwind 코드 생성
- Playwright로 스크린샷 촬영 후 Supabase Storage 업로드
- designs 테이블에 레코드 삽입 및 중복 조합 방지

필수 환경 변수 (.env 등)
- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY
- GEMINI_API_KEY
선택 환경 변수
- GEMINI_MODEL (기본값: gemini-3.0-flash)
- SUPABASE_DESIGNS_BUCKET (기본값: designs-bucket)
- SUPABASE_DESIGNS_FOLDER (기본값: designs)
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import random
import re
import hashlib
import subprocess
import tempfile
from pathlib import Path
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from google import genai
from playwright.async_api import async_playwright
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
STORAGE_BUCKET = os.getenv("SUPABASE_DESIGNS_BUCKET", "designs-bucket")
STORAGE_FOLDER = os.getenv("SUPABASE_DESIGNS_FOLDER", "designs")

if not all([SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY]):
    raise RuntimeError("SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, GEMINI_API_KEY가 필요합니다.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

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
    # --- 추가된 구조 ---
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
    # --- 추가된 스타일 ---
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


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "design"


def build_prompt(category: str, structure: str, style: str) -> str:
    return (
        "Act as a senior UI engineer. "
        f"Create a {category} experience using the '{structure}' layout and '{style}' art direction. "
        "The output must be valid JSON with keys: title (string), description (4 sentences including security & UX tips), "
        "code (full HTML + Tailwind CSS), colors (array of 3-6 HEX values). "
        "Ensure Tailwind classes are embedded directly in the markup and focus on production-ready UI.")


def parse_gemini_json(response: Any) -> Dict[str, Any]:
    candidates = getattr(response, "candidates", None) or []
    for candidate in candidates:
        parts = getattr(getattr(candidate, "content", None), "parts", [])
        for part in parts:
            text = getattr(part, "text", "").strip()
            if not text:
                continue
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                continue
    raise ValueError("Gemini가 유효한 JSON을 반환하지 않았습니다.")


def ensure_payload_shape(payload: Dict[str, Any]) -> Dict[str, Any]:
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
    response = supabase.table("designs").select("id", count="exact").eq("prompt", combo_key).limit(1).execute()
    return bool(response.data)


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


def wrap_html_if_needed(html: str) -> str:
    if "<html" in html.lower():
        return html
    return f"<!DOCTYPE html>\n<html lang=\"en\">\n<head>\n  <meta charset=\"UTF-8\" />\n  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n  <script src=\"https://cdn.tailwindcss.com\"></script>\n  <title>AI Design</title>\n</head>\n<body class=\"min-h-screen bg-gray-50 flex items-center justify-center p-10\">\n{html}\n</body>\n</html>"


async def capture_screenshot(html: str) -> bytes:
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1400, "height": 900})
        await page.set_content(html, wait_until="networkidle")
        await page.wait_for_timeout(800)
        screenshot = await page.screenshot(full_page=True, type="png")
        await browser.close()
    return screenshot


def upload_image(image_bytes: bytes, category: str) -> str:
    filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{category.replace(' ', '_')}_{uuid.uuid4().hex[:6]}.png"
    object_path = f"{STORAGE_FOLDER}/{filename}"
    storage = supabase.storage.from_(STORAGE_BUCKET)
    storage.upload(object_path, image_bytes, {"content-type": "image/png"})
    return storage.get_public_url(object_path)


async def generate_single_design(max_attempts: int = 3) -> bool:
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
            response = await asyncio.to_thread(
                gemini_client.models.generate_content,
                model=GEMINI_MODEL,
                config={"response_mime_type": "application/json"},
                contents=[{"role": "user", "parts": [{"text": prompt}]}],
            )
            payload = ensure_payload_shape(parse_gemini_json(response))
            html = wrap_html_if_needed(payload["code"])
            screenshot = await capture_screenshot(html)
            image_url = upload_image(screenshot, category)
            slug = ensure_unique_slug(payload["title"])

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
            print(f"[success] 저장 완료: {payload['title']}")
            return True

        except Exception as exc:  # pragma: no cover - 런타임 네트워크 예외 처리
            message = str(exc)
            if "429" in message or "quota" in message.lower():
                print("[error] Gemini API 할당량 초과. 24시간 대기 필요.")
                return False
            print(f"[retry] 에러 발생 (시도 {attempt}/{max_attempts}): {exc}")

    return False


async def run_batch(count: int) -> None:
    successes = 0
    for _ in range(count):
        created = await generate_single_design()
        if created:
            successes += 1
    print(f"총 {successes}/{count}개 생성 완료")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gemini 기반 디자인 생성기")
    parser.add_argument("--count", type=int, default=1, help="생성할 디자인 수")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    asyncio.run(run_batch(args.count))
