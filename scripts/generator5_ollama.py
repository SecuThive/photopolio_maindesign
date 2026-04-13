#!/usr/bin/env python3
"""
UI-Syntax Design Generator — v5.1 (Ollama Local Multi-Pass + Score Loop Edition)

전략:
  Pass 1 : 디자인 브리프 — 카테고리/스타일/구조/컬러/타이포 결정
  Pass 2 : HTML 초안 생성
  [Loop, 최대 --max-refine 회]
    Pass N-review : 자가 리뷰 — 점수 + 개선점 목록 추출
    score >= --min-score 이면 종료
    Pass N-refine : 개선점 반영 HTML 재생성
  → 스크린샷 → Supabase 저장
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
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Browser
from supabase import Client, create_client

# ── 로깅 ──────────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
log = logging.getLogger(__name__)

# ── 환경 변수 ─────────────────────────────────────────────────────────────────
load_dotenv()

def _normalize_supabase_url(raw: str) -> str:
    """https:// 없으면 자동 추가, 후행 슬래시 제거"""
    url = raw.strip().rstrip("/")
    if url and not url.startswith("http"):
        url = "https://" + url
    return url

SUPABASE_URL    = _normalize_supabase_url(
    os.getenv("SUPABASE_URL") or os.getenv("NEXT_PUBLIC_SUPABASE_URL") or ""
)
SUPABASE_KEY    = (
    os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_KEY") or ""
).strip()
STORAGE_BUCKET  = os.getenv("SUPABASE_DESIGNS_BUCKET", "designs-bucket")
STORAGE_FOLDER  = os.getenv("SUPABASE_DESIGNS_FOLDER", "designs")

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL    = os.getenv("OLLAMA_MODEL", "gemma4:e4b")
OLLAMA_TIMEOUT  = int(os.getenv("OLLAMA_TIMEOUT", "300"))  # 초

# 품질 루프 기본값 (CLI 인자로 덮어쓸 수 있음)
DEFAULT_MIN_SCORE  = 0    # 0 = 루프 없이 기존 4-pass 동작
DEFAULT_MAX_REFINE = 3    # 최대 추가 개선 횟수

# ── 유효성 검사 ───────────────────────────────────────────────────────────────
_missing = []
if not SUPABASE_URL or ".supabase.co" not in SUPABASE_URL:
    _missing.append(f"SUPABASE_URL (현재값: '{SUPABASE_URL or '없음'}')")
if not SUPABASE_KEY:
    _missing.append("SUPABASE_SERVICE_ROLE_KEY")
if _missing:
    log.error("필수 환경변수 오류: %s", " | ".join(_missing))
    raise SystemExit(1)

log.info("[env] Supabase: %s", SUPABASE_URL)

# ── Supabase 클라이언트 ───────────────────────────────────────────────────────
_supabase_client: Optional[Client] = None

def get_supabase() -> Client:
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client

# ── 데이터 상수 ───────────────────────────────────────────────────────────────
CATEGORIES = ["Landing Page", "Dashboard", "E-commerce", "Portfolio", "Blog", "SaaS App"]

