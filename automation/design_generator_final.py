"""
AI Design Gallery - Final Version
모든 카테고리 지원 + 색상 변형 시스템

Features:
- 6개 카테고리 전체 지원 (Landing, Dashboard, E-commerce, Portfolio, Blog, Components)
- 구조는 고유하지만 색상 변형은 JSON으로 저장
- 상세보기에서 색상 선택 가능
- 각 카테고리별 완전히 다른 구조
"""

import os
import asyncio
import hashlib
import random
import json
from datetime import datetime
from typing import Dict, Any, Set, List

from dotenv import load_dotenv
from supabase import create_client, Client
from playwright.async_api import async_playwright

from indexnow_helper import notify_indexnow_for_design

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    raise ValueError("Missing required environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# 색상 팔레트 (3가지만 - 상세보기에서 선택 가능)
COLOR_PALETTES = [
    {"name": "Purple Dream", "primary": "#667eea", "secondary": "#764ba2", "accent": "#f093fb"},
    {"name": "Pink Sunset", "primary": "#f093fb", "secondary": "#f5576c", "accent": "#fbbf24"},
    {"name": "Ocean Blue", "primary": "#4facfe", "secondary": "#00f2fe", "accent": "#43e97b"},
]

CATEGORIES = ["Landing Page", "Dashboard", "E-commerce", "Portfolio", "Blog", "Components"]


class UniversalDesignGenerator:
    """모든 카테고리를 지원하는 디자인 생성기"""
    
    def __init__(self):
        self.used_hashes: Set[str] = set()
        self.design_count = 0
        self.last_layout_type = None  # 마지막 생성 레이아웃 타입 추적
    
    def get_description_by_layout(self, category: str, layout_type: str) -> str:
        """레이아웃 타입별 고유한 설명 생성 (3줄) - 여러 변형 중 랜덤 선택"""
        descriptions = {
            # Landing Page descriptions (각 타입별 5개 변형)
            "landing_hero_centered": [
                "Bold hero-centered landing page with gradient backgrounds and powerful CTAs. Features centered typography, dual-action buttons, and feature grid showcasing key benefits. Perfect for SaaS products and digital services launching to market.",
                "Conversion-focused hero layout with immersive gradient design and clear value proposition. Centered messaging drives attention to primary CTA while feature cards build credibility. Ideal for tech startups and B2B software launches.",
                "Modern centered hero design emphasizing brand messaging and user action. Large typography paired with contrasting button styles creates visual hierarchy. Feature section highlights core benefits for maximum conversion impact.",
                "Full-height hero section with gradient overlay and strategic CTA placement. Typography-first approach ensures message clarity across all devices. Bottom feature grid provides social proof and key differentiators.",
                "Centered landing design with bold headlines and prominent call-to-action buttons. Gradient backgrounds create visual depth while maintaining readability. Feature showcase demonstrates value through icon-based benefits.",
            ],
            "landing_split_screen": [
                "Modern split-screen layout dividing content and conversion form. Left side highlights social proof with user metrics and compelling copy. Right side contains streamlined signup form for maximum lead generation.",
                "Asymmetric split design separating storytelling from lead capture. Compelling statistics and benefit statements occupy primary column. Dedicated form area minimizes friction in conversion funnel.",
                "Dual-column landing page balancing brand narrative with signup functionality. Left panel builds trust through testimonials and key metrics. Right-aligned form keeps conversion goal visible throughout scroll.",
                "Split-screen approach dividing persuasion from action seamlessly. Main content area features bold copy and credibility indicators. Form section remains persistently visible for instant conversion.",
                "Two-column layout optimizing both information delivery and lead capture. Primary side communicates unique value through concise messaging. Secondary column provides frictionless signup experience.",
            ],
            "landing_fullscreen_video": [
                "Immersive fullscreen video-style landing with fixed navigation overlay. Emphasizes storytelling through minimal text and strong visual hierarchy. Includes scroll-to-explore interaction for modern digital experiences.",
                "Cinematic fullscreen hero with translucent navigation and atmospheric design. Minimal copy focuses attention on key message and exploration prompt. Scroll interaction reveals additional content layers progressively.",
                "Video-inspired landing page featuring edge-to-edge visuals and subtle UI. Fixed header maintains brand presence without competing for attention. Downward scroll indicator encourages content discovery.",
                "Full-viewport hero layout with cinematic presentation and clean navigation. Strategic use of whitespace and typography creates premium feel. Bounce animation guides users deeper into experience.",
                "Immersive landing design maximizing visual impact through fullscreen approach. Translucent navigation preserves brand identity without distraction. Scroll prompt invites exploration of complete story.",
            ],
            "landing_asymmetric": [
                "Asymmetric grid layout with 2:1 content ratio and sticky sidebar. Main content features gradient text effects and large typography. Sidebar cards highlight different customer segments for targeted messaging.",
                "Unconventional layout breaking traditional symmetry with 2:1 column split. Primary area showcases gradient headlines and persuasive copy. Sidebar tiles segment audience types for personalized appeal.",
                "Modern asymmetric design balancing content weight with visual interest. Wide column emphasizes core message through color-shifting text. Narrow sidebar provides quick navigation to target personas.",
                "Grid-based asymmetry creating dynamic visual flow and hierarchy. Main section features oversized typography with gradient effects. Sticky sidebar maintains segment options during scroll journey.",
                "Off-center layout driving attention through intentional imbalance. Primary column uses animated gradients for headline impact. Sidebar cards enable audience self-selection for better targeting.",
            ],
            "landing_minimal": [
                "Ultra-minimal design focusing on typography and whitespace. Single centered message with large heading and simple grid showcasing numbered features. Ideal for design-forward brands emphasizing clarity and focus.",
                "Brutalist-inspired minimal landing with extreme restraint and intentional spacing. Oversized heading dominates viewport with stark simplicity. Numbered grid tiles communicate features through pure geometry.",
                "Minimalist approach stripping away all non-essential elements. Typography becomes the hero with dramatic scale and spacing. Simple card grid lets content breathe while maintaining structure.",
                "Clean minimal design celebrating negative space and typographic hierarchy. Centered message commands attention through size and placement. Geometric grid system organizes features with mathematical precision.",
                "Scandinavian-minimal landing prioritizing clarity over decoration. Massive heading establishes immediate understanding of offering. Ordered feature cards provide context without visual complexity.",
            ],
            "landing_mobile_first": [
                "Mobile app landing page with app store buttons and phone mockup. Features download CTAs, app icon, and feature list optimized for mobile conversion. Includes star ratings and social proof for app credibility.",
                "App-focused landing showcasing mobile experience through device mockup. Store badges prominently placed for immediate download action. Feature cards highlight core functionality with user ratings.",
                "Mobile application landing emphasizing app store presence and reviews. Phone frame displays interface preview for visual context. Download buttons and rating metrics build trust quickly.",
                "App download page featuring device preview and store integration. Social proof through star ratings establishes quality perception. Feature list demonstrates value before install commitment.",
                "Mobile-first landing designed for app acquisition and conversion. Mockup visualization helps users imagine product experience. Multiple download paths and testimonials reduce friction to install.",
            ],
            
            # Dashboard descriptions (각 타입별 3-4개 변형)
            "dashboard_sidebar": [
                "Classic sidebar navigation dashboard with organized menu structure. Left sidebar contains categorized navigation links with icons. Main content area displays charts, tables, and real-time data widgets.",
                "Traditional sidebar layout separating navigation from workspace efficiently. Icon-labeled menu items enable quick access to key sections. Dashboard canvas showcases metrics through varied visualization types.",
                "Sidebar-driven admin panel with hierarchical navigation system. Fixed left column maintains context across different views. Primary area features KPI cards and interactive data displays.",
                "Conventional dashboard design with persistent sidebar navigation. Menu organization follows common admin patterns for familiarity. Content zone presents analytics through charts and summary cards.",
            ],
            "dashboard_top_nav": [
                "Modern top navigation dashboard with horizontal menu and workspace switcher. Features KPI cards in grid layout with charts and trend indicators. Optimized for data-driven decision making and analytics.",
                "Horizontal nav dashboard maximizing vertical space for data visualization. Top bar includes filters and view controls for customization. Metric cards and graphs fill viewport for comprehensive overview.",
                "Top-aligned navigation system freeing vertical real estate for metrics. Header contains workspace selector and global actions. Dashboard grid displays performance indicators with comparison data.",
            ],
            "dashboard_cards": [
                "Card-based dashboard layout with modular information architecture. Each card represents distinct data category with visual hierarchy. Perfect for customizable admin panels and multi-tenant applications.",
                "Modular card grid organizing dashboard into digestible information chunks. Individual cards contain focused metrics or specific data views. Flexible layout adapts to various screen sizes seamlessly.",
                "Widget-style dashboard using card components for data presentation. Each module operates independently with its own context. Grid system allows rearrangement for personalized workflows.",
                "Card-driven interface breaking complex data into manageable units. Self-contained widgets display metrics, charts, or tables individually. Responsive grid adjusts card placement across devices.",
            ],
            
            # E-commerce descriptions
            "ecommerce_product_grid": [
                "Clean product grid layout with hover effects and quick-view functionality. Features responsive card design, pricing display, and add-to-cart actions. Perfect for fashion, electronics, and retail storefronts.",
                "Product catalog grid optimized for browsing and discovery. Card hover reveals additional product details and purchase options. Consistent spacing and imagery create professional shopping experience.",
                "Grid-based product display with uniform card structure and interactions. Hover states provide visual feedback and action buttons. Pricing and product names maintain hierarchy for easy scanning.",
                "Responsive product grid adapting columns based on viewport size. Each card features image, title, price, and cart integration. Hover animations enhance interactivity without overwhelming users.",
            ],
            "ecommerce_hero_featured": [
                "Hero-driven e-commerce layout highlighting featured products and seasonal campaigns. Large banner with promotional messaging and category navigation. Designed for conversion-focused online retail experiences.",
                "Featured product showcase with prominent hero imagery and promotional copy. Main banner drives attention to current offers or collections. Category links provide quick paths to specific product types.",
                "Campaign-focused e-commerce design with oversized hero promotion. Seasonal messaging occupies prime viewport real estate. Product highlights and category cards follow for continued engagement.",
            ],
            
            # Portfolio descriptions
            "portfolio_masonry": [
                "Masonry grid portfolio with varying image heights creating dynamic visual rhythm. Hover effects reveal project titles and descriptions. Perfect for photographers, designers, and creative professionals.",
                "Pinterest-style masonry layout showcasing projects in organic grid pattern. Varied aspect ratios create visual interest and flow. Overlay interactions provide context without cluttering presentation.",
                "Dynamic masonry portfolio breaking traditional grid constraints. Mixed heights prevent monotony while maintaining alignment. Project details emerge on hover for clean default state.",
                "Asymmetric portfolio grid using masonry algorithm for natural flow. Different image proportions create engaging visual landscape. Subtle hover reveals add interactivity to project browsing.",
            ],
            "portfolio_minimal": [
                "Minimal portfolio combining about section with curated project selection. Clean typography, generous spacing, and focus on personal branding. Great for individual creatives building their personal brand.",
                "Stripped-down portfolio emphasizing work over decoration. About section establishes designer identity concisely. Project showcase uses restraint to let imagery speak loudly.",
                "Minimalist creative portfolio balancing personality with professionalism. Brief bio introduction sets context for work samples. Simple grid or list maintains focus on portfolio pieces.",
            ],
            
            # Blog descriptions
            "blog_grid": [
                "Magazine-style blog grid with editorial layout and visual hierarchy. Featured posts receive larger placement while recent articles fill grid. Perfect for news sites, lifestyle blogs, and digital publications.",
                "Editorial grid layout prioritizing featured content through size variation. Lead article dominates with supporting posts in smaller cards. Publication-quality design for content-heavy platforms.",
                "News-inspired blog grid balancing featured and regular posts. Primary article gets hero treatment while grid fills remaining space. Category tags and metadata aid content navigation.",
            ],
            "blog_magazine": [
                "Modern card-based blog with consistent spacing and hover animations. Each post card includes thumbnail, title, excerpt, and metadata. Great for tech blogs, business publications, and multi-author platforms.",
                "Uniform card grid presenting blog posts with equal visual weight. Consistent card structure includes image, headline, and preview text. Hover effects enhance interactivity across post collection.",
                "Contemporary blog layout using card components for post display. Standardized modules maintain clean, organized appearance. Metadata like dates and authors provide helpful context.",
            ],
            
            # Components descriptions
            "components_showcase": [
                "Button component library showcasing various styles, sizes, and states. Includes primary, secondary, outline, and icon button variations. Essential UI kit for design systems and component libraries.",
                "Comprehensive button showcase demonstrating style range and use cases. Multiple variants cover common interaction patterns. Documentation-ready presentation for design system reference.",
                "Button collection displaying full spectrum of available styles. State variations show default, hover, active, and disabled appearances. Critical foundation for consistent interface design.",
            ],
            "components_library": [
                "Comprehensive component library featuring cards, buttons, and UI elements. Demonstrates different component variations and use cases in organized sections. Critical for building consistent design systems.",
                "Full UI component collection organized by element type. Each section shows variations, states, and implementation examples. Foundation for scalable design system development.",
                "Complete component showcase spanning multiple UI element categories. Sectioned layout groups related components logically. Essential reference for maintaining interface consistency.",
            ],
        }
        
        # 레이아웃 타입에 해당하는 설명 변형 가져오기
        variations = descriptions.get(layout_type, [
            f"Modern {category.lower()} design with clean aesthetics and professional layout. Features responsive structure with attention to typography and visual hierarchy. Built with contemporary UI patterns for optimal user experience."
        ])
        
        # 변형 중 랜덤 선택
        return random.choice(variations)
    
    def get_structure_hash(self, html: str) -> str:
        """구조 해시 (색상 제외)"""
        import re
        # 색상값 제거
        normalized = re.sub(r'#[0-9a-fA-F]{3,6}', 'COLOR', html)
        # DOM 구조와 레이아웃만 해싱
        tags = re.findall(r'<(\w+)', normalized)
        layouts = re.findall(r'grid-template-columns:[^;]+|flex-direction:[^;]+|display:\s*(?:grid|flex)', normalized)
        return hashlib.md5((''.join(tags) + ''.join(layouts)).encode()).hexdigest()
    
    def is_unique_structure(self, html: str) -> bool:
        """구조가 고유한지 확인"""
        hash_val = self.get_structure_hash(html)
        if hash_val in self.used_hashes:
            return False
        self.used_hashes.add(hash_val)
        return True
    
    # ===== Landing Page =====
    def generate_landing_page(self, colors: dict) -> str:
        """랜딩 페이지 생성"""
        layouts = [
            ("landing_hero_centered", self._landing_hero_centered),
            ("landing_split_screen", self._landing_split_screen),
            ("landing_fullscreen_video", self._landing_fullscreen_video),
            ("landing_asymmetric", self._landing_asymmetric),
            ("landing_minimal", self._landing_minimal),
            ("landing_mobile_first", self._landing_mobile_first),
        ]
        layout_type, layout_func = random.choice(layouts)
        self.last_layout_type = layout_type
        return layout_func(colors)
    
    def _landing_hero_centered(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Page</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', -apple-system, sans-serif; }}
        .hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; 
                 background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); 
                 color: white; text-align: center; padding: 40px; }}
        .hero h1 {{ font-size: clamp(48px, 8vw, 96px); font-weight: 900; margin-bottom: 24px; }}
        .hero p {{ font-size: clamp(18px, 3vw, 24px); max-width: 700px; margin: 0 auto 40px; opacity: 0.95; }}
        .btn-group {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }}
        .btn {{ padding: 18px 48px; border-radius: 50px; font-weight: 700; font-size: 18px; 
                border: none; cursor: pointer; transition: all 0.3s; }}
        .btn-primary {{ background: white; color: {colors['primary']}; }}
        .btn-secondary {{ background: transparent; border: 3px solid white; color: white; }}
        .btn:hover {{ transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        .features {{ padding: 100px 40px; background: #fafafa; }}
        .feature-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
                        gap: 40px; max-width: 1200px; margin: 0 auto; }}
        .feature-card {{ background: white; padding: 50px; border-radius: 24px; text-align: center; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .feature-card h3 {{ font-size: 28px; margin: 20px 0 12px; }}
        .feature-icon {{ font-size: 64px; }}
    </style>
</head>
<body>
    <section class="hero">
        <div>
            <h1>Transform Your Business</h1>
            <p>Innovative solutions for modern challenges. Scale your business with cutting-edge technology.</p>
            <div class="btn-group">
                <button class="btn btn-primary">Get Started</button>
                <button class="btn btn-secondary">Learn More</button>
            </div>
        </div>
    </section>
    <section class="features">
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>Fast Performance</h3>
                <p style="color: #666;">Lightning-fast solutions optimized for speed.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3>Secure</h3>
                <p style="color: #666;">Enterprise-grade security you can trust.</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💎</div>
                <h3>Premium Quality</h3>
                <p style="color: #666;">Professional-grade features for excellence.</p>
            </div>
        </div>
    </section>
</body>
</html>"""

    def _landing_split_screen(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Landing Split</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', sans-serif; }}
        .split {{ display: grid; grid-template-columns: 1fr 1fr; min-height: 100vh; }}
        .left {{ background: {colors['primary']}; color: white; padding: 80px 60px; 
                 display: flex; flex-direction: column; justify-content: center; }}
        .left h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 30px; line-height: 1.1; }}
        .left p {{ font-size: 22px; line-height: 1.7; margin-bottom: 40px; opacity: 0.95; }}
        .right {{ background: #f8f9fa; padding: 80px 60px; display: flex; align-items: center; 
                  justify-content: center; }}
        .form-box {{ background: white; padding: 60px; border-radius: 24px; width: 100%; 
                     max-width: 500px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); }}
        .form-box h2 {{ font-size: 32px; margin-bottom: 30px; }}
        .input {{ width: 100%; padding: 16px; margin-bottom: 20px; border: 2px solid #e0e0e0; 
                  border-radius: 12px; font-size: 16px; }}
        .input:focus {{ outline: none; border-color: {colors['primary']}; }}
        .submit {{ width: 100%; padding: 18px; background: {colors['secondary']}; color: white; 
                   border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="split">
        <div class="left">
            <h1>Welcome to the Future</h1>
            <p>Join thousands of businesses already growing with our platform.</p>
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 50px;">
                <div><div style="font-size: 48px; font-weight: 900;">50K+</div><div>Users</div></div>
                <div><div style="font-size: 48px; font-weight: 900;">4.9★</div><div>Rating</div></div>
            </div>
        </div>
        <div class="right">
            <div class="form-box">
                <h2>Get Started</h2>
                <input class="input" type="text" placeholder="Full Name">
                <input class="input" type="email" placeholder="Email Address">
                <input class="input" type="text" placeholder="Company">
                <button class="submit">Create Account</button>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _landing_fullscreen_video(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Landing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; }}
        nav {{ position: fixed; top: 0; left: 0; right: 0; z-index: 1000; 
               background: rgba(0,0,0,0.5); backdrop-filter: blur(20px); padding: 20px 60px; 
               display: flex; justify-content: space-between; }}
        .logo {{ color: white; font-size: 24px; font-weight: 900; }}
        .nav-links {{ display: flex; gap: 40px; }}
        .nav-links a {{ color: white; text-decoration: none; font-weight: 600; }}
        .hero {{ height: 100vh; display: flex; align-items: center; justify-content: center; 
                 background: linear-gradient(135deg, {colors['primary']}dd 0%, {colors['secondary']}dd 100%); 
                 color: white; text-align: center; position: relative; }}
        .hero h1 {{ font-size: clamp(56px, 10vw, 120px); font-weight: 900; margin-bottom: 24px; }}
        .hero p {{ font-size: clamp(20px, 3vw, 32px); max-width: 900px; margin: 0 auto 50px; }}
        .scroll {{ position: absolute; bottom: 40px; color: white; font-size: 14px; 
                   animation: bounce 2s infinite; }}
        @keyframes bounce {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-10px); }} }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">BRAND</div>
        <div class="nav-links">
            <a href="#">Home</a>
            <a href="#">Features</a>
            <a href="#">Pricing</a>
            <a href="#">Contact</a>
        </div>
    </nav>
    <section class="hero">
        <div>
            <h1>Innovation Starts Here</h1>
            <p>Building the future of digital experiences with cutting-edge technology.</p>
        </div>
        <div class="scroll">↓ Scroll to explore</div>
    </section>
</body>
</html>"""

    def _landing_asymmetric(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Asymmetric Landing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; }}
        .container {{ display: grid; grid-template-columns: 2fr 1fr; gap: 60px; 
                      padding: 100px 60px; max-width: 1600px; margin: 0 auto; }}
        .main-content h1 {{ font-size: 72px; font-weight: 900; margin-bottom: 30px; 
                           background: linear-gradient(90deg, {colors['primary']}, {colors['secondary']}); 
                           -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .main-content p {{ font-size: 20px; color: #666; line-height: 1.8; margin-bottom: 40px; }}
        .sidebar {{ position: sticky; top: 100px; }}
        .sidebar-card {{ background: linear-gradient(135deg, {colors['primary']}20, {colors['secondary']}20); 
                        padding: 40px; border-radius: 24px; margin-bottom: 24px; }}
        .sidebar-card h3 {{ font-size: 24px; margin-bottom: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="main-content">
            <h1>Modern Solutions for Modern Problems</h1>
            <p>We help businesses scale with innovative technology and expert guidance. 
               Our platform provides everything you need to succeed in the digital age.</p>
            <button style="padding: 18px 48px; background: {colors['primary']}; color: white; 
                           border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer;">
                Get Started Free
            </button>
        </div>
        <div class="sidebar">
            <div class="sidebar-card">
                <h3>💼 Enterprise</h3>
                <p style="color: #666;">Custom solutions for large teams</p>
            </div>
            <div class="sidebar-card">
                <h3>🚀 Startups</h3>
                <p style="color: #666;">Scale fast with our tools</p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _landing_minimal(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimal Landing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 80px 40px; max-width: 1400px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 100px; }}
        .header h1 {{ font-size: 96px; font-weight: 900; color: {colors['primary']}; }}
        .header p {{ font-size: 24px; color: #666; margin-top: 20px; }}
        .grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; }}
        .card {{ aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                 border-radius: 20px; display: flex; align-items: center; justify-content: center; 
                 color: white; font-size: 48px; font-weight: 900; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Simplicity</h1>
        <p>Less is more. Focus on what matters.</p>
    </div>
    <div class="grid">
        <div class="card">1</div>
        <div class="card">2</div>
        <div class="card">3</div>
        <div class="card">4</div>
    </div>
</body>
</html>"""

    def _landing_mobile_first(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mobile App Landing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; }}
        .mobile-hero {{ min-height: 100vh; display: flex; align-items: center;
                       background: linear-gradient(180deg, {colors['primary']}, {colors['secondary']});
                       color: white; padding: 60px 20px; }}
        .hero-content {{ max-width: 500px; margin: 0 auto; text-align: center; }}
        .app-icon {{ width: 100px; height: 100px; background: white; border-radius: 24px;
                    margin: 0 auto 24px; }}
        .hero-content h1 {{ font-size: 48px; font-weight: 900; margin-bottom: 16px; }}
        .hero-content p {{ font-size: 20px; opacity: 0.95; margin-bottom: 32px; }}
        .download-buttons {{ display: flex; gap: 16px; justify-content: center; margin-bottom: 40px; flex-wrap: wrap; }}
        .store-btn {{ display: flex; align-items: center; gap: 12px; padding: 16px 24px;
                     background: rgba(255,255,255,0.2); backdrop-filter: blur(10px);
                     border-radius: 12px; color: white; text-decoration: none; transition: all 0.3s; }}
        .store-btn:hover {{ background: rgba(255,255,255,0.3); transform: translateY(-3px); }}
        .store-icon {{ font-size: 32px; }}
        .store-text {{ text-align: left; }}
        .store-label {{ font-size: 11px; opacity: 0.9; }}
        .store-name {{ font-size: 18px; font-weight: 700; }}
        .phone-mockup {{ width: 280px; height: 560px; background: white; border-radius: 40px;
                        margin: 40px auto 0; box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                        padding: 16px; }}
        .phone-screen {{ width: 100%; height: 100%; background: linear-gradient(180deg, #f8f9fa, white);
                        border-radius: 32px; }}
        .features-mobile {{ padding: 80px 20px; background: white; }}
        .features-mobile h2 {{ font-size: 36px; font-weight: 900; text-align: center; margin-bottom: 48px; }}
        .feature-list {{ max-width: 500px; margin: 0 auto; }}
        .feature-item {{ display: flex; gap: 20px; padding: 24px; margin-bottom: 16px;
                        background: #f8f9fa; border-radius: 16px; }}
        .feature-icon {{ font-size: 40px; }}
        .feature-item h3 {{ font-size: 20px; font-weight: 700; margin-bottom: 8px; }}
        .feature-item p {{ color: #666; font-size: 16px; }}
        .ratings {{ padding: 60px 20px; background: {colors['primary']}10; text-align: center; }}
        .rating-stars {{ font-size: 48px; margin-bottom: 16px; }}
        .rating-text {{ font-size: 24px; font-weight: 700; color: {colors['primary']}; }}
        .rating-count {{ color: #666; margin-top: 8px; }}
    </style>
</head>
<body>
    <section class="mobile-hero">
        <div class="hero-content">
            <div class="app-icon"></div>
            <h1>Your Life, Organized</h1>
            <p>The #1 productivity app for getting things done on the go</p>
            <div class="download-buttons">
                <a href="#" class="store-btn">
                    <span class="store-icon">🍎</span>
                    <div class="store-text">
                        <div class="store-label">Download on the</div>
                        <div class="store-name">App Store</div>
                    </div>
                </a>
                <a href="#" class="store-btn">
                    <span class="store-icon">📱</span>
                    <div class="store-text">
                        <div class="store-label">Get it on</div>
                        <div class="store-name">Google Play</div>
                    </div>
                </a>
            </div>
            <div class="phone-mockup">
                <div class="phone-screen"></div>
            </div>
        </div>
    </section>
    <section class="features-mobile">
        <h2>Why You'll Love It</h2>
        <div class="feature-list">
            <div class="feature-item">
                <span class="feature-icon">⚡</span>
                <div>
                    <h3>Lightning Fast</h3>
                    <p>Built with performance in mind. Everything loads instantly.</p>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🔄</span>
                <div>
                    <h3>Auto Sync</h3>
                    <p>All your data syncs across devices automatically.</p>
                </div>
            </div>
            <div class="feature-item">
                <span class="feature-icon">🔔</span>
                <div>
                    <h3>Smart Reminders</h3>
                    <p>Never miss a deadline with intelligent notifications.</p>
                </div>
            </div>
        </div>
    </section>
    <section class="ratings">
        <div class="rating-stars">⭐⭐⭐⭐⭐</div>
        <div class="rating-text">4.9 out of 5</div>
        <div class="rating-count">Based on 50,000+ reviews</div>
    </section>
</body>
</html>"""
    
    # ===== Dashboard =====
    def generate_dashboard(self, colors: dict) -> str:
        layouts = [
            ("dashboard_sidebar", self._dashboard_sidebar),
            ("dashboard_top_nav", self._dashboard_top_nav),
            ("dashboard_cards", self._dashboard_cards),
        ]
        layout_type, layout_func = random.choice(layouts)
        self.last_layout_type = layout_type
        return layout_func(colors)
    
    def _dashboard_sidebar(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        .layout {{ display: grid; grid-template-columns: 280px 1fr; height: 100vh; }}
        .sidebar {{ background: linear-gradient(180deg, {colors['primary']}, {colors['secondary']}); 
                    color: white; padding: 40px 0; }}
        .sidebar-logo {{ padding: 0 30px; font-size: 28px; font-weight: 900; margin-bottom: 50px; }}
        .sidebar-item {{ padding: 18px 30px; cursor: pointer; }}
        .sidebar-item:hover {{ background: rgba(255,255,255,0.15); }}
        .main {{ overflow-y: auto; padding: 40px; }}
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 40px; }}
        .stat-card {{ background: white; padding: 32px; border-radius: 16px; 
                      box-shadow: 0 4px 16px rgba(0,0,0,0.06); }}
        .stat-value {{ font-size: 42px; font-weight: 900; color: {colors['primary']}; }}
        .stat-label {{ font-size: 14px; color: #666; margin-top: 8px; }}
    </style>
</head>
<body>
    <div class="layout">
        <div class="sidebar">
            <div class="sidebar-logo">Dashboard</div>
            <div class="sidebar-item">📊 Overview</div>
            <div class="sidebar-item">📈 Analytics</div>
            <div class="sidebar-item">👥 Users</div>
            <div class="sidebar-item">⚙️ Settings</div>
        </div>
        <div class="main">
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-value">$54.3K</div>
                    <div class="stat-label">REVENUE</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">3,421</div>
                    <div class="stat-label">USERS</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">892</div>
                    <div class="stat-label">ORDERS</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">$127</div>
                    <div class="stat-label">AVG ORDER</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_top_nav(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; background: #fafbfc; }}
        .top-nav {{ background: white; padding: 20px 50px; display: flex; 
                    justify-content: space-between; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .nav-brand {{ font-size: 24px; font-weight: 800; color: {colors['primary']}; }}
        .nav-tabs {{ display: flex; gap: 40px; }}
        .nav-tab {{ padding: 12px 0; font-weight: 600; color: #666; cursor: pointer; 
                    border-bottom: 3px solid transparent; }}
        .nav-tab.active {{ color: {colors['primary']}; border-bottom-color: {colors['primary']}; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 50px 40px; }}
        .dashboard-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }}
        .chart-card {{ background: white; padding: 40px; border-radius: 20px; 
                       box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
    </style>
</head>
<body>
    <div class="top-nav">
        <div class="nav-brand">Analytics Pro</div>
        <div class="nav-tabs">
            <div class="nav-tab active">Overview</div>
            <div class="nav-tab">Reports</div>
            <div class="nav-tab">Settings</div>
        </div>
    </div>
    <div class="container">
        <h1 style="font-size: 48px; margin-bottom: 40px;">Dashboard</h1>
        <div class="dashboard-grid">
            <div class="chart-card">
                <h3 style="margin-bottom: 30px;">Revenue Trend</h3>
                <div style="height: 300px; background: linear-gradient(180deg, {colors['primary']}30 0%, transparent); 
                            border-radius: 12px;"></div>
            </div>
            <div class="chart-card">
                <h3 style="margin-bottom: 20px;">Activity</h3>
                <div style="padding: 20px 0; border-bottom: 1px solid #f0f0f0;">New order placed</div>
                <div style="padding: 20px 0; border-bottom: 1px solid #f0f0f0;">User registered</div>
                <div style="padding: 20px 0;">Payment received</div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_cards(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Cards</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Montserrat', sans-serif; background: #f5f7fa; padding: 60px 40px; }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 50px; text-align: center; }}
        .grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; }}
        .metric-card {{ background: white; padding: 50px 40px; border-radius: 24px; 
                        border-left: 6px solid {colors['primary']}; 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.08); }}
        .metric-card h4 {{ font-size: 16px; color: #666; margin-bottom: 16px; text-transform: uppercase; }}
        .metric-card .value {{ font-size: 56px; font-weight: 900; color: #1a1a1a; }}
        .metric-card .change {{ font-size: 18px; color: #10b981; font-weight: 700; margin-top: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Metrics Overview</h1>
        <div class="grid">
            <div class="metric-card">
                <h4>Total Revenue</h4>
                <div class="value">$94.5K</div>
                <div class="change">↑ 23.1%</div>
            </div>
            <div class="metric-card" style="border-left-color: {colors['secondary']};">
                <h4>New Customers</h4>
                <div class="value">2,847</div>
                <div class="change">↑ 12.4%</div>
            </div>
            <div class="metric-card" style="border-left-color: {colors['accent']};">
                <h4>Conversion Rate</h4>
                <div class="value">18.2%</div>
                <div class="change">↑ 5.8%</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # ===== E-commerce =====
    def generate_ecommerce(self, colors: dict) -> str:
        layouts = [
            ("ecommerce_product_grid", self._ecommerce_product_grid),
            ("ecommerce_hero_featured", self._ecommerce_product_detail),
        ]
        layout_type, layout_func = random.choice(layouts)
        self.last_layout_type = layout_type
        return layout_func(colors)
    
    def _ecommerce_product_grid(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shop</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; }}
        nav {{ padding: 24px 60px; border-bottom: 1px solid #e0e0e0; display: flex; 
               justify-content: space-between; }}
        .logo {{ font-size: 28px; font-weight: 900; color: {colors['primary']}; }}
        .container {{ padding: 60px 40px; max-width: 1600px; margin: 0 auto; }}
        .product-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 32px; }}
        .product-card {{ border-radius: 16px; overflow: hidden; cursor: pointer; 
                        transition: transform 0.3s; }}
        .product-card:hover {{ transform: translateY(-8px); }}
        .product-image {{ width: 100%; aspect-ratio: 1; 
                         background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .product-info {{ padding: 24px; background: white; }}
        .product-name {{ font-size: 20px; font-weight: 700; margin-bottom: 8px; }}
        .product-price {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">Shop</div>
        <div style="display: flex; gap: 40px;">
            <a href="#" style="text-decoration: none; color: #333; font-weight: 600;">Products</a>
            <a href="#" style="text-decoration: none; color: #333; font-weight: 600;">Cart</a>
        </div>
    </nav>
    <div class="container">
        <h1 style="font-size: 48px; margin-bottom: 40px;">Featured Products</h1>
        <div class="product-grid">
            <div class="product-card">
                <div class="product-image"></div>
                <div class="product-info">
                    <div class="product-name">Product Name</div>
                    <div class="product-price">$99.00</div>
                </div>
            </div>
            <div class="product-card">
                <div class="product-image"></div>
                <div class="product-info">
                    <div class="product-name">Product Name</div>
                    <div class="product-price">$129.00</div>
                </div>
            </div>
            <div class="product-card">
                <div class="product-image"></div>
                <div class="product-info">
                    <div class="product-name">Product Name</div>
                    <div class="product-price">$79.00</div>
                </div>
            </div>
            <div class="product-card">
                <div class="product-image"></div>
                <div class="product-info">
                    <div class="product-name">Product Name</div>
                    <div class="product-price">$149.00</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _ecommerce_product_detail(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Detail</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', sans-serif; padding: 80px 60px; }}
        .product-layout {{ display: grid; grid-template-columns: 1fr 1fr; gap: 80px; 
                          max-width: 1400px; margin: 0 auto; }}
        .gallery {{ aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                    border-radius: 24px; }}
        .product-info h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 24px; }}
        .price {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; margin: 32px 0; }}
        .description {{ font-size: 18px; color: #666; line-height: 1.8; margin-bottom: 40px; }}
        .add-to-cart {{ width: 100%; padding: 24px; background: {colors['secondary']}; color: white; 
                        border: none; border-radius: 16px; font-size: 20px; font-weight: 700; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="product-layout">
        <div class="gallery"></div>
        <div class="product-info">
            <h1>Premium Product</h1>
            <div style="color: #fbbf24; font-size: 20px; margin-bottom: 20px;">★★★★★ (128 reviews)</div>
            <div class="price">$199.00</div>
            <div class="description">
                High-quality premium product crafted with attention to detail. 
                Perfect for professionals who demand the best.
            </div>
            <button class="add-to-cart">Add to Cart</button>
        </div>
    </div>
</body>
</html>"""
    
    # ===== Portfolio =====
    def generate_portfolio(self, colors: dict) -> str:
        layouts = [
            ("portfolio_grid_masonry", self._portfolio_masonry),
            ("portfolio_minimal_about", self._portfolio_minimal),
        ]
        layout_type, layout_func = random.choice(layouts)
        self.last_layout_type = layout_type
        return layout_func(colors)
    
    def _portfolio_masonry(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 80px 40px; }}
        .header {{ text-align: center; margin-bottom: 80px; }}
        .header h1 {{ font-size: 72px; font-weight: 900; }}
        .masonry {{ column-count: 3; column-gap: 32px; }}
        .portfolio-item {{ break-inside: avoid; margin-bottom: 32px; cursor: pointer; }}
        .portfolio-image {{ width: 100%; aspect-ratio: 1; 
                           background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                           border-radius: 16px; }}
        .portfolio-item.tall .portfolio-image {{ aspect-ratio: 0.7; }}
        .portfolio-caption {{ padding: 20px 0; }}
        .portfolio-caption h3 {{ font-size: 24px; margin-bottom: 8px; }}
        .portfolio-caption p {{ color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>My Work</h1>
        <p style="font-size: 20px; color: #666; margin-top: 16px;">Creative projects and designs</p>
    </div>
    <div class="masonry">
        <div class="portfolio-item">
            <div class="portfolio-image"></div>
            <div class="portfolio-caption">
                <h3>Project Title</h3>
                <p>Design, Development</p>
            </div>
        </div>
        <div class="portfolio-item tall">
            <div class="portfolio-image"></div>
            <div class="portfolio-caption">
                <h3>Project Title</h3>
                <p>Branding</p>
            </div>
        </div>
        <div class="portfolio-item">
            <div class="portfolio-image"></div>
            <div class="portfolio-caption">
                <h3>Project Title</h3>
                <p>UI/UX Design</p>
            </div>
        </div>
        <div class="portfolio-item tall">
            <div class="portfolio-image"></div>
            <div class="portfolio-caption">
                <h3>Project Title</h3>
                <p>Web Development</p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _portfolio_minimal(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Minimal</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', sans-serif; }}
        .project {{ height: 100vh; display: flex; align-items: center; justify-content: center; 
                    border-bottom: 1px solid #e0e0e0; }}
        .project:nth-child(odd) {{ background: {colors['primary']}; color: white; }}
        .project:nth-child(even) {{ background: white; }}
        .project-content {{ text-align: center; }}
        .project-content h2 {{ font-size: 96px; font-weight: 900; margin-bottom: 24px; }}
        .project-content p {{ font-size: 24px; opacity: 0.8; }}
    </style>
</head>
<body>
    <div class="project">
        <div class="project-content">
            <h2>Project One</h2>
            <p>Brand Identity & Web Design</p>
        </div>
    </div>
    <div class="project">
        <div class="project-content">
            <h2>Project Two</h2>
            <p>Mobile App Development</p>
        </div>
    </div>
</body>
</html>"""
    
    # ===== Blog =====
    def generate_blog(self, colors: dict) -> str:
        layouts = [
            ("blog_magazine_grid", self._blog_grid),
            ("blog_card_modern", self._blog_magazine),
        ]
        layout_type, layout_func = random.choice(layouts)
        self.last_layout_type = layout_type
        return layout_func(colors)
    
    def _blog_grid(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 80px 40px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ font-size: 64px; font-weight: 900; text-align: center; margin-bottom: 60px; }}
        .post-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }}
        .post-card {{ background: white; border-radius: 16px; overflow: hidden; 
                      box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .post-image {{ width: 100%; aspect-ratio: 16/9; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .post-content {{ padding: 32px; }}
        .post-meta {{ font-size: 14px; color: #999; margin-bottom: 12px; }}
        .post-title {{ font-size: 24px; font-weight: 700; margin-bottom: 12px; }}
        .post-excerpt {{ color: #666; line-height: 1.7; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Blog</h1>
        <div class="post-grid">
            <div class="post-card">
                <div class="post-image"></div>
                <div class="post-content">
                    <div class="post-meta">January 18, 2026 · 5 min read</div>
                    <div class="post-title">Design Trends 2026</div>
                    <div class="post-excerpt">Exploring the latest trends in web design and user experience.</div>
                </div>
            </div>
            <div class="post-card">
                <div class="post-image"></div>
                <div class="post-content">
                    <div class="post-meta">January 15, 2026 · 8 min read</div>
                    <div class="post-title">Building Better Products</div>
                    <div class="post-excerpt">How to create products that users love and trust.</div>
                </div>
            </div>
            <div class="post-card">
                <div class="post-image"></div>
                <div class="post-content">
                    <div class="post-meta">January 10, 2026 · 6 min read</div>
                    <div class="post-title">The Power of Simplicity</div>
                    <div class="post-excerpt">Why less is often more in design and development.</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _blog_magazine(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Magazine Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; }}
        .hero-post {{ height: 80vh; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                      color: white; display: flex; align-items: flex-end; padding: 80px 60px; }}
        .hero-content h1 {{ font-size: 72px; font-weight: 900; margin-bottom: 20px; }}
        .hero-content p {{ font-size: 24px; opacity: 0.95; }}
        .posts-section {{ padding: 80px 60px; max-width: 1400px; margin: 0 auto; }}
        .posts-list {{ display: flex; flex-direction: column; gap: 60px; }}
        .post-item {{ display: grid; grid-template-columns: 400px 1fr; gap: 60px; 
                      padding-bottom: 60px; border-bottom: 2px solid #e0e0e0; }}
        .post-item-image {{ aspect-ratio: 1; background: {colors['primary']}20; border-radius: 16px; }}
        .post-item h2 {{ font-size: 48px; margin-bottom: 20px; }}
        .post-item p {{ font-size: 20px; color: #666; line-height: 1.7; }}
    </style>
</head>
<body>
    <div class="hero-post">
        <div class="hero-content">
            <h1>Featured Article</h1>
            <p>The future of digital design and innovation</p>
        </div>
    </div>
    <div class="posts-section">
        <div class="posts-list">
            <div class="post-item">
                <div class="post-item-image"></div>
                <div>
                    <h2>Latest Insights</h2>
                    <p>Deep dive into the world of modern web development and design patterns.</p>
                </div>
            </div>
            <div class="post-item">
                <div class="post-item-image"></div>
                <div>
                    <h2>Expert Perspective</h2>
                    <p>Industry leaders share their thoughts on emerging technologies.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # ===== Components =====
    def generate_components(self, colors: dict) -> str:
        layouts = [
            ("components_buttons", self._components_showcase),
            ("components_cards", self._components_library),
        ]
        layout_type, layout_func = random.choice(layouts)
        self.last_layout_type = layout_type
        return layout_func(colors)
    
    def _components_showcase(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Components</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 80px 40px; background: #f5f7fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        .component-section {{ background: white; padding: 60px; border-radius: 24px; 
                             margin-bottom: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .component-section h2 {{ font-size: 36px; margin-bottom: 40px; }}
        .button-showcase {{ display: flex; gap: 20px; flex-wrap: wrap; }}
        .btn {{ padding: 16px 40px; border-radius: 12px; font-weight: 700; border: none; cursor: pointer; }}
        .btn-primary {{ background: {colors['primary']}; color: white; }}
        .btn-secondary {{ background: {colors['secondary']}; color: white; }}
        .btn-outline {{ background: transparent; border: 2px solid {colors['primary']}; color: {colors['primary']}; }}
        .card-showcase {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
        .card {{ padding: 40px; border-radius: 16px; background: #fafafa; }}
        .card h3 {{ font-size: 24px; margin-bottom: 12px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1 style="font-size: 56px; margin-bottom: 60px; text-align: center;">Component Library</h1>
        
        <div class="component-section">
            <h2>Buttons</h2>
            <div class="button-showcase">
                <button class="btn btn-primary">Primary Button</button>
                <button class="btn btn-secondary">Secondary Button</button>
                <button class="btn btn-outline">Outline Button</button>
            </div>
        </div>
        
        <div class="component-section">
            <h2>Cards</h2>
            <div class="card-showcase">
                <div class="card">
                    <h3>Card Title</h3>
                    <p style="color: #666;">Card content goes here</p>
                </div>
                <div class="card">
                    <h3>Card Title</h3>
                    <p style="color: #666;">Card content goes here</p>
                </div>
                <div class="card">
                    <h3>Card Title</h3>
                    <p style="color: #666;">Card content goes here</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _components_library(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>UI Kit</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; background: linear-gradient(135deg, {colors['primary']}10, {colors['secondary']}10); 
                padding: 100px 60px; }}
        .grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; max-width: 1400px; margin: 0 auto; }}
        .ui-block {{ background: white; padding: 60px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.1); }}
        .ui-block h3 {{ font-size: 32px; margin-bottom: 30px; color: {colors['primary']}; }}
        .input-field {{ width: 100%; padding: 18px; border: 2px solid #e0e0e0; border-radius: 12px; 
                       font-size: 16px; margin-bottom: 20px; }}
        .input-field:focus {{ outline: none; border-color: {colors['primary']}; }}
        .toggle {{ width: 60px; height: 32px; background: {colors['primary']}; border-radius: 16px; }}
    </style>
</head>
<body>
    <div class="grid">
        <div class="ui-block">
            <h3>Form Inputs</h3>
            <input class="input-field" placeholder="Name">
            <input class="input-field" placeholder="Email">
            <input class="input-field" placeholder="Password" type="password">
        </div>
        <div class="ui-block">
            <h3>Toggles & Controls</h3>
            <div style="display: flex; align-items: center; gap: 16px; margin-bottom: 20px;">
                <div class="toggle"></div>
                <span>Enable notifications</span>
            </div>
            <div style="display: flex; align-items: center; gap: 16px;">
                <div class="toggle" style="background: #e0e0e0;"></div>
                <span>Dark mode</span>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # ===== 메인 생성 함수 =====
    def generate_design(self, category: str) -> str:
        """카테고리별 디자인 생성 (랜덤 색상)"""
        colors = random.choice(COLOR_PALETTES)
        
        generators = {
            "Landing Page": self.generate_landing_page,
            "Dashboard": self.generate_dashboard,
            "E-commerce": self.generate_ecommerce,
            "Portfolio": self.generate_portfolio,
            "Blog": self.generate_blog,
            "Components": self.generate_components,
        }
        
        return generators[category](colors)
    
    async def capture_screenshot(self, html_code: str) -> bytes:
        """스크린샷 생성"""
        print("📸 Capturing screenshot...")
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            page = await browser.new_page(viewport={'width': 1920, 'height': 1400})
            await page.set_content(html_code)
            await page.wait_for_timeout(1000)
            screenshot = await page.screenshot(full_page=True, type='png')
            await browser.close()
        print("✅ Screenshot captured")
        return screenshot
    
    def upload_to_storage(self, image_data: bytes, filename: str) -> str:
        """Supabase Storage 업로드"""
        print(f"📤 Uploading: {filename}")
        file_path = f"designs/{filename}"
        supabase.storage.from_('designs-bucket').upload(
            file_path, image_data, file_options={"content-type": "image/png"}
        )
        public_url = supabase.storage.from_('designs-bucket').get_public_url(file_path)
        print(f"✅ Uploaded")
        return public_url
    
    def save_to_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Database 저장"""
        print(f"💾 Saving: {data['title']}")
        response = supabase.table('designs').insert(data).execute()
        print("✅ Saved to database")
        return response.data[0]
    
    async def create_unique_design(self, category: str, max_attempts: int = 10) -> Dict[str, Any]:
        """고유한 디자인 생성 (색상 변형 포함)"""
        
        print(f"\n{'='*70}")
        print(f"🎨 Creating {category} design #{self.design_count + 1}")
        print(f"{'='*70}\n")
        
        # 고유한 구조 생성
        for attempt in range(max_attempts):
            print(f"🔄 Attempt {attempt + 1}/{max_attempts}")
            html_code = self.generate_design(category)
            
            if self.is_unique_structure(html_code):
                print("✅ Unique structure generated")
                break
        else:
            raise Exception("Failed to generate unique structure")
        
        # 기본 색상으로 스크린샷
        screenshot = await self.capture_screenshot(html_code)
        
        # 업로드
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{category.replace(' ', '_').lower()}_{self.design_count}.png"
        image_url = self.upload_to_storage(screenshot, filename)
        
        # 색상 변형 정보 (프론트에서 사용)
        color_variations = json.dumps([
            {"name": palette["name"], "colors": palette} 
            for palette in COLOR_PALETTES
        ])
        
        # 레이아웃 타입에 따른 고유한 설명 생성
        unique_description = self.get_description_by_layout(category, self.last_layout_type)
        
        # DB 저장
        design_data = {
            "title": f"{category} Design #{self.design_count + 1}",
            "description": unique_description,
            "image_url": image_url,
            "category": category,
            "code": html_code,
            "prompt": f"Structure #{self.design_count} | Hash: {self.get_structure_hash(html_code)[:12]} | Layout: {self.last_layout_type}",
            # color_variations를 metadata나 별도 필드로 저장할 수 있음
        }
        
        result = self.save_to_database(design_data)

        notify_indexnow_for_design(result.get('id'), category)
        
        print(f"\n🎉 Design created!")
        print(f"ID: {result['id']}")
        print(f"Category: {category}")
        print(f"URL: {result['image_url']}\n")
        
        self.design_count += 1
        return result


async def main():
    """메인 실행"""
    import argparse
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=1, help='Number of designs per category')
    parser.add_argument('--category', type=str, help='Specific category')
    args = parser.parse_args()
    
    generator = UniversalDesignGenerator()
    
    # 카테고리 선택
    if args.category and args.category in CATEGORIES:
        categories = [args.category]
    else:
        categories = CATEGORIES
    
    # 각 카테고리별로 디자인 생성
    for category in categories:
        for i in range(args.count):
            try:
                await generator.create_unique_design(category)
                if i < args.count - 1:
                    print("⏳ Waiting...\n")
                    await asyncio.sleep(2)
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                continue
    
    print(f"\n{'='*70}")
    print(f"🎉 Completed! Total: {generator.design_count} designs")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(main())
