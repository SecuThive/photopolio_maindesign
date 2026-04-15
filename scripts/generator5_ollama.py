#!/usr/bin/env python3
"""
UI-Syntax Design Generator — v6.0 (6-Pass Structured Workflow)

전략:
  Pass 0 : CSS 디자인 시스템 — 토큰/변수 먼저 확정 (일관성 보장)
  Pass 1 : 섹션별 구조 브리프 — 각 섹션의 내용·레이아웃·컴포넌트 명세
  Pass 2 : HTML 생성 — Pass0 CSS + Pass1 브리프 기반, 섹션 순서 보장
  [Loop, 최대 --max-refine 회]
    Pass 3 : 심층 리뷰 — 5개 기준 각각 세부 점수화, critical 이슈 우선
    score >= --min-score 이면 종료
    Pass 4 : 집중 수정 — critical 이슈 2개만 타깃, 전체 재생성 최소화
  Pass 5 : 최종 검증 — 빠른 스코어 확인 (optional, target_score 근접 시)
  → 스크린샷 → Supabase 저장

모델 권장: qwen2.5-coder:32b (HTML/CSS 생성 최상, Tailwind 정확도 높음)
          devstral:24b (코딩 에이전트 특화, 구조적 출력 강함)
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
from typing import Any, Dict, List, Optional

import httpx
from dotenv import load_dotenv
from playwright.async_api import async_playwright, Browser
from supabase import Client, create_client

from trend_researcher import get_trends, format_trend_prompt_block

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
OLLAMA_TIMEOUT  = int(os.getenv("OLLAMA_TIMEOUT", "600"))

# ── Pass별 전문 모델 설정 ─────────────────────────────────────────────────────
# 각 Pass는 역할이 다르므로 최적 모델을 분리 적용
#
#   CODER  모델: HTML/CSS/JS 코딩 특화  → qwen2.5-coder:7b  (Pass 0, 2, 4)
#   BRIEF  모델: 창의적 기획/디자인 감각 → gemma4:e4b        (Pass 1)
#   REVIEW 모델: 추론/분석 특화          → deepseek-r1:14b   (Pass 3)
#
# 환경변수로 개별 오버라이드 가능:
#   OLLAMA_MODEL_CODER=qwen2.5-coder:7b
#   OLLAMA_MODEL_BRIEF=gemma4:e4b
#   OLLAMA_MODEL_REVIEW=deepseek-r1:14b
#   OLLAMA_MODEL=<fallback for all>  (설정 안 하면 각 기본값 사용)
_FALLBACK_MODEL = os.getenv("OLLAMA_MODEL", "")

MODEL_CODER  = os.getenv("OLLAMA_MODEL_CODER",  _FALLBACK_MODEL or "qwen2.5-coder:7b")
MODEL_BRIEF  = os.getenv("OLLAMA_MODEL_BRIEF",  _FALLBACK_MODEL or "gemma4:e4b")
MODEL_REVIEW = os.getenv("OLLAMA_MODEL_REVIEW", _FALLBACK_MODEL or "deepseek-r1:14b")

# 품질 루프 기본값 (CLI 인자로 덮어쓸 수 있음)
DEFAULT_MIN_SCORE  = 75   # 75점 이상 도달할 때까지 개선 루프 반복
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
log.info("[model] CODER  (pass0/2/4): %s", MODEL_CODER)
log.info("[model] BRIEF  (pass1):     %s", MODEL_BRIEF)
log.info("[model] REVIEW (pass3):     %s", MODEL_REVIEW)

# ── Supabase 클라이언트 ───────────────────────────────────────────────────────
_supabase_client: Optional[Client] = None

def get_supabase() -> Client:
    global _supabase_client
    if _supabase_client is None:
        _supabase_client = create_client(SUPABASE_URL, SUPABASE_KEY)
    return _supabase_client

# ── 데이터 상수 ───────────────────────────────────────────────────────────────
CATEGORIES = [
    "Landing Page", "Dashboard", "E-commerce", "Portfolio",
    "Blog", "SaaS App", "Mobile App UI", "Agency Site",
    "Event / Conference Page", "Developer Tool", "Waitlist / Launch Page",
]

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
    # ── 추가 스타일 ──────────────────────────────────────────────────────────
    "Swiss International Style":    [
        "Strict Grid with Heavy Typography", "Off-centered Asymmetric Layout", "Photo + Text Overlap Grid",
    ],
    "Japanese Minimalism (Ma)":     [
        "Ultra-sparse Hero with Single Element", "White Space Dominant Product Page", "Text-only Navigation with Generous Padding",
    ],
    "Organic Earthy Natural":       [
        "Warm Texture Background with Hand-drawn Elements", "Rounded Bio Cards with Nature Imagery", "Full-bleed Plant Photography Hero",
    ],
    "Y2K / Retro Internet":         [
        "Bevel-bordered Windows UI", "Animated GIF-style Ticker + Blinking Elements", "Pixel-art Accent with Grunge Texture",
    ],
    "Neumorphism Soft UI":          [
        "Soft Inset Card Controls", "Toggle + Slider Panel", "Music Player with Pressed Buttons",
    ],
}

# ── 색상 무드 (강제 지정 — 모델이 임의로 바꾸지 못하게) ─────────────────────
COLOR_MOODS = [
    "Warm Earth: bg=#FAF3E8, primary=#C4622D, secondary=#6B4F3A, accent=#E8A87C, text=#2C1810",
    "Cool Nordic: bg=#F0F4F8, primary=#2B4C7E, secondary=#4A6FA5, accent=#88B4E7, text=#1A2744",
    "Vibrant Coral+Teal: bg=#FFF9F0, primary=#FF6B6B, secondary=#4ECDC4, accent=#FFE66D, text=#2D3436",
    "Muted Sage Pastel: bg=#F7F3EE, primary=#87A878, secondary=#C9B8D8, accent=#F7C5CC, text=#3D3D3D",
    "Bold Primary Flat: bg=#FFFFFF, primary=#E63946, secondary=#0077FF, accent=#FFD60A, text=#0D0D0D",
    "Charcoal Monochrome: bg=#1C1C1E, primary=#AEAEB2, secondary=#636366, accent=#F2F2F7, text=#FFFFFF",
    "Dark Jewel Emerald: bg=#0A1628, primary=#0D4F3C, secondary=#C9A84C, accent=#52B788, text=#E8F5E9",
    "High Contrast Neon: bg=#000000, primary=#00FF94, secondary=#FF0090, accent=#FFFF00, text=#FFFFFF",
    "Sunset Warm: bg=#FFF1E6, primary=#FF6B35, secondary=#DA4167, accent=#F7C59F, text=#1A0A00",
    "Deep Ocean: bg=#03045E, primary=#0077B6, secondary=#00B4D8, accent=#90E0EF, text=#CAF0F8",
    "Midnight Purple: bg=#1A0533, primary=#9D4EDD, secondary=#C77DFF, accent=#E0AAFF, text=#F8F0FF",
    "Forest Organic: bg=#1B4332, primary=#52B788, secondary=#2D6A4F, accent=#B7E4C7, text=#D8F3DC",
    "Warm Cream Gold: bg=#FAF7F0, primary=#C4A265, secondary=#8B4513, accent=#E8D5A3, text=#2C1810",
    "Electric Indigo: bg=#0D0221, primary=#4361EE, secondary=#7209B7, accent=#F72585, text=#E2EAFC",
    "Soft Lavender Studio: bg=#F5F0FF, primary=#7C3AED, secondary=#A78BFA, accent=#FCD34D, text=#1E1B4B",
    "Neo-Mint: bg=#F0FFF4, primary=#10B981, secondary=#064E3B, accent=#FCD34D, text=#022C22",
    "Rust Industrial: bg=#1A1A2E, primary=#E94560, secondary=#F5A623, accent=#C0C0C0, text=#EAEAEA",
    "Paper White Editorial: bg=#FDFCF8, primary=#1A1A1A, secondary=#888888, accent=#D4AF37, text=#111111",
]

# ── 레이아웃 아키타입 (구조적으로 강제 다양화) ───────────────────────────────
LAYOUT_ARCHETYPES = [
    "Asymmetric Split: huge text LEFT (60%) + visual RIGHT (40%), no centering",
    "Editorial Overlap: text and image elements physically overlap across columns",
    "Bento Box Mosaic: grid of 6+ cards with wildly different sizes (1×1, 2×1, 1×2, 3×1)",
    "Terminal / CLI: monospace font, dark bg, simulated command-line prompt aesthetic",
    "Sticky Sidebar App: fixed left panel (240px) + scrollable right content area",
    "Magazine F-Pattern: left-dominant large image, right-column text, horizontal rule dividers",
    "Swiss Grid: strict 12-col alignment, lots of whitespace, numbers + labels as design elements",
    "Brutalist Raw: thick black borders (3-4px), hard offset box-shadows, system fonts, NO rounded corners",
    "Floating Layers: cards at 3 depth levels using z-index + shadow, background shapes peek through",
    "Full-bleed Sections: each content block spans full width with alternating bg colors",
    "Radial / Circular: circular stats, ring progress bars, radial menus as primary design motif",
    "Card Waterfall: Pinterest-style masonry irregular height cards",
    "Single-focus Minimal: ONE big element centered, rest is whitespace — zen approach",
    "Split Horizontal Scroll: left panel fixed, right panel scrolls independently",
    "Timeline Vertical: chronological flow with connector lines, dates on alternating sides",
]

# ── 애니메이션 아키타입 ───────────────────────────────────────────────────────
ANIMATION_ARCHETYPES = [
    "stagger-reveal: items fade+translateY(20px) in sequence with 0.1s delay each",
    "parallax-drift: background moves at 0.5x scroll speed (transform: translateY calc)",
    "hover-lift: translateY(-6px) + box-shadow expand over 0.25s ease on cards",
    "typewriter: headline characters appear one by one via clip-path or width animation",
    "count-up: numeric stats animate from 0 to final value using CSS counter or JS",
    "blob-morph: background SVG blob shapes animate border-radius with @keyframes",
    "shimmer-sweep: diagonal light sweep across cards (background-position animation)",
    "neon-pulse: glow box-shadow breathes in/out with @keyframes (0%↔100% opacity)",
    "rotation-slow: decorative element slowly rotates 360° over 20s infinitely",
    "scale-bounce: elements spring to scale(1) from scale(0.8) with cubic-bezier(0.34,1.56,0.64,1)",
    "line-draw: SVG stroke-dashoffset animates to draw borders/underlines",
    "color-shift: gradient background hue rotates with @keyframes hue-rotate",
]

# ── 생성 히스토리 (반복 방지) ────────────────────────────────────────────────
HISTORY_FILE = Path(__file__).parent / ".generator_history.json"
HISTORY_KEEP = 20

def _load_history() -> List[Dict]:
    try:
        return json.loads(HISTORY_FILE.read_text(encoding="utf-8"))
    except Exception:
        return []

def _save_history(entry: Dict) -> None:
    history = _load_history()
    history.insert(0, entry)
    try:
        HISTORY_FILE.write_text(
            json.dumps(history[:HISTORY_KEEP], indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass  # 히스토리 저장 실패는 치명적 오류 아님


# ── 자기학습 메모리 ──────────────────────────────────────────────────────────
LESSONS_FILE = Path(__file__).parent / ".generator_lessons.json"
LESSONS_TOP_N = 6   # 프롬프트에 주입할 최상위 교훈 수
LESSONS_MAX   = 200 # 저장할 최대 이슈 키 수 (오래된 것 자동 정리)

def _load_lessons() -> Dict:
    try:
        return json.loads(LESSONS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return {
            "stats":       {"attempts": 0, "failures": 0, "successes": 0},
            "fixes":       {},   # key → {area, severity, fix, count, last_seen}
            "style_stats": {},   # style → {attempts, total_score, avg_score}
        }

def _save_lessons(lessons: Dict) -> None:
    try:
        LESSONS_FILE.write_text(
            json.dumps(lessons, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
    except Exception:
        pass

def _record_result(
    issues: List[Dict],
    score:  int,
    dna:    Dict,
    success: bool,
) -> None:
    """생성 결과에서 교훈을 학습하여 저장"""
    lessons = _load_lessons()

    # 통계 업데이트
    s = lessons.setdefault("stats", {"attempts": 0, "failures": 0, "successes": 0})
    s["attempts"]  = s.get("attempts",  0) + 1
    s["successes"] = s.get("successes", 0) + (1 if success else 0)
    s["failures"]  = s.get("failures",  0) + (0 if success else 1)

    # 실패 이슈 누적 학습
    if not success and issues:
        fixes = lessons.setdefault("fixes", {})
        for issue in issues:
            area     = issue.get("area", "general")
            fix_text = issue.get("fix", "").strip()
            severity = issue.get("severity", "minor")
            if not fix_text:
                continue
            key = f"{area}:{fix_text[:60]}"
            if key not in fixes:
                fixes[key] = {
                    "area":      area,
                    "severity":  severity,
                    "fix":       fix_text,
                    "count":     0,
                    "last_seen": "",
                }
            fixes[key]["count"]    += 1
            fixes[key]["last_seen"] = datetime.utcnow().isoformat()
            # 심각도 업그레이드 (minor → major → critical)
            sev_rank = {"critical": 2, "major": 1, "minor": 0}
            if sev_rank.get(severity, 0) > sev_rank.get(fixes[key]["severity"], 0):
                fixes[key]["severity"] = severity

        # 오래된 항목 정리 (count 낮은 것부터 제거)
        if len(fixes) > LESSONS_MAX:
            sorted_keys = sorted(fixes, key=lambda k: fixes[k]["count"])
            for k in sorted_keys[:len(fixes) - LESSONS_MAX]:
                del fixes[k]

    # 스타일별 성능 통계
    style = dna.get("style", "")
    if style:
        ss = lessons.setdefault("style_stats", {})
        if style not in ss:
            ss[style] = {"attempts": 0, "total_score": 0, "avg_score": 0}
        ss[style]["attempts"]   += 1
        ss[style]["total_score"] = ss[style].get("total_score", 0) + score
        ss[style]["avg_score"]   = ss[style]["total_score"] // ss[style]["attempts"]

    _save_lessons(lessons)
    log.info(
        "[학습] %s | score=%d | 누적 이슈=%d개 | 성공률=%.0f%%",
        "성공" if success else "실패",
        score,
        len(lessons.get("fixes", {})),
        (lessons["stats"]["successes"] / max(lessons["stats"]["attempts"], 1)) * 100,
    )

def _get_top_lessons(n: int = LESSONS_TOP_N) -> str:
    """가장 빈출·고심각도 이슈를 학습 교훈 텍스트로 반환"""
    fixes = _load_lessons().get("fixes", {})
    if not fixes:
        return ""
    sev_weight = {"critical": 3, "major": 2, "minor": 1}
    sorted_fixes = sorted(
        fixes.values(),
        key=lambda x: (sev_weight.get(x.get("severity", "minor"), 1) * 1000 + x.get("count", 0)),
        reverse=True,
    )
    lines = [
        f"- [{f['area'].upper()}]({f['severity']}) {f['fix']}  (과거 {f['count']}회 발생)"
        for f in sorted_fixes[:n]
    ]
    return "\n".join(lines)


# ── HTML 구조 검증 (Pass 2/4 후 자동 실행) ────────────────────────────────────

def validate_html(html: str) -> tuple[bool, List[str]]:
    """
    생성된 HTML의 구조적 무결성을 검증.
    Returns (is_valid, issues_list)
    """
    issues: List[str] = []
    html_lower = html.lower()

    # 1. Tailwind CDN 포함 여부
    if "cdn.tailwindcss.com" not in html:
        issues.append("MISSING_TAILWIND: <script src='https://cdn.tailwindcss.com'> not found")

    # 2. 기본 HTML 구조
    if "<html" not in html_lower:
        issues.append("MISSING_HTML_TAG: no <html> tag found")
    if "<head" not in html_lower:
        issues.append("MISSING_HEAD_TAG: no <head> tag found")
    if "<body" not in html_lower:
        issues.append("MISSING_BODY_TAG: no <body> tag found")

    # 3. 최소 콘텐츠 길이 (너무 짧으면 불완전)
    if len(html) < 2000:
        issues.append(f"TOO_SHORT: HTML is only {len(html)} chars (minimum 2000 expected)")

    # 4. 섹션 수 확인 (최소 3개 섹션)
    section_count = len(re.findall(r"<(?:section|main|article|footer|header|nav)\b", html, re.IGNORECASE))
    if section_count < 3:
        issues.append(f"FEW_SECTIONS: only {section_count} semantic sections found (minimum 3)")

    # 5. 프리뷰 깨뜨리는 패턴 감지
    broken_patterns = [
        (r"min-h-screen", "FIXED_HEIGHT: min-h-screen found (breaks preview)"),
        (r"h-screen", "FIXED_HEIGHT: h-screen found (breaks preview)"),
        (r"height:\s*100vh", "FIXED_HEIGHT: height:100vh found (breaks preview)"),
        (r"min-height:\s*100vh", "FIXED_HEIGHT: min-height:100vh found (breaks preview)"),
        (r"position:\s*fixed", "FIXED_POSITION: position:fixed found (breaks iframe preview)"),
    ]
    for pattern, msg in broken_patterns:
        if re.search(pattern, html, re.IGNORECASE):
            issues.append(msg)

    # 6. 닫히지 않은 태그 검사 (심각한 깨짐 원인)
    open_tags = len(re.findall(r"<(?:div|section|main|article)\b", html, re.IGNORECASE))
    close_tags = len(re.findall(r"</(?:div|section|main|article)>", html, re.IGNORECASE))
    if open_tags > 0 and abs(open_tags - close_tags) > 3:
        issues.append(f"UNCLOSED_TAGS: {open_tags} opening vs {close_tags} closing tags (diff > 3)")

    # 7. Google Fonts 링크 확인
    if "fonts.googleapis.com" not in html and "fonts.gstatic.com" not in html:
        issues.append("MISSING_FONTS: no Google Fonts link found")

    is_valid = len(issues) == 0
    return is_valid, issues


def fix_html_structure(html: str) -> str:
    """
    프리뷰 깨짐을 유발하는 CSS 패턴을 자동 수정.
    LLM 재호출 없이 코드 레벨에서 즉시 처리.
    """
    # min-h-screen, h-screen → 자연 높이
    html = re.sub(r'\bmin-h-screen\b', '', html)
    html = re.sub(r'\bh-screen\b', '', html)
    # 인라인 100vh 제거
    html = re.sub(r'min-height:\s*100vh\s*;?', '', html)
    html = re.sub(r'height:\s*100vh\s*;?', '', html)
    # position: fixed → sticky (네비바 등)
    html = re.sub(r'position:\s*fixed\s*;', 'position: sticky;', html)
    # Tailwind CDN 보장
    if "cdn.tailwindcss.com" not in html:
        html = html.replace("<head>", '<head>\n<script src="https://cdn.tailwindcss.com"></script>', 1)
        if "<head>" not in html.lower():
            html = f'<script src="https://cdn.tailwindcss.com"></script>\n{html}'
    return html


def pick_design_dna() -> Dict[str, str]:
    """모든 다양성 차원을 조합해 고유한 디자인 DNA 생성 (히스토리 반복 방지)"""
    history = _load_history()
    recent_styles    = {h.get("style", "")          for h in history[:6]}
    recent_categories= {h.get("category", "")       for h in history[:4]}
    recent_colors    = {h.get("color_key", "")      for h in history[:8]}
    recent_layouts   = {h.get("layout_key", "")     for h in history[:5]}

    # 스타일 선택 — 최근 6개 제외
    style_pool = [s for s in STYLE_STRUCTURE_AFFINITY if s not in recent_styles]
    if not style_pool:
        style_pool = list(STYLE_STRUCTURE_AFFINITY.keys())
    style     = random.choice(style_pool)
    structure = random.choice(STYLE_STRUCTURE_AFFINITY[style])

    # 카테고리 선택 — 최근 4개 제외
    cat_pool  = [c for c in CATEGORIES if c not in recent_categories]
    if not cat_pool:
        cat_pool = CATEGORIES
    category  = random.choice(cat_pool)

    # 색상 무드 선택 — 최근 8개 제외
    color_pool = [c for c in COLOR_MOODS if c not in recent_colors]
    if not color_pool:
        color_pool = COLOR_MOODS
    color_mood = random.choice(color_pool)

    # 레이아웃 아키타입 — 최근 5개 제외
    layout_pool = [l for l in LAYOUT_ARCHETYPES if l not in recent_layouts]
    if not layout_pool:
        layout_pool = LAYOUT_ARCHETYPES
    layout_arch = random.choice(layout_pool)

    animation = random.choice(ANIMATION_ARCHETYPES)

    return {
        "category":      category,
        "style":         style,
        "structure":     structure,
        "color_mood":    color_mood,
        "color_key":     color_mood,
        "layout_arch":   layout_arch,
        "layout_key":    layout_arch,
        "animation":     animation,
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
async def ollama_chat(
    messages: List[Dict[str, str]],
    *,
    model: str,
    temperature: float = 0.85,
    num_ctx: int = 32768,
) -> str:
    """Ollama /api/chat 호출 (스트리밍 없이 전체 응답 반환)

    model 은 반드시 명시적으로 전달 — Pass별 전문 모델을 쓰기 위해 기본값 없음.
      Pass 0, 2, 4 → MODEL_CODER  (qwen2.5-coder:32b  — HTML/CSS 코딩 최강)
      Pass 1       → MODEL_BRIEF  (gemma4:e4b          — 창의적 기획/디자인 감각)
      Pass 3       → MODEL_REVIEW (deepseek-r1:14b     — 추론/채점 특화)

    temperature 가이드:
      - CSS 시스템/브리프 (창의적): 0.7~0.9
      - HTML 생성 (구조 중요):      0.75~0.8
      - 리뷰/검증 (정확성 중요):    0.2~0.3
      - 수정 (지시 준수):           0.6~0.7
    """
    url = f"{OLLAMA_BASE_URL}/api/chat"
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "temperature": temperature,
            "top_p": 0.95,
            "top_k": 40,
            "num_ctx": num_ctx,        # 32k 컨텍스트 (긴 HTML 전체 처리)
            "repeat_penalty": 1.1,     # 반복 억제
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

# ── Pass 0: CSS 디자인 시스템 ────────────────────────────────────────────────
CSS_SYSTEM_PROMPT = """\
You are a senior design systems engineer. Your job is to create a complete CSS design token system.
Output ONLY a raw <style> block — no explanation, no markdown fences, no HTML wrapper.
The style block must start with <style> and end with </style>."""

async def pass0_css_system(dna: Dict[str, str]) -> str:
    """
    디자인 DNA를 받아 일관된 CSS 변수 시스템을 생성.
    이후 모든 패스가 이 시스템을 참조해 색상·타이포·그림자 일관성을 유지.
    """
    color_mood  = dna.get("color_mood", "")
    style       = dna.get("style", "")
    animation   = dna.get("animation", "")

    prompt = f"""\
