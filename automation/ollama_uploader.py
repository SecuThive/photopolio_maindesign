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
        self.used_combinations = set()  # 중복 방지용
        self.design_counter = {}  # 각 카테고리별 카운터

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
        """Ollama 실패 시 사용할 카테고리별 고품질 템플릿 (변형 포함)"""
        
        # 카테고리별 카운터 증가
        if category not in self.design_counter:
            self.design_counter[category] = 0
        
        variation = self.design_counter[category] % 5  # 5가지 변형
        self.design_counter[category] += 1
        
        templates = {
            "Landing Page": self._landing_page_template(description, variation),
            "Dashboard": self._dashboard_template(description, variation),
            "E-commerce": self._ecommerce_template(description, variation),
            "Portfolio": self._portfolio_template(description, variation),
            "Blog": self._blog_template(description, variation),
            "Components": self._component_template(description, variation),
        }
        
        return templates.get(category, self._default_template(category, description))
    
    def _landing_page_template(self, description: str, variation: int = 0) -> str:
        # 5가지 색상 스킴
        color_schemes = [
            {"primary": "#667eea", "secondary": "#764ba2"},  # Purple
            {"primary": "#f093fb", "secondary": "#f5576c"},  # Pink
            {"primary": "#4facfe", "secondary": "#00f2fe"},  # Blue
            {"primary": "#43e97b", "secondary": "#38f9d7"},  # Green
            {"primary": "#fa709a", "secondary": "#fee140"},  # Orange
        ]
        
        colors = color_schemes[variation % 5]
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Landing Page</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
        nav {{ display: flex; justify-content: space-between; align-items: center; padding: 20px 60px; position: fixed; width: 100%; background: rgba(255,255,255,0.95); backdrop-filter: blur(10px); z-index: 100; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .logo {{ font-size: 24px; font-weight: 700; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        nav ul {{ display: flex; list-style: none; gap: 40px; }}
        nav a {{ text-decoration: none; color: #333; font-weight: 500; transition: color 0.3s; }}
        nav a:hover {{ color: {colors['primary']}; }}
        .hero {{ padding: 150px 60px 100px; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); color: white; text-align: center; }}
        .hero h1 {{ font-size: 64px; font-weight: 800; margin-bottom: 20px; line-height: 1.2; }}
        .hero p {{ font-size: 22px; opacity: 0.95; margin-bottom: 40px; max-width: 700px; margin-left: auto; margin-right: auto; }}
        .cta-group {{ display: flex; gap: 20px; justify-content: center; }}
        .btn {{ padding: 16px 40px; border-radius: 8px; text-decoration: none; font-weight: 600; font-size: 18px; transition: transform 0.2s; cursor: pointer; border: none; }}
        .btn-primary {{ background: white; color: {colors['primary']}; }}
        .btn-secondary {{ background: transparent; color: white; border: 2px solid white; }}
        .btn:hover { transform: translateY(-2px); }
        .features { padding: 100px 60px; max-width: 1200px; margin: 0 auto; }
        .features h2 { text-align: center; font-size: 42px; margin-bottom: 60px; color: #1a1a1a; }
        .feature-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }
        .feature-card { padding: 40px; background: #f8f9fa; border-radius: 12px; transition: transform 0.3s; }
        .feature-card:hover { transform: translateY(-5px); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
        .feature-icon { width: 60px; height: 60px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; display: flex; align-items: center; justify-content: center; font-size: 30px; margin-bottom: 20px; }
        .feature-card h3 { font-size: 24px; margin-bottom: 12px; color: #1a1a1a; }
        .feature-card p { color: #666; line-height: 1.6; }
        .pricing { padding: 100px 60px; background: #f8f9fa; }
        .pricing h2 { text-align: center; font-size: 42px; margin-bottom: 60px; color: #1a1a1a; }
        .pricing-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; max-width: 1200px; margin: 0 auto; }
        .pricing-card { background: white; padding: 40px; border-radius: 12px; text-align: center; border: 2px solid #e0e0e0; transition: all 0.3s; }
        .pricing-card:hover { border-color: #667eea; transform: translateY(-5px); }
        .pricing-card.popular { border-color: #667eea; position: relative; }
        .popular-badge { position: absolute; top: -15px; left: 50%; transform: translateX(-50%); background: #667eea; color: white; padding: 6px 20px; border-radius: 20px; font-size: 12px; font-weight: 600; }
        .price { font-size: 48px; font-weight: 800; color: #1a1a1a; margin: 20px 0; }
        .price span { font-size: 20px; color: #666; }
        .pricing-card ul { list-style: none; margin: 30px 0; }
        .pricing-card li { padding: 12px 0; color: #666; border-bottom: 1px solid #f0f0f0; }
        footer { background: #1a1a1a; color: white; padding: 60px; text-align: center; }
    </style>
</head>
<body>
    <nav>
        <div class="logo">YourBrand</div>
        <ul>
            <li><a href="#features">Features</a></li>
            <li><a href="#pricing">Pricing</a></li>
            <li><a href="#about">About</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
    
    <section class="hero">
        <h1>Build Something Amazing</h1>
        <p>""" + description + """</p>
        <div class="cta-group">
            <a href="#" class="btn btn-primary">Get Started Free</a>
            <a href="#" class="btn btn-secondary">Watch Demo</a>
        </div>
    </section>
    
    <section class="features" id="features">
        <h2>Why Choose Us</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>Lightning Fast</h3>
                <p>Optimized performance that delivers results in milliseconds, not seconds.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3>Secure by Default</h3>
                <p>Enterprise-grade security with end-to-end encryption and compliance.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <h3>Beautiful Design</h3>
                <p>Stunning interfaces that users love, crafted with attention to detail.</p>
            </div>
        </div>
    </section>
    
    <section class="pricing" id="pricing">
        <h2>Simple, Transparent Pricing</h2>
        <div class="pricing-grid">
            <div class="pricing-card">
                <h3>Starter</h3>
                <div class="price">$9<span>/mo</span></div>
                <ul>
                    <li>Up to 10 projects</li>
                    <li>Basic analytics</li>
                    <li>Email support</li>
                    <li>1GB storage</li>
                </ul>
                <a href="#" class="btn btn-secondary">Start Free Trial</a>
            </div>
            <div class="pricing-card popular">
                <div class="popular-badge">POPULAR</div>
                <h3>Professional</h3>
                <div class="price">$29<span>/mo</span></div>
                <ul>
                    <li>Unlimited projects</li>
                    <li>Advanced analytics</li>
                    <li>Priority support</li>
                    <li>50GB storage</li>
                </ul>
                <a href="#" class="btn btn-primary">Get Started</a>
            </div>
            <div class="pricing-card">
                <h3>Enterprise</h3>
                <div class="price">$99<span>/mo</span></div>
                <ul>
                    <li>Everything in Pro</li>
                    <li>Custom integrations</li>
                    <li>Dedicated support</li>
                    <li>Unlimited storage</li>
                </ul>
                <a href="#" class="btn btn-secondary">Contact Sales</a>
            </div>
        </div>
    </section>
    
    <footer>
        <p>&copy; 2026 YourBrand. All rights reserved.</p>
    </footer>
</body>
</html>"""

    def _dashboard_template(self, description: str) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f7fa; }
        .layout { display: flex; height: 100vh; }
        .sidebar { width: 260px; background: #1a1d2e; color: white; padding: 30px 0; }
        .logo { padding: 0 30px 30px; font-size: 24px; font-weight: 700; border-bottom: 1px solid rgba(255,255,255,0.1); }
        .nav-item { padding: 15px 30px; cursor: pointer; transition: background 0.3s; display: flex; align-items: center; gap: 12px; }
        .nav-item:hover { background: rgba(255,255,255,0.1); }
        .nav-item.active { background: linear-gradient(90deg, #667eea 0%, #764ba2 100%); }
        .main { flex: 1; overflow-y: auto; }
        .header { background: white; padding: 25px 40px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .search { padding: 10px 20px; border: 1px solid #e0e0e0; border-radius: 8px; width: 300px; font-size: 14px; }
        .user-profile { display: flex; align-items: center; gap: 12px; }
        .avatar { width: 40px; height: 40px; border-radius: 50%; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .content { padding: 40px; }
        .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 40px; }
        .stat-card { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }
        .stat-value { font-size: 36px; font-weight: 700; color: #1a1a1a; margin: 10px 0; }
        .stat-label { color: #666; font-size: 14px; }
        .stat-change { color: #10b981; font-size: 14px; font-weight: 600; }
        .stat-change.negative { color: #ef4444; }
        .chart-container { background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 24px; }
        .chart-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }
        .chart-title { font-size: 20px; font-weight: 600; color: #1a1a1a; }
        .chart-bar { height: 250px; display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; padding: 20px 0; }
        .bar { flex: 1; background: linear-gradient(180deg, #667eea 0%, #764ba2 100%); border-radius: 8px 8px 0 0; position: relative; }
        .bar-label { position: absolute; bottom: -30px; width: 100%; text-align: center; font-size: 12px; color: #666; }
        .table-container { background: white; border-radius: 12px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); overflow: hidden; }
        table { width: 100%; border-collapse: collapse; }
        th { background: #f8f9fa; padding: 16px; text-align: left; font-weight: 600; color: #666; font-size: 13px; text-transform: uppercase; }
        td { padding: 16px; border-top: 1px solid #f0f0f0; }
        .status { padding: 6px 12px; border-radius: 20px; font-size: 12px; font-weight: 600; }
        .status.success { background: #d1fae5; color: #065f46; }
        .status.pending { background: #fef3c7; color: #92400e; }
    </style>
</head>
<body>
    <div class="layout">
        <div class="sidebar">
            <div class="logo">Dashboard</div>
            <div class="nav-item active">📊 Overview</div>
            <div class="nav-item">📈 Analytics</div>
            <div class="nav-item">👥 Customers</div>
            <div class="nav-item">💰 Revenue</div>
            <div class="nav-item">⚙️ Settings</div>
        </div>
        <div class="main">
            <div class="header">
                <input type="text" class="search" placeholder="Search...">
                <div class="user-profile">
                    <div class="avatar"></div>
                    <span style="font-weight: 600;">John Doe</span>
                </div>
            </div>
            <div class="content">
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-label">Total Revenue</div>
                        <div class="stat-value">$45,231</div>
                        <div class="stat-change">↑ 20.1%</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Active Users</div>
                        <div class="stat-value">2,543</div>
                        <div class="stat-change">↑ 12.5%</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Conversions</div>
                        <div class="stat-value">1,234</div>
                        <div class="stat-change negative">↓ 4.3%</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-label">Avg. Order</div>
                        <div class="stat-value">$89.50</div>
                        <div class="stat-change">↑ 8.2%</div>
                    </div>
                </div>
                
                <div class="chart-container">
                    <div class="chart-header">
                        <div class="chart-title">Revenue Overview</div>
                        <select style="padding: 8px 16px; border: 1px solid #e0e0e0; border-radius: 6px;">
                            <option>Last 7 days</option>
                        </select>
                    </div>
                    <div class="chart-bar">
                        <div class="bar" style="height: 60%;"><span class="bar-label">Mon</span></div>
                        <div class="bar" style="height: 75%;"><span class="bar-label">Tue</span></div>
                        <div class="bar" style="height: 50%;"><span class="bar-label">Wed</span></div>
                        <div class="bar" style="height: 90%;"><span class="bar-label">Thu</span></div>
                        <div class="bar" style="height: 70%;"><span class="bar-label">Fri</span></div>
                        <div class="bar" style="height: 85%;"><span class="bar-label">Sat</span></div>
                        <div class="bar" style="height: 100%;"><span class="bar-label">Sun</span></div>
                    </div>
                </div>
                
                <div class="table-container">
                    <table>
                        <thead>
                            <tr>
                                <th>Order ID</th>
                                <th>Customer</th>
                                <th>Amount</th>
                                <th>Status</th>
                                <th>Date</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>#ORD-001</td>
                                <td>Alice Johnson</td>
                                <td>$129.00</td>
                                <td><span class="status success">Completed</span></td>
                                <td>Jan 18, 2026</td>
                            </tr>
                            <tr>
                                <td>#ORD-002</td>
                                <td>Bob Smith</td>
                                <td>$89.50</td>
                                <td><span class="status pending">Pending</span></td>
                                <td>Jan 18, 2026</td>
                            </tr>
                            <tr>
                                <td>#ORD-003</td>
                                <td>Carol White</td>
                                <td>$199.00</td>
                                <td><span class="status success">Completed</span></td>
                                <td>Jan 17, 2026</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _ecommerce_template(self, description: str) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Page</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }
        nav { display: flex; justify-content: space-between; align-items: center; padding: 20px 60px; border-bottom: 1px solid #e0e0e0; }
        .logo { font-size: 24px; font-weight: 700; }
        .nav-links { display: flex; gap: 40px; list-style: none; }
        .nav-links a { text-decoration: none; color: #333; font-weight: 500; }
        .product-page { max-width: 1400px; margin: 60px auto; padding: 0 60px; display: grid; grid-template-columns: 1fr 1fr; gap: 80px; }
        .gallery { display: grid; gap: 20px; }
        .main-image { width: 100%; aspect-ratio: 1; background: #f5f5f5; border-radius: 12px; object-fit: cover; }
        .thumbnails { display: grid; grid-template-columns: repeat(4, 1fr); gap: 15px; }
        .thumbnail { aspect-ratio: 1; background: #f5f5f5; border-radius: 8px; cursor: pointer; border: 2px solid transparent; }
        .thumbnail.active { border-color: #000; }
        .product-info h1 { font-size: 36px; margin-bottom: 12px; }
        .rating { display: flex; gap: 8px; align-items: center; margin-bottom: 20px; color: #fbbf24; }
        .price { font-size: 32px; font-weight: 700; margin: 30px 0; }
        .description { color: #666; line-height: 1.8; margin-bottom: 30px; }
        .options { margin: 30px 0; }
        .option-group { margin: 25px 0; }
        .option-label { font-weight: 600; margin-bottom: 12px; display: block; }
        .size-options { display: flex; gap: 12px; }
        .size-btn { padding: 12px 24px; border: 2px solid #e0e0e0; border-radius: 8px; background: none; cursor: pointer; font-weight: 500; transition: all 0.2s; }
        .size-btn.active { border-color: #000; background: #000; color: white; }
        .quantity { display: flex; align-items: center; gap: 15px; }
        .qty-btn { width: 40px; height: 40px; border: 1px solid #e0e0e0; background: white; border-radius: 8px; cursor: pointer; font-size: 20px; }
        .qty-value { font-size: 18px; font-weight: 600; }
        .actions { display: flex; gap: 15px; margin-top: 40px; }
        .btn { padding: 18px 40px; border: none; border-radius: 8px; font-size: 16px; font-weight: 600; cursor: pointer; transition: all 0.2s; }
        .btn-primary { background: #000; color: white; flex: 1; }
        .btn-secondary { background: white; border: 2px solid #000; flex: 1; }
        .btn:hover { transform: translateY(-2px); }
        .features { display: grid; gap: 20px; margin-top: 40px; padding-top: 40px; border-top: 1px solid #e0e0e0; }
        .feature { display: flex; gap: 15px; align-items: start; }
        .feature-icon { font-size: 24px; }
    </style>
</head>
<body>
    <nav>
        <div class="logo">STORE</div>
        <ul class="nav-links">
            <li><a href="#">New</a></li>
            <li><a href="#">Men</a></li>
            <li><a href="#">Women</a></li>
            <li><a href="#">Sale</a></li>
        </ul>
        <div style="display: flex; gap: 20px;">
            <span>🔍</span>
            <span>❤️</span>
            <span>🛒</span>
        </div>
    </nav>
    
    <div class="product-page">
        <div class="gallery">
            <img src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='600' height='600'%3E%3Crect fill='%23f5f5f5' width='600' height='600'/%3E%3Ctext x='50%25' y='50%25' dominant-baseline='middle' text-anchor='middle' font-family='sans-serif' font-size='24' fill='%23999'%3EProduct Image%3C/text%3E%3C/svg%3E" class="main-image" alt="Product">
            <div class="thumbnails">
                <div class="thumbnail active"></div>
                <div class="thumbnail"></div>
                <div class="thumbnail"></div>
                <div class="thumbnail"></div>
            </div>
        </div>
        
        <div class="product-info">
            <h1>Premium Product Name</h1>
            <div class="rating">
                ⭐⭐⭐⭐⭐ <span style="color: #666;">(128 reviews)</span>
            </div>
            <div class="price">$129.00</div>
            <p class="description">""" + description + """</p>
            
            <div class="options">
                <div class="option-group">
                    <label class="option-label">Size</label>
                    <div class="size-options">
                        <button class="size-btn">XS</button>
                        <button class="size-btn active">S</button>
                        <button class="size-btn">M</button>
                        <button class="size-btn">L</button>
                        <button class="size-btn">XL</button>
                    </div>
                </div>
                
                <div class="option-group">
                    <label class="option-label">Quantity</label>
                    <div class="quantity">
                        <button class="qty-btn">-</button>
                        <span class="qty-value">1</span>
                        <button class="qty-btn">+</button>
                    </div>
                </div>
            </div>
            
            <div class="actions">
                <button class="btn btn-primary">Add to Cart</button>
                <button class="btn btn-secondary">Buy Now</button>
            </div>
            
            <div class="features">
                <div class="feature">
                    <span class="feature-icon">🚚</span>
                    <div>
                        <strong>Free Shipping</strong>
                        <p style="color: #666; font-size: 14px;">On orders over $50</p>
                    </div>
                </div>
                <div class="feature">
                    <span class="feature-icon">↩️</span>
                    <div>
                        <strong>Easy Returns</strong>
                        <p style="color: #666; font-size: 14px;">30-day return policy</p>
                    </div>
                </div>
                <div class="feature">
                    <span class="feature-icon">🔒</span>
                    <div>
                        <strong>Secure Payment</strong>
                        <p style="color: #666; font-size: 14px;">Your data is protected</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _portfolio_template(self, description: str) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Georgia', serif; background: #0a0a0a; color: white; }
        .hero { height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center; text-align: center; padding: 40px; }
        .hero h1 { font-size: 72px; font-weight: 300; letter-spacing: -2px; margin-bottom: 20px; }
        .hero p { font-size: 24px; opacity: 0.7; max-width: 600px; font-family: sans-serif; }
        .projects { padding: 100px 60px; max-width: 1400px; margin: 0 auto; }
        .section-title { font-size: 48px; margin-bottom: 60px; font-weight: 300; }
        .project-grid { display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; }
        .project-card { background: #1a1a1a; border-radius: 12px; overflow: hidden; transition: transform 0.3s; cursor: pointer; }
        .project-card:hover { transform: translateY(-10px); }
        .project-image { width: 100%; aspect-ratio: 16/10; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
        .project-info { padding: 30px; }
        .project-title { font-size: 28px; margin-bottom: 12px; }
        .project-desc { opacity: 0.7; line-height: 1.6; font-family: sans-serif; font-size: 16px; }
        .project-tags { display: flex; gap: 10px; margin-top: 20px; flex-wrap: wrap; }
        .tag { padding: 6px 16px; background: rgba(255,255,255,0.1); border-radius: 20px; font-size: 13px; font-family: sans-serif; }
        .about { padding: 100px 60px; max-width: 1000px; margin: 0 auto; }
        .about-content { display: grid; grid-template-columns: 1fr 2fr; gap: 60px; align-items: center; }
        .about-image { width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); border-radius: 12px; }
        .about-text h2 { font-size: 42px; margin-bottom: 24px; font-weight: 300; }
        .about-text p { opacity: 0.8; line-height: 1.8; font-family: sans-serif; margin-bottom: 30px; }
        .skills { display: flex; gap: 12px; flex-wrap: wrap; }
        .skill { padding: 10px 20px; background: rgba(255,255,255,0.05); border: 1px solid rgba(255,255,255,0.2); border-radius: 8px; font-family: sans-serif; }
        footer { padding: 60px; text-align: center; border-top: 1px solid rgba(255,255,255,0.1); }
    </style>
</head>
<body>
    <section class="hero">
        <h1>Creative Designer</h1>
        <p>""" + description + """</p>
    </section>
    
    <section class="projects">
        <h2 class="section-title">Selected Works</h2>
        <div class="project-grid">
            <div class="project-card">
                <div class="project-image"></div>
                <div class="project-info">
                    <h3 class="project-title">Brand Identity System</h3>
                    <p class="project-desc">Complete visual identity for a modern tech startup, including logo, colors, and guidelines.</p>
                    <div class="project-tags">
                        <span class="tag">Branding</span>
                        <span class="tag">Identity</span>
                        <span class="tag">UI/UX</span>
                    </div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-image" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);"></div>
                <div class="project-info">
                    <h3 class="project-title">E-commerce Platform</h3>
                    <p class="project-desc">Modern shopping experience with intuitive navigation and seamless checkout flow.</p>
                    <div class="project-tags">
                        <span class="tag">Web Design</span>
                        <span class="tag">E-commerce</span>
                        <span class="tag">Mobile</span>
                    </div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-image" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);"></div>
                <div class="project-info">
                    <h3 class="project-title">Mobile App Design</h3>
                    <p class="project-desc">Clean and minimalist interface for a fitness tracking application.</p>
                    <div class="project-tags">
                        <span class="tag">Mobile</span>
                        <span class="tag">App Design</span>
                        <span class="tag">iOS</span>
                    </div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-image" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);"></div>
                <div class="project-info">
                    <h3 class="project-title">Dashboard Interface</h3>
                    <p class="project-desc">Data visualization and analytics dashboard for enterprise clients.</p>
                    <div class="project-tags">
                        <span class="tag">Dashboard</span>
                        <span class="tag">Data Viz</span>
                        <span class="tag">Enterprise</span>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="about">
        <div class="about-content">
            <div class="about-image"></div>
            <div class="about-text">
                <h2>About Me</h2>
                <p>I'm a passionate designer with over 8 years of experience creating beautiful, functional digital experiences. I believe in the power of good design to solve problems and delight users.</p>
                <div class="skills">
                    <span class="skill">UI/UX Design</span>
                    <span class="skill">Branding</span>
                    <span class="skill">Prototyping</span>
                    <span class="skill">Figma</span>
                    <span class="skill">Adobe Suite</span>
                </div>
            </div>
        </div>
    </section>
    
    <footer>
        <p style="opacity: 0.7; font-family: sans-serif;">© 2026 Portfolio. All rights reserved.</p>
    </footer>
</body>
</html>"""

    def _blog_template(self, description: str) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: 'Georgia', serif; color: #1a1a1a; line-height: 1.8; }
        header { border-bottom: 1px solid #e0e0e0; padding: 30px 0; }
        .container { max-width: 800px; margin: 0 auto; padding: 0 40px; }
        .site-title { font-size: 32px; font-weight: 400; text-align: center; }
        nav { display: flex; justify-content: center; gap: 40px; margin-top: 20px; font-family: sans-serif; font-size: 14px; }
        nav a { text-decoration: none; color: #666; text-transform: uppercase; letter-spacing: 1px; }
        .featured { padding: 80px 0; border-bottom: 1px solid #e0e0e0; }
        .featured-image { width: 100%; height: 400px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); margin-bottom: 40px; border-radius: 8px; }
        .post-meta { font-family: sans-serif; font-size: 13px; color: #999; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 16px; }
        .post-title { font-size: 42px; font-weight: 400; margin-bottom: 20px; line-height: 1.3; }
        .post-excerpt { font-size: 18px; color: #666; margin-bottom: 30px; }
        .read-more { display: inline-block; padding: 12px 30px; background: #1a1a1a; color: white; text-decoration: none; font-family: sans-serif; font-size: 14px; letter-spacing: 1px; border-radius: 4px; }
        .posts-grid { padding: 80px 0; display: grid; gap: 60px; }
        .post-card { display: grid; grid-template-columns: 250px 1fr; gap: 40px; padding-bottom: 60px; border-bottom: 1px solid #e0e0e0; }
        .post-image { width: 100%; aspect-ratio: 4/3; background: #f5f5f5; border-radius: 8px; }
        .post-card h3 { font-size: 28px; font-weight: 400; margin-bottom: 12px; }
        .post-card p { color: #666; margin-bottom: 20px; }
        .categories { display: flex; gap: 12px; flex-wrap: wrap; margin-top: 16px; }
        .category { padding: 6px 16px; background: #f5f5f5; font-family: sans-serif; font-size: 12px; border-radius: 20px; text-decoration: none; color: #666; }
        footer { background: #1a1a1a; color: white; padding: 60px 0; margin-top: 80px; text-align: center; }
    </style>
</head>
<body>
    <header>
        <div class="container">
            <h1 class="site-title">The Design Blog</h1>
            <nav>
                <a href="#">Home</a>
                <a href="#">Design</a>
                <a href="#">Technology</a>
                <a href="#">About</a>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <article class="featured">
            <div class="featured-image"></div>
            <div class="post-meta">January 18, 2026 • 5 min read</div>
            <h2 class="post-title">The Future of Web Design in 2026</h2>
            <p class="post-excerpt">""" + description + """</p>
            <a href="#" class="read-more">Read Full Article</a>
        </article>
        
        <div class="posts-grid">
            <article class="post-card">
                <div class="post-image" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);"></div>
                <div>
                    <div class="post-meta">January 15, 2026 • 4 min read</div>
                    <h3>Minimalism in Modern Interface Design</h3>
                    <p>Exploring how less can be more when it comes to creating beautiful, functional user interfaces that users love.</p>
                    <div class="categories">
                        <a href="#" class="category">Design</a>
                        <a href="#" class="category">UI/UX</a>
                    </div>
                </div>
            </article>
            
            <article class="post-card">
                <div class="post-image" style="background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);"></div>
                <div>
                    <div class="post-meta">January 12, 2026 • 6 min read</div>
                    <h3>Typography Trends You Should Know</h3>
                    <p>A deep dive into the latest typography trends shaping digital design and how to implement them effectively.</p>
                    <div class="categories">
                        <a href="#" class="category">Typography</a>
                        <a href="#" class="category">Trends</a>
                    </div>
                </div>
            </article>
            
            <article class="post-card">
                <div class="post-image" style="background: linear-gradient(135deg, #fa709a 0%, #fee140 100%);"></div>
                <div>
                    <div class="post-meta">January 10, 2026 • 3 min read</div>
                    <h3>Color Psychology in Digital Products</h3>
                    <p>Understanding how colors affect user behavior and decision-making in digital interfaces.</p>
                    <div class="categories">
                        <a href="#" class="category">Design Theory</a>
                        <a href="#" class="category">Psychology</a>
                    </div>
                </div>
            </article>
        </div>
    </div>
    
    <footer>
        <div class="container">
            <p style="opacity: 0.8;">© 2026 The Design Blog. All rights reserved.</p>
        </div>
    </footer>
</body>
</html>"""

    def _component_template(self, description: str) -> str:
        return """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Component Showcase</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #f5f7fa; padding: 60px 40px; }
        .component { max-width: 1200px; margin: 0 auto; background: white; padding: 60px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
        .component-title { font-size: 32px; margin-bottom: 40px; text-align: center; }
        .hero { text-align: center; padding: 80px 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 12px; }
        .hero h1 { font-size: 56px; margin-bottom: 20px; }
        .hero p { font-size: 20px; opacity: 0.95; margin-bottom: 40px; }
        .hero-buttons { display: flex; gap: 20px; justify-content: center; }
        .btn { padding: 16px 40px; border-radius: 8px; text-decoration: none; font-weight: 600; cursor: pointer; border: none; font-size: 16px; }
        .btn-primary { background: white; color: #667eea; }
        .btn-secondary { background: transparent; color: white; border: 2px solid white; }
    </style>
</head>
<body>
    <div class="component">
        <h2 class="component-title">Component Preview</h2>
        <div class="hero">
            <h1>Beautiful Component</h1>
            <p>""" + description + """</p>
            <div class="hero-buttons">
                <button class="btn btn-primary">Get Started</button>
                <button class="btn btn-secondary">Learn More</button>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _default_template(self, category: str, description: str) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; display: flex; align-items: center; justify-content: center; padding: 40px; }}
        .container {{ max-width: 800px; background: white; border-radius: 16px; padding: 60px; box-shadow: 0 20px 60px rgba(0,0,0,0.3); text-align: center; }}
        h1 {{ font-size: 48px; margin-bottom: 20px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
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
            await generator.create_design(category, description)
            
            # 다음 생성 전 대기
            if i < args.count - 1:
                print("⏳ Waiting 3 seconds before next generation...\n")
                await asyncio.sleep(3)
                
        except Exception as e:
            print(f"\n❌ Failed to create design: {e}\n")
            continue


if __name__ == "__main__":
    asyncio.run(main())
