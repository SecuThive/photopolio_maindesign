"""
AI Design Gallery - Ollama Upload Script

이 스크립트는 로컬 Ollama LLM을 사용해 HTML/CSS 디자인을 생성하고
Playwright로 스크린샷을 캡처해 Supabase에 업로드합니다.

Requirements:
- Ollama 실행 (예: `ollama serve`, `ollama pull llama3`)
- pip install -r automation/requirements.txt
- playwright install chromium

Usage:
- python automation/upload_design.py --category "Landing Page"
- python automation/upload_design.py --category "Landing Page" --orientation mobile
"""

import os
import argparse
import asyncio
import random
import hashlib
import re
from datetime import datetime
from typing import Optional, Dict, Any, Set

from dotenv import load_dotenv
from supabase import create_client, Client
import requests
from playwright.async_api import async_playwright

from indexnow_helper import notify_indexnow_for_design

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
OLLAMA_MODEL = os.getenv('OLLAMA_MODEL', 'llama3')

# Validate environment variables
if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Design templates for different categories
DESIGN_TEMPLATES = {
    "Landing Page": [
        "A modern, minimalist landing page for a SaaS product with hero section, features grid, and call-to-action",
        "Clean landing page design for a mobile app with gradient background and floating UI elements",
        "Professional landing page for a fintech startup with dark mode, glassmorphism effects",
    ],
    "Dashboard": [
        "Analytics dashboard with charts, metrics cards, and data visualization in a clean layout",
        "Admin dashboard with sidebar navigation, data tables, and modern UI components",
        "Project management dashboard with kanban boards and task tracking interface",
    ],
    "E-commerce": [
        "E-commerce product page with image gallery, product details, and shopping cart",
        "Online store homepage with product grid, categories, and promotional banners",
        "Fashion e-commerce website with elegant design and product showcase",
    ],
    "Portfolio": [
        "Creative portfolio website for a designer with project showcase and case studies",
        "Photography portfolio with full-screen images and minimalist navigation",
        "Developer portfolio with project cards and skills section",
    ],
    "Blog": [
        "Modern blog homepage with featured articles and card-based layout",
        "Minimalist blog design with typography focus and reading experience",
        "Tech blog with dark theme and code-friendly design",
    ],
}

AUTO_MOBILE_CATEGORIES = {"Landing Page", "Portfolio", "E-commerce", "Blog"}
MOBILE_ORIENTATION_RATIO = 0.4
DEFAULT_DESKTOP_VIEWPORT = {"width": 1440, "height": 900, "scale": 1.15}
DEFAULT_MOBILE_VIEWPORT = {"width": 414, "height": 896, "scale": 2.0}
MAX_STRUCTURE_ATTEMPTS = 5


