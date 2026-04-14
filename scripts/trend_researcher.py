#!/usr/bin/env python3
"""
UI Design Trend Researcher
웹에서 최신 UI/UX 트렌드를 자동 수집·분석하여 캐싱

Sources:
  - DuckDuckGo Lite (웹 디자인 트렌드 검색어 2개)
  - Codrops RSS       (최신 showcase & creative dev 제목)
  - Webdesigner Depot RSS (트렌드 분석 기사)
  - CSS-Tricks RSS    (CSS 기법 최신 동향)
  - Smashing Magazine RSS (UX/UI 아티클)

Cache: scripts/.trends_cache.json (기본 24시간 TTL)
"""

from __future__ import annotations

import asyncio
import json
import logging
import re
import time
import urllib.parse
from pathlib import Path
from typing import Dict, List, Optional

import httpx

log = logging.getLogger(__name__)

TRENDS_CACHE_FILE = Path(__file__).parent / ".trends_cache.json"
TRENDS_CACHE_TTL  = 24 * 3600   # 초 단위 (24시간)
FETCH_TIMEOUT     = 12          # 소스 페이지 fetch 타임아웃 (초)
OLLAMA_TIMEOUT    = 180         # Ollama 분석 타임아웃 (초)

_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

RSS_SOURCES: List[Dict] = [
    {"name": "Codrops",           "url": "https://tympanus.net/codrops/feed/"},
    {"name": "Webdesigner Depot", "url": "https://webdesignerdepot.com/feed/"},
    {"name": "CSS-Tricks",        "url": "https://css-tricks.com/feed/"},
    {"name": "Smashing Magazine", "url": "https://smashingmagazine.com/feed/"},
]

DDG_QUERIES: List[str] = [
    "web design trends 2025 2026 popular UI styles visual",
    "best website design examples awards aesthetic 2026",
]


# ── HTML → 텍스트 추출기 ──────────────────────────────────────────────────────

def _html_to_text(html: str, max_chars: int = 4000) -> str:
    """HTML → 가시 텍스트 (script/style/head 제거 후 태그 strip)"""
    # head 영역 제거
    html = re.sub(r"<head[^>]*>[\s\S]*?</head>", "", html, flags=re.IGNORECASE)
    # script / style 블록 제거
    html = re.sub(r"<(script|style|noscript|iframe)[^>]*>[\s\S]*?</\1>", "", html, flags=re.IGNORECASE)
    # HTML 엔티티 간단 치환
    html = html.replace("&nbsp;", " ").replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">")
    # 나머지 태그 제거
    text = re.sub(r"<[^>]+>", " ", html)
    # 공백 정리
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


# ── 네트워크 fetch ────────────────────────────────────────────────────────────

async def _fetch(
    url: str,
    post_data: Optional[bytes] = None,
    timeout: int = FETCH_TIMEOUT,
) -> str:
    """URL 내용 반환. 실패 시 빈 문자열."""
    try:
        extra: Dict = {}
        if post_data:
            extra["content"] = post_data
            extra["headers"] = {**_HEADERS, "Content-Type": "application/x-www-form-urlencoded"}
            method = "POST"
        else:
            extra["headers"] = _HEADERS
            method = "GET"

        async with httpx.AsyncClient(timeout=timeout, follow_redirects=True) as c:
            r = await c.request(method, url, **extra)
            r.raise_for_status()
            return r.text
    except Exception as exc:
        log.debug("[trend] fetch 실패 %s: %s", url[:60], exc)
        return ""


async def _fetch_rss_text(source: Dict) -> str:
    """RSS 피드 → 제목·설명 텍스트 (Ollama 분석용)"""
    html = await _fetch(source["url"])
    if not html:
        return ""

    # CDATA 포함 title/description 추출
    titles = re.findall(
        r"<title[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</title>",
        html, re.DOTALL | re.IGNORECASE,
    )
    descs = re.findall(
        r"<description[^>]*>(?:<!\[CDATA\[)?(.*?)(?:\]\]>)?</description>",
        html, re.DOTALL | re.IGNORECASE,
    )

    lines: list[str] = []
    for i, t in enumerate(titles[1:9]):   # 채널 제목(첫 번째) 제외
        clean_t = re.sub(r"<[^>]+>|&[a-z#0-9]+;", "", t).strip()
        if clean_t:
            lines.append(f"• {clean_t}")
        if i + 1 < len(descs):
            clean_d = re.sub(r"<[^>]+>|&[a-z#0-9]+;", "", descs[i + 1]).strip()
            if clean_d:
                lines.append(f"  {clean_d[:220]}")

    return "\n".join(lines[:24])


