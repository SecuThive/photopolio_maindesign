#!/usr/bin/env python3
"""Gemini + Supabase 디자인 자동 생성기 (최적화 버전 v2.3.1).

- [v2.3.1 Fix] Supabase JSON Array 에러 방어 (colors 데이터를 무조건 list로 강제 변환)
- [v2.3.0 Upgrade] 프리미엄 UI/UX 퀄리티 패치 (시니어 디자이너급 프롬프트, 고급 폰트 적용)
- [v2.2.2 Fix] 타임아웃 에러 방어 및 캡처 안정성 강화
- [v2.2 Fix] 프리뷰 깨짐 방지 및 타이트 캡처 로직 적용
- React(JSX) 코드 동시 생성 및 애드센스 승인을 위한 텍스트 설명 보강
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
from typing import Any, Dict, Optional

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
    "Flat Illustration Pop", "Skeuomorphic Modern Leather", "High-Gloss Plastic Candy",
    "Stripe-inspired Fintech Clean", "Linear App Dark Mode Elegance",
    "Apple Premium Glassmorphism", "Vercel-style Developer Minimal",
    "Notion-like Clean Typography", "Modern SaaS Dashboard Aesthetic"
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
    """프리미엄 UI/UX를 강제하는 시니어 디자이너 프롬프트"""
    return (
        "Act as a world-class Senior UI/UX Designer and Frontend Engineer working at a top Silicon Valley agency (like Apple, Stripe, or Linear). "
        f"Design a stunning, production-ready '{category}' component using the '{structure}' layout and '{style}' aesthetic. "
        "\n\n"
        "CRITICAL DESIGN RULES (Must Follow):\n"
        "1. Typography Mastery: Never use generic fonts. Use 'tracking-tight' for bold headings (font-extrabold or font-bold). Use 'text-gray-500' and 'font-medium' for readable subtext. Play with font sizes strategically (e.g., text-sm uppercase tracking-widest for kickers).\n"
        "2. Premium Spacing (8pt Grid): Use generous whitespace. Use p-8, p-12, gap-8. Never cramp elements together.\n"
        "3. Sophisticated Colors: NEVER use pure black (#000000). Use slate-900, zinc-900, or neutral-900 for dark text/backgrounds. Use soft off-whites (bg-gray-50, bg-zinc-50) for backgrounds.\n"
        "4. Depth & Glassmorphism: Use subtle shadows (shadow-sm, shadow-xl) with very low opacity. Use 'backdrop-blur-md bg-white/70' for sticky headers or floating cards. Add delicate borders (border border-gray-200/50) to cards.\n"
        "5. Micro-interactions: Include hover states for ALL clickable elements (hover:bg-gray-100, hover:shadow-md, transition-all duration-300).\n"
        "6. Modern Accents: Use subtle gradients for primary buttons or hero text (bg-gradient-to-r, bg-clip-text, text-transparent).\n"
        "\n"
        "Requirements:\n"
        "1. Output MUST be valid JSON only. Do not wrap in markdown.\n"
        "2. JSON Keys: 'title', 'description', 'features', 'usage', 'html_code', 'react_code', 'colors'.\n"
        "3. Images: Use beautiful unsplash URLs. Include placeholder icons using basic SVG code if needed.\n"
        "4. The UI must be production-ready and fully responsive.\n"
        "5. CRITICAL LAYOUT RULE: Do NOT wrap the component in a `min-h-screen`, `h-screen`, or full-height container unless it is strictly a full dashboard layout. "
        "   The outermost element MUST shrink to fit its content tightly to prevent excessive vertical white space.\n"
    )


def build_prompt_from_request(
    category: str,
    structure: str,
    style: str,
    request_title: str,
    request_description: str,
    target_audience: Optional[str] = None,
    reference_notes: Optional[str] = None,
) -> str:
    base_prompt = build_prompt(category, structure, style)
    request_block = [
        "\n",
        "Request Context (Highest Priority):\n",
        f"- Requested design title: {request_title}\n",
        f"- Requested details: {request_description}\n",
    ]
    if target_audience:
        request_block.append(f"- Target audience: {target_audience}\n")
    if reference_notes:
        request_block.append(f"- References / notes: {reference_notes}\n")
    request_block.append(
        "- IMPORTANT: Follow the request context above while preserving production-ready quality.\n"
    )
    return base_prompt + "".join(request_block)


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
                print(f"[debug] JSON 파싱 실패 (일부 텍스트): {text[:80]}...")
                continue
    raise ValueError("Gemini가 유효한 JSON을 반환하지 않았습니다.")


def wrap_html_if_needed(html: str) -> str:
    """고급 폰트(Inter)를 적용한 캡처 전용 래퍼"""
    if "<html" in html.lower():
        return html

    return (
        "<!DOCTYPE html>\n"
        "<html lang=\"en\">\n"
        "<head>\n"
        "  <meta charset=\"UTF-8\" />\n"
        "  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />\n"
        "  <script src=\"https://cdn.tailwindcss.com\"></script>\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">\n"
        "  <link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>\n"
        "  <link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap\" rel=\"stylesheet\">\n"
        "  <style>\n"
        "    body { font-family: 'Inter', sans-serif; }\n"
        "  </style>\n"
        "  <title>Preview</title>\n"
        "</head>\n"
        "  <body class=\"bg-gray-50 text-slate-900 antialiased m-0 p-0\">\n"
        "    <div id=\"capture-box\" class=\"w-full max-w-[1400px] mx-auto flow-root\">\n"
        f"      {html}\n"
        "    </div>\n"
        "  </body>\n"
        "</html>"
    )


async def capture_screenshot(browser: Browser, html: str) -> bytes:
    page = await browser.new_page(viewport={"width": 1400, "height": 900})

    try:
        try:
            await page.set_content(html, wait_until="load", timeout=15000)
        except Exception as load_err:
            print(f"[warning] 페이지 로딩 지연 (무시하고 캡처 진행): {load_err}")

        await page.wait_for_timeout(3000)

        await page.evaluate("""
            (() => {
              const root = document.getElementById('capture-box') || document.body;
              if (!root) return;

              const selector = [
                '.min-h-screen',
                '.h-screen',
                '.min-h-\\\\[100vh\\\\]',
                '.h-\\\\[100vh\\\\]'
              ].join(', ');

              const targets = root.querySelectorAll(selector);
              targets.forEach(el => {
                el.classList.remove('min-h-screen', 'h-screen', 'min-h-[100vh]', 'h-[100vh]');
                el.style.minHeight = 'auto';
                el.style.height = 'auto';
              });

              const all = root.querySelectorAll('*');
              all.forEach(el => {
                const mh = (el.style && el.style.minHeight) ? el.style.minHeight : '';
                const h  = (el.style && el.style.height) ? el.style.height : '';
                if (mh.includes('100vh')) el.style.minHeight = 'auto';
                if (h.includes('100vh')) el.style.height = 'auto';
              });

              document.documentElement.style.margin = '0';
              document.documentElement.style.padding = '0';
              document.body.style.margin = '0';
              document.body.style.padding = '0';
            })();
        """)

        await page.wait_for_timeout(200)

        dims = await page.evaluate("""
            (() => {
              const el = document.getElementById('capture-box') || document.body;
              const rect = el.getBoundingClientRect();
              const height = Math.ceil(el.scrollHeight || rect.height || 900);
              return { height };
            })();
        """)
        height = int(dims.get("height", 900))
        height = max(900, min(height + 50, 6000))
        await page.set_viewport_size({"width": 1400, "height": height})
        await page.wait_for_timeout(200)

        target = await page.query_selector("#capture-box") or await page.query_selector("body")
        screenshot = await target.screenshot(type="png")

    except Exception as e:
        print(f"[error] 캡처 중 에러 발생, 기본 바디 캡처로 대체: {e}")
        target = await page.query_selector("body")
        screenshot = await target.screenshot(type="png")

    finally:
        await page.close()

    return screenshot


def upload_image(image_bytes: bytes, category: str) -> str:
    filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{slugify(category)}_{uuid.uuid4().hex[:6]}.png"
    object_path = f"{STORAGE_FOLDER}/{filename}"
    supabase.storage.from_(STORAGE_BUCKET).upload(
        object_path,
        image_bytes,
        {"content-type": "image/png"},
    )
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


def normalize_request_category(value: Optional[str]) -> str:
    if not value:
        return random.choice(CATEGORIES)

    normalized = value.strip().lower()
    mapping = {
        "landing page": "Landing Page",
        "dashboard": "Dashboard",
        "e-commerce": "E-commerce",
        "ecommerce": "E-commerce",
        "portfolio": "Portfolio",
        "blog": "Blog",
        "component": "Component",
        "components": "Component",
    }
    return mapping.get(normalized, "Landing Page")


def fetch_next_pending_request() -> Optional[Dict[str, Any]]:
    try:
        response = (
            supabase.table("design_requests")
            .select("id,title,description,category,target_audience,reference_notes,vote_count")
            .eq("status", "pending")
            .order("vote_count", desc=True)
            .order("created_at", desc=False)
            .limit(1)
            .execute()
        )
        rows = response.data or []
        if not rows:
            return None
        return rows[0]
    except Exception as exc:
        print(f"[warning] 신청 테이블 조회 실패 (랜덤 모드로 계속): {exc}")
        return None


def update_request_status(request_id: str, status: str, linked_design_id: Optional[str] = None) -> None:
    payload: Dict[str, Any] = {"status": status}
    if linked_design_id:
        payload["linked_design_id"] = linked_design_id
    (
        supabase.table("design_requests")
        .update(payload)
        .eq("id", request_id)
        .execute()
    )


async def generate_single_design(
    browser: Browser,
    max_attempts: int = 3,
    source_request: Optional[Dict[str, Any]] = None,
) -> tuple[bool, Optional[str]]:
    for attempt in range(1, max_attempts + 1):
        category = normalize_request_category(source_request.get("category")) if source_request else random.choice(CATEGORIES)
        structure = random.choice(STRUCTURES)
        style = random.choice(STYLES)
        combo_key = f"{structure}_{style}".lower().replace(" ", "_")

        if source_request:
            prompt = build_prompt_from_request(
                category=category,
                structure=structure,
                style=style,
                request_title=str(source_request.get("title", "Untitled Request")),
                request_description=str(source_request.get("description", "")),
                target_audience=source_request.get("target_audience"),
                reference_notes=source_request.get("reference_notes"),
            )
            print(f"[request] 신청기반 | {category} | {structure} | {style} | {source_request.get('title')}")
        else:
            prompt = build_prompt(category, structure, style)
            print(f"[request] 랜덤 | {category} | {structure} | {style}")

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

            # [방어 로직] AI가 던진 colors 데이터를 무조건 List로 강제 변환
            raw_colors = payload.get("colors", [])
            safe_colors = []
            if isinstance(raw_colors, list):
                safe_colors = [str(c) for c in raw_colors]
            elif isinstance(raw_colors, dict):
                safe_colors = [str(v) for v in raw_colors.values()]
            elif isinstance(raw_colors, str):
                safe_colors = [raw_colors]

            screenshot = await capture_screenshot(browser, wrapped_html)
            image_url = upload_image(screenshot, category)
            slug = ensure_unique_slug(payload.get("title", "Untitled Design"))
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
                "colors": safe_colors,  # 안전하게 정제된 데이터 삽입
                "slug": slug,
                "status": "published",
                "sns_promoted": False,
                "pinterest_promoted": False,
                "created_at": datetime.utcnow().isoformat(),
            }

            supabase.table("designs").insert(record).execute()
            print(f"[success] 저장 완료: {record['title']} ({slug})")
            return True, design_id

        except Exception as exc:
            message = str(exc)
            if "429" in message or "quota" in message.lower():
                print("[error] Gemini API 할당량 초과. 잠시 대기하거나 중단합니다.")
                return False, None
            print(f"[retry] 에러 발생 (시도 {attempt}/{max_attempts}): {exc}")
            await asyncio.sleep(2)

    return False, None


async def run_batch(count: int, use_requests: bool, requests_only: bool) -> None:
    successes = 0
    mode = "신청 우선" if use_requests else "랜덤"
    print(f"[system] 디자인 {count}개 생성을 시작합니다... (모드: {mode})")

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i in range(count):
            print(f"\n--- 작업 진행 ({i+1}/{count}) ---")
            source_request: Optional[Dict[str, Any]] = None

            if use_requests:
                source_request = fetch_next_pending_request()
                if source_request:
                    try:
                        update_request_status(source_request["id"], "in_progress")
                    except Exception as exc:
                        print(f"[warning] 신청 상태 업데이트 실패(in_progress): {exc}")
                elif requests_only:
                    print("[info] 처리할 pending 신청이 없습니다. 요청 모드를 종료합니다.")
                    break

            ok, design_id = await generate_single_design(browser, source_request=source_request)
            if ok:
                successes += 1
                if source_request and design_id:
                    try:
                        update_request_status(source_request["id"], "completed", linked_design_id=design_id)
                        print(f"[success] 신청 완료 처리: {source_request['id']} -> {design_id}")
                    except Exception as exc:
                        print(f"[warning] 신청 완료 업데이트 실패: {exc}")
            elif source_request:
                try:
                    update_request_status(source_request["id"], "pending")
                    print(f"[info] 신청 재대기 처리: {source_request['id']}")
                except Exception as exc:
                    print(f"[warning] 신청 재대기 업데이트 실패: {exc}")
            await asyncio.sleep(3)
        await browser.close()

    print(f"\n[결과] 총 {successes}/{count}개 생성 완료")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Gemini 기반 디자인 생성기")
    parser.add_argument("--count", type=int, default=3, help="생성할 디자인 수 (기본값: 3)")
    parser.add_argument(
        "--use-requests",
        action="store_true",
        help="design_requests의 pending 요청을 우선 처리합니다.",
    )
    parser.add_argument(
        "--requests-only",
        action="store_true",
        help="pending 요청만 처리하고 없으면 종료합니다. (use-requests 포함)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    try:
        asyncio.run(
            run_batch(
                args.count,
                use_requests=(args.use_requests or args.requests_only),
                requests_only=args.requests_only,
            )
        )
    except KeyboardInterrupt:
        print("\n[stop] 사용자에 의해 중단되었습니다.")
