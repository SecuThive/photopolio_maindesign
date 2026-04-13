#!/usr/bin/env python3
"""
UI-Syntax Design Generator — v4.1  (Quality-First Edition)

주요 개선 사항:
  [v4.1] 100+ 줄 설계 시스템 룰 + 카테고리별 상세 가이드
  [v4.1] 자가 채점(60점 만점, 42점 이상만 저장) → 낮으면 재생성
  [v4.1] 스타일·구조 어피니티 맵 확장 (21개 스타일 조합)
  [v4.1] 스크린샷 파이프라인 강화 (폰트 로딩 대기 + vh 클린업)
  [v4.1] 실제 콘텐츠 생성 강제 (Lorem Ipsum 금지)
  [v4.1] SNS 스레드 영어 고품질 생성 유지
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

try:
    import tweepy
    _TWEEPY_AVAILABLE = True
except ImportError:
    _TWEEPY_AVAILABLE = False
from dotenv import load_dotenv
from google import genai
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

SUPABASE_URL              = os.getenv("SUPABASE_URL")
SUPABASE_KEY              = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
GEMINI_API_KEY            = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL              = os.getenv("GEMINI_MODEL", "gemini-2.5-pro-latest")
# 503 / 과부하 시 자동 전환할 폴백 모델 목록
GEMINI_FALLBACK_MODELS    = [m.strip() for m in os.getenv(
    "GEMINI_FALLBACK_MODELS", "gemini-2.0-flash,gemini-1.5-pro"
).split(",") if m.strip()]
STORAGE_BUCKET            = os.getenv("SUPABASE_DESIGNS_BUCKET", "designs-bucket")
STORAGE_FOLDER            = os.getenv("SUPABASE_DESIGNS_FOLDER", "designs")
REQUEST_NOTIFY_BASE_URL   = os.getenv("REQUEST_NOTIFY_BASE_URL", "http://localhost:3000").rstrip("/")
REQUEST_NOTIFY_SECRET     = os.getenv("REQUEST_NOTIFY_SECRET", "")
MIN_QUALITY_SCORE         = int(os.getenv("MIN_QUALITY_SCORE", "42"))   # /60

X_CONSUMER_KEY        = os.getenv("X_CONSUMER_KEY")
X_CONSUMER_SECRET     = os.getenv("X_CONSUMER_SECRET")
X_ACCESS_TOKEN        = os.getenv("X_ACCESS_TOKEN")
X_ACCESS_TOKEN_SECRET = os.getenv("X_ACCESS_TOKEN_SECRET")

RPM_LIMIT            = 5
RPD_LIMIT            = int(os.getenv("GEMINI_RPD_LIMIT", "100"))
MIN_REQUEST_INTERVAL = 60 / RPM_LIMIT + 1

# ── 클라이언트 지연 초기화 ────────────────────────────────────────────────────
_supabase_client: Optional[Client] = None
_gemini_client:   Optional[genai.Client] = None


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


# ── Rate Limiter ──────────────────────────────────────────────────────────────
class RateLimiter:
    def __init__(self, rpm: int, rpd: int, min_interval: float):
        self.rpm = rpm; self.rpd = rpd; self.min_interval = min_interval
        self._last: float = 0.0; self._daily: int = 0
        self._day: str = datetime.utcnow().strftime("%Y-%m-%d")

    def _reset(self) -> None:
        today = datetime.utcnow().strftime("%Y-%m-%d")
        if today != self._day:
            self._daily = 0; self._day = today

    async def acquire(self) -> None:
        self._reset()
        if self._daily >= self.rpd:
            raise RuntimeError(f"RPD 한도 {self.rpd} 도달")
        elapsed = time.monotonic() - self._last
        if elapsed < self.min_interval:
            await asyncio.sleep(self.min_interval - elapsed)
        self._last = time.monotonic(); self._daily += 1


rate_limiter = RateLimiter(rpm=RPM_LIMIT, rpd=RPD_LIMIT, min_interval=MIN_REQUEST_INTERVAL)

# ── 디자인 상수 ───────────────────────────────────────────────────────────────
CATEGORIES = ["Landing Page", "Dashboard", "E-commerce", "Portfolio", "Blog", "Component"]

# 스타일 + 어울리는 레이아웃 구조 어피니티 맵 (확장판)
STYLE_STRUCTURE_AFFINITY: Dict[str, list[str]] = {
    # ─ Minimal / Clean ─────────────────────────────────────────────
    "Apple-inspired Minimal White": [
        "Hero with Center Call-to-Action", "Split Screen Feature Display",
        "Step-by-step Onboarding Flow", "Minimalist Article Feed",
        "Centered Newsletter Subscription",
    ],
    "Vercel-style Developer Minimal": [
        "Bento Grid Dashboard", "Multi-column Technical Documentation",
        "Tabbed Dashboard Interface", "Command Palette Quick Search",
        "Stat-heavy Admin Panel",
    ],
    "Notion-like Clean Typography": [
        "Minimalist Article Feed", "Accordion FAQ List",
        "Vertical Timeline of Events", "Profile Header with Stats",
        "Multi-column Technical Documentation",
    ],
    "Nordic Arctic Clean": [
        "Hero with Center Call-to-Action", "Masonry Gallery Layout",
        "Minimalist Article Feed", "Team Member Circle Grid",
        "Clean Contact Form with Map",
    ],
    # ─ Dark Mode / Premium ──────────────────────────────────────────
    "Linear App Dark Mode Elegance": [
        "Sticky Sidebar Navigation", "Draggable Kanban Board",
        "Settings Page with Toggle Buttons", "Notification Center List",
        "Expandable Sidebar with Tooltips",
    ],
    "Luxury Gold & Deep Black": [
        "Hero with Center Call-to-Action", "E-commerce Product Showcase with Filter",
        "Team Member Circle Grid", "Testimonial Slider Grid",
        "Split Screen Feature Display",
    ],
    "Deep Ocean Dark Mode": [
        "Interactive Heatmap Dashboard", "Radial Progress Dashboard",
        "Bento Grid Dashboard", "Stat-heavy Admin Panel",
        "Live Activity Feed Sidebar",
    ],
    "Stealth All-Black Aesthetic": [
        "Full-page Video Background", "Hero with Center Call-to-Action",
        "Masonry Gallery Layout", "Project Portfolio Masonry",
        "Marquee-based Logo Wall",
    ],
    "Midnight Aurora Borealis": [
        "Hero with Center Call-to-Action", "Floating Interactive Cards",
        "Bento Grid Dashboard", "Full-page Video Background",
        "Radial Progress Dashboard",
    ],
    # ─ Glassmorphism / Gradient ─────────────────────────────────────
    "Glassmorphism Frosted": [
        "Floating Interactive Cards", "Layered Overlay Components",
        "Hero with Center Call-to-Action", "Stat-heavy Admin Panel",
        "Full-page Video Background",
    ],
    "Soft Pastel Gradient": [
        "Hero with Center Call-to-Action", "Three-tier Pricing Table",
        "Testimonial Slider Grid", "Centered Newsletter Subscription",
        "Team Member Circle Grid",
    ],
    "Liquid Gradient Flow": [
        "Hero with Center Call-to-Action", "Marquee-based Logo Wall",
        "Floating Interactive Cards", "Bento Grid Dashboard",
        "Split Screen Feature Display",
    ],
    # ─ Bold / Expressive ────────────────────────────────────────────
    "Neo-Brutalism High Contrast": [
        "Hero with Center Call-to-Action", "Masonry Gallery Layout",
        "E-commerce Product Showcase with Filter", "Project Portfolio Masonry",
        "Floating Interactive Cards",
    ],
    "Cyberpunk Neon Pink & Blue": [
        "Bento Grid Dashboard", "Full-page Video Background",
        "Radial Progress Dashboard", "Interactive Heatmap Dashboard",
        "Marquee-based Logo Wall",
    ],
    "Vibrant Memphis Pop": [
        "Hero with Center Call-to-Action", "Masonry Gallery Layout",
        "E-commerce Product Showcase with Filter", "Three-tier Pricing Table",
        "Bento Grid Dashboard",
    ],
    # ─ Fintech / SaaS ───────────────────────────────────────────────
    "Stripe-inspired Fintech Clean": [
        "Three-tier Pricing Table", "Hero with Center Call-to-Action",
        "Floating Interactive Cards", "Data-rich Table with Pagination",
        "Footer with Sitemap and Newsletter",
    ],
    "Enterprise Professional Blue": [
        "Sticky Sidebar Navigation", "Data-rich Table with Pagination",
        "Tabbed Dashboard Interface", "Stat-heavy Admin Panel",
        "Settings Page with Toggle Buttons",
    ],
    # ─ Retro / Artistic ─────────────────────────────────────────────
    "Retro 80s Synthwave": [
        "Full-page Video Background", "Hero with Center Call-to-Action",
        "Radial Progress Dashboard", "Marquee-based Logo Wall",
        "Masonry Gallery Layout",
    ],
    "Bauhaus Primary Colors": [
        "Hero with Center Call-to-Action", "Bento Grid Dashboard",
        "Masonry Gallery Layout", "Three-tier Pricing Table",
        "Floating Interactive Cards",
    ],
    # ─ Minimal Editorial ────────────────────────────────────────────
    "Japanese Zen Minimal": [
        "Minimalist Article Feed", "Hero with Center Call-to-Action",
        "Project Portfolio Masonry", "Vertical Timeline of Events",
        "Profile Header with Stats",
    ],
    "Modern Swiss Typographic": [
        "Multi-column Technical Documentation", "Minimalist Article Feed",
        "Hero with Center Call-to-Action", "Three-tier Pricing Table",
        "Accordion FAQ List",
    ],
}

STYLE_REFERENCE_BRANDS: Dict[str, str] = {
    "Apple-inspired Minimal White":    "Apple.com, Craft Docs, Bear App",
    "Vercel-style Developer Minimal":  "Vercel.com, Next.js docs, Tailwind UI",
    "Notion-like Clean Typography":    "Notion.so, Linear.app docs, Cron app",
    "Nordic Arctic Clean":             "Figma community, Framer.com, Nordic design",
    "Linear App Dark Mode Elegance":   "Linear.app, Raycast, Arc Browser",
    "Luxury Gold & Deep Black":        "Rolls-Royce, Armani, high-end hotel brands",
    "Deep Ocean Dark Mode":            "GitHub, VS Code dark, Planetscale",
    "Stealth All-Black Aesthetic":     "Apple AirPods Pro page, Darkroom app",
    "Midnight Aurora Borealis":        "Framer.com, Lottie files, Spline.design",
    "Glassmorphism Frosted":           "macOS Big Sur UI, iOS widgets, Figma UI3",
    "Soft Pastel Gradient":            "Lemon app, Superhuman onboarding, Typeform",
    "Liquid Gradient Flow":            "Stripe homepage, Shopify Polaris, Lottie",
    "Neo-Brutalism High Contrast":     "Gumroad, Read.cv, Awwwards featured sites",
    "Cyberpunk Neon Pink & Blue":      "Razer, Cyberpunk 2077 UI, SynthWave84 VSCode",
    "Vibrant Memphis Pop":             "Duolingo, Headspace, Mailchimp brand",
    "Stripe-inspired Fintech Clean":   "Stripe.com, Brex, Wise, Mercury Bank",
    "Enterprise Professional Blue":    "Salesforce Lightning, SAP Fiori, Atlassian",
    "Retro 80s Synthwave":             "SynthWave84, Outrun art, Lo-fi aesthetics",
    "Bauhaus Primary Colors":          "Figma brand, Material Design, Bauhaus 100",
    "Japanese Zen Minimal":            "Muji design, Uniqlo web, tofubeats aesthetic",
    "Modern Swiss Typographic":        "Swiss graphic design, Helvetica Now, Adobe",
}


def pick_style_structure() -> tuple[str, str]:
    style = random.choice(list(STYLE_STRUCTURE_AFFINITY.keys()))
    structure = random.choice(STYLE_STRUCTURE_AFFINITY[style])
    return style, structure


# ── 디자인 시스템 공통 룰 ─────────────────────────────────────────────────────
DESIGN_SYSTEM_RULES = """\
╔══════════════════════════════════════════════════════════════╗
║           ABSOLUTE DESIGN SYSTEM RULES  (never violate)     ║
╚══════════════════════════════════════════════════════════════╝