async def _search_ddg(query: str) -> str:
    """DuckDuckGo Lite POST 검색 → 스니펫 텍스트"""
    data = urllib.parse.urlencode({"q": query}).encode()
    html = await _fetch("https://lite.duckduckgo.com/lite/", post_data=data)
    if not html:
        return ""
    text = _html_to_text(html, max_chars=8000)
    # DDG Lite 구조: 검색결과는 "Past Year" 이후 또는 "1." 번호 목록으로 시작
    # 네비게이션(국가 드롭다운 + 기간 필터) 이후 부분만 추출
    cut = re.search(r"Past\s+Year\s*", text)
    if cut:
        text = text[cut.end():]
    # 남은 공백 정리
    text = re.sub(r"\s+", " ", text).strip()
    return text[:2800]


# ── Ollama 트렌드 분석 ─────────────────────────────────────────────────────────

_ANALYSIS_PROMPT = """\
You are a senior UI/UX design trend analyst with deep knowledge of Awwwards, Dribbble, and the broader web design community.

Analyze the following content collected from design news sites, RSS feeds, and web searches.
Extract CONCRETE, ACTIONABLE insights about what visual styles and UI techniques are popular RIGHT NOW in 2025-2026.

Content:
{text}

Return ONLY a valid JSON object with these exact keys (no markdown, no extra text):
{{
  "trending_styles": [
    "5 specific visual style names currently dominant — e.g. 'Neobrutalism with raw borders', 'Dark editorial with cinematic photography'"
  ],
  "trending_colors": [
    "3 specific color palette descriptions — e.g. 'Warm sand + terracotta + off-white', 'Pitch black + electric lime accents'"
  ],
  "trending_layouts": [
    "4 layout patterns being widely praised — e.g. 'Oversized headline bleeding off viewport', 'Sticky left panel + right scroll'"
  ],
  "trending_elements": [
    "4 specific CSS/HTML elements or techniques getting attention — e.g. 'Noise texture overlays via SVG filter', 'Variable font weight animation on scroll'"
  ],
  "trending_interactions": [
    "3 interaction patterns popular now — e.g. 'View Transitions API for page morphing', 'Scroll-triggered GSAP clip-path reveals'"
  ],
  "avoid_cliche": [
    "3 overused patterns to avoid in 2026 — e.g. 'Purple-to-blue gradient SaaS hero', 'Generic 3-column feature grid with icons'"
  ],
  "design_direction": "1-2 sentences summarizing the overall mood and what makes a design feel current right now"
}}"""


async def _analyze_with_ollama(
    combined_text: str,
    ollama_url: str,
    model: str,
) -> Dict:
    """Ollama로 트렌드 분석 → 구조화된 dict 반환"""
    prompt = _ANALYSIS_PROMPT.format(text=combined_text[:9000])
    try:
        async with httpx.AsyncClient(timeout=OLLAMA_TIMEOUT) as c:
            r = await c.post(
                f"{ollama_url.rstrip('/')}/api/chat",
                json={
                    "model":   model,
                    "messages": [{"role": "user", "content": prompt}],
                    "stream":   False,
                },
            )
            r.raise_for_status()
            raw_text: str = r.json()["message"]["content"]

        m = re.search(r"\{[\s\S]+\}", raw_text)
        if m:
            return json.loads(m.group(0))
        log.warning("[trend] Ollama 응답에서 JSON 못 찾음")
    except Exception as exc:
        log.warning("[trend] Ollama 분석 오류: %s", exc)
    return {}


# ── 공개 API ──────────────────────────────────────────────────────────────────

