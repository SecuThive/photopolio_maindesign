#!/usr/bin/env python3
"""UI-Syntax Design Generator v4.0 Pro — Ollama Multi-Model Pipeline.

Architecture:
  [Phase 1] Designer (qwen2.5-coder:32b)  → 디자인 생성
  [Phase 2] Critic  (deepseek-r1:14b)     → 구조적 리뷰 + 점수
  [Phase 3] Refiner (qwen2.5-coder:32b)   → 피드백 반영 개선
  [Gate]    score < threshold → Phase 1부터 재시도

No external API keys needed. 100% local Ollama.
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
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from dotenv import load_dotenv
from playwright.async_api import async_playwright, Browser
from supabase import Client, create_client

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)
log = logging.getLogger("gen4pro")

# ---------------------------------------------------------------------------
# Environment
# ---------------------------------------------------------------------------
ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT / ".env")

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
STORAGE_BUCKET = os.getenv("SUPABASE_DESIGNS_BUCKET", "designs-bucket")
STORAGE_FOLDER = os.getenv("SUPABASE_DESIGNS_FOLDER", "designs")

OLLAMA_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")
DESIGNER_MODEL = os.getenv("DESIGNER_MODEL", "qwen2.5-coder:32b")
CRITIC_MODEL = os.getenv("CRITIC_MODEL", "deepseek-r1:14b")
REFINER_MODEL = os.getenv("REFINER_MODEL", "qwen2.5-coder:32b")

QUALITY_THRESHOLD = int(os.getenv("QUALITY_THRESHOLD", "60"))
MAX_ATTEMPTS = int(os.getenv("MAX_ATTEMPTS", "3"))

if not all([SUPABASE_URL, SUPABASE_KEY]):
    raise RuntimeError("SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY 필요")

# ---------------------------------------------------------------------------
# Lazy Supabase client
# ---------------------------------------------------------------------------
_supabase: Optional[Client] = None


def get_supabase() -> Client:
    global _supabase
    if _supabase is None:
        _supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase


# ---------------------------------------------------------------------------
# Ollama client
# ---------------------------------------------------------------------------
import httpx

OLLAMA_TIMEOUT = 600  # 32b 모델은 응답이 느릴 수 있음


async def ollama_generate(model: str, prompt: str, temperature: float = 0.7) -> str:
    async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
        log.info("[ollama] → %s (temp=%.1f)", model, temperature)
        t0 = time.monotonic()
        resp = await client.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_ctx": 16384,
                    "top_p": 0.9,
                },
            },
        )
        resp.raise_for_status()
        elapsed = time.monotonic() - t0
        text = resp.json().get("response", "").strip()
        log.info("[ollama] ← %s (%.1fs, %d chars)", model, elapsed, len(text))
        return text


# ---------------------------------------------------------------------------
# JSON parsing
# ---------------------------------------------------------------------------

def clean_json(text: str) -> str:
    text = text.strip()
    # deepseek-r1 <think>...</think> 블록 제거
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL).strip()
    m = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    start = text.find("{")
    end = text.rfind("}")
    if start >= 0 and end > start:
        text = text[start : end + 1]
    text = re.sub(r",\s*([}\]])", r"\1", text)
    text = text.replace("\u201c", '"').replace("\u201d", '"')
    text = text.replace("\u2018", "'").replace("\u2019", "'")
    return text


def parse_json_safe(text: str) -> Dict[str, Any]:
    for candidate in [text, clean_json(text)]:
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            continue
    raise ValueError(f"JSON 파싱 실패: {text[:300]}...")


# ---------------------------------------------------------------------------
# Design Constants
# ---------------------------------------------------------------------------

CATEGORIES = ["Landing Page", "Dashboard", "E-commerce", "Portfolio", "Blog", "Component"]

STRUCTURES: Dict[str, List[str]] = {
    "Landing Page": [
        "Hero with Center CTA + Feature Grid + Social Proof + Footer",
        "Split Screen Hero (Text Left, Visual Right) + Benefits Strip + Testimonials",
        "Full-width Video Background Hero + Floating Stats Bar + CTA Section",
        "Bento Grid Hero + Icon Feature Cards + Pricing Table",
        "Asymmetric Hero with Overlapping Cards + Logo Wall + FAQ Accordion",
        "Minimal Single-Column Hero + Horizontal Scroll Features + Newsletter",
        "Gradient Mesh Hero + Animated Counter Stats + Team Grid",
    ],
    "Dashboard": [
        "Sidebar Nav + KPI Cards Row + Charts Grid + Activity Feed",
        "Top Nav + Tab Panels + Data Table with Pagination",
        "Collapsible Sidebar + Kanban Board + Quick Actions FAB",
        "Header Stats Bar + Split Panel (Charts Left, Table Right)",
        "Command Palette Header + Metric Tiles + Timeline Feed",
        "Minimal Top Nav + Full-width Analytics Charts + Alert Cards",
    ],
    "E-commerce": [
        "Hero Sale Banner + Product Grid with Filters + Quick View Modal",
        "Product Detail: Gallery Left + Info Right + Tabs (Reviews/Specs)",
        "Category Page: Breadcrumbs + Filter Sidebar + Product Cards Grid",
        "Cart/Checkout: Progress Steps + Items List + Order Summary Sidebar",
        "Wishlist Grid + Recommendation Carousel + Recently Viewed",
        "Search Results: Faceted Filters + List/Grid Toggle + Sort Controls",
    ],
    "Portfolio": [
        "Masonry Project Grid + Hover Overlay Details + Filter Tabs",
        "Minimal Timeline: Year Markers + Project Cards + Skill Tags",
        "Hero Bio + Horizontal Scroll Project Showcase + Contact Form",
        "Bento Grid Portfolio + Stats Counter + Testimonials Carousel",
        "Full-page Project Case Study Layout + Next/Prev Navigation",
    ],
    "Blog": [
        "Featured Article Hero + 2-Column Recent Grid + Sidebar Categories",
        "Magazine Layout: Large Feature + Small Grid + Newsletter CTA",
        "Minimal Article: Centered Prose + TOC Sidebar + Related Posts",
        "Card-based Feed + Tag Filters + Infinite Scroll Skeleton",
    ],
    "Component": [
        "Pricing Table: 3-Tier with Popular Badge + Feature Comparison",
        "Testimonial Section: Cards with Avatars + Star Ratings + Carousel",
        "Contact Form: Floating Labels + Validation States + Map Background",
        "CTA Section: Gradient Background + Dual Buttons + Trust Badges",
        "Feature Comparison Table + Toggle Annual/Monthly + Highlight Row",
        "Authentication: Split Screen Login/Register + Social OAuth Buttons",
    ],
}

STYLES = [
    "Apple Minimal — bg-white, Inter, slate-900 text, blue-600 accent, generous whitespace, subtle shadows",
    "Vercel Developer Dark — bg-black/bg-zinc-950, Geist/mono, white text, blue-500 links, code-block feel",
    "Stripe Fintech — bg-white, indigo-600 primary, crisp borders, clean data presentation, trust-focused",
    "Linear Elegant Dark — bg-zinc-950, purple-500 accent, subtle gradients, SF Pro vibe, smooth transitions",
    "Notion Clean — bg-white, system font, warm-gray text, minimal borders, content-first hierarchy",
    "Glassmorphism Frosted — backdrop-blur-xl, bg-white/10, border-white/20, gradient mesh background",
    "Neo-Brutalism — bold bg-yellow-300/lime-300, thick 2px black borders, shadow-[4px_4px_0] solid, chunky type",
    "Soft Pastel Gradient — bg-gradient rose-to-violet, rounded-3xl cards, soft shadow-xl, dreamy feel",
    "Cyberpunk Neon — bg-gray-950, neon cyan/magenta accents, glowing ring borders, mono font, tech grid",
    "Luxury Gold & Dark — bg-zinc-900, amber-400/yellow-500 accents, serif headings, wide letter-spacing",
    "Nordic Frost — bg-slate-50, cool blue-gray palette, clean geometric lines, lots of breathing room",
    "Modern SaaS — bg-white, violet-600 primary, pill-shaped buttons, gradient hero text, social proof focus",
    "Sunset Warm — bg-orange-50, amber-to-rose gradient accents, rounded cards, warm comfortable feel",
    "Deep Ocean Dark — bg-slate-900, teal-400 accents, flowing wave decorations, layered depth",
    "Japanese Zen — bg-stone-50, minimal ink palette, asymmetric whitespace, refined simplicity",
    "High-tech Grid — bg-gray-950, emerald-400 mono accents, dot-grid pattern bg, data-visualization feel",
    "Claymorphism Soft 3D — bg-neutral-100, rounded-2xl, inset shadow + outer shadow, puffy tactile feel",
    "Editorial Magazine — off-white bg, serif+sans combo, editorial grid, large typography, print-inspired",
]

# ---------------------------------------------------------------------------
# Prompt: Phase 1 — Designer
# ---------------------------------------------------------------------------

def build_designer_prompt(category: str, structure: str, style: str) -> str:
    return f"""You are a world-class Senior UI/UX Designer and Frontend Engineer.
