"""
AI Design Gallery - Ollama Automated Upload Script

Ollama를 사용하여 웹 디자인 코드를 생성하고, 
스크린샷을 찍어서 Supabase에 자동 업로드합니다.

Requirements:
- Ollama 설치 및 실행 (llama3 또는 codellama 모델)
- pip install -r requirements.txt
- playwright install chromium

Usage:
- 단일 실행: python automation/ollama_uploader.py
- 2개 생성: python automation/ollama_uploader.py --count 2
"""

import os
import io
import base64
import tempfile
import asyncio
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from supabase import create_client, Client
import requests
from playwright.async_api import async_playwright
from PIL import Image

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
OLLAMA_API_URL = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')

# Validate environment variables
if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

# Design templates
DESIGN_CATEGORIES = {
    "Landing Page": [
        "modern SaaS landing page with hero section, features grid, pricing table, and testimonials",
        "minimalist portfolio landing page with large typography, projects showcase, and contact form",
        "tech startup landing page with gradient background, product preview, and call-to-action",
        "creative agency landing page with bold colors, case studies grid, and team section",
        "app landing page with device mockups, feature highlights, and download buttons",
    ],
    "Dashboard": [
        "analytics dashboard with line charts, bar graphs, metrics cards, and data visualization",
        "admin panel with sidebar navigation, data tables, search filters, and modern UI components",
        "crypto trading dashboard with real-time charts, wallet balance, and transaction history",
        "e-commerce admin dashboard with sales graphs, order management, and inventory tracking",
        "project management dashboard with kanban board, task lists, and team members",
    ],
    "E-commerce": [
        "product detail page with image gallery, size selector, reviews, and add to cart button",
        "online store homepage with product grid, promotional banners, and category filters",
        "fashion e-commerce with elegant design, lookbook showcase, and wishlist feature",
        "electronics store with product comparison table, specifications, and ratings",
        "shopping cart page with item list, coupon input, and checkout summary",
    ],
    "Portfolio": [
        "developer portfolio with project showcase, tech stack, GitHub stats, and skills section",
        "photography portfolio with full-screen images, masonry gallery, and about section",
        "designer portfolio with case studies, project details, process explanation, and testimonials",
        "creative portfolio with interactive elements, animations, and contact form",
        "minimal portfolio with large images, simple navigation, and bio section",
    ],
    "Blog": [
        "modern blog homepage with featured articles, card layout, and sidebar",
        "minimalist blog with typography focus, reading time, and article tags",
        "tech blog with code snippets, syntax highlighting, dark theme, and table of contents",
        "personal blog with author profile, category filters, and popular posts section",
        "magazine-style blog with hero article, trending topics, and newsletter signup",
    ],
    "Components": [
        "hero section with background image, headline, subtitle, and CTA buttons",
        "pricing table with three tiers, feature comparison, and popular badge",
        "testimonials section with customer reviews, ratings, and profile images",
        "feature grid with icons, titles, descriptions in card layout",
        "contact form with input fields, textarea, submit button, and validation",
        "footer with logo, navigation links, social icons, and copyright",
    ],
}