Create a complete CSS design token system for a "{style}" UI design.

Color palette source (extract hex values from this):
{color_mood}

Output a single <style> block containing:

1. :root {{ }} with ALL these CSS variables:
   /* Core colors */
   --color-bg:          /* main page background */
   --color-bg-alt:      /* alternating section bg (MUST differ from --color-bg) */
   --color-bg-card:     /* card/panel background */
   --color-bg-nav:      /* navbar background */
   --color-border:      /* default border color */
   --color-border-strong: /* emphasized border */

   /* Text */
   --color-text:        /* primary body text */
   --color-text-muted:  /* secondary/helper text */
   --color-text-heading:/* headline color */

   /* Brand */
   --color-primary:     /* primary action/CTA color */
   --color-primary-hover: /* CTA hover state (lighten or darken 10%) */
   --color-secondary:   /* secondary accent */
   --color-accent:      /* highlight/decorative accent */

   /* Semantic */
   --color-success:     #22c55e;
   --color-warning:     #f59e0b;

   /* Typography */
   --font-heading: /* Google Font name, fallback */
   --font-body:    /* Google Font name, fallback */
   --font-mono:    /* monospace stack */

   /* Scale */
   --text-xs:   0.75rem;
   --text-sm:   0.875rem;
   --text-base: 1rem;
   --text-lg:   1.125rem;
   --text-xl:   1.25rem;
   --text-2xl:  1.5rem;
   --text-3xl:  1.875rem;
   --text-4xl:  2.25rem;
   --text-5xl:  3rem;
   --text-6xl:  3.75rem;

   /* Spacing */
   --space-section: 5rem;
   --space-gap:     1.5rem;

   /* Radius */
   --radius-sm:  4px;
   --radius-md:  8px;
   --radius-lg:  16px;
   --radius-xl:  24px;
   --radius-full: 9999px;

   /* Shadows */
   --shadow-sm:  /* subtle shadow matching the color scheme */
   --shadow-md:  /* medium shadow */
   --shadow-lg:  /* strong shadow for floating elements */
   --shadow-glow: /* colored glow using --color-primary at low opacity */