Design a production-ready "{category}" page.

LAYOUT: {structure}
AESTHETIC: {style}

━━━ MANDATORY DESIGN RULES ━━━

TYPOGRAPHY:
• Inter font via Google Fonts CDN. tracking-tight on headings (text-3xl+).
• Headings: font-extrabold or font-bold. Body: text-gray-600 font-medium.
• Kickers/labels: text-xs uppercase tracking-widest font-semibold with accent color.
• NEVER use default browser serif. NEVER text-black.

SPACING:
• 8pt grid: p-6, p-8, p-12, gap-6, gap-8. Sections: py-16 md:py-24.
• max-w-7xl mx-auto for containment. Cards: p-6 md:p-8 rounded-xl.
• CRITICAL: NO min-h-screen or h-screen on outermost element.

COLOR:
• NEVER #000000. Dark text = slate-900/zinc-900. Backgrounds = gray-50/zinc-50/white.
• ONE consistent accent color. Gradients for hero text or buttons.

DEPTH:
• Cards: border border-gray-200/60 shadow-sm hover:shadow-lg transition-all duration-300.
• Glassmorphism where fit: backdrop-blur-xl bg-white/80.

INTERACTIONS:
• ALL buttons: hover state + active:scale-[0.98] + transition-all duration-200.
• Cards: hover:-translate-y-1 hover:shadow-xl. Links: hover:underline.
• group/group-hover for reveal effects.