class OllamaDesignGenerator:
    """Ollama를 사용한 디자인 생성 및 업로드"""

    def __init__(self):
        self.supabase = supabase
        self.ollama_url = OLLAMA_API_URL

    def generate_html_code(self, category: str, description: str) -> str:
        """Ollama를 사용하여 HTML/CSS 코드 생성"""
        
        prompt = f"""Create a complete, beautiful HTML page for: {description}

Requirements:
- Single HTML file with embedded CSS (no external files)
- Modern, clean design with professional styling
- Responsive layout
- Use modern CSS (flexbox, grid, gradients, shadows)
- Include realistic content (text, headings, sections)
- Color scheme: professional and elegant
- No JavaScript needed
- Complete and ready to render

Category: {category}

Provide ONLY the HTML code, no explanations:"""

        print(f"🤖 Generating code with Ollama...")
        
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={
                    "model": "llama3",  # or "codellama"
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                code = result.get('response', '')
                
                # HTML 코드 추출 (```html 등의 마크다운 제거)
                if '```html' in code:
                    code = code.split('```html')[1].split('```')[0]
                elif '```' in code:
                    code = code.split('```')[1].split('```')[0]
                
                code = code.strip()
                
                # HTML 태그가 없으면 기본 템플릿 사용
                if not code.startswith('<!DOCTYPE') and not code.startswith('<html'):
                    code = self.get_fallback_template(category, description)
                
                print("✅ Code generated successfully")
                return code
            else:
                print(f"⚠️ Ollama API error, using fallback template")
                return self.get_fallback_template(category, description)
                
        except Exception as e:
            print(f"⚠️ Error calling Ollama: {e}, using fallback template")
            return self.get_fallback_template(category, description)

    def get_fallback_template(self, category: str, description: str) -> str:
        """Ollama 실패 시 사용할 기본 템플릿"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 40px 20px;
        }}
        .container {{
            max-width: 1200px;
            background: white;
            border-radius: 20px;
            padding: 60px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }}
        h1 {{
            font-size: 48px;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 20px;
        }}
        p {{
            font-size: 20px;
            color: #666;
            line-height: 1.6;
            margin-bottom: 30px;
        }}
        .cta {{
            display: inline-block;
            padding: 16px 40px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            text-decoration: none;
            border-radius: 30px;
            font-weight: 600;
            font-size: 18px;
            transition: transform 0.3s;
        }}
        .cta:hover {{
            transform: translateY(-2px);
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{category}</h1>
        <p>{description}</p>
        <a href="#" class="cta">Get Started</a>
    </div>
</body>
</html>"""

    async def capture_screenshot(self, html_code: str) -> bytes:
        """HTML 코드를 렌더링하여 스크린샷 생성"""
        print("📸 Capturing screenshot...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': 1920, 'height': 1400})
            
            # HTML 설정
            await page.set_content(html_code)
            await page.wait_for_timeout(1000)  # 렌더링 대기
            
            # 스크린샷
            screenshot = await page.screenshot(full_page=True, type='png')
            
            await browser.close()
            
        print("✅ Screenshot captured")
        return screenshot

    def upload_to_storage(self, image_data: bytes, filename: str) -> str:
        """Supabase Storage에 이미지 업로드"""
        print(f"📤 Uploading to Supabase Storage: {filename}")
        
        try:
            file_path = f"designs/{filename}"
            
            response = self.supabase.storage.from_('designs-bucket').upload(
                file_path,
                image_data,
                file_options={"content-type": "image/png"}
            )
            
            public_url = self.supabase.storage.from_('designs-bucket').get_public_url(file_path)
            
            print(f"✅ Uploaded: {public_url}")
            return public_url
            
        except Exception as e:
            print(f"❌ Upload error: {e}")
            raise

    def save_to_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Supabase Database에 저장"""
        print(f"💾 Saving to database: {data['title']}")
        
        try:
            response = self.supabase.table('designs').insert(data).execute()
            print("✅ Saved successfully")
            return response.data[0]
            
        except Exception as e:
            print(f"❌ Database error: {e}")
            raise

    async def create_design(self, category: str, description: str) -> Dict[str, Any]:
        """전체 워크플로우: 코드 생성 → 스크린샷 → 업로드 → DB 저장"""
        
        print(f"\n{'='*60}")
        print(f"🎨 Creating {category} design")
        print(f"{'='*60}\n")
        
        # 1. HTML 코드 생성
        html_code = self.generate_html_code(category, description)
        
        # 2. 스크린샷 생성
        screenshot = await self.capture_screenshot(html_code)
        
        # 3. 파일명 생성
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{category.replace(' ', '_').lower()}.png"
        
        # 4. Supabase Storage 업로드
        image_url = self.upload_to_storage(screenshot, filename)
        
        # 5. 제목 생성
        title = f"{category} - {datetime.now().strftime('%B %d, %Y')}"
        
        # 6. Database 저장
        design_data = {
            "title": title,
            "description": description,
            "image_url": image_url,
            "category": category,
            "code": html_code,
            "prompt": f"Generated with Ollama: {description}",
        }
        
        result = self.save_to_database(design_data)
        
        print("\n🎉 Design created successfully!")
        print(f"ID: {result['id']}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['image_url']}\n")
        
        return result


async def main():
    """메인 실행 함수"""
    import argparse
    import random
    
    parser = argparse.ArgumentParser(description="Generate designs with Ollama")
    parser.add_argument('--count', type=int, default=1, help='Number of designs to generate')
    parser.add_argument('--category', type=str, help='Specific category to generate')
    
    args = parser.parse_args()
    
    generator = OllamaDesignGenerator()
    
    for i in range(args.count):
        # 카테고리 선택
        if args.category and args.category in DESIGN_CATEGORIES:
            category = args.category
        else:
            category = random.choice(list(DESIGN_CATEGORIES.keys()))
        
        # 설명 선택
        description = random.choice(DESIGN_CATEGORIES[category])
        
        try:
            await generator.create_design(category, description)
            
            # 다음 생성 전 대기
            if i < args.count - 1:
                print("⏳ Waiting 5 seconds before next generation...\n")
                await asyncio.sleep(5)
                
        except Exception as e:
            print(f"\n❌ Failed to create design: {e}\n")
            continue


if __name__ == "__main__":
    asyncio.run(main())