STYLE_STRUCTURE_AFFINITY: Dict[str, List[str]] = {
    # ── 모던 미니멀 ──────────────────────────────────────────────────────────
    "Apple-inspired Minimal White": [
        "Hero with Oversized Typography", "Split Screen with Large Visual", "Centered Minimal CTA",
    ],
    "Vercel-style Dark Developer":  [
        "Bento Grid with Code Snippets", "Command Palette Interface", "Gradient Hero with Terminal",
    ],
    "Stripe-inspired Fintech":      [
        "Three-tier Pricing with Toggle", "Feature Grid with Animated Icons", "Stats Dashboard with Graphs",
    ],
    # ── 다크 럭셔리 ──────────────────────────────────────────────────────────
    "Linear Dark Mode Elegance":    [
        "Sidebar App with Kanban", "Settings Panel with Toggles", "Activity Feed Dashboard",
    ],
    "Luxury Gold on Deep Black":    [
        "Full-bleed Hero with Gold Accents", "Product Showcase with Parallax Cards", "Testimonial with Large Quote",
    ],
    "Deep Space Dark with Nebula":  [
        "Hero with Particle Background", "Feature Cards with Glow Effect", "Bento Grid with Gradient Borders",
    ],
    # ── 글래스모피즘 / 그라디언트 ────────────────────────────────────────────
    "Glassmorphism with Vivid Blobs": [
        "Floating Glass Cards", "Dashboard with Frosted Sidebar", "Pricing with Glass Panels",
    ],
    "Aurora Gradient Mesh":         [
        "Hero with Animated Gradient Background", "Feature Sections with Gradient Cards", "Split Layout with Color Wash",
    ],
    "Vibrant Gradient Pop":         [
        "Bold Hero with Gradient Text", "Grid of Colorful Feature Tiles", "Testimonial Carousel with Gradient Borders",
    ],
    # ── 네오브루탈 / 레트로 ──────────────────────────────────────────────────
    "Neo-Brutalism Bold Shadows":   [
        "Hero with Hard-shadow Cards", "Product Grid with Thick Borders", "Pricing Table with Offset Shadows",
    ],
    "Retro 90s Memphis":            [
        "Colorful Grid with Geometric Shapes", "Hero with Pattern Background", "Product Cards with Retro Typography",
    ],
    "Cyberpunk Neon on Black":      [
        "Neon Glow Dashboard", "Radial Stats with Neon Rings", "Hero with Scanline Overlay",
    ],
    # ── 2025 트렌드 ──────────────────────────────────────────────────────────
    "Claymorphism Soft 3D":         [
        "Soft 3D Product Cards", "App UI with Puffy Elements", "Dashboard with Clay Icons",
    ],
    "Editorial Magazine Layout":    [
        "Large-type Editorial Hero", "Mixed Grid with Image Collage", "Article with Pull Quotes",
    ],
    "Monochrome Typographic":       [
        "All-text Bold Hero", "Data-heavy Table with Clean Lines", "Portfolio Grid Minimal",
    ],
}

def pick_style_structure() -> tuple[str, str]:
    style = random.choice(list(STYLE_STRUCTURE_AFFINITY.keys()))
    structure = random.choice(STYLE_STRUCTURE_AFFINITY[style])
    return style, structure

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def unique_slug(base: str) -> str:
    candidate = slugify(base)
    suffix = 2
    while True:
        resp = get_supabase().table("designs").select("id").eq("slug", candidate).limit(1).execute()
        if not resp.data:
            return candidate
        candidate = f"{slugify(base)}-{suffix}"
        suffix += 1

# ── Ollama API 호출 ───────────────────────────────────────────────────────────
async def ollama_chat(messages: List[Dict[str, str]], *, model: str = OLLAMA_MODEL) -> str:
    """Ollama /api/chat 호출 (스트리밍 없이 전체 응답 반환)"""
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": 0.9,   # 더 창의적인 결과 (0.8 → 0.9)
            "top_p": 0.95,
            "top_k": 50,
            "num_ctx": 20480,     # 컨텍스트 창 확장 (더 긴 HTML 처리)
        },
    }
    async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as client:
        resp = await client.post(url, json=payload)
        resp.raise_for_status()
        data = resp.json()
        return data["message"]["content"].strip()

def extract_json(text: str) -> Any:
    """응답 텍스트에서 JSON 블록 추출"""
    # ```json ... ``` 펜스 제거
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.IGNORECASE)
    cleaned = re.sub(r"\s*```$", "", cleaned)
    return json.loads(cleaned)

def extract_html(text: str) -> str:
    """응답 텍스트에서 HTML 블록만 추출"""
    # ```html ... ``` 블록 우선
    m = re.search(r"```html\s*([\s\S]+?)\s*```", text, re.IGNORECASE)
    if m:
        return m.group(1).strip()
    # 없으면 <!DOCTYPE 또는 <html 부터 끝까지
    m2 = re.search(r"(<!DOCTYPE[\s\S]+|<html[\s\S]+)", text, re.IGNORECASE)
    if m2:
        return m2.group(1).strip()
    return text.strip()

