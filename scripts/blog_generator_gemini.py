#!/usr/bin/env python3
"""Gemini-based blog post generator for UI Syntax.

- Generates markdown posts for frontend and AI topics
- Writes directly to Supabase posts table

Required env vars:
- SUPABASE_URL
- SUPABASE_SERVICE_ROLE_KEY
- GEMINI_API_KEY
Optional:
- GEMINI_MODEL (default: gemini-2.5-flash)
"""

from __future__ import annotations

import argparse
import json
import os
import random
import re
import uuid
from datetime import datetime
from typing import Any, Dict, List

from dotenv import load_dotenv
from google import genai
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

if not all([SUPABASE_URL, SUPABASE_KEY, GEMINI_API_KEY]):
    raise RuntimeError("SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, GEMINI_API_KEY are required.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
gemini_client = genai.Client(api_key=GEMINI_API_KEY)

CATEGORIES = [
    "Frontend",
    "React",
    "Next.js",
    "Performance",
    "AI Engineering",
    "Developer Experience",
    "TypeScript",
]

AUTHOR_POOL = [
    {
        "name": "UI Syntax Studio",
        "role": "Product Engineering",
        "avatar": "https://images.unsplash.com/photo-1528892952291-009c663ce843?auto=format&fit=crop&w=200&q=80",
    },
    {
        "name": "UI Syntax Research",
        "role": "AI Systems",
        "avatar": "https://images.unsplash.com/photo-1545239351-1141bd82e8a6?auto=format&fit=crop&w=200&q=80",
    },
]

COVER_IMAGES = [
    "https://images.unsplash.com/photo-1483058712412-4245e9b90334?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1519389950473-47ba0277781c?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1553877522-43269d4ea984?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1520607162513-77705c0f0d4a?auto=format&fit=crop&w=1600&q=80",
    "https://images.unsplash.com/photo-1521737604893-d14cc237f11d?auto=format&fit=crop&w=1600&q=80",
]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "post"


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
    raise ValueError("Gemini did not return valid JSON.")


def ensure_payload_shape(payload: Dict[str, Any]) -> Dict[str, Any]:
    required = ["title", "excerpt", "content", "category", "tags"]
    missing = [key for key in required if key not in payload]
    if missing:
        raise ValueError(f"Missing fields: {', '.join(missing)}")

    title = str(payload["title"]).strip() or "Untitled Post"
    excerpt = str(payload["excerpt"]).strip()
    content = str(payload["content"]).strip()
    category = str(payload["category"]).strip() or "Frontend"
    tags_raw = payload.get("tags", [])
    tags = [str(tag).strip() for tag in tags_raw if isinstance(tag, str)]

    return {
        "title": title,
        "excerpt": excerpt,
        "content": content,
        "category": category,
        "tags": tags[:6],
    }


def ensure_unique_slug(base_title: str) -> str:
    base = slugify(base_title)
    candidate = base
    suffix = 2
    while True:
        response = supabase.table("posts").select("id").eq("slug", candidate).limit(1).execute()
        if not response.data:
            return candidate
        candidate = f"{base}-{suffix}"
        suffix += 1


def build_prompt(topic_hint: str | None, category: str) -> str:
    focus_line = f"Topic hint: {topic_hint}." if topic_hint else "Choose a timely frontend or AI engineering topic."
    return (
        "You are a senior engineer writing for a global audience. "
        "Write a premium, practical blog post for an IT audience in English. "
        f"{focus_line} "
        "Return valid JSON only with keys: "
        "title (string), excerpt (1-2 sentences), content (markdown), category (string), tags (array of 3-6 short strings). "
        "The markdown content must include: "
        "- A short intro paragraph\n"
        "- At least 3 H2 sections (use ## headings)\n"
        "- One fenced code block\n"
        "- One blockquote\n"
        "- A concise conclusion\n"
        "Use concrete, actionable advice and avoid hype."
    )


def generate_post(topic_hint: str | None) -> Dict[str, Any]:
    category = random.choice(CATEGORIES)
    prompt = build_prompt(topic_hint, category)
    response = gemini_client.models.generate_content(
        model=GEMINI_MODEL,
        config={"response_mime_type": "application/json"},
        contents=[{"role": "user", "parts": [{"text": prompt}]}],
    )
    payload = ensure_payload_shape(parse_gemini_json(response))
    author = random.choice(AUTHOR_POOL)
    cover_image_url = random.choice(COVER_IMAGES)

    return {
        "id": str(uuid.uuid4()),
        "slug": ensure_unique_slug(payload["title"]),
        "title": payload["title"],
        "excerpt": payload["excerpt"],
        "content": payload["content"],
        "category": payload["category"],
        "tags": payload["tags"],
        "author": author["name"],
        "author_role": author["role"],
        "author_avatar_url": author["avatar"],
        "cover_image_url": cover_image_url,
        "published_at": datetime.utcnow().isoformat(),
        "status": "published",
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": datetime.utcnow().isoformat(),
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate blog posts with Gemini")
    parser.add_argument("--count", type=int, default=1, help="Number of posts to generate")
    parser.add_argument("--topic", type=str, default=None, help="Optional topic hint")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    created = 0
    for _ in range(args.count):
        record = generate_post(args.topic)
        supabase.table("posts").insert(record).execute()
        created += 1
        print(f"[success] {record['title']}")
    print(f"Created {created} post(s).")


if __name__ == "__main__":
    main()
