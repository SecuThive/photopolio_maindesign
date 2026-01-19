"""Helpers for IndexNow pings triggered by automation scripts."""

from __future__ import annotations

import os
from typing import Iterable, List, Optional, Sequence
from urllib.parse import quote, urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

INDEXNOW_ENDPOINT = os.getenv("INDEXNOW_ENDPOINT", "https://indexnow.bing.com/indexnow")
SITE_BASE_URL = os.getenv("SITE_BASE_URL")
INDEXNOW_KEY = os.getenv("INDEXNOW_KEY")
INDEXNOW_KEY_LOCATION = os.getenv("INDEXNOW_KEY_LOCATION")


def _normalize_base_url(url: Optional[str]) -> Optional[str]:
    if not url:
        return None
    return url.rstrip("/")


def _chunk(sequence: Sequence[str], size: int) -> Iterable[List[str]]:
    for i in range(0, len(sequence), size):
        yield list(sequence[i : i + size])


BASE_URL = _normalize_base_url(SITE_BASE_URL)
HOST = urlparse(BASE_URL).netloc if BASE_URL else None


def indexnow_configured() -> bool:
    return all([INDEXNOW_KEY, INDEXNOW_KEY_LOCATION, BASE_URL, HOST])


def _submit_urls(urls: Sequence[str]) -> bool:
    if not indexnow_configured() or not urls:
        return False

    success = True
    for chunk in _chunk(urls, 10000):
        payload = {
            "host": HOST,
            "key": INDEXNOW_KEY,
            "keyLocation": INDEXNOW_KEY_LOCATION,
            "urlList": chunk,
        }
        try:
            response = requests.post(INDEXNOW_ENDPOINT, json=payload, timeout=10)
            response.raise_for_status()
            print(f"🔔 IndexNow notified for {len(chunk)} URL(s).")
        except Exception as exc:  # pragma: no cover - network errors should not crash the pipeline
            success = False
            print(f"⚠️ IndexNow ping failed: {exc}")
    return success


def _build_design_url(design_id: str) -> Optional[str]:
    if not BASE_URL or not design_id:
        return None
    return f"{BASE_URL}/?design={design_id}"


def _build_category_url(category: str) -> Optional[str]:
    if not BASE_URL or not category:
        return None
    return f"{BASE_URL}/?category={quote(category)}"


def notify_indexnow_for_design(
    design_id: str,
    category: Optional[str] = None,
    extra_urls: Optional[Sequence[str]] = None,
) -> bool:
    """Send IndexNow pings for a newly published design."""

    urls: List[str] = []

    if BASE_URL:
        urls.append(BASE_URL)

    design_url = _build_design_url(design_id)
    if design_url:
        urls.append(design_url)

    if category:
        category_url = _build_category_url(category)
        if category_url:
            urls.append(category_url)

    if extra_urls:
        urls.extend(extra_urls)

    deduped: List[str] = []
    seen = set()
    for url in urls:
        if url and url not in seen:
            deduped.append(url)
            seen.add(url)

    return _submit_urls(deduped)