# ── Pass 1: 디자인 브리프 ─────────────────────────────────────────────────────
BRIEF_SYSTEM = """\
You are a world-class UI/UX designer at a top-tier design agency (think Apple, Stripe, Linear).
Your briefs inspire stunning, award-winning interfaces — not generic templates.
Always respond with a single valid JSON object — no markdown, no extra text."""

async def pass1_brief(category: str, style: str, structure: str) -> Dict[str, Any]:
    prompt = f"""\
Create a premium design brief for a {category} UI.
Style direction: {style}
Layout structure: {structure}

Push for something visually striking and memorable — not a boring template.
Think about what would win an Awwwards or Dribbble Popular award.

Return JSON with these exact keys:
{{
  "title": "evocative product/brand name (3-6 words, NOT generic)",
  "concept": "2 vivid sentences: the emotional feel + the visual hook that makes it unforgettable",
  "color_palette": ["#primary", "#secondary", "#accent", "#background", "#surface"],
  "typography": "specific Google Font pairing: heading font + body font, with weight and style notes",
  "visual_details": "2-3 specific visual flourishes: e.g. 'soft drop shadows on cards, CSS blur backdrop on nav, subtle grain texture overlay on hero'",
  "content_strategy": "specific realistic content — brand names, real numbers, real copy (absolutely no lorem ipsum or placeholder text)",
  "animation_hints": "1-2 CSS-only animation ideas: e.g. 'cards lift on hover with scale(1.03) + shadow', 'hero gradient shifts with @keyframes'"
}}"""

    log.info("[pass1] 브리프 생성 중...")
    text = await ollama_chat([
        {"role": "system", "content": BRIEF_SYSTEM},
        {"role": "user", "content": prompt},
    ])
    return extract_json(text)

# ── Pass 2: HTML 초안 ─────────────────────────────────────────────────────────
HTML_SYSTEM = """\
You are an elite frontend engineer who builds stunning, visually rich UIs.
Your output looks like it was designed by a top agency — not a generic template.

HARD RULES:
- Include <script src="https://cdn.tailwindcss.com"></script> in <head>
- Include Google Fonts <link> for the specified fonts
- Use REAL content only — zero lorem ipsum, zero "placeholder text", zero "Image here"
- Outermost wrapper must NOT use min-h-screen — size naturally to content
- Respond with ONLY the raw HTML — no explanation, no ```fences```

VISUAL QUALITY RULES (non-negotiable):
- Write a <style> block with custom CSS: @keyframes animations, custom gradients, special effects
- Use multi-layer box-shadows for depth: e.g. `box-shadow: 0 4px 6px rgba(0,0,0,.07), 0 20px 40px rgba(0,0,0,.12)`
- Cards and panels must have visible depth — borders, shadows, or background contrast
- Use CSS backdrop-filter: blur() for glassmorphism elements where appropriate
- Typography must have strong hierarchy: at least 3 distinct text sizes with weight contrast
- Hero sections need a visually rich background: gradient, mesh, pattern, or layered shapes via CSS
- All interactive elements need smooth transitions (transition-all duration-300) and hover states
- Add at least 2 decorative elements: gradient blobs, geometric shapes, background patterns, SVG decorations
- Color usage must be intentional: don't use plain white backgrounds unless the style demands it
- Spacing must be generous — padding and margins that give content room to breathe
- Inline SVG icons preferred over emoji for a professional look

FORBIDDEN (instant quality penalty):
- Plain white/gray backgrounds with no visual interest
- Flat cards with no shadow or border
- Generic button styles (rounded-md bg-blue-500 only)
- Missing hover states on interactive elements
- Walls of same-size text with no hierarchy"""