ICONS:
• Use inline SVG icons (simple Lucide-style paths). NO external icon URLs.
• For images: use gradient/colored placeholder divs or simple SVG illustrations.
• NEVER use example.com, placeholder.com, or broken image URLs.
• For avatars: colored circles with text initials.

CONTENT:
• Headlines: 5-8 words, benefit-driven. No "Welcome to our platform".
• Button labels: specific actions ("Start Building Free", "View Live Demo").
• Feature names: realistic ("Real-time Collaboration", "End-to-end Encryption").
• Use realistic SaaS/product context. No lorem ipsum.

ACCESSIBILITY:
• Semantic: <header>, <main>, <section>, <nav>, <footer>.
• Buttons must be <button> or <a>. All have focus:ring-2 states.

━━━ OUTPUT ━━━

Return ONLY valid JSON (no markdown fences, no explanation):
{{
  "title": "Compelling design title",
  "description": "2-3 sentences about this design and target audience",
  "concept": "Creative direction / design rationale in 1-2 sentences",
  "features": ["Specific feature 1", "Specific feature 2", "..."],
  "usage": "How a developer would use this component",
  "html_code": "COMPLETE standalone HTML document with <!DOCTYPE html>, Tailwind CDN script tag, Inter font link, fully renderable",
  "react_code": "Equivalent React functional component using Tailwind classes",
  "colors": ["#hex1", "#hex2", "#hex3", "#hex4", "#hex5"]
}}