2. Base styles:
   *, *::before, *::after {{ box-sizing: border-box; }}
   html, body {{ margin: 0; padding: 0; background: var(--color-bg); color: var(--color-text); font-family: var(--font-body); }}

3. @keyframes for "{animation}":
   Name it appropriately (e.g., @keyframes stagger-reveal, @keyframes neon-pulse).
   Write the complete keyframe — not a placeholder.

4. Utility classes using these variables:
   .btn-primary    {{ background: var(--color-primary); color: #fff or contrast color; ... }}
   .btn-secondary  {{ border: 1px solid var(--color-primary); color: var(--color-primary); ... }}
   .card           {{ background: var(--color-bg-card); border: 1px solid var(--color-border); border-radius: var(--radius-lg); }}
   .badge          {{ ... }}
   .section-alt    {{ background: var(--color-bg-alt); }}
   .text-gradient  {{ background: linear-gradient(...); -webkit-background-clip: text; ... }}

All hex values MUST come from the color palette above. Do NOT use default browser colors.
Output the <style> block only — nothing else."""

    log.info("[pass0] CSS 디자인 시스템 생성 중... model=%s style=%s", MODEL_CODER, style[:40])
    return await ollama_chat(
        [
            {"role": "system", "content": CSS_SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        model=MODEL_CODER,
        temperature=0.7,   # 변수 생성은 일관성 중요 → 낮은 temperature
        num_ctx=16384,
    )


# ── Pass 1: 디자인 브리프 ─────────────────────────────────────────────────────
BRIEF_SYSTEM = """\
You are a world-class UI/UX designer at a top-tier design agency (think Apple, Stripe, Linear).
Your briefs inspire stunning, award-winning interfaces — not generic templates.
Always respond with a single valid JSON object — no markdown, no extra text."""

async def pass1_brief(category: str, style: str, structure: str,
                      dna: Optional[Dict[str, str]] = None,
                      trend_context: str = "") -> Dict[str, Any]:
    color_mood   = dna.get("color_mood", "")   if dna else ""
    layout_arch  = dna.get("layout_arch", "")  if dna else ""
    animation    = dna.get("animation", "")    if dna else ""

    prompt = f"""\
Create a design brief for a {category} UI.

MANDATORY CONSTRAINTS — you MUST follow these exactly, no exceptions:
1. Visual style: {style}
2. Layout structure: {structure}
3. Layout archetype (STRICT): {layout_arch or "your choice"}
   → Do NOT default to a standard hero + feature-cards grid. Follow the archetype above.
4. Color mood (STRICT — use ONLY these hex values as your palette base):
   {color_mood or "your choice — pick something unexpected, NOT blue/purple gradient"}
   → The colors MUST visually match this mood. Do not substitute with blue/purple/gray defaults.
5. Primary animation: {animation or "your choice"}

DIVERSITY MANDATE: This design must be structurally and visually DIFFERENT from a typical SaaS landing page.
Push the layout to extremes — if the archetype says asymmetric, make it dramatically asymmetric.
If it says brutalist, make it genuinely rough and raw. Commit to the direction fully.
{trend_context if trend_context else ""}
━━ YOUR TASK ━━
Return JSON with these exact keys:
{{
  "title": "evocative product/brand name (3-6 words, NOT generic like 'Nexus Flow' or 'Spark Pro')",
  "concept": "2 vivid sentences: emotional feel + the ONE visual choice that makes this unforgettable",
  "color_palette": ["#hex1", "#hex2", "#hex3", "#hex4", "#hex5"],
  "color_roles": {{
    "body_bg": "#hex — page/body background",
    "nav_bg": "#hex — navbar/header background (can differ from body_bg)",
    "nav_text": "#hex — navbar links and logo color",
    "hero_bg": "#hex — hero section background",
    "hero_text": "#hex — hero headline color",
    "section_alt_bg": "#hex — alternating section background (must differ from body_bg)",
    "card_bg": "#hex — card/tile background",
    "card_border": "#hex — card border or divider color",
    "btn_primary_bg": "#hex — primary CTA button background",
    "btn_primary_text": "#hex — primary button label",
    "btn_secondary_bg": "#hex — secondary/ghost button color",
    "input_bg": "#hex — form input field background",
    "input_border": "#hex — form input border",
    "badge_bg": "#hex — tag/badge/chip background",
    "badge_text": "#hex — tag/badge label",
    "icon_fill": "#hex — icon and decorative element color",
    "footer_bg": "#hex — footer background",
    "footer_text": "#hex — footer body text"
  }},
  "typography": "specific Google Font pairing: heading font + body font, size/weight notes — must MATCH the mood (e.g. serif for editorial, monospace for terminal)",
  "visual_details": "3 specific visual treatments — name exact CSS techniques: e.g. 'backdrop-filter:blur(20px) on nav', 'repeating-linear-gradient noise texture', 'border: 3px solid black with 6px offset shadow'",
  "content_strategy": "specific realistic content — real brand names, actual product copy, real stats (NO lorem ipsum, NO 'placeholder', NO 'Image here')",
  "animation_hints": "implement {animation or 'the chosen animation'} with exact CSS property names and values",
  "sections": [
    {{
      "id": "nav",
      "type": "navbar",
      "content": "logo name + 3-4 nav links + CTA button — actual text, NOT placeholder",
      "style_note": "use nav_bg color, sticky position, backdrop-blur"
    }},
    {{
      "id": "hero",
      "type": "hero",
      "layout_note": "follow the layout archetype above STRICTLY",
      "content": "headline (max 8 words, bold claim) + subheadline + CTA — real copy",
      "style_note": "hero_bg color, hero_text for headline, decorative elements"
    }},
    {{
      "id": "section-2",
      "type": "features or stats or showcase",
      "content": "3-4 items with real metrics/names/descriptions",
      "style_note": "section_alt_bg, card_bg for cards"
    }},
    {{
      "id": "section-3",
      "type": "testimonials or pricing or gallery",
      "content": "real names, real quotes or realistic pricing tiers",
      "style_note": "vary background from section-2"
    }},
    {{
      "id": "footer",
      "type": "footer",
      "content": "brand name + 3 columns of links + copyright",
      "style_note": "footer_bg, footer_text colors"
    }}
  ]
}}"""

    log.info("[pass1] 브리프 생성 중... model=%s style=%s | layout=%s",
             MODEL_BRIEF, style, (layout_arch or "free")[:40])
    text = await ollama_chat(
        [
            {"role": "system", "content": BRIEF_SYSTEM},
            {"role": "user",   "content": prompt},
        ],
        model=MODEL_BRIEF,
        temperature=0.88,   # 창의적 기획 → 높은 다양성
        num_ctx=16384,
    )
    return extract_json(text)

# ── Pass 2: HTML 초안 ─────────────────────────────────────────────────────────
HTML_SYSTEM = """\
You are an elite frontend engineer who builds visually distinctive UIs.
You can do ANY aesthetic — minimal, brutalist, dark luxury, editorial, retro, organic — and you commit fully to the chosen direction.

HARD RULES:
- Start with <!DOCTYPE html><html lang="en"><head>...</head><body>...</body></html>
- Include <script src="https://cdn.tailwindcss.com"></script> as the FIRST element in <head>
- Include Google Fonts <link> for the specified fonts in <head>
- Use REAL content only — zero lorem ipsum, zero "placeholder text", zero "Image here"
- NEVER use min-h-screen, h-screen, 100vh, or position:fixed — these BREAK the preview iframe
- Use min-h-0 or auto height instead — let content determine page height naturally
- Respond with ONLY the raw HTML — no explanation, no ```fences```

STRUCTURAL DIVERSITY RULES (read carefully):
- Follow the layout archetype EXACTLY — if it says asymmetric, make ONE side dramatically larger
- If it says brutalist, use thick black borders and NO rounded corners anywhere
- If it says terminal/CLI, use monospace font and a dark console aesthetic throughout
- If it says editorial, let elements OVERLAP columns and break the grid intentionally
- DO NOT default to a standard centered hero + 3-column feature grid — that is the forbidden default

VISUAL QUALITY RULES:
- Write a <style> block: @keyframes for the specified animation, custom CSS for special effects
- Use the EXACT colors from the color_palette — do not substitute with Tailwind default blues/grays
- Typography hierarchy: at least 3 distinct sizes, weights, and styles
- Every section needs a different background treatment — avoid repeating the same bg color
- All interactive elements need hover states (transition: all 0.25s)
- Add at least 2 decorative CSS elements: geometric shapes, patterns, blobs, lines — as `::before`/`::after` or divs

COMPONENT COLOR RULES (mandatory — apply color_roles to every element):
- body / page wrapper → body_bg color (set as background-color on body or outermost div)
- navbar / header → nav_bg background, nav_text for links and logo
- hero section → hero_bg background, hero_text for the main headline
- alternating sections → use section_alt_bg (must visually differ from body_bg)
- cards / panels / tiles → card_bg background, card_border as border or box-shadow base color
- primary CTA buttons → btn_primary_bg fill, btn_primary_text label; darken ~10% on :hover
- secondary / ghost buttons → btn_secondary_bg as outline or subtle fill
- form inputs (input, textarea, select) → input_bg background, input_border border color
- tags / badges / chips → badge_bg background, badge_text label color
- icons and inline decorative shapes → icon_fill color
- footer → footer_bg background, footer_text for all footer copy and links
- NEVER leave a major UI component at the browser default white/black when a color_role is provided

MOBILE & RESPONSIVE:
- Use responsive Tailwind breakpoints (sm:, md:, lg:) — NOT desktop-only widths
- Grid columns must collapse: lg:grid-cols-3 → md:grid-cols-2 → grid-cols-1
- Text sizes must scale: hero text-4xl on mobile → text-6xl on lg
- Touch targets: all clickable elements min 44px height on mobile
- Images must use max-w-full and responsive widths

CONTENT QUALITY (critical for user engagement):
- Write REAL product copy that sounds like a funded startup — not generic placeholder
- Use specific numbers: "$2.4M ARR", "99.97% uptime", "14-day free trial"
- Include real-sounding testimonials with full names, titles, and companies
- Pricing tiers should have specific features and realistic prices ($29/$79/$199)
- Navigation should feel complete: Logo, 4-5 links, CTA button

FORBIDDEN:
- Standard hero with centered text + subtitle + two buttons as the only layout idea
- All-blue or all-purple color scheme unless explicitly specified
- Flat cards with no border, shadow, or background distinction
- The same card layout repeating for every section
- Walls of same-size text with no typographic contrast
- Generic copy like "Welcome to our platform" or "Get started today"
- Placeholder images or "Image here" text"""

async def pass2_html_draft(brief: Dict[str, Any], category: str, style: str, structure: str,
                           dna: Optional[Dict[str, str]] = None,
                           trend_context: str = "",
                           css_system: str = "") -> str:
    colors      = " | ".join(brief.get("color_palette", []))
    layout_arch = dna.get("layout_arch", structure) if dna else structure
    animation   = dna.get("animation", "hover lifts") if dna else "hover lifts"

    # 컴포넌트별 색상 역할 포맷
    color_roles = brief.get("color_roles", {})
    role_lines  = "\n".join(f"  {r}: {c}" for r, c in color_roles.items()) if color_roles else ""
    color_roles_block = f"""
━━ COMPONENT COLOR MAP (apply EXACTLY — no browser defaults) ━━
{role_lines}
→ Use CSS variables from the injected <style> block (var(--color-*)) wherever possible.
→ Where Tailwind can't express a custom hex, use inline style or the var() reference.
""" if role_lines else ""

    # 섹션 명세 (Pass1에서 생성된 구조 활용)
    sections = brief.get("sections", [])
    sections_block = ""
    if sections:
        sec_lines = "\n".join(
            f"  [{s.get('id','?')}] type={s.get('type','?')} | {s.get('layout_note') or s.get('style_note','')}\n"
            f"    content: {s.get('content','')}"
            for s in sections
        )
        sections_block = f"""
━━ REQUIRED SECTIONS (build in this order) ━━
{sec_lines}
→ Every section above MUST appear in the final HTML.
→ Apply the correct background color to each section as specified.
"""

    # 자기학습 교훈 주입
    top_lessons = _get_top_lessons()
    lessons_block = f"""
━━ PREEMPTIVE FIXES (learned from {_load_lessons()["stats"].get("attempts",0)} past attempts) ━━
{top_lessons}
→ These issues caused low scores before. Solve them BEFORE writing HTML.
""" if top_lessons else ""

    prompt = f"""\
Build a complete {category} UI. Read EVERY constraint before writing a single line.

━━ DESIGN SYSTEM (injected — use var(--color-*) throughout) ━━
The <style> block below contains your complete CSS variable system. USE IT.
Do NOT hardcode hex colors — reference var(--color-bg), var(--color-primary), etc.
{css_system if css_system else "No CSS system provided — define your own CSS variables in <style>."}

━━ LAYOUT ARCHETYPE (MANDATORY — structural, not decorative) ━━
{layout_arch}
→ If "asymmetric" → one side is 60%+ of width, the other 40%-.
→ If "brutalist" → thick borders (3px+), zero border-radius, hard offset shadows.
→ If "bento" → at least 6 cells, varying sizes (span-2, span-3 mixed).
→ If "editorial" → elements intentionally overlap columns, break the grid.
→ FORBIDDEN: standard centered hero + subtitle + 3-column cards. That is the default everyone does.

━━ VISUAL STYLE ━━
Style: {style}
Structure variant: {structure}

━━ COLORS ━━
Palette: {colors}
{color_roles_block}
━━ ANIMATION ━━
{animation}
→ The @keyframes is already in the injected <style>. Use the class names you defined.

━━ CONTENT & BRAND ━━
Brand: {brief.get("title")}
Concept: {brief.get("concept")}
Typography: {brief.get("typography")} — load from Google Fonts
Visual treatments: {brief.get("visual_details", "")}
Content strategy: {brief.get("content_strategy")}
Animation hints: {brief.get("animation_hints", "")}
{sections_block}
{trend_context if trend_context else ""}
{lessons_block}
━━ HARD RULES ━━
1. <head> must include Tailwind CDN + Google Fonts link
2. Inject the CSS system <style> block at the top of <head>
3. body background = var(--color-bg)
4. Each section uses its designated background — never the same bg twice in a row
5. Every button must have a hover state
6. Add ≥2 decorative elements (::before/::after or empty divs with CSS shapes)
7. Real content only — NO lorem ipsum, NO "placeholder", NO "coming soon" filler
8. Outermost element must NOT have min-h-screen

━━ PRE-WRITE CHECKLIST ━━
□ Layout matches the archetype (not a default hero-grid)?
□ CSS variables used instead of hardcoded hex?
□ Every section has its correct background color?
□ Buttons use var(--color-primary) for fill?
□ Animation class is applied to at least one element?
□ All 5+ sections from the list above are present?

Write the COMPLETE HTML now — all sections, no truncation."""

    log.info("[pass2] HTML 초안 생성 중... model=%s (css_system=%d chars)", MODEL_CODER, len(css_system))
    text = await ollama_chat(
        [
            {"role": "system", "content": HTML_SYSTEM},
            {"role": "user",   "content": prompt},
        ],
        model=MODEL_CODER,
        temperature=0.78,   # HTML 생성: 구조 일관성 > 창의성
        num_ctx=32768,
    )
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
{html[:12000]}
```

Score it STRICTLY on visual beauty and design quality. Be harsh — a score of 75+ means genuinely stunning.

Scoring criteria:
- Visual depth & layering (shadows, gradients, glassmorphism): 0-15 pts
- Typography hierarchy & font pairing quality: 0-15 pts
- Color harmony & component color consistency (navbar, cards, buttons, inputs, footer each with distinct intentional colors — NOT all the same bg): 0-15 pts
- Animation & micro-interactions (CSS): 0-10 pts
- Decorative richness (backgrounds, shapes, accents): 0-10 pts
- Content realism & copy quality (real product names, specific numbers, compelling headlines — NOT generic placeholder copy): 0-15 pts
- Responsive design (Tailwind breakpoints, mobile-friendly grids, scalable text): 0-10 pts
- Overall polish & "would I screenshot this?" factor: 0-10 pts

Score each criterion SEPARATELY, then sum for total:
{{
  "scores": {{
    "visual_depth":   <0-15>,  // shadows, gradients, layering, glassmorphism
    "typography":     <0-15>,  // hierarchy, font pairing, size contrast
    "color_system":   <0-15>,  // palette harmony, component color consistency, no defaults
    "animation":      <0-10>,  // CSS animations present and working, micro-interactions
    "decoration":     <0-10>,  // backgrounds, shapes, accents, visual richness
    "content_quality":<0-15>,  // realistic copy, specific numbers, compelling headlines, NO lorem ipsum
    "responsiveness": <0-10>,  // Tailwind responsive breakpoints, mobile-friendly layout
    "polish":         <0-10>   // overall "wow factor", screenshot-worthy, cohesive feel
  }},
  "score": <sum of all scores above, integer>,
  "critical_issues": [
    {{
      "area": "depth|typography|color|animation|decoration|spacing|content",
      "problem": "exact element or CSS rule that is wrong",
      "fix": "specific CSS/HTML fix with exact property names and values",
      "impact": <estimated score gain 1-8>
    }}
  ],
  "minor_issues": [
    {{
      "area": "...",
      "fix": "specific fix"
    }}
  ],
  "strengths": ["what specifically works well — be concrete"]
}}

List at most 3 critical_issues and 3 minor_issues. Order by impact descending.
Be HARSH — a real 80+ score means it could be featured on Awwwards. Most designs score 50-70."""

    log.info("[pass3] 심층 리뷰 중... model=%s", MODEL_REVIEW)
    text = await ollama_chat(
        [
            {"role": "system", "content": REVIEW_SYSTEM},
            {"role": "user",   "content": prompt},
        ],
        model=MODEL_REVIEW,
        temperature=0.25,   # 리뷰는 일관성/정확성 최우선 → 낮은 temperature
        num_ctx=32768,
    )
    # deepseek-r1 등 추론 모델은 <think>...</think> 블록 출력 후 JSON 제공
    # → <think> 블록을 제거하고 JSON만 추출
    text = re.sub(r"<think>[\s\S]*?</think>", "", text, flags=re.IGNORECASE).strip()
    try:
        result = extract_json(text)
        # 하위 호환: critical_issues → issues 로 통합
        if "critical_issues" in result and "issues" not in result:
            result["issues"] = result["critical_issues"] + result.get("minor_issues", [])
        # scores 합산이 score와 불일치 시 보정
        if "scores" in result:
            computed = sum(result["scores"].values())
            if abs(computed - result.get("score", 0)) > 5:
                result["score"] = computed
                log.debug("[pass3] score 보정: %d → %d (합산)", result.get("score", 0), computed)
        return result
    except Exception:
        return {"score": 50, "issues": [], "strengths": [], "scores": {}}

# ── 컴포넌트 색상 역할 포맷 (pass4 재사용) ────────────────────────────────────
def _format_color_roles_for_refinement(color_roles: Dict[str, str]) -> str:
    if not color_roles:
        return ""
    lines = "\n".join(f"  {role}: {color}" for role, color in color_roles.items())
    return f"""
Component color map (verify every component matches):
{lines}
"""

# ── Pass 4: Critical 이슈 집중 수정 ──────────────────────────────────────────
async def pass4_refined_html(html: str, review: Dict[str, Any], brief: Dict[str, Any],
                              category: str, style: str, css_system: str = "") -> str:
    # critical_issues 우선, 없으면 issues에서 상위 3개
    critical = review.get("critical_issues", [])
    if not critical:
        all_issues = review.get("issues", [])
        severity_order = {"critical": 0, "major": 1, "minor": 2}
        critical = sorted(all_issues, key=lambda i: severity_order.get(i.get("severity", "minor"), 2))[:3]

    if not critical:
        log.info("[pass4] 수정할 이슈 없음 — 초안 유지")
        return html

    # impact 기준으로 상위 3개만 처리 (너무 많으면 다른 곳 망가짐)
    top_fixes = sorted(critical, key=lambda i: -i.get("impact", 5))[:3]
    fix_lines = "\n".join(
        f"{idx+1}. [{f.get('area','?').upper()}] {f.get('problem', '')} → {f.get('fix', f.get('fix',''))}"
        for idx, f in enumerate(top_fixes)
    )
    score_detail = ""
    if "scores" in review:
        score_detail = "Current sub-scores: " + ", ".join(
            f"{k}={v}" for k, v in review["scores"].items()
        )

    css_block = f"\nCSS Design System (use var() references):\n{css_system}\n" if css_system else ""

    prompt = f"""\
You are surgically fixing a {category} UI (style: {style}).
Apply ONLY these {len(top_fixes)} targeted fixes — do NOT change anything else:

{fix_lines}

{score_detail}
{css_block}
Current HTML (FULL):
```html
{html}
```

Design reference:
- Brand: {brief.get("title")}
- Color palette: {" | ".join(brief.get("color_palette", []))}
- Visual details: {brief.get("visual_details", "")}
- Animation: {brief.get("animation_hints", "")}
{_format_color_roles_for_refinement(brief.get("color_roles", {}))}
RULES:
- Apply the {len(top_fixes)} fixes above with surgical precision
- Keep ALL existing content, structure, sections unchanged
- If fix requires adding CSS → add it to the existing <style> block
- If fix requires changing a class → change only that element
- Do NOT simplify or remove sections to make the job easier
- Return ONLY the complete corrected HTML — no explanation, no fences"""

    log.info("[pass4] Critical %d개 이슈 집중 수정 중... model=%s", len(top_fixes), MODEL_CODER)
    text = await ollama_chat(
        [
            {"role": "system", "content": HTML_SYSTEM},
            {"role": "user", "content": prompt},
        ],
        model=MODEL_CODER,
        temperature=0.65,
        num_ctx=32768,
    )
    return extract_html(text)

# ── 스크린샷 촬영 ─────────────────────────────────────────────────────────────
async def capture_screenshot(browser: Browser, html: str) -> bytes:
    page = await browser.new_page(viewport={"width": 1400, "height": 900})
    try:
        await page.set_content(html, wait_until="networkidle")
        # Tailwind CDN + Google Fonts 로딩 대기
        await page.evaluate("document.fonts.ready")
        await page.wait_for_timeout(3000)
        # 프리뷰 깨짐 방지: vh 단위 + fixed 포지션 + h-screen 클래스 제거
        await page.evaluate("""
            document.querySelectorAll('*').forEach(el => {
                const s = window.getComputedStyle(el);
                ['height', 'min-height', 'max-height'].forEach(prop => {
                    const v = s.getPropertyValue(prop);
                    if (v && (v.includes('vh') || v === '100%' && prop === 'height' && el.tagName !== 'HTML'))
                        el.style[prop] = 'auto';
                });
                if (s.position === 'fixed') el.style.position = 'sticky';
            });
            // Tailwind의 h-screen, min-h-screen 클래스 제거
            document.querySelectorAll('.h-screen, .min-h-screen').forEach(el => {
                el.classList.remove('h-screen', 'min-h-screen');
                el.style.height = 'auto';
                el.style.minHeight = 'auto';
            });
        """)
        await page.wait_for_timeout(500)
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
    trend_context: str = "",
) -> tuple[bool, Optional[DesignData], int, Dict]:
    """
    디자인을 생성하고 데이터를 반환 — DB/Storage 저장은 하지 않음.
    저장 여부는 호출자(run_batch)가 score를 보고 결정.

    Returns (success, design_data, score, last_review)
    """
    # DNA 기반으로 모든 다양성 차원 한 번에 결정
    dna = pick_design_dna()
    category  = dna["category"]
    style     = dna["style"]
    structure = dna["structure"]
    design_id = str(uuid.uuid4())

    log.info("[start] category=%s | style=%s", category, style)
    log.info("[dna] layout=%s", dna.get("layout_arch", "")[:60])
    log.info("[dna] color=%s", dna.get("color_mood", "")[:60])
    log.info("[dna] animation=%s", dna.get("animation", "")[:60])
    log.info("[config] min_score=%d | max_refine=%d", min_score, max_refine)

    try:
        # Pass 0: CSS 디자인 시스템 (토큰/변수 먼저 확정)
        log.info("[pass0] CSS 디자인 시스템 생성 중...")
        css_system = await pass0_css_system(dna)
        log.info("[pass0] CSS 시스템 생성 완료 (%d chars)", len(css_system))

        # Pass 1: 브리프 (DNA + 트렌드 전달)
        brief = await pass1_brief(category, style, structure, dna=dna, trend_context=trend_context)
        title = brief.get("title", "Untitled Design")
        log.info("[brief] 제목: %s", title)

        # Pass 2: HTML 초안 (DNA + 트렌드 전달 — 색상/레이아웃/트렌드 강제)
        html_current = await pass2_html_draft(
            brief, category, style, structure, dna=dna, trend_context=trend_context,
            css_system=css_system,
        )
        if not html_current.strip():
            log.error("[pass2] HTML 초안 비어있음")
            return False, None, 0, {}

        # Pass 2.5: 구조 검증 + 자동 수정
        is_valid, html_issues = validate_html(html_current)
        if html_issues:
            log.warning("[validate] HTML 구조 이슈 %d개: %s", len(html_issues), " | ".join(html_issues[:3]))
        html_current = fix_html_structure(html_current)
        if not is_valid:
            # 재검증
            is_valid2, remaining = validate_html(html_current)
            if remaining:
                log.warning("[validate] 자동 수정 후에도 남은 이슈: %s", " | ".join(remaining[:2]))

        # 품질 개선 루프
        score = 0
        last_review: Dict = {}
        total_passes = max_refine if min_score > 0 else 1

        for refine_idx in range(total_passes):
            round_label = f"[refine {refine_idx + 1}/{total_passes}]" if total_passes > 1 else "[review]"

            review = await pass3_review(html_current, category, style)
            last_review = review
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

            refined = await pass4_refined_html(html_current, review, brief, category, style, css_system=css_system)
            if refined.strip():
                refined = fix_html_structure(refined)
                # 개선 버전이 원본보다 너무 짧으면 폐기 (섹션 삭제 방지)
                if len(refined) < len(html_current) * 0.6:
                    log.warning("%s 개선 HTML이 원본의 60%% 미만 (%d→%d chars) — 원본 유지",
                                round_label, len(html_current), len(refined))
                else:
                    html_current = refined
            else:
                log.warning("%s 개선 HTML 비어있음 — 이전 버전 유지", round_label)

        html_final = fix_html_structure(html_current)

        # 스크린샷
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
            # DNA 추가 저장 (히스토리용)
            "dna":         dna,
        }

        log.info("[생성완료] %s | score=%d | layout=%s",
                 title, score, dna.get("layout_arch", "")[:40])
        return True, design_data, score, last_review

    except Exception as exc:
        log.error("[error] 생성 실패: %s", exc, exc_info=True)
        return False, None, 0, {}