async def pass2_html_draft(brief: Dict[str, Any], category: str, style: str, structure: str) -> str:
    colors = " | ".join(brief.get("color_palette", []))
    prompt = f"""\
Build a visually stunning {category} UI.
Layout structure: {structure}
Visual style: {style}

Design Brief:
- Brand/Title: {brief.get("title")}
- Concept: {brief.get("concept")}
- Color palette: {colors}
- Typography: {brief.get("typography")}
- Visual details: {brief.get("visual_details", "rich shadows, depth, decorative elements")}
- Content: {brief.get("content_strategy")}
- Animations: {brief.get("animation_hints", "subtle hover lifts and smooth transitions")}

This should look like a real, polished product that could win Dribbble Popular.
Make it visually rich — not a generic template. Write the complete HTML now."""

    log.info("[pass2] HTML 초안 생성 중...")
    text = await ollama_chat([
        {"role": "system", "content": HTML_SYSTEM},
        {"role": "user", "content": prompt},
    ])
    return extract_html(text)

# ── Pass 3: 자가 리뷰 ─────────────────────────────────────────────────────────
REVIEW_SYSTEM = """\
You are a senior design critic at an award-winning agency (Awwwards judge level).
You score UI designs on visual quality, NOT just functionality.
A score of 80+ means it could win Dribbble Popular. Most first drafts score 40-60.
Respond with a single valid JSON object only — no markdown."""

async def pass3_review(html: str, category: str, style: str) -> Dict[str, Any]:
    prompt = f"""\
Critically review this {category} UI (target style: {style}) as an Awwwards judge.

HTML to review:
```html
{html[:7000]}
```

Score it STRICTLY on visual beauty and design quality. Be harsh — a score of 75+ means genuinely stunning.

Scoring criteria:
- Visual depth & layering (shadows, gradients, glassmorphism): 0-20 pts
- Typography hierarchy & font pairing quality: 0-20 pts
- Color harmony & intentional palette use: 0-20 pts
- Animation & micro-interactions (CSS): 0-15 pts
- Decorative richness (backgrounds, shapes, accents): 0-15 pts
- Content realism & spacing generosity: 0-10 pts

Return JSON:
{{
  "score": <integer 1-100>,
  "issues": [
    {{
      "area": "depth|typography|color|animation|decoration|spacing|content",
      "severity": "critical|major|minor",
      "fix": "very specific CSS/HTML fix with exact values — e.g. 'Add box-shadow: 0 20px 60px rgba(0,0,0,0.3) to .card elements'"
    }}
  ],
  "strengths": ["specific strength 1", "specific strength 2"]
}}

List up to 7 issues, prioritized by severity. Be specific — no vague advice."""

    log.info("[pass3] 자가 리뷰 중...")
    text = await ollama_chat([
        {"role": "system", "content": REVIEW_SYSTEM},
        {"role": "user", "content": prompt},
    ])
    try:
        return extract_json(text)
    except Exception:
        return {"score": 50, "issues": [], "strengths": []}

# ── Pass 4: 개선된 최종 HTML ──────────────────────────────────────────────────
async def pass4_refined_html(html: str, review: Dict[str, Any], brief: Dict[str, Any],
                              category: str, style: str) -> str:
    issues = review.get("issues", [])
    if not issues:
        log.info("[pass4] 개선 사항 없음 — 초안 사용")
        return html

    # critical/major 우선 정렬
    severity_order = {"critical": 0, "major": 1, "minor": 2}
    sorted_issues = sorted(issues, key=lambda i: severity_order.get(i.get("severity", "minor"), 2))
    fixes = "\n".join(
        f"- [{i['area'].upper()}] ({i.get('severity','minor')}) {i['fix']}"
        for i in sorted_issues
    )

    prompt = f"""\
You are refining a {category} UI to make it visually stunning (target style: {style}).
Apply ALL the following design improvements — be thorough and precise:

{fixes}

Current HTML:
```html
{html[:9000]}
```

Design reference:
- Brand: {brief.get("title")}
- Colors: {" | ".join(brief.get("color_palette", []))}
- Visual details: {brief.get("visual_details", "")}
- Animation hints: {brief.get("animation_hints", "")}

IMPORTANT:
- Apply every single fix listed above
- Maintain all existing content — only improve visuals
- Add CSS in a <style> block for anything Tailwind can't express
- The result must look significantly more polished than the input
- Return ONLY the complete improved HTML — no explanation"""

    log.info("[pass4] 개선된 HTML 생성 중... (%d개 수정사항)", len(issues))
    text = await ollama_chat([
        {"role": "system", "content": HTML_SYSTEM},
        {"role": "user", "content": prompt},
    ])
    return extract_html(text)