The html_code MUST be a complete HTML document that renders perfectly when opened in a browser.
Include <script src="https://cdn.tailwindcss.com"></script> and Inter font <link> in <head>."""


# ---------------------------------------------------------------------------
# Prompt: Phase 2 — Critic
# ---------------------------------------------------------------------------

def build_critic_prompt(design_json: Dict[str, Any]) -> str:
    html_preview = design_json.get("html_code", "")[:4000]
    return f"""You are a harsh but fair senior design critic at a top agency.
Review this UI design for real-world production quality.

DESIGN TITLE: {design_json.get('title', 'Untitled')}
CONCEPT: {design_json.get('concept', '')}
COLORS: {design_json.get('colors', [])}

HTML CODE (first 4000 chars):
{html_preview}

━━━ EVALUATION CRITERIA (score each 1-10) ━━━

1. visual_hierarchy — Is there a clear primary → secondary → tertiary flow?
2. typography — Inter font? tracking-tight headings? Proper weight usage? No text-black?
3. spacing — 8pt grid? Generous whitespace? No cramped sections?
4. color_harmony — Cohesive palette? No pure #000000? Consistent accent?
5. interaction_design — Hover states on all clickables? Transitions? Focus rings?
6. content_quality — Realistic copy? No lorem/placeholder? Benefit-driven headlines?
7. layout_structure — Proper semantic HTML? Responsive hints? Logical section flow?
8. visual_polish — Shadows, borders, gradients used well? Premium feel?
9. icon_imagery — SVG icons used? No broken image URLs? Proper placeholders?
10. overall_impression — Would this pass review at Stripe/Linear/Vercel?

━━━ OUTPUT ━━━

Return ONLY valid JSON (no markdown fences):
{{
  "scores": {{
    "visual_hierarchy": 0,
    "typography": 0,
    "spacing": 0,
    "color_harmony": 0,
    "interaction_design": 0,
    "content_quality": 0,
    "layout_structure": 0,
    "visual_polish": 0,
    "icon_imagery": 0,
    "overall_impression": 0
  }},
  "total": 0,
  "strengths": ["strength 1", "strength 2", "strength 3"],
  "critical_issues": ["most important issue to fix", "second issue", "third issue"],
  "specific_improvements": [
    "Exact CSS/Tailwind change to make (e.g., 'Change p-4 to p-8 on the hero section')",
    "Another specific fix",
    "Another specific fix"
  ],
  "verdict": "PASS or FAIL"
}}

Be brutally honest. A score of 70+ means genuinely production-ready.
Most AI-generated designs score 40-60. Only give 80+ to truly exceptional work."""


# ---------------------------------------------------------------------------
# Prompt: Phase 3 — Refiner
# ---------------------------------------------------------------------------

def build_refiner_prompt(
    original: Dict[str, Any],
    review: Dict[str, Any],
    category: str,
    structure: str,
    style: str,
) -> str:
    issues = review.get("critical_issues", [])
    improvements = review.get("specific_improvements", [])
    scores = review.get("scores", {})
    weakest = sorted(scores.items(), key=lambda x: x[1])[:3] if scores else []

    return f"""You are a senior frontend engineer fixing a design that failed review.

ORIGINAL TITLE: {original.get('title', '')}
CATEGORY: {category} | LAYOUT: {structure} | STYLE: {style}
REVIEW SCORE: {review.get('total', 0)}/100

WEAKEST AREAS:
{chr(10).join(f'• {k}: {v}/10' for k, v in weakest)}

CRITICAL ISSUES TO FIX:
{chr(10).join(f'• {i}' for i in issues)}

SPECIFIC CHANGES REQUIRED:
{chr(10).join(f'• {i}' for i in improvements)}

ORIGINAL HTML:
{original.get('html_code', '')}

━━━ YOUR TASK ━━━