class DesignUploader:
    """Generates HTML via Ollama, captures screenshots, and uploads the result."""

    def __init__(self):
        self.supabase = supabase
        self.ollama_url = OLLAMA_API_URL.rstrip('/')
        self.model = OLLAMA_MODEL
        self.structure_hashes: Set[str] = set()
        self._hydrate_structure_hashes()

    def _hydrate_structure_hashes(self) -> None:
        """Load existing design structure hashes from Supabase to prevent duplicates."""
        print("📦 Loading existing design structures...")
        start = 0
        batch_size = 500

        try:
            while True:
                response = (
                    self.supabase
                    .table('designs')
                    .select('id, code')
                    .range(start, start + batch_size - 1)
                    .execute()
                )

                rows = response.data or []
                for row in rows:
                    html = row.get('code') or ''
                    if not html:
                        continue
                    self.structure_hashes.add(self._structure_hash(html))

                if len(rows) < batch_size:
                    break
                start += batch_size

            print(f"✅ Loaded {len(self.structure_hashes)} existing structure hash(es)")
        except Exception as exc:
            print(f"⚠️ Unable to preload structure hashes: {exc}")
            self.structure_hashes.clear()

    def _structure_hash(self, html: str) -> str:
        """Return a layout-focused hash that ignores color differences."""
        sanitized = re.sub(r'#[0-9a-fA-F]{3,6}', 'COLOR', html or '')
        tags = ''.join(re.findall(r'<([a-zA-Z0-9-]+)', sanitized))
        layouts = ''.join(
            re.findall(r'grid-template-columns:[^;]+|flex-direction:[^;]+|display:\s*(?:grid|flex)', sanitized)
        )
        return hashlib.md5((tags + layouts).encode('utf-8')).hexdigest()

    def generate_html(self, category: str, prompt: str, orientation: str) -> str:
        """Generate HTML markup from Ollama for the given category and prompt."""
        orientation_hint = (
            "Design must be mobile-first portrait layout optimized for ~414px width screens, include touch-friendly spacing."
            if orientation == 'mobile'
            else "Design must target desktop widescreen layouts around 1440px width with multi-column sections."
        )

        ollama_prompt = f"""Create a complete HTML document for the following brief.

Category: {category}
Description: {prompt}
Orientation requirement: {orientation_hint}

Rules:
- Return a single HTML file with inline CSS inside <style> tags.
- Use modern, premium styling with gradients, grids, and professional typography.
- Include multiple sections relevant to the category.
- Ensure the layout is fully responsive and visually rich.
- Do not output markdown fences or explanations. Provide only raw HTML starting with <!DOCTYPE html>.
"""

        response = requests.post(
            f"{self.ollama_url}/api/generate",
            json={
                "model": self.model,
                "prompt": ollama_prompt,
                "stream": False,
                "options": {"temperature": 0.6},
            },
            timeout=180,
        )
        response.raise_for_status()
        data = response.json()
        code = data.get('response', '').strip()

        if '```' in code:
            code = code.split('```')[1].split('```')[0].strip()

        if not code.lower().startswith('<!doctype'):
            code = self._fallback_template(prompt, orientation)

        return code

    def _fallback_template(self, prompt: str, orientation: str) -> str:
        """Provide a minimal HTML fallback if Ollama response is invalid."""
        base_padding = '32px' if orientation == 'desktop' else '20px'
        heading_size = '72px' if orientation == 'desktop' else '42px'
        grid_columns = 'repeat(3, 1fr)' if orientation == 'desktop' else 'repeat(auto-fit, minmax(200px, 1fr))'

        return f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Generated Design</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fb; color: #0f172a; }}
        .hero {{ min-height: 80vh; display: flex; align-items: center; justify-content: center; text-align: center;
                 padding: {base_padding}; background: linear-gradient(135deg, #667eea, #764ba2); color: white; }}
        .hero h1 {{ font-size: {heading_size}; font-weight: 800; margin-bottom: 24px; }}
        .hero p {{ font-size: 20px; max-width: 640px; margin: 0 auto; opacity: 0.9; }}
        .grid {{ display: grid; grid-template-columns: {grid_columns}; gap: 24px; padding: {base_padding}; max-width: 1200px; margin: -60px auto 80px; }}
        .card {{ background: white; border-radius: 24px; padding: 32px; box-shadow: 0 20px 60px rgba(15, 23, 42, 0.08); }}
        .card h3 {{ font-size: 22px; margin-bottom: 12px; }}
        .card p {{ color: #475569; }}
    </style>
</head>
<body>
    <section class="hero">
        <div>
            <h1>Visionary Experiences</h1>
            <p>{prompt}</p>
        </div>
    </section>
    <section class="grid">
        <div class="card"><h3>Premium UI</h3><p>High-end interface for visionary brands.</p></div>
        <div class="card"><h3>Responsive</h3><p>Looks perfect on every device size.</p></div>
        <div class="card"><h3>Fast Setup</h3><p>Ready-to-use section library.</p></div>
    </section>
</body>
</html>'''

    def render_screenshot(self, html: str, orientation: str) -> bytes:
        """Render the HTML in Chromium via Playwright and capture a screenshot."""
        viewport = DEFAULT_MOBILE_VIEWPORT if orientation == 'mobile' else DEFAULT_DESKTOP_VIEWPORT
        return asyncio.run(self._render_async(html, viewport))

    async def _render_async(self, html: str, viewport: Dict[str, float]) -> bytes:
        async with async_playwright() as playwright:
            browser = await playwright.chromium.launch()
            page = await browser.new_page(
                viewport={"width": viewport['width'], "height": viewport['height']},
                device_scale_factor=viewport['scale'],
            )
            await page.set_content(html, wait_until='networkidle')
            await page.wait_for_timeout(600)
            screenshot = await page.screenshot(full_page=True, type='png')
            await browser.close()
            return screenshot

    def upload_to_storage(self, image_data: bytes, filename: str) -> str:
        file_path = f"designs/{filename}"
        self.supabase.storage.from_('designs-bucket').upload(
            file_path,
            image_data,
            file_options={"content-type": "image/png"},
        )
        return self.supabase.storage.from_('designs-bucket').get_public_url(file_path)

    def save_to_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        response = self.supabase.table('designs').insert(data).execute()
        return response.data[0]

    def create_design(
        self,
        category: str,
        custom_prompt: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
        orientation: str = 'auto',
    ) -> Dict[str, Any]:
        if custom_prompt:
            prompt = custom_prompt
        else:
            if category not in DESIGN_TEMPLATES:
                raise ValueError(f"Invalid category: {category}")
            prompt = random.choice(DESIGN_TEMPLATES[category])

        orientation = orientation.lower()
        if orientation not in {'desktop', 'mobile', 'auto'}:
            raise ValueError("orientation must be 'desktop', 'mobile', or 'auto'")

        if orientation == 'mobile':
            final_orientation = 'mobile'
        elif orientation == 'desktop':
            final_orientation = 'desktop'
        else:
            auto_pick = category in AUTO_MOBILE_CATEGORIES and random.random() < MOBILE_ORIENTATION_RATIO
            final_orientation = 'mobile' if auto_pick else 'desktop'

        print(f"📱 Orientation: {final_orientation}")

        html = None
        structure_hash = ''
        for attempt in range(1, MAX_STRUCTURE_ATTEMPTS + 1):
            candidate_html = self.generate_html(category, prompt, final_orientation)
            candidate_hash = self._structure_hash(candidate_html)

            if candidate_hash and candidate_hash not in self.structure_hashes:
                html = candidate_html
                structure_hash = candidate_hash
                self.structure_hashes.add(candidate_hash)
                break

            print(
                f"⚠️ Duplicate structure detected (attempt {attempt}/{MAX_STRUCTURE_ATTEMPTS}). Regenerating...",
            )

        if html is None:
            raise RuntimeError('Failed to generate a unique design structure after multiple attempts.')

        print(f"🔐 Structure hash: {structure_hash}")

        screenshot = self.render_screenshot(html, final_orientation)

        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}.png"
        image_url = self.upload_to_storage(screenshot, filename)

        design_data = {
            "title": title or f"{category} Design - {timestamp}",
            "description": description or f"AI-generated {category.lower()} design",
            "image_url": image_url,
            "category": category,
            "prompt": prompt,
            "code": html,
        }

        result = self.save_to_database(design_data)

        notify_indexnow_for_design(result.get('id'), category)
        print("\n🎉 Design created successfully!")
        print(f"ID: {result['id']}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['image_url']}")
        return result


def main():
    parser = argparse.ArgumentParser(description="Generate and upload AI design via Ollama")
    parser.add_argument(
        '--category',
        type=str,
        default='Landing Page',
        choices=list(DESIGN_TEMPLATES.keys()),
        help='Design category',
    )
    parser.add_argument('--prompt', type=str, help='Custom prompt for generation')
    parser.add_argument('--title', type=str, help='Custom title')
    parser.add_argument('--description', type=str, help='Custom description')
    parser.add_argument(
        '--orientation',
        type=str,
        choices=['auto', 'desktop', 'mobile'],
        default='auto',
        help='Orientation for the layout (auto mixes both)',
    )

    args = parser.parse_args()
    uploader = DesignUploader()

    try:
        uploader.create_design(
            category=args.category,
            custom_prompt=args.prompt,
            title=args.title,
            description=args.description,
            orientation=args.orientation,
        )
    except Exception as exc:
        print(f"\n❌ Failed to create design: {exc}")
        raise


if __name__ == "__main__":
    main()