# ── 스크린샷 촬영 ─────────────────────────────────────────────────────────────
async def capture_screenshot(browser: Browser, html: str) -> bytes:
    page = await browser.new_page(viewport={"width": 1400, "height": 900})
    try:
        await page.set_content(html, wait_until="networkidle")
        # 폰트 로딩 대기
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(1500)
        # vh 단위를 px로 클린업
        await page.evaluate("""
            document.querySelectorAll('*').forEach(el => {
                const s = window.getComputedStyle(el);
                ['height', 'min-height', 'max-height'].forEach(prop => {
                    const v = s.getPropertyValue(prop);
                    if (v && v.includes('vh')) el.style[prop] = 'auto';
                });
            });
        """)
        screenshot = await page.screenshot(type="png", full_page=True)
        return screenshot
    finally:
        await page.close()

# ── Supabase Storage 업로드 ───────────────────────────────────────────────────
def upload_image(image_bytes: bytes, slug: str) -> str:
    filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{slug}.png"
    path = f"{STORAGE_FOLDER}/{filename}"
    sb = get_supabase()
    sb.storage.from_(STORAGE_BUCKET).upload(path, image_bytes, {"content-type": "image/png"})
    return sb.storage.from_(STORAGE_BUCKET).get_public_url(path)

# ── DB 저장 ───────────────────────────────────────────────────────────────────
def save_to_db(design_id: str, title: str, slug: str, category: str,
               description: str, html_code: str, image_url: str,
               colors: List[str], score: int, prompt_tag: str) -> None:
    record = {
        "id":          design_id,
        "title":       title,
        "description": description,
        "image_url":   image_url,
        "category":    category,
        "code":        html_code,
        "prompt":      prompt_tag,
        "colors":      colors,
        "slug":        slug,
        "status":      "published",
        "created_at":  datetime.utcnow().isoformat(),
    }
    # optional 컬럼 시도
    try:
        get_supabase().table("designs").insert({**record, "quality_score": score}).execute()
        log.info("[db] 저장 완료 (quality_score 포함)")
    except Exception as exc:
        log.warning("[db] quality_score 컬럼 없음, 기본 저장: %s", exc)
        try:
            get_supabase().table("designs").insert(record).execute()
            log.info("[db] 저장 완료 (기본 컬럼)")
        except Exception as exc2:
            log.error("[db] 저장 실패: %s", exc2)
            raise

# ── 디자인 데이터 타입 ──────────────────────────────────────────────────────────
DesignData = Dict[str, Any]   # 생성된 디자인 데이터 (미저장)