Rewrite the HTML from scratch, addressing EVERY issue above. The result must:
1. Fix all critical issues identified by the reviewer
2. Apply all specific improvements
3. Strengthen the weakest scoring areas
4. Maintain the original design concept but elevate the execution
5. Be a COMPLETE standalone HTML document with Tailwind CDN + Inter font

Return ONLY valid JSON (no markdown fences):
{{
  "title": "Improved title",
  "description": "Updated description",
  "concept": "Refined creative direction",
  "features": ["feature1", "feature2", "..."],
  "usage": "Usage description",
  "html_code": "COMPLETE improved HTML document",
  "react_code": "Improved React component",
  "colors": ["#hex1", "#hex2", "#hex3", "#hex4", "#hex5"]
}}

Make it genuinely world-class. This is the final version that ships."""


# ---------------------------------------------------------------------------
# Utility
# ---------------------------------------------------------------------------

def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "design"


def normalize_colors(raw: Any) -> List[str]:
    if isinstance(raw, list):
        return [str(c) for c in raw if c]
    if isinstance(raw, dict):
        return [str(v) for v in raw.values() if v]
    if isinstance(raw, str):
        return [c.strip() for c in raw.split(",") if c.strip()]
    return []


def infer_tags(category: str, structure: str, style: str, title: str) -> List[str]:
    tags = []
    kw_map = {
        "hero": "hero", "pricing": "pricing", "dashboard": "dashboard",
        "saas": "saas", "card": "cards", "grid": "grid", "form": "form",
        "table": "table", "dark": "dark-mode", "light": "light-mode",
        "e-commerce": "ecommerce", "product": "product", "blog": "blog",
        "portfolio": "portfolio", "login": "auth", "testimonial": "social-proof",
        "cta": "conversion", "minimal": "minimal", "glassmorphism": "glassmorphism",
        "neon": "neon", "gradient": "gradient", "checkout": "checkout",
    }
    combined = f"{category} {structure} {style} {title}".lower()
    for kw, tag in kw_map.items():
        if kw in combined and tag not in tags:
            tags.append(tag)
    return tags[:8]


def ensure_unique_slug(base_title: str) -> str:
    base = slugify(base_title)
    candidate = base
    suffix = 2
    sb = get_supabase()
    while True:
        resp = sb.table("designs").select("id").eq("slug", candidate).limit(1).execute()
        if not resp.data:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1


# ---------------------------------------------------------------------------
# HTML Wrapper
# ---------------------------------------------------------------------------

def wrap_html(html: str) -> str:
    if "<html" in html.lower():
        if "cdn.tailwindcss.com" not in html:
            html = html.replace("</head>", '  <script src="https://cdn.tailwindcss.com"></script>\n</head>')
        return html

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <style>
    body {{ font-family: 'Inter', system-ui, -apple-system, sans-serif; -webkit-font-smoothing: antialiased; }}
  </style>
</head>
<body class="bg-gray-50 text-slate-900 antialiased m-0 p-0">
  <div id="capture-box" class="w-full max-w-[1400px] mx-auto flow-root">
    {html}
  </div>
</body>
</html>"""


# ---------------------------------------------------------------------------
# Screenshot Capture (tight capture from v2.3.1)
# ---------------------------------------------------------------------------

