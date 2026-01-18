"""
AI Design Gallery - Ollama Automated Upload Script (V2 - 중복 방지 + 다양한 디자인)

Ollama를 사용하여 웹 디자인 코드를 생성하고, 
스크린샷을 찍어서 Supabase에 자동 업로드합니다.

Features:
- 중복 체크: DB에서 기존 디자인 확인
- 다양한 변형: 같은 카테고리도 색상/레이아웃이 다름
- 5가지 색상 스킴 적용
"""

import os
import io
import base64
import tempfile
import asyncio
import hashlib
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
    ],
}

# 색상 스킴 (5가지)
COLOR_SCHEMES = [
    {"name": "Purple", "primary": "#667eea", "secondary": "#764ba2", "accent": "#8b5cf6"},
    {"name": "Pink", "primary": "#f093fb", "secondary": "#f5576c", "accent": "#ec4899"},
    {"name": "Blue", "primary": "#4facfe", "secondary": "#00f2fe", "accent": "#3b82f6"},
    {"name": "Green", "primary": "#43e97b", "secondary": "#38f9d7", "accent": "#10b981"},
    {"name": "Orange", "primary": "#fa709a", "secondary": "#fee140", "accent": "#f59e0b"},
]


class OllamaDesignGenerator:
    """Ollama를 사용한 디자인 생성 및 업로드 (V2 - 중복 방지)"""

    def __init__(self):
        self.supabase = supabase
        self.ollama_url = OLLAMA_API_URL
        self.design_counter = {}  # 각 카테고리별 카운터
        
    async def check_duplicate(self, category: str, description: str) -> bool:
        """DB에서 중복 체크"""
        try:
            response = self.supabase.table('designs').select('title, description').eq('category', category).execute()
            
            existing = response.data
            for design in existing:
                if design.get('description') == description:
                    print(f"⚠️  중복 발견: {description[:50]}...")
                    return True
            
            return False
        except Exception as e:
            print(f"⚠️  중복 체크 실패: {e}")
            return False

    def get_unique_title(self, category: str, description: str, variation: int) -> str:
        """고유한 제목 생성"""
        # 설명에서 키워드 추출
        keywords = description.split()[:3]
        title_base = ' '.join(keywords).title()
        
        color_name = COLOR_SCHEMES[variation % 5]["name"]
        
        return f"{category} - {title_base} ({color_name})"

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
                    "model": "llama3",
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.8,  # 더 다양한 결과
                    }
                },
                timeout=120
            )
            
            if response.status_code == 200:
                result = response.json()
                code = result.get('response', '')
                
                # HTML 코드 추출
                if '```html' in code:
                    code = code.split('```html')[1].split('```')[0]
                elif '```' in code:
                    code = code.split('```')[1].split('```')[0]
                
                code = code.strip()
                
                if not code.startswith('<!DOCTYPE') and not code.startswith('<html'):
                    code = self.get_fallback_template(category, description)
                
                print("✅ Code generated successfully")
                return code
            else:
                print(f"⚠️  Ollama API error, using fallback template")
                return self.get_fallback_template(category, description)
                
        except Exception as e:
            print(f"⚠️  Error calling Ollama: {e}, using fallback template")
            return self.get_fallback_template(category, description)

    def get_fallback_template(self, category: str, description: str) -> str:
        """카테고리별 고품질 템플릿 (변형 포함)"""
        
        # 카테고리별 카운터 증가
        if category not in self.design_counter:
            self.design_counter[category] = 0
        
        variation = self.design_counter[category] % 5  # 5가지 변형
        self.design_counter[category] += 1
        
        templates = {
            "Landing Page": self._landing_page_var(description, variation),
            "Dashboard": self._dashboard_var(description, variation),
            "E-commerce": self._ecommerce_var(description, variation),
            "Portfolio": self._portfolio_var(description, variation),
            "Blog": self._blog_var(description, variation),
            "Components": self._component_var(description, variation),
        }
        
        return templates.get(category, self._default_template(category, description, variation))

    def _landing_page_var(self, description: str, var: int) -> str:
        """Landing Page 변형 (5가지 색상)"""
        colors = COLOR_SCHEMES[var]
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, system-ui, sans-serif; }}
        nav {{ padding: 20px 60px; background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.05); display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 24px; font-weight: 800; color: {colors['primary']}; }}
        nav ul {{ display: flex; list-style: none; gap: 30px; }}
        nav a {{ text-decoration: none; color: #333; font-weight: 500; }}
        .hero {{ padding: 120px 60px; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); color: white; text-align: center; }}
        .hero h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 24px; }}
        .hero p {{ font-size: 20px; opacity: 0.9; max-width: 600px; margin: 0 auto 40px; }}
        .cta-btn {{ display: inline-block; padding: 16px 48px; background: white; color: {colors['primary']}; text-decoration: none; border-radius: 8px; font-weight: 700; font-size: 18px; }}
        .features {{ padding: 100px 60px; max-width: 1200px; margin: 0 auto; }}
        .features h2 {{ text-align: center; font-size: 40px; margin-bottom: 60px; }}
        .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }}
        .card {{ padding: 40px; background: #f9fafb; border-radius: 12px; text-align: center; }}
        .card h3 {{ font-size: 22px; margin: 20px 0 12px; color: {colors['primary']}; }}
        .card p {{ color: #666; line-height: 1.6; }}
        .icon {{ width: 60px; height: 60px; background: {colors['primary']}; border-radius: 12px; margin: 0 auto; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">Brand</div>
        <ul>
            <li><a href="#features">Features</a></li>
            <li><a href="#pricing">Pricing</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
    <div class="hero">
        <h1>Welcome to Innovation</h1>
        <p>{description}</p>
        <a href="#" class="cta-btn">Get Started</a>
    </div>
    <div class="features">
        <h2>Why Choose Us</h2>
        <div class="grid">
            <div class="card"><div class="icon"></div><h3>Fast</h3><p>Lightning-fast performance for your needs</p></div>
            <div class="card"><div class="icon"></div><h3>Secure</h3><p>Enterprise-grade security and privacy</p></div>
            <div class="card"><div class="icon"></div><h3>Reliable</h3><p>99.9% uptime guarantee</p></div>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_var(self, description: str, var: int) -> str:
        """Dashboard 변형"""
        colors = COLOR_SCHEMES[var]
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; background: #f5f7fa; }}
        .layout {{ display: flex; height: 100vh; }}
        .sidebar {{ width: 240px; background: {colors['primary']}; color: white; padding: 30px 0; }}
        .logo {{ padding: 0 24px 24px; font-size: 20px; font-weight: 700; }}
        .nav-item {{ padding: 12px 24px; cursor: pointer; }}
        .nav-item:hover {{ background: rgba(255,255,255,0.1); }}
        .main {{ flex: 1; padding: 40px; overflow-y: auto; }}
        .header {{ font-size: 28px; font-weight: 700; margin-bottom: 30px; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; margin-bottom: 30px; }}
        .stat {{ background: white; padding: 24px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }}
        .stat-value {{ font-size: 32px; font-weight: 800; color: {colors['primary']}; }}
        .stat-label {{ color: #666; font-size: 14px; margin-top: 8px; }}
        .chart {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.04); }}
        .chart-title {{ font-size: 18px; font-weight: 600; margin-bottom: 20px; }}
        .bars {{ display: flex; align-items: flex-end; gap: 12px; height: 200px; }}
        .bar {{ flex: 1; background: {colors['primary']}; border-radius: 4px 4px 0 0; }}
    </style>
</head>
<body>
    <div class="layout">
        <div class="sidebar">
            <div class="logo">Dashboard</div>
            <div class="nav-item">📊 Overview</div>
            <div class="nav-item">📈 Analytics</div>
            <div class="nav-item">👥 Users</div>
            <div class="nav-item">⚙️ Settings</div>
        </div>
        <div class="main">
            <div class="header">Analytics Overview</div>
            <div class="stats">
                <div class="stat"><div class="stat-value">12.5K</div><div class="stat-label">Total Users</div></div>
                <div class="stat"><div class="stat-value">$45K</div><div class="stat-label">Revenue</div></div>
                <div class="stat"><div class="stat-value">89%</div><div class="stat-label">Growth</div></div>
                <div class="stat"><div class="stat-value">234</div><div class="stat-label">Active Now</div></div>
            </div>
            <div class="chart">
                <div class="chart-title">Weekly Performance</div>
                <div class="bars">
                    <div class="bar" style="height: 60%;"></div>
                    <div class="bar" style="height: 80%;"></div>
                    <div class="bar" style="height: 50%;"></div>
                    <div class="bar" style="height: 90%;"></div>
                    <div class="bar" style="height: 70%;"></div>
                    <div class="bar" style="height: 95%;"></div>
                    <div class="bar" style="height: 85%;"></div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _ecommerce_var(self, description: str, var: int) -> str:
        """E-commerce 변형"""
        colors = COLOR_SCHEMES[var]
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; }}
        nav {{ padding: 20px 60px; border-bottom: 1px solid #e5e7eb; display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 24px; font-weight: 800; color: {colors['primary']}; }}
        .product {{ max-width: 1200px; margin: 60px auto; padding: 0 60px; display: grid; grid-template-columns: 1fr 1fr; gap: 60px; }}
        .gallery {{ background: #f9fafb; aspect-ratio: 1; border-radius: 12px; }}
        .info h1 {{ font-size: 36px; margin-bottom: 16px; }}
        .price {{ font-size: 32px; font-weight: 800; color: {colors['primary']}; margin: 20px 0; }}
        .description {{ color: #666; line-height: 1.8; margin-bottom: 30px; }}
        .buy-btn {{ display: block; width: 100%; padding: 18px; background: {colors['primary']}; color: white; border: none; border-radius: 8px; font-size: 18px; font-weight: 700; cursor: pointer; }}
        .features {{ margin-top: 30px; padding-top: 30px; border-top: 1px solid #e5e7eb; }}
        .feature {{ display: flex; gap: 12px; margin: 12px 0; color: #666; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">STORE</div>
        <div>🛒 Cart (0)</div>
    </nav>
    <div class="product">
        <div class="gallery"></div>
        <div class="info">
            <h1>Premium Product</h1>
            <div class="price">$129.00</div>
            <p class="description">{description}</p>
            <button class="buy-btn">Add to Cart</button>
            <div class="features">
                <div class="feature">✓ Free shipping</div>
                <div class="feature">✓ 30-day returns</div>
                <div class="feature">✓ Secure checkout</div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _portfolio_var(self, description: str, var: int) -> str:
        """Portfolio 변형"""
        colors = COLOR_SCHEMES[var]
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Georgia, serif; background: #0a0a0a; color: white; }}
        .hero {{ height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; }}
        .hero h1 {{ font-size: 64px; font-weight: 300; margin-bottom: 24px; }}
        .hero p {{ font-size: 20px; opacity: 0.8; max-width: 600px; }}
        .projects {{ padding: 100px 60px; max-width: 1400px; margin: 0 auto; }}
        .projects h2 {{ font-size: 40px; font-weight: 300; margin-bottom: 60px; }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; }}
        .project {{ background: #1a1a1a; border-radius: 12px; overflow: hidden; }}
        .project-img {{ width: 100%; aspect-ratio: 16/10; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); }}
        .project-info {{ padding: 30px; }}
        .project h3 {{ font-size: 24px; margin-bottom: 12px; }}
        .project p {{ opacity: 0.7; line-height: 1.6; }}
        .tag {{ display: inline-block; padding: 6px 16px; background: rgba(255,255,255,0.1); border-radius: 20px; font-size: 12px; margin: 8px 4px 0 0; }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Creative Work</h1>
        <p>{description}</p>
    </div>
    <div class="projects">
        <h2>Selected Projects</h2>
        <div class="grid">
            <div class="project">
                <div class="project-img"></div>
                <div class="project-info">
                    <h3>Project Alpha</h3>
                    <p>A modern web application with beautiful design</p>
                    <span class="tag">Design</span><span class="tag">Development</span>
                </div>
            </div>
            <div class="project">
                <div class="project-img" style="background: linear-gradient(135deg, {colors['secondary']} 0%, {colors['accent']} 100%);"></div>
                <div class="project-info">
                    <h3>Project Beta</h3>
                    <p>Elegant solution for complex problems</p>
                    <span class="tag">UI/UX</span><span class="tag">Branding</span>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _blog_var(self, description: str, var: int) -> str:
        """Blog 변형"""
        colors = COLOR_SCHEMES[var]
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: Georgia, serif; }}
        header {{ border-bottom: 1px solid #e5e7eb; padding: 30px 0; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 0 40px; }}
        .site-title {{ text-align: center; font-size: 32px; font-weight: 400; }}
        .featured {{ padding: 80px 0; border-bottom: 1px solid #e5e7eb; }}
        .featured-img {{ width: 100%; height: 400px; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); border-radius: 8px; margin-bottom: 30px; }}
        .meta {{ font-family: sans-serif; font-size: 13px; color: #999; margin-bottom: 16px; }}
        h2 {{ font-size: 40px; font-weight: 400; margin-bottom: 20px; }}
        .excerpt {{ font-size: 18px; color: #666; margin-bottom: 24px; line-height: 1.8; }}
        .read-more {{ display: inline-block; padding: 12px 30px; background: {colors['primary']}; color: white; text-decoration: none; border-radius: 4px; }}
        .posts {{ padding: 60px 0; }}
        .post {{ padding: 40px 0; border-bottom: 1px solid #e5e7eb; }}
        .post h3 {{ font-size: 24px; font-weight: 400; margin-bottom: 12px; }}
        .post p {{ color: #666; line-height: 1.6; }}
    </style>
</head>
<body>
    <header>
        <div class="container">
            <div class="site-title">The Blog</div>
        </div>
    </header>
    <div class="container">
        <article class="featured">
            <div class="featured-img"></div>
            <div class="meta">January 18, 2026 • 5 min read</div>
            <h2>Featured Article</h2>
            <p class="excerpt">{description}</p>
            <a href="#" class="read-more">Read More</a>
        </article>
        <div class="posts">
            <article class="post">
                <div class="meta">January 15, 2026 • 3 min read</div>
                <h3>Recent Post Title</h3>
                <p>Exploring new trends in web design and development</p>
            </article>
            <article class="post">
                <div class="meta">January 12, 2026 • 4 min read</div>
                <h3>Another Great Article</h3>
                <p>Deep dive into modern CSS techniques</p>
            </article>
        </div>
    </div>
</body>
</html>"""

    def _component_var(self, description: str, var: int) -> str:
        """Component 변형"""
        colors = COLOR_SCHEMES[var]
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: system-ui, sans-serif; background: #f5f7fa; padding: 60px 40px; }}
        .component {{ max-width: 1000px; margin: 0 auto; background: white; padding: 60px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .hero {{ text-align: center; padding: 60px 40px; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); color: white; border-radius: 12px; }}
        .hero h1 {{ font-size: 48px; margin-bottom: 20px; }}
        .hero p {{ font-size: 18px; opacity: 0.95; margin-bottom: 30px; }}
        .cta {{ display: inline-block; padding: 14px 36px; background: white; color: {colors['primary']}; text-decoration: none; border-radius: 8px; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="component">
        <div class="hero">
            <h1>Component Showcase</h1>
            <p>{description}</p>
            <a href="#" class="cta">Get Started</a>
        </div>
    </div>
</body>
</html>"""

    def _default_template(self, category: str, description: str, var: int) -> str:
        """기본 템플릿"""
        colors = COLOR_SCHEMES[var]
        
        return f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <style>
        body {{ font-family: system-ui, sans-serif; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 40px; }}
        .container {{ max-width: 700px; background: white; border-radius: 16px; padding: 60px; text-align: center; box-shadow: 0 20px 60px rgba(0,0,0,0.3); }}
        h1 {{ font-size: 42px; color: {colors['primary']}; margin-bottom: 20px; }}
        p {{ font-size: 18px; color: #666; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>{category}</h1>
        <p>{description}</p>
    </div>
</body>
</html>"""

    async def capture_screenshot(self, html_code: str) -> bytes:
        """HTML을 렌더링하여 스크린샷 캡처"""
        print("📸 Capturing screenshot...")
        
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page(viewport={'width': 1920, 'height': 1080})
            
            # HTML을 data URL로 로드
            await page.set_content(html_code, wait_until='networkidle')
            
            # 전체 페이지 스크린샷
            screenshot = await page.screenshot(full_page=True, type='png')
            
            await browser.close()
            
        print("✅ Screenshot captured")
        return screenshot

    async def upload_to_storage(self, screenshot: bytes, category: str) -> str:
        """Supabase Storage에 이미지 업로드"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{category.lower().replace(' ', '_').replace('-', '_')}.png"
        file_path = f"designs/{filename}"
        
        print(f"📤 Uploading to Supabase Storage: {filename}")
        
        try:
            # Upload file
            response = self.supabase.storage.from_('designs-bucket').upload(
                file_path,
                screenshot,
                {
                    'content-type': 'image/png',
                    'cache-control': '3600',
                }
            )
            
            # Get public URL
            public_url = self.supabase.storage.from_('designs-bucket').get_public_url(file_path)
            
            print(f"✅ Uploaded: {public_url}")
            return public_url
            
        except Exception as e:
            print(f"❌ Upload failed: {e}")
            raise

    async def save_to_database(self, title: str, description: str, image_url: str, category: str, prompt: str, code: str) -> Dict[str, Any]:
        """데이터베이스에 디자인 정보 저장"""
        print(f"💾 Saving to database: {title}")
        
        try:
            response = self.supabase.table('designs').insert({
                'title': title,
                'description': description,
                'image_url': image_url,
                'category': category,
                'prompt': prompt,
                'code': code,
            }).execute()
            
            print("✅ Saved successfully")
            return response.data[0]
            
        except Exception as e:
            print(f"❌ Database save failed: {e}")
            raise

    async def create_design(self, category: str, description: str) -> Dict[str, Any]:
        """디자인 생성 및 업로드 전체 프로세스"""
        print("=" * 60)
        print(f"🎨 Creating {category} design")
        print("=" * 60)
        print()
        
        # 중복 체크
        is_duplicate = await self.check_duplicate(category, description)
        if is_duplicate:
            print("⏭️  Skipping duplicate design\n")
            return None
        
        # 1. HTML 코드 생성
        html_code = self.generate_html_code(category, description)
        
        # 2. 스크린샷 캡처
        screenshot = await self.capture_screenshot(html_code)
        
        # 3. Storage에 업로드
        image_url = await self.upload_to_storage(screenshot, category)
        
        # 4. 고유한 제목 생성
        variation = self.design_counter.get(category, 0) - 1
        title = self.get_unique_title(category, description, variation)
        
        # 5. 데이터베이스에 저장
        result = await self.save_to_database(
            title=title,
            description=description,
            image_url=image_url,
            category=category,
            prompt=f"Category: {category}\nDescription: {description}",
            code=html_code
        )
        
        print(f"\n🎉 Design created successfully!")
        print(f"ID: {result['id']}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['image_url']}\n")
        
        return result


async def main():
    """메인 실행 함수 - 중복 없이 균등하게 분산"""
    import argparse
    import random
    
    parser = argparse.ArgumentParser(description="Generate designs with Ollama")
    parser.add_argument('--count', type=int, default=1, help='Number of designs to generate')
    parser.add_argument('--category', type=str, help='Specific category to generate')
    
    args = parser.parse_args()
    
    generator = OllamaDesignGenerator()
    
    # 중복 방지: 각 카테고리별로 사용할 설명 풀 생성
    category_descriptions = {}
    for cat, descs in DESIGN_CATEGORIES.items():
        category_descriptions[cat] = descs.copy()
        random.shuffle(category_descriptions[cat])
    
    # 카테고리를 순서대로 순환하며 균등 분산
    categories = list(DESIGN_CATEGORIES.keys())
    
    success_count = 0
    skip_count = 0
    
    for i in range(args.count):
        # 특정 카테고리 지정 또는 순환
        if args.category and args.category in DESIGN_CATEGORIES:
            category = args.category
        else:
            # 균등하게 분산
            category = categories[i % len(categories)]
        
        # 해당 카테고리에서 아직 사용하지 않은 설명 선택
        if not category_descriptions[category]:
            # 모든 설명을 사용했으면 다시 채우기
            category_descriptions[category] = DESIGN_CATEGORIES[category].copy()
            random.shuffle(category_descriptions[category])
        
        description = category_descriptions[category].pop(0)
        
        try:
            result = await generator.create_design(category, description)
            
            if result:
                success_count += 1
            else:
                skip_count += 1
            
            # 다음 생성 전 대기
            if i < args.count - 1:
                print("⏳ Waiting 2 seconds before next generation...\n")
                await asyncio.sleep(2)
                
        except Exception as e:
            print(f"\n❌ Failed to create design: {e}\n")
            continue
    
    print("\n" + "=" * 60)
    print(f"✅ 완료: {success_count}개 생성, {skip_count}개 중복 스킵")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