def publish_design(data: DesignData) -> str:
    """Storage 업로드 + DB 저장 + 히스토리 기록. 저장된 slug 반환."""
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

    # 히스토리 저장 — 다음 생성 시 중복 방지용
    dna = data.get("dna", {})
    _save_history({
        "title":      data["title"],
        "slug":       slug,
        "score":      data["score"],
        "category":   data["category"],
        "style":      dna.get("style", ""),
        "structure":  dna.get("structure", ""),
        "color_key":  dna.get("color_key", ""),
        "layout_key": dna.get("layout_key", ""),
        "animation":  dna.get("animation", ""),
        "ts":         datetime.utcnow().isoformat(),
    })

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
    use_trends: bool = True,
    refresh_trends_cache: bool = False,
) -> None:
    """
    count               : 목표 저장 디자인 수
    min_score           : 단일 디자인 내 개선 반복 기준 점수
    max_refine          : 단일 디자인 내 최대 개선 횟수
    target_score        : 이 점수 이상인 디자인만 저장 (0 = 비활성화)
                          미달 시 새 디자인을 처음부터 다시 생성
    max_attempts        : target_score 달성을 위한 최대 시도 횟수 (무한루프 방지)
    use_trends          : True = 웹 트렌드 수집 후 프롬프트에 주입
    refresh_trends_cache: True = 기존 캐시 무시하고 강제 갱신
    """
    log.info(
        "[system] Ollama(CODER=%s / BRIEF=%s / REVIEW=%s) | 목표 %d개 | min_score=%d | max_refine=%d | target_score=%d | max_attempts=%d | trends=%s",
        MODEL_CODER, MODEL_BRIEF, MODEL_REVIEW, count, min_score, max_refine, target_score, max_attempts,
        "on" if use_trends else "off",
    )

    # Ollama 연결 확인
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            r = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            models = [m["name"] for m in r.json().get("models", [])]
            log.info("[ollama] 사용 가능한 모델: %s", models)
            for _m in {MODEL_CODER, MODEL_BRIEF, MODEL_REVIEW}:
                if _m not in models:
                    log.warning("[ollama] %s 모델이 목록에 없습니다. 그래도 시도합니다.", _m)
    except Exception as exc:
        log.error("[ollama] 연결 실패: %s — Ollama가 실행 중인지 확인하세요", exc)
        return

    # 학습 메모리 현황 출력
    lessons_data = _load_lessons()
    ls = lessons_data.get("stats", {})
    log.info(
        "[학습메모리] 총 %d회 시도 | 성공 %d회 | 학습된 이슈 %d개",
        ls.get("attempts", 0), ls.get("successes", 0), len(lessons_data.get("fixes", {})),
    )

    # 웹 트렌드 수집 (캐시 활용 또는 갱신)
    trend_context = ""
    if use_trends:
        log.info("[trend] 트렌드 데이터 로드 중...")
        try:
            trends = await get_trends(OLLAMA_BASE_URL, MODEL_CODER, force_refresh=refresh_trends_cache)
            trend_context = format_trend_prompt_block(trends)
            if trend_context:
                log.info("[trend] 트렌드 컨텍스트 준비 완료 (%d chars)", len(trend_context))
            else:
                log.info("[trend] 트렌드 데이터 없음 — 트렌드 없이 진행")
        except Exception as exc:
            log.warning("[trend] 트렌드 로드 실패 (무시하고 진행): %s", exc)

    successes = 0
    async with async_playwright() as p:
        browser = await p.chromium.launch()

        for i in range(count):
            log.info("\n═══ 디자인 %d/%d 목표 ═══", i + 1, count)

            if target_score > 0:
                # ── target_score 달성할 때까지 새 디자인 반복 생성 ──────────
                attempt = 0
                best_score = 0
                best_data: Optional[DesignData]  = None
                best_review: Dict                = {}

                while attempt < max_attempts:
                    attempt += 1
                    log.info("  [시도 %d/%d] 새 디자인 생성 중... (목표: score >= %d)",
                             attempt, max_attempts, target_score)
                    ok, design_data, score, last_review = await generate_one_design(
                        browser, min_score=min_score, max_refine=max_refine,
                        trend_context=trend_context,
                    )

                    # 이번 시도가 지금까지 최고점이면 백업
                    if ok and design_data and score > best_score:
                        best_score  = score
                        best_data   = design_data
                        best_review = last_review

                    if ok and score >= target_score:
                        log.info("  [✓] 목표 달성! score=%d >= %d (시도 %d회) — 저장 중...",
                                 score, target_score, attempt)
                        _record_result(
                            last_review.get("issues", []),
                            score,
                            design_data.get("dna", {}),
                            success=True,
                        )
                        slug = await asyncio.to_thread(publish_design, design_data)
                        log.info("  [✓] 게시 완료: https://ui-syntax.com/design/%s", slug)
                        successes += 1
                        break
                    elif ok:
                        log.info("  [✗] score=%d < %d — 폐기 후 재시도 (현재 최고: %d)",
                                 score, target_score, best_score)
                        _record_result(
                            last_review.get("issues", []),
                            score,
                            design_data.get("dna", {}),
                            success=False,
                        )
                    else:
                        log.warning("  [✗] 생성 실패 — 재시도")
                        _record_result([], 0, {}, success=False)

                    if attempt < max_attempts:
                        await asyncio.sleep(2)
                else:
                    # ── 모든 시도 소진 — 최고점 디자인 폴백 저장 ─────────────
                    fallback_threshold = max(target_score - 10, min_score, 60)
                    if best_data and best_score >= fallback_threshold:
                        log.warning(
                            "  [폴백] %d회 시도 후 목표(%d점) 미달. 최고 %d점 디자인 저장 (임계값: %d)",
                            max_attempts, target_score, best_score, fallback_threshold,
                        )
                        _record_result(
                            best_review.get("issues", []),
                            best_score,
                            best_data.get("dna", {}),
                            success=False,   # 학습: 목표 미달이므로 실패로 기록
                        )
                        slug = await asyncio.to_thread(publish_design, best_data)
                        log.info("  [폴백 저장] https://ui-syntax.com/design/%s", slug)
                        successes += 1
                    else:
                        log.warning(
                            "  [포기] %d회 시도 후 목표(%d점) 미달. 최고 점수=%d < 폴백 임계값=%d — 저장 안 함",
                            max_attempts, target_score, best_score, fallback_threshold,
                        )
            else:
                # ── 기존 단순 생성 (target_score 없으면 무조건 저장) ──────────
                ok, design_data, score, last_review = await generate_one_design(
                    browser, min_score=min_score, max_refine=max_refine,
                    trend_context=trend_context,
                )
                if ok and design_data:
                    _record_result(
                        last_review.get("issues", []),
                        score,
                        design_data.get("dna", {}),
                        success=True,
                    )
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
    parser.add_argument("--model",      type=str, default=_FALLBACK_MODEL, help="모든 패스에 적용할 단일 Ollama 모델 (미지정 시 패스별 기본 모델 사용)")
    parser.add_argument("--ollama",     type=str, default=OLLAMA_BASE_URL,  help="Ollama 서버 URL")
    parser.add_argument("--min-score",    type=int, default=DEFAULT_MIN_SCORE,
                        help="단일 디자인 내 개선 반복 기준 점수 (0=비활성화, 권장: 75-85)")
    parser.add_argument("--max-refine",   type=int, default=DEFAULT_MAX_REFINE,
                        help="단일 디자인 내 최대 개선 반복 횟수 (기본: 3)")
    parser.add_argument("--target-score", type=int, default=0,
                        help="이 점수 미만이면 새 디자인을 처음부터 재생성 (0=비활성화, 권장: 85-90)")
    parser.add_argument("--max-attempts", type=int, default=10,
                        help="target-score 달성을 위한 최대 시도 횟수 (기본: 10)")
    parser.add_argument("--no-trend",       action="store_true",
                        help="웹 트렌드 수집 비활성화 (오프라인 환경용)")
    parser.add_argument("--refresh-trends", action="store_true",
                        help="트렌드 캐시 무시하고 강제 갱신")
    args = parser.parse_args()

    # --model 인자가 지정되면 모든 패스를 해당 모델로 통일
    if args.model:
        MODEL_CODER  = args.model
        MODEL_BRIEF  = args.model
        MODEL_REVIEW = args.model
    OLLAMA_BASE_URL = args.ollama

    asyncio.run(run_batch(
        args.count,
        min_score=args.min_score,
        max_refine=args.max_refine,
        target_score=args.target_score,
        max_attempts=args.max_attempts,
        use_trends=not args.no_trend,
        refresh_trends_cache=args.refresh_trends,
    ))