async def capture_screenshot(browser: Browser, html: str) -> bytes:
    page = await browser.new_page(viewport={"width": 1400, "height": 900})
    try:
        try:
            await page.set_content(html, wait_until="load", timeout=15000)
        except Exception as e:
            log.warning("페이지 로딩 지연: %s", e)

        await page.wait_for_timeout(3000)

        await page.evaluate("""(() => {
            const root = document.getElementById('capture-box') || document.body;
            root.querySelectorAll('.min-h-screen,.h-screen').forEach(el => {
                el.classList.remove('min-h-screen','h-screen');
                el.style.minHeight = 'auto';
                el.style.height = 'auto';
            });
            root.querySelectorAll('*').forEach(el => {
                if (el.style?.minHeight?.includes('100vh')) el.style.minHeight = 'auto';
                if (el.style?.height?.includes('100vh')) el.style.height = 'auto';
            });
            document.documentElement.style.margin = '0';
            document.body.style.margin = '0';
        })()""")
        await page.wait_for_timeout(200)

        dims = await page.evaluate("""(() => {
            const el = document.getElementById('capture-box') || document.body;
            return { height: Math.ceil(el.scrollHeight || 900) };
        })()""")
        height = max(900, min(int(dims.get("height", 900)) + 50, 6000))
        await page.set_viewport_size({"width": 1400, "height": height})
        await page.wait_for_timeout(200)

        target = await page.query_selector("#capture-box") or await page.query_selector("body")
        screenshot = await target.screenshot(type="png")
    except Exception as e:
        log.error("캡처 에러, body 대체: %s", e)
        target = await page.query_selector("body")
        screenshot = await target.screenshot(type="png")
    finally:
        await page.close()
    return screenshot


# ---------------------------------------------------------------------------
# Supabase upload
# ---------------------------------------------------------------------------

def upload_image(image_bytes: bytes, slug: str) -> str:
    filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{slug}_{uuid.uuid4().hex[:6]}.png"
    path = f"{STORAGE_FOLDER}/{filename}"
    sb = get_supabase()
    sb.storage.from_(STORAGE_BUCKET).upload(path, image_bytes, {"content-type": "image/png"})
    return sb.storage.from_(STORAGE_BUCKET).get_public_url(path)


# ---------------------------------------------------------------------------
# Design Request Support
# ---------------------------------------------------------------------------

def fetch_pending_request() -> Optional[Dict[str, Any]]:
    try:
        resp = (
            get_supabase().table("design_requests")
            .select("id,title,description,category,target_audience,reference_notes,vote_count")
            .eq("status", "pending")
            .order("vote_count", desc=True)
            .order("created_at", desc=False)
            .limit(1)
            .execute()
        )
        return (resp.data or [None])[0]
    except Exception as e:
        log.warning("신청 조회 실패: %s", e)
        return None


def update_request_status(req_id: str, status: str, design_id: Optional[str] = None):
    payload: Dict[str, Any] = {"status": status}
    if design_id:
        payload["linked_design_id"] = design_id
    get_supabase().table("design_requests").update(payload).eq("id", req_id).execute()


# ---------------------------------------------------------------------------
# Core Pipeline
# ---------------------------------------------------------------------------