async def refresh_trends(ollama_url: str, model: str) -> Dict:
    """
    모든 소스에서 병렬 수집 → Ollama 분석 → .trends_cache.json 저장.
    반환값: 분석된 트렌드 dict (실패 시 빈 dict)
    """
    log.info("[trend] 트렌드 수집 시작 (소스 %d개)", len(RSS_SOURCES) + len(DDG_QUERIES))

    tasks = (
        [_search_ddg(q) for q in DDG_QUERIES]
        + [_fetch_rss_text(s) for s in RSS_SOURCES]
    )
    labels = (
        [f"Search: {q[:50]}" for q in DDG_QUERIES]
        + [s["name"] for s in RSS_SOURCES]
    )

    raw_results = await asyncio.gather(*tasks, return_exceptions=True)

    sections: list[str] = []
    for label, res in zip(labels, raw_results):
        if isinstance(res, str) and len(res) > 60:
            sections.append(f"\n--- {label} ---\n{res[:2500]}")
            log.info("[trend] ✓ %s (%d chars)", label, len(res))
        else:
            log.debug("[trend] 스킵 %s: %s", label, res if not isinstance(res, str) else "too short")

    if not sections:
        log.warning("[trend] 수집된 데이터 없음 — 트렌드 없이 진행")
        return {}

    combined = "\n".join(sections)
    log.info("[trend] Ollama 분석 중... (총 %d chars)", len(combined))

    trends = await _analyze_with_ollama(combined, ollama_url, model)
    if not trends:
        log.warning("[trend] 분석 실패 — 트렌드 없이 진행")
        return {}

    # 캐시 저장
    try:
        TRENDS_CACHE_FILE.write_text(
            json.dumps({"fetched_at": time.time(), "trends": trends}, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )
        log.info("[trend] 캐시 저장: %s", TRENDS_CACHE_FILE.name)
    except Exception as exc:
        log.warning("[trend] 캐시 저장 실패: %s", exc)

    return trends


def load_cached_trends() -> Optional[Dict]:
    """캐시 로드. TTL 초과 또는 파일 없으면 None."""
    try:
        data = json.loads(TRENDS_CACHE_FILE.read_text(encoding="utf-8"))
        age  = time.time() - data.get("fetched_at", 0)
        if age < TRENDS_CACHE_TTL:
            log.info("[trend] 캐시 사용 (%.1f시간 전 수집)", age / 3600)
            return data.get("trends") or {}
    except Exception:
        pass
    return None


async def get_trends(
    ollama_url: str,
    model: str,
    force_refresh: bool = False,
) -> Dict:
    """
    트렌드 반환 (캐시 우선, 만료 시 자동 갱신).
    실패해도 빈 dict 반환 → 생성 파이프라인은 중단 없이 계속.
    """
    if not force_refresh:
        cached = load_cached_trends()
        if cached is not None:
            return cached
    return await refresh_trends(ollama_url, model)


def format_trend_prompt_block(trends: Dict) -> str:
    """
    트렌드 dict → 프롬프트 주입용 텍스트 블록.
    trends가 비어 있으면 빈 문자열 반환.
    """
    if not trends:
        return ""

    lines: list[str] = []
    if ts := trends.get("trending_styles"):
        lines.append("Trending styles now: " + " | ".join(ts[:5]))
    if tc := trends.get("trending_colors"):
        lines.append("Popular color palettes: " + " | ".join(tc[:3]))
    if tl := trends.get("trending_layouts"):
        lines.append("Praised layouts: " + " | ".join(tl[:4]))
    if te := trends.get("trending_elements"):
        lines.append("Hot CSS/UI elements: " + " | ".join(te[:4]))
    if ti := trends.get("trending_interactions"):
        lines.append("Trending interactions: " + " | ".join(ti[:3]))
    if ac := trends.get("avoid_cliche"):
        lines.append("Avoid (overused in 2026): " + " | ".join(ac[:3]))
    if dd := trends.get("design_direction"):
        lines.append(f'Market direction: "{dd}"')

    if not lines:
        return ""

    header = "━━ CURRENT MARKET TRENDS (live data from design news & search) ━━"
    footer = ("→ Let these trends inform your choices — especially where the constraints above\n"
              "   leave room. Don't copy exactly; synthesize with your assigned style.\n"
              "→ Actively avoid the 'overused' patterns listed above.")
    return f"\n{header}\n" + "\n".join(lines) + f"\n{footer}\n"


# ── CLI (단독 실행 시 트렌드 갱신) ───────────────────────────────────────────
if __name__ == "__main__":
    import argparse

    logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

    ap = argparse.ArgumentParser(description="UI Design Trend Researcher")
    ap.add_argument("--ollama",  default="http://localhost:11434")
    ap.add_argument("--model",   default="gemma4:e4b")
    ap.add_argument("--force",   action="store_true", help="캐시 무시하고 강제 갱신")
    args = ap.parse_args()

    result = asyncio.run(get_trends(args.ollama, args.model, force_refresh=args.force))
    print("\n=== 트렌드 분석 결과 ===")
    print(json.dumps(result, indent=2, ensure_ascii=False))
    print("\n=== 프롬프트 블록 미리보기 ===")
    print(format_trend_prompt_block(result))