# ── 핵심 생성 루프 (저장 없이 데이터만 반환) ────────────────────────────────────
async def generate_one_design(
    browser: Browser,
    min_score: int = DEFAULT_MIN_SCORE,
    max_refine: int = DEFAULT_MAX_REFINE,
) -> tuple[bool, Optional[DesignData], int]:
    """
    디자인을 생성하고 데이터를 반환 — DB/Storage 저장은 하지 않음.
    저장 여부는 호출자(run_batch)가 score를 보고 결정.

    Returns (success, design_data, score)
    design_data keys: title, slug, category, description, html_code,
                      screenshot_bytes, colors, score, prompt_tag
    """
    category = random.choice(CATEGORIES)
    style, structure = pick_style_structure()
    design_id = str(uuid.uuid4())

    log.info("[start] %s | %s | %s", category, structure, style)
    log.info("[config] min_score=%d | max_refine=%d", min_score, max_refine)

    try:
        # Pass 1: 브리프
        brief = await pass1_brief(category, style, structure)
        title = brief.get("title", "Untitled Design")
        log.info("[brief] 제목: %s", title)

        # Pass 2: HTML 초안
        html_current = await pass2_html_draft(brief, category, style, structure)
        if not html_current.strip():
            log.error("[pass2] HTML 초안 비어있음")
            return False, None, 0

        # 품질 개선 루프
        score = 0
        total_passes = max_refine if min_score > 0 else 1

        for refine_idx in range(total_passes):
            round_label = f"[refine {refine_idx + 1}/{total_passes}]" if total_passes > 1 else "[review]"

            review = await pass3_review(html_current, category, style)
            score = review.get("score", 50)
            log.info("%s 점수: %d/100 | 이슈: %d개 | 강점: %s",
                     round_label, score,
                     len(review.get("issues", [])),
                     review.get("strengths", [])[:2])

            if min_score > 0 and score >= min_score:
                log.info("%s 목표 점수 달성 (%d >= %d) — 개선 루프 종료", round_label, score, min_score)
                break

            is_last = (refine_idx == total_passes - 1)
            if is_last or not review.get("issues"):
                if not review.get("issues"):
                    log.info("%s 이슈 없음 — 현재 HTML 사용", round_label)
                break

            refined = await pass4_refined_html(html_current, review, brief, category, style)
            if refined.strip():
                html_current = refined
            else:
                log.warning("%s 개선 HTML 비어있음 — 이전 버전 유지", round_label)

        html_final = html_current

        # 스크린샷 (저장 전 미리 찍어 둠)
        log.info("[screenshot] 캡처 중...")
        screenshot_bytes = await capture_screenshot(browser, html_final)

        design_data: DesignData = {
            "id":          design_id,
            "title":       title,
            "category":    category,
            "description": brief.get("concept", ""),
            "html_code":   html_final,
            "screenshot":  screenshot_bytes,
            "colors":      brief.get("color_palette", []),
            "score":       score,
            "prompt_tag":  f"{structure}_{style}".lower().replace(" ", "_"),
        }

        log.info("[생성완료] %s | score=%d", title, score)
        return True, design_data, score

    except Exception as exc:
        log.error("[error] 생성 실패: %s", exc, exc_info=True)
        return False, None, 0


def publish_design(data: DesignData) -> str:
    """Storage 업로드 + DB 저장. 저장된 slug 반환."""
    slug = unique_slug(data["title"])
    log.info("[upload] Storage 업로드 중... (slug=%s)", slug)
    image_url = upload_image(data["screenshot"], slug)

    save_to_db(
        design_id=data["id"],
        title=data["title"],
        slug=slug,
        category=data["category"],
        description=data["description"],
        html_code=data["html_code"],
        image_url=image_url,
        colors=data["colors"],
        score=data["score"],
        prompt_tag=data["prompt_tag"],
    )
    log.info("[✓] 게시 완료: %s | score=%d | https://ui-syntax.com/design/%s",
             data["title"], data["score"], slug)
    return slug