async def generate_design(
    browser: Browser,
    source_request: Optional[Dict[str, Any]] = None,
) -> Tuple[bool, Optional[str]]:

    category = random.choice(CATEGORIES)
    structures_for_cat = STRUCTURES.get(category, STRUCTURES["Landing Page"])
    structure = random.choice(structures_for_cat)
    style = random.choice(STYLES)

    if source_request:
        cat_raw = source_request.get("category", "")
        if cat_raw:
            from difflib import get_close_matches
            match = get_close_matches(cat_raw, CATEGORIES, n=1, cutoff=0.4)
            if match:
                category = match[0]
                structures_for_cat = STRUCTURES.get(category, STRUCTURES["Landing Page"])
                structure = random.choice(structures_for_cat)

    log.info("=" * 60)
    log.info("[config] Category: %s", category)
    log.info("[config] Structure: %s", structure)
    log.info("[config] Style: %s", style)
    log.info("=" * 60)

    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            # ── Phase 1: Designer generates ──
            log.info("[phase1] Designer (%s) 생성 중...", DESIGNER_MODEL)
            designer_prompt = build_designer_prompt(category, structure, style)
            if source_request:
                designer_prompt += (
                    f"\n\nUSER REQUEST (highest priority):\n"
                    f"- Title: {source_request.get('title', '')}\n"
                    f"- Description: {source_request.get('description', '')}\n"
                )
                if source_request.get("target_audience"):
                    designer_prompt += f"- Audience: {source_request['target_audience']}\n"

            raw = await ollama_generate(DESIGNER_MODEL, designer_prompt, temperature=0.7)
            design = parse_json_safe(raw)

            if not design.get("html_code"):
                log.warning("[phase1] html_code 비어있음, 재시도")
                continue

            log.info("[phase1] ✓ '%s' 생성 완료", design.get("title", "?"))

            # ── Phase 2: Critic reviews ──
            log.info("[phase2] Critic (%s) 리뷰 중...", CRITIC_MODEL)
            critic_prompt = build_critic_prompt(design)
            raw_review = await ollama_generate(CRITIC_MODEL, critic_prompt, temperature=0.3)
            review = parse_json_safe(raw_review)

            total = review.get("total", 0)
            verdict = review.get("verdict", "FAIL")
            log.info("[phase2] ✓ Score: %d/100 | Verdict: %s", total, verdict)

            if review.get("critical_issues"):
                for issue in review["critical_issues"][:3]:
                    log.info("[phase2]   ✗ %s", issue)

            # ── Phase 3: Refine if needed ──
            if total < QUALITY_THRESHOLD:
                log.info("[phase3] Score %d < %d, Refiner (%s) 개선 중...",
                         total, QUALITY_THRESHOLD, REFINER_MODEL)
                refiner_prompt = build_refiner_prompt(design, review, category, structure, style)
                raw_improved = await ollama_generate(REFINER_MODEL, refiner_prompt, temperature=0.6)
                improved = parse_json_safe(raw_improved)

                if improved.get("html_code"):
                    design = improved
                    log.info("[phase3] ✓ '%s' 개선 완료", design.get("title", "?"))

                    # Quick re-review for logging (don't block on this)
                    log.info("[phase3] 개선본 빠른 리뷰...")
                    raw_re = await ollama_generate(CRITIC_MODEL, build_critic_prompt(design), temperature=0.3)
                    try:
                        re_review = parse_json_safe(raw_re)
                        total = re_review.get("total", total)
                        log.info("[phase3] ✓ Improved score: %d/100", total)
                    except Exception:
                        log.warning("[phase3] 리뷰 파싱 실패, 원래 점수 유지")
                else:
                    log.warning("[phase3] 개선본 html_code 없음, 원본 사용")

            # ── Save ──
            html_code = design.get("html_code", "")
            wrapped = wrap_html(html_code)
            screenshot = await capture_screenshot(browser, wrapped)
            slug = ensure_unique_slug(design.get("title", "Untitled Design"))
            image_url = upload_image(screenshot, slug)
            design_id = str(uuid.uuid4())

            record = {
                "id": design_id,
                "title": design.get("title", "Untitled Design"),
                "description": design.get("description", ""),
                "features": design.get("features", []),
                "usage": design.get("usage", ""),
                "image_url": image_url,
                "category": category,
                "code": html_code,
                "code_react": design.get("react_code", ""),
                "prompt": json.dumps({
                    "structure": structure,
                    "style": style,
                    "concept": design.get("concept", ""),
                    "quality_score": total,
                    "attempt": attempt,
                    "generator": "v4.0-pro-ollama",
                    "models": {
                        "designer": DESIGNER_MODEL,
                        "critic": CRITIC_MODEL,
                        "refiner": REFINER_MODEL,
                    },
                }, ensure_ascii=False),
                "colors": normalize_colors(design.get("colors", [])),
                "tags": infer_tags(category, structure, style, design.get("title", "")),
                "slug": slug,
                "status": "published",
                "sns_promoted": False,
                "pinterest_promoted": False,
                "created_at": datetime.utcnow().isoformat(),
            }

            get_supabase().table("designs").insert(record).execute()
            log.info("[saved] ✓ %s (slug=%s, score=%d, attempt=%d)", record["title"], slug, total, attempt)
            return True, design_id

        except Exception as e:
            log.error("[error] attempt %d/%d: %s", attempt, MAX_ATTEMPTS, e)
            await asyncio.sleep(3)

    return False, None