▌TYPOGRAPHY SCALE
  Display : 72–96px | weight 900 | letter-spacing -0.03em
  H1      : 48–64px | weight 800 | letter-spacing -0.02em
  H2      : 32–40px | weight 700 | letter-spacing -0.01em
  H3      : 20–24px | weight 600 | letter-spacing 0
  Body    : 15–17px | weight 400 | line-height 1.65
  Caption : 13px    | weight 500 | letter-spacing 0.01em
  Kicker  : 11–12px | weight 600 | letter-spacing 0.08em | UPPERCASE
  • Use ONLY: Inter, Plus Jakarta Sans, or Geist (Google Fonts)
  • Max 2 font weights per section
  • Heading always has tighter tracking than body text

▌SPACING (8pt base grid)
  4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 80 / 96 / 128px
  Section vertical padding : min 80px (5rem)
  Card inner padding       : 24–32px
  Between sibling elements : multiples of 8px ONLY
  Grid gaps                : 16px (tight), 24px (normal), 32px (open)

▌COLOR CONSTRAINTS
  Light BG  : #f8f9fa | #f5f5f7 | #fafaf9 | #f9fafb  (NEVER #fff)
  Dark BG   : #0a0a0b | #0f0f12 | #111218 | #13141a  (NEVER #000)
  Light text: slate-900 (#0f172a)
  Dark text : zinc-50 (#fafafa)
  Muted     : 50–60% opacity of main text
  Accent    : ONE primary color, used in < 20% of design surface area
  Semantic  : green = success, red = error, amber = warning

▌DEPTH & SHADOW SYSTEM
  Flat   : box-shadow: 0 1px 3px rgba(0,0,0,0.06)
  Raised : box-shadow: 0 4px 16px rgba(0,0,0,0.08)
  Float  : box-shadow: 0 20px 40px rgba(0,0,0,0.12), 0 2px 8px rgba(0,0,0,0.05)
  Glass  : backdrop-filter: blur(20px); background: rgba(255,255,255,0.08); border: 1px solid rgba(255,255,255,0.12)
  • NEVER use pure black in shadows — always rgba with alpha < 0.2

▌BORDER RADIUS
  Tags / badges    : 4–6px
  Inputs / buttons : 8–10px
  Cards            : 12–16px
  Large sections   : 20–24px
  Pills            : 9999px

▌MICRO-INTERACTIONS (mandatory)
  Every <a>, <button>, card, row → hover state REQUIRED
  Transition: all 0.2s ease   (NEVER > 0.4s for interactions)
  Hover button : brightness(1.05) or slight bg shift
  Hover card   : translateY(-2px) + shadow increase
  Active state : scale(0.97) or brightness(0.95)
  Focus ring   : outline: 2px solid #accent; outline-offset: 2px

▌IMAGES & CONTENT
  • Unsplash format: https://images.unsplash.com/photo-{ID}?w=800&q=80&auto=format&fit=crop
  • NEVER use placeholder.com, placehold.it, or lorempixel
  • NEVER use Lorem Ipsum — write real, specific copy
  • Realistic numbers: "12,847 users" not "1,000 users"  |  "$2.4M ARR" not "$1M"
  • Product/company names must fit the aesthetic (e.g., "Nebula", "Solace", "Axiom")
"""

CATEGORY_RULES: Dict[str, str] = {
    "Landing Page": """\
▌LANDING PAGE CHECKLIST
  ✓ Hero : full-viewport height | clear value prop ≤ 8 words | gradient/image bg
  ✓ Sub-headline : 1–2 sentences that expand on the headline
  ✓ Primary CTA : filled, gradient-accented button (min 48px height)
  ✓ Secondary CTA : ghost/outline button OR "Learn more" link
  ✓ Social proof : near hero — user count, logos strip, or quote snippet
  ✓ Feature section : 3 or 6 features, icon + title + 1-line description
  ✓ Closing CTA : repeat primary CTA at bottom with slightly different framing
  ✗ Anti-patterns: vague "The Future of X" headlines | more than 2 primary CTAs
                   hero with plain solid-color background | no social proof
""",
    "Dashboard": """\
▌DASHBOARD CHECKLIST
  ✓ Navigation : fixed sidebar (240–280px) OR top navbar (64px) — with active state
  ✓ KPI grid : exactly 4 cards | metric + ±% trend + mini-sparkline or icon
  ✓ Main chart: area or line chart with realistic non-uniform data points
  ✓ Secondary widget: table, donut chart, or activity feed
  ✓ Status dots: green/amber/red semantic colors
  ✓ Data labels: always show units (e.g., "$", "ms", "%", "K")
  ✗ Anti-patterns: no trends on KPI cards | perfectly uniform chart data
                   more than 5 colors in one chart | no data labels
""",
    "E-commerce": """\
▌E-COMMERCE CHECKLIST
  ✓ Product card : image (aspect 3:4 or 4:3) | name | price | star rating | add-to-cart
  ✓ Price display : bold, prominent; show strikethrough if on sale
  ✓ Filter system: category chips OR left sidebar with toggle options
  ✓ Cart badge   : count indicator in nav
  ✓ Trust signals: ★ rating count | "Free shipping" badge | "In stock" indicator
  ✓ Grid        : 2 cols mobile → 3–4 cols desktop (CSS grid, not flex)
  ✓ Hover       : image slight zoom (transform: scale(1.04)) + "Quick View" overlay
  ✗ Anti-patterns: no visible price | no add-to-cart | generic product names
                   no filter system | no trust indicators
""",
    "Portfolio": """\
▌PORTFOLIO CHECKLIST
  ✓ Hero/About  : photo avatar + name + role + 2-sentence bio + social icon links
  ✓ Work grid   : project image (16:9) | category tag | title | hover overlay w/ CTA
  ✓ Filter tabs : by category (UI Design / Branding / Web Dev / etc.)
  ✓ Case study  : client | year | tools | challenge → solution format
  ✓ Skills      : visual grouping by domain — NOT a flat list
  ✓ Contact     : email OR simple 3-field form + response time note
  ✗ Anti-patterns: no project names | no case study depth | generic "John Doe" bio
                   skills as plain bullet list only | no hover on cards
""",
    "Blog": """\
▌BLOG CHECKLIST
  ✓ Article card : cover image (16:9) | category badge (colored) | title | excerpt (2 lines)
                   author avatar+name | date | read time (e.g., "5 min read")
  ✓ Featured     : 1 hero-size article with full-width or 2-col span treatment
  ✓ Categories   : visible navigation chips or sidebar category list
  ✓ Typography   : article titles use serif or semi-serif for editorial personality
  ✓ Author info  : avatar + name + short bio on featured cards
  ✗ Anti-patterns: no author info | no dates | no category system | no read time
                   all cards same size (no visual hierarchy) | Lorem Ipsum excerpts
""",
    "Component": """\
▌COMPONENT SHOWCASE CHECKLIST
  ✓ Section header : component type title + usage description + context label
  ✓ Variants       : minimum 4 variations (size S/M/L/XL or state/style variants)
  ✓ States         : show default / hover / active / disabled / error–success where applicable
  ✓ Labels         : clear monospace or caption label on each variant
  ✓ Background     : light gray (#f4f5f7) to reveal white/light components
  ✓ Grouping       : 32–48px gap between different component categories
  ✗ Anti-patterns: only 1 variant | no state labels | inconsistent spacing
                   dark bg making dark components invisible | missing disabled state
""",
}

# ── 프롬프트 빌더 ─────────────────────────────────────────────────────────────

def build_design_prompt(
    category: str,
    structure: str,
    style: str,
    reference_brands: str = "",
    request_context: str = "",
) -> str:
    cat_rules = CATEGORY_RULES.get(category, "")
    ref_line = f"\n  Reference brands / aesthetic direction: {reference_brands}" if reference_brands else ""

    return f"""\
You are the creative principal at a world-class product design studio — the person \
who sets the bar for quality at companies like Linear, Vercel, and Stripe. \
You ship pixel-perfect, production-ready HTML components that look stunning in a real browser.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  DESIGN BRIEF
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Category  : {category}
  Layout    : {structure}
  Aesthetic : {style}{ref_line}
{request_context}

{DESIGN_SYSTEM_RULES}

{cat_rules}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  HTML IMPLEMENTATION REQUIREMENTS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1. ALWAYS include both in <head>:
   <script src="https://cdn.tailwindcss.com"></script>
   <link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">

2. Outermost element MUST shrink to fit its content:
   • NO min-h-screen / h-screen on the wrapper element
   • Use min-h-screen ONLY for elements INSIDE the component (e.g. sidebar panel)

3. Write semantic HTML: <header>, <nav>, <main>, <section>, <article>, <footer>

4. Include at least ONE of these depth effects:
   • Glassmorphism card: backdrop-blur-xl bg-white/8 border border-white/10
   • Soft ambient glow: box-shadow: 0 0 120px -40px rgba(accent, 0.35)
   • Layered background: radial-gradient overlay on top of base color

5. Real, specific content (MANDATORY):
   • Company name: fits the aesthetic (e.g. "Axiom" | "Solace" | "Nebula" | "Vanta")
   • Realistic metrics: "14,203 active teams" | "$4.2M raised" | "99.97% uptime"
   • Write headlines that a real marketer would write
   • No Lorem Ipsum anywhere

6. Images: use these exact Unsplash base URLs (add ?w=800&q=80&auto=format&fit=crop):
   People  : photo-1534528741775-53994a69daeb | photo-1517841905240-472988babdf9
   Tech    : photo-1461749280684-dccba630e2f6 | photo-1555066931-4365d14bab8c
   Abstract: photo-1618005182384-a83a8bd57fbe | photo-1620641788421-7a1c342ea42e
   Product : photo-1523275335684-37898b6baf30 | photo-1491553895911-0055eca6402d

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  QUALITY SELF-REVIEW (before submitting)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Score each dimension 1–10:
  A. Visual hierarchy  — Does the eye flow naturally? Clear focal point?
  B. Typography system — Consistent scale? Tight headings, airy body text?
  C. Color harmony     — Palette feels intentional and cohesive? No clashing?
  D. Spacing rhythm    — Follows 8pt grid? No cramped or over-spaced sections?
  E. Micro-interactions— hover/transition on ALL clickable elements?
  F. Content quality   — Real copy? Specific numbers? No Lorem Ipsum?
Total MUST be ≥ 42 / 60. If below 42, revise the design before outputting.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  OUTPUT FORMAT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Return ONLY one valid JSON object (no markdown code fences):
{{
  "title": "Design name — 3–5 evocative words",
  "description": "Three sentences: what it is | who it is for | what makes it distinctive",
  "features": ["specific feature 1", "specific feature 2", "specific feature 3", "specific feature 4"],
  "usage": "One paragraph on use-case and implementation context",
  "self_review": {{
    "visual_hierarchy": 0,
    "typography": 0,
    "color_harmony": 0,
    "spacing": 0,
    "interactions": 0,
    "content_quality": 0,
    "total": 0,
    "design_notes": "2-3 sentences on key design decisions made"
  }},
  "html_code": "complete standalone HTML (with <head> containing Tailwind + fonts)",
  "react_code": "equivalent React component using Tailwind classes",
  "colors": ["#primary", "#secondary", "#accent", "#background", "#text"]
}}
"""


def build_sns_thread_prompt(title: str, category: str, style: str, slug: str, design_notes: str) -> str:
    return f"""\
You are a top-tier UI/UX design influencer on X (Twitter) with 80K followers. \
Your threads are known for being insightful, visually descriptive, and genuinely educational.

Write a 3-tweet English thread to showcase "{title}" — a {category} design with a {style} aesthetic.

Design context: {design_notes}

THREAD RULES:
- Tweet 1 (Hook + Reveal): One punchy opening line. What makes this design special? Describe the visual impact.
  End with a GIF-style description of the first impression. Add 1–2 relevant emojis.
- Tweet 2 (3 Design Insights): "Here's what makes it work:" followed by 3 bullet points
  with specific, technical UI/UX observations (reference actual techniques: e.g., "8pt grid spacing",
  "glassmorphism with 20px blur", "split complementary palette"). Educational tone.
- Tweet 3 (CTA): Friendly summary + link + max 2 hashtags (e.g., #UIUX #FrontendDesign).
  URL: https://ui-syntax.com/design/{slug}

FORMAT: Return ONLY valid JSON: {{ "tweets": ["tweet1", "tweet2", "tweet3"] }}
Character limit per tweet: 280.
"""


# ── 스크린샷 파이프라인 ───────────────────────────────────────────────────────
async def capture_screenshot(browser: Browser, html: str) -> bytes:
    """고품질 스크린샷: 폰트 로딩 대기 + vh 정리 + 타이트 크롭"""
    page = await browser.new_page(viewport={"width": 1400, "height": 900})
    try:
        # 페이지 로드
        try:
            await page.set_content(html, wait_until="networkidle", timeout=20_000)
        except Exception:
            await page.set_content(html, wait_until="load", timeout=15_000)

        # 폰트 완전 로딩 대기
        await page.evaluate("""
            () => document.fonts.ready
        """)
        await page.wait_for_timeout(1500)

        # vh/vw 기반 전체 높이 요소 축소 (빈 공간 방지)
        await page.evaluate("""\
            (() => {
              const root = document.getElementById('capture-box') || document.body;
              const viewport_selectors = [
                '.min-h-screen', '.h-screen',
                '.min-h-\\\\[100vh\\\\]', '.h-\\\\[100vh\\\\]'
              ].join(', ');

              root.querySelectorAll(viewport_selectors).forEach(el => {
                el.style.minHeight = 'auto';
                el.style.height = 'auto';
              });
              root.querySelectorAll('*').forEach(el => {
                const s = el.style;
                if (s.minHeight?.includes('100vh')) s.minHeight = 'auto';
                if (s.height?.includes('100vh')) s.height = 'auto';
              });
              document.documentElement.style.cssText += 'margin:0;padding:0;';
              document.body.style.cssText += 'margin:0;padding:0;';
            })();
        """)
        await page.wait_for_timeout(300)

        # 정확한 콘텐츠 높이 계산
        dims = await page.evaluate("""\
            (() => {
              const el = document.getElementById('capture-box') || document.body;
              return { height: Math.ceil(el.scrollHeight || 900) };
            })();
        """)
        height = max(900, min(int(dims.get("height", 900)) + 40, 7000))
        await page.set_viewport_size({"width": 1400, "height": height})
        await page.wait_for_timeout(200)

        target = await page.query_selector("#capture-box") or await page.query_selector("body")
        screenshot = await target.screenshot(type="png")
    except Exception as exc:
        log.error("[screenshot] 에러: %s — 폴백 캡처", exc)
        screenshot = await page.screenshot(type="png")
    finally:
        await page.close()
    return screenshot


def wrap_html_for_capture(html: str) -> str:
    """캡처용 래퍼 (Inter + Tailwind CDN 포함)"""
    if "<html" in html.lower():
        return html
    return (
        '<!DOCTYPE html><html lang="en"><head>'
        '<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1">'
        '<script src="https://cdn.tailwindcss.com"></script>'
        '<link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">'
        '<style>body{font-family:"Inter",sans-serif;margin:0;padding:0;}</style>'
        '<title>Preview</title></head>'
        '<body class="bg-gray-50 text-slate-900 antialiased m-0 p-0">'
        '<div id="capture-box" class="w-full max-w-[1400px] mx-auto flow-root">'
        f'{html}'
        '</div></body></html>'
    )


# ── Supabase 헬퍼 ─────────────────────────────────────────────────────────────
def slugify(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "design"


def ensure_unique_slug(base: str) -> str:
    candidate = slugify(base)
    suffix = 2
    while True:
        resp = get_supabase().table("designs").select("id").eq("slug", candidate).limit(1).execute()
        if not resp.data:
            return candidate
        candidate = f"{slugify(base)}-{suffix}"
        suffix += 1


def upload_image(image_bytes: bytes, category: str) -> str:
    filename = f"{datetime.utcnow():%Y%m%d_%H%M%S}_{slugify(category)}_{uuid.uuid4().hex[:6]}.png"
    path = f"{STORAGE_FOLDER}/{filename}"
    sb = get_supabase()
    sb.storage.from_(STORAGE_BUCKET).upload(path, image_bytes, {"content-type": "image/png"})
    return sb.storage.from_(STORAGE_BUCKET).get_public_url(path)


# ── SNS 업로드 ────────────────────────────────────────────────────────────────
async def post_to_x_thread(title: str, image_bytes: bytes, slug: str, tweets: list[str]) -> bool:
    if not _TWEEPY_AVAILABLE:
        log.info("[X] tweepy 미설치: 업로드 건너뜀 (venv pip install tweepy 로 설치 가능)")
        return False
    if not all([X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]):
        log.info("[X] API 키 미설정: 업로드 건너뜀")
        return False
    try:
        auth = tweepy.OAuth1UserHandler(X_CONSUMER_KEY, X_CONSUMER_SECRET, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET)
        api_v1 = tweepy.API(auth)
        client_v2 = tweepy.Client(
            consumer_key=X_CONSUMER_KEY, consumer_secret=X_CONSUMER_SECRET,
            access_token=X_ACCESS_TOKEN, access_token_secret=X_ACCESS_TOKEN_SECRET,
        )
        tmp = f"tmp_x_{uuid.uuid4().hex[:6]}.png"
        with open(tmp, "wb") as f:
            f.write(image_bytes)
        media = await asyncio.to_thread(api_v1.media_upload, filename=tmp)
        first = tweets[0] if tweets else f"✨ New UI Design: {title}\n\n👉 https://ui-syntax.com/design/{slug}"
        resp = await asyncio.to_thread(client_v2.create_tweet, text=first, media_ids=[media.media_id])
        last_id = resp.data["id"]
        for tweet in tweets[1:]:
            await asyncio.sleep(2)
            resp = await asyncio.to_thread(client_v2.create_tweet, text=tweet, in_reply_to_tweet_id=last_id)
            last_id = resp.data["id"]
        if os.path.exists(tmp):
            os.remove(tmp)
        log.info("[X] 스레드 업로드 성공")
        return True
    except Exception as exc:
        log.error("[X] 업로드 실패: %s", exc)
        return False


# ── 디자인 요청 처리 ──────────────────────────────────────────────────────────
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
        rows = resp.data or []
        return rows[0] if rows else None
    except Exception as exc:
        log.warning("[request] 조회 실패 (랜덤 모드 계속): %s", exc)
        return None


def update_request_status(rid: str, status: str, design_id: Optional[str] = None) -> None:
    payload: Dict[str, Any] = {"status": status}
    if design_id:
        payload["linked_design_id"] = design_id
    get_supabase().table("design_requests").update(payload).eq("id", rid).execute()


# ── 핵심 생성 루프 ────────────────────────────────────────────────────────────
async def generate_single_design(
    browser: Browser,
    source_request: Optional[Dict[str, Any]] = None,
    max_attempts: int = 3,
) -> tuple[bool, Optional[str]]:
    """
    디자인 1개 생성.
    품질 점수(self_review.total) < MIN_QUALITY_SCORE 이면 최대 max_attempts회 재시도.
    """
    category = (
        source_request.get("category", "Landing Page")
        if source_request
        else random.choice(CATEGORIES)
    )
    style, structure = pick_style_structure()
    ref_brands = STYLE_REFERENCE_BRANDS.get(style, "")

    req_context = ""
    if source_request:
        req_context = (
            "\n━━━ USER REQUEST CONTEXT (highest priority) ━━━\n"
            f"  Title      : {source_request.get('title', '')}\n"
            f"  Details    : {source_request.get('description', '')}\n"
        )
        if source_request.get("target_audience"):
            req_context += f"  Audience   : {source_request['target_audience']}\n"
        if source_request.get("reference_notes"):
            req_context += f"  References : {source_request['reference_notes']}\n"

    design_prompt = build_design_prompt(category, structure, style, ref_brands, req_context)
    log.info("[brief] %s | %s | %s", category, structure, style)

    # 시도 순서: 기본 모델 → 폴백 모델들
    model_queue = [GEMINI_MODEL] + GEMINI_FALLBACK_MODELS
    current_model = model_queue[0]
    model_idx = 0

    for attempt in range(1, max_attempts + 1):
        log.info("[attempt %d/%d] Gemini 호출 중... (model=%s)", attempt, max_attempts, current_model)
        await rate_limiter.acquire()

        try:
            response = await asyncio.to_thread(
                get_gemini().models.generate_content,
                model=current_model,
                config={"response_mime_type": "application/json"},
                contents=[design_prompt],
            )
            raw = response.text.strip()
            # JSON 펜스 제거
            raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.IGNORECASE)
            raw = re.sub(r"\s*```$", "", raw)
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            log.warning("[attempt %d] JSON 파싱 실패: %s", attempt, exc)
            await asyncio.sleep(5)
            continue
        except Exception as exc:
            msg = str(exc)
            if "429" in msg or "quota" in msg.lower():
                log.error("[rate-limit] Gemini 할당량 초과")
                return False, None
            # 503 / 과부하 → 다음 폴백 모델로 전환
            if "503" in msg or "UNAVAILABLE" in msg or "high demand" in msg.lower():
                model_idx += 1
                if model_idx < len(model_queue):
                    current_model = model_queue[model_idx]
                    log.warning("[attempt %d] 503 과부하 — 폴백 모델로 전환: %s", attempt, current_model)
                    await asyncio.sleep(5)
                else:
                    log.error("[attempt %d] 모든 폴백 모델 소진 — 포기", attempt)
                    return False, None
            else:
                log.warning("[attempt %d] API 에러: %s", attempt, exc)
                await asyncio.sleep(5)
            continue

        # 품질 점수 확인
        review = payload.get("self_review", {})
        score = review.get("total", 0)
        if isinstance(score, str):
            try:
                score = int(score)
            except ValueError:
                score = 0
        log.info("[quality] 점수: %d/60 (기준: %d)", score, MIN_QUALITY_SCORE)
        if score < MIN_QUALITY_SCORE and attempt < max_attempts:
            log.warning("[quality] 기준 미달 — 재생성 (attempt %d)", attempt + 1)
            await asyncio.sleep(2)
            continue

        html_code = payload.get("html_code", "")
        react_code = payload.get("react_code", "")
        design_notes = review.get("design_notes", "")
        if not html_code.strip():
            log.warning("[attempt %d] html_code 없음 — 재시도", attempt)
            continue

        # 스크린샷
        wrapped = wrap_html_for_capture(html_code)
        try:
            screenshot = await capture_screenshot(browser, wrapped)
        except Exception as exc:
            log.error("[screenshot] 실패: %s", exc)
            return False, None

        # 이미지 업로드
        try:
            image_url = await asyncio.to_thread(upload_image, screenshot, category)
        except Exception as exc:
            log.error("[upload] 실패: %s", exc)
            return False, None

        # Slug / ID
        design_id = str(uuid.uuid4())
        slug = ensure_unique_slug(payload.get("title", "Untitled Design"))

        # colors 정규화
        raw_colors = payload.get("colors", [])
        if isinstance(raw_colors, dict):
            safe_colors = list(raw_colors.values())
        elif isinstance(raw_colors, list):
            safe_colors = [str(c) for c in raw_colors]
        else:
            safe_colors = [str(raw_colors)]

        # SNS 스레드 생성 (별도 API 호출)
        tweets: list[str] = []
        try:
            await rate_limiter.acquire()
            sns_prompt = build_sns_thread_prompt(
                payload.get("title", "Untitled"), category, style, slug, design_notes
            )
            sns_resp = await asyncio.to_thread(
                get_gemini().models.generate_content,
                model=current_model,  # 디자인 생성에 성공한 모델 재사용
                config={"response_mime_type": "application/json"},
                contents=[sns_prompt],
            )
            tweets = json.loads(sns_resp.text).get("tweets", [])
        except Exception as exc:
            log.warning("[sns] 스레드 생성 실패 (건너뜀): %s", exc)

        # X 업로드
        await post_to_x_thread(payload.get("title", ""), screenshot, slug, tweets)

        # DB 저장 — 실제 designs 테이블 스키마에 맞는 컬럼만 사용
        record = {
            "id":           design_id,
            "title":        payload.get("title", "Untitled Design"),
            "description":  payload.get("description", ""),
            "image_url":    image_url,
            "category":     category,
            "code":         html_code,
            "prompt":       f"{structure}_{style}".lower().replace(" ", "_"),
            "colors":       safe_colors,
            "slug":         slug,
            "status":       "published",
            "created_at":   datetime.utcnow().isoformat(),
        }
        # 옵션 컬럼: 존재할 수도 있는 컬럼은 별도 시도
        optional_fields = {
            "quality_score": score,
            "design_notes":  design_notes,
            "usage_notes":   payload.get("usage", ""),
        }
        try:
            await asyncio.to_thread(
                get_supabase().table("designs").insert({**record, **optional_fields}).execute
            )
            log.info("[db] 전체 컬럼 저장 성공")
        except Exception as exc:
            log.warning("[db] 일부 컬럼 없음, 기본 컬럼만 저장: %s", exc)
            try:
                await asyncio.to_thread(
                    get_supabase().table("designs").insert(record).execute
                )
                log.info("[db] 기본 컬럼 저장 성공")
            except Exception as exc2:
                log.error("[db] 저장 실패: %s", exc2)
                return False, None

        log.info("[✓] 저장 완료: %s (score=%d, slug=%s)", payload.get("title"), score, slug)
        return True, design_id

    log.error("[fail] %d회 시도 모두 실패", max_attempts)
    return False, None


# ── 배치 실행 ─────────────────────────────────────────────────────────────────
async def run_batch(count: int, use_requests: bool = True) -> None:
    successes = 0
    log.info("[system] %d개 생성 시작 (use_requests=%s)", count, use_requests)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        for i in range(count):
            log.info("\n─── 작업 %d/%d ───", i + 1, count)
            source_request: Optional[Dict[str, Any]] = None

            if use_requests:
                source_request = fetch_pending_request()
                if source_request:
                    update_request_status(source_request["id"], "in_progress")

            ok, design_id = await generate_single_design(browser, source_request=source_request)
            if ok:
                successes += 1
                if source_request and design_id:
                    update_request_status(source_request["id"], "completed", design_id)
            elif source_request:
                update_request_status(source_request["id"], "pending")

            if i < count - 1:
                log.info("[wait] 다음 생성까지 15초 대기...")
                await asyncio.sleep(15)

        await browser.close()

    log.info("\n[결과] %d / %d 성공", successes, count)


# ── CLI ───────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="UI-Syntax Design Generator v4.1")
    parser.add_argument("--count",        type=int,  default=1,    help="생성 개수 (기본 1)")
    parser.add_argument("--no-requests",  action="store_true",     help="사용자 신청 무시, 랜덤 모드")
    parser.add_argument("--min-score",    type=int,  default=None, help="최소 품질 점수 override (0–60)")
    args = parser.parse_args()

    if args.min_score is not None:
        MIN_QUALITY_SCORE = args.min_score

    if not all([SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY]):
        log.error("필수 환경변수 누락: SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, GEMINI_API_KEY")
        raise SystemExit(1)

    asyncio.run(run_batch(args.count, use_requests=not args.no_requests))