# ── 배치 실행 ─────────────────────────────────────────────────────────────────
async def run_batch(
    count: int,
    min_score: int = DEFAULT_MIN_SCORE,
    max_refine: int = DEFAULT_MAX_REFINE,
    target_score: int = 0,
    max_attempts: int = 10,
) -> None:
    """
    count        : 목표 저장 디자인 수
    min_score    : 단일 디자인 내 개선 반복 기준 점수
    max_refine   : 단일 디자인 내 최대 개선 횟수
    target_score : 이 점수 이상인 디자인만 저장 (0 = 비활성화)
                   미달 시 새 디자인을 처음부터 다시 생성
    max_attempts : target_score 달성을 위한 최대 시도 횟수 (무한루프 방지)
    """
    log.info(
        "[system] Ollama(%s) | 목표 %d개 | min_score=%d | max_refine=%d | target_score=%d | max_attempts=%d",
        OLLAMA_MODEL, count, min_score, max_refine, target_score, max_attempts,
    )

    # Ollama 연결 확인
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            models = [m["name"] for m in r.json().get("models", [])]
            log.info("[ollama] 사용 가능한 모델: %s", models)
            if OLLAMA_MODEL not in models:
                log.warning("[ollama] %s 모델이 목록에 없습니다. 그래도 시도합니다.", OLLAMA_MODEL)
    except Exception as exc:
        log.error("[ollama] 연결 실패: %s — Ollama가 실행 중인지 확인하세요", exc)
        return

    successes = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for i in range(count):
            log.info("\n═══ 디자인 %d/%d 목표 ═══", i + 1, count)

            if target_score > 0:
                # ── target_score 달성할 때까지 새 디자인 반복 생성 ──────────
                # 90점 미달 디자인은 저장하지 않고 폐기
                attempt = 0
                best_score = 0
                while attempt < max_attempts:
                    attempt += 1
                    log.info("  [시도 %d/%d] 새 디자인 생성 중... (목표: score >= %d)",
                             attempt, max_attempts, target_score)
                    ok, design_data, score = await generate_one_design(
                        browser, min_score=min_score, max_refine=max_refine,
                    )
                    if score > best_score:
                        best_score = score

                    if ok and score >= target_score:
                        log.info("  [✓] 목표 달성! score=%d >= %d (시도 %d회) — 저장 중...",
                                 score, target_score, attempt)
                        slug = await asyncio.to_thread(publish_design, design_data)
                        log.info("  [✓] 게시 완료: https://ui-syntax.com/design/%s", slug)
                        successes += 1
                        break
                    elif ok:
                        log.info("  [✗] score=%d < %d — 저장 안 함, 폐기 후 재시도 (최고: %d)",
                                 score, target_score, best_score)
                    else:
                        log.warning("  [✗] 생성 실패 — 재시도")

                    if attempt < max_attempts:
                        await asyncio.sleep(2)
                else:
                    log.warning(
                        "  [포기] %d회 시도했지만 목표(%d점) 미달. 최고 점수: %d — 저장 안 함",
                        max_attempts, target_score, best_score,
                    )
            else:
                # ── 기존 단순 생성 (target_score 없으면 무조건 저장) ──────────
                ok, design_data, score = await generate_one_design(
                    browser, min_score=min_score, max_refine=max_refine,
                )
                if ok and design_data:
                    slug = await asyncio.to_thread(publish_design, design_data)
                    successes += 1
                    log.info("[작업 완료] 최종 점수: %d | slug=%s", score, slug)

            if i < count - 1:
                await asyncio.sleep(3)

        await browser.close()

    log.info("\n[결과] %d / %d 성공", successes, count)

# ── CLI ────────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI-Syntax Design Generator v5.1 (Ollama)")
    parser.add_argument("--count",      type=int, default=1,              help="생성할 디자인 수")
    parser.add_argument("--model",      type=str, default=OLLAMA_MODEL,   help="Ollama 모델 이름")
    parser.add_argument("--ollama",     type=str, default=OLLAMA_BASE_URL, help="Ollama 서버 URL")
    parser.add_argument("--min-score",    type=int, default=DEFAULT_MIN_SCORE,
                        help="단일 디자인 내 개선 반복 기준 점수 (0=비활성화, 권장: 75-85)")
    parser.add_argument("--max-refine",   type=int, default=DEFAULT_MAX_REFINE,
                        help="단일 디자인 내 최대 개선 반복 횟수 (기본: 3)")
    parser.add_argument("--target-score", type=int, default=0,
                        help="이 점수 미만이면 새 디자인을 처음부터 재생성 (0=비활성화, 권장: 85-90)")
    parser.add_argument("--max-attempts", type=int, default=10,
                        help="target-score 달성을 위한 최대 시도 횟수 (기본: 10)")
    args = parser.parse_args()

    OLLAMA_MODEL    = args.model
    OLLAMA_BASE_URL = args.ollama

    asyncio.run(run_batch(
        args.count,
        min_score=args.min_score,
        max_refine=args.max_refine,
        target_score=args.target_score,
        max_attempts=args.max_attempts,
    ))