# ---------------------------------------------------------------------------
# Batch Runner
# ---------------------------------------------------------------------------

async def run_batch(count: int, use_requests: bool, requests_only: bool):
    successes = 0
    log.info("[start] %d개 생성 | Designer=%s | Critic=%s | Refiner=%s",
             count, DESIGNER_MODEL, CRITIC_MODEL, REFINER_MODEL)
    log.info("[start] Quality threshold: %d/100", QUALITY_THRESHOLD)

    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for i in range(count):
            log.info("\n━━━━━━━━━━ [%d/%d] ━━━━━━━━━━", i + 1, count)
            source_request: Optional[Dict[str, Any]] = None

            if use_requests:
                source_request = fetch_pending_request()
                if source_request:
                    try:
                        update_request_status(source_request["id"], "in_progress")
                        log.info("[request] %s", source_request.get("title", "?"))
                    except Exception as e:
                        log.warning("상태 업데이트 실패: %s", e)
                elif requests_only:
                    log.info("[done] pending 신청 없음")
                    break

            ok, design_id = await generate_design(browser, source_request=source_request)

            if ok:
                successes += 1
                if source_request and design_id:
                    try:
                        update_request_status(source_request["id"], "completed", design_id)
                    except Exception:
                        pass
            elif source_request:
                try:
                    update_request_status(source_request["id"], "pending")
                except Exception:
                    pass

        await browser.close()

    log.info("\n[result] %d/%d 생성 완료", successes, count)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="UI-Syntax Generator v4.0 Pro (Ollama Multi-Model)")
    parser.add_argument("--count", type=int, default=1, help="생성할 디자인 수")
    parser.add_argument("--category", type=str, default=None, help="카테고리 고정")
    parser.add_argument("--use-requests", action="store_true", help="신청 우선 처리")
    parser.add_argument("--requests-only", action="store_true", help="신청만 처리")
    parser.add_argument("--threshold", type=int, default=None, help="품질 임계값 (1-100)")
    parser.add_argument("--designer", type=str, default=None, help="Designer 모델 오버라이드")
    parser.add_argument("--critic", type=str, default=None, help="Critic 모델 오버라이드")
    parser.add_argument("--refiner", type=str, default=None, help="Refiner 모델 오버라이드")
    parser.add_argument("--dry-run", action="store_true", help="프롬프트 확인만 (생성 안함)")
    args = parser.parse_args()

    global QUALITY_THRESHOLD, DESIGNER_MODEL, CRITIC_MODEL, REFINER_MODEL
    if args.threshold is not None:
        QUALITY_THRESHOLD = args.threshold
    if args.designer:
        DESIGNER_MODEL = args.designer
    if args.critic:
        CRITIC_MODEL = args.critic
    if args.refiner:
        REFINER_MODEL = args.refiner

    if args.category:
        from difflib import get_close_matches
        match = get_close_matches(args.category, CATEGORIES, n=1, cutoff=0.3)
        if match:
            CATEGORIES.clear()
            CATEGORIES.append(match[0])
            log.info("[config] 카테고리: %s", match[0])

    if args.dry_run:
        cat = random.choice(CATEGORIES)
        struct = random.choice(STRUCTURES.get(cat, STRUCTURES["Landing Page"]))
        sty = random.choice(STYLES)
        print(f"\n{'='*60}")
        print(f"Category:  {cat}")
        print(f"Structure: {struct}")
        print(f"Style:     {sty}")
        print(f"Designer:  {DESIGNER_MODEL}")
        print(f"Critic:    {CRITIC_MODEL}")
        print(f"Refiner:   {REFINER_MODEL}")
        print(f"Threshold: {QUALITY_THRESHOLD}/100")
        print(f"{'='*60}")
        print("\n[Designer Prompt]")
        print(build_designer_prompt(cat, struct, sty))
        return

    asyncio.run(run_batch(
        args.count,
        use_requests=(args.use_requests or args.requests_only),
        requests_only=args.requests_only,
    ))


if __name__ == "__main__":
    main()
