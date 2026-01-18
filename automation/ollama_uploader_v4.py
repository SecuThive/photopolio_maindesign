"""
AI Design Gallery - Dynamic Structure Generator V4
매번 완전히 다른 구조를 동적으로 생성

Features:
- 무한한 레이아웃 조합 (랜덤 생성)
- 구조 요소를 동적으로 조합
- 강력한 중복 방지
- 각 디자인이 완전히 고유함
"""

import os
import asyncio
import hashlib
import random
from datetime import datetime
from typing import Dict, Any, Set, List

from dotenv import load_dotenv
from supabase import create_client, Client
from playwright.async_api import async_playwright

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    raise ValueError("Missing required environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# 레이아웃 구성 요소들
LAYOUT_TYPES = [
    "grid-2-col", "grid-3-col", "grid-4-col",
    "flex-row", "flex-column", 
    "masonry", "split-screen",
    "sidebar-left", "sidebar-right",
    "centered", "full-width",
    "asymmetric", "overlapping"
]

HERO_STYLES = [
    "centered-text", "split-content", "fullscreen-bg",
    "minimal", "bold-typography", "image-left",
    "image-right", "diagonal-split", "curved-bottom",
    "gradient-overlay", "pattern-bg", "video-bg"
]

CARD_STYLES = [
    "flat", "elevated", "bordered", "gradient",
    "glass", "neumorphic", "minimal", "bold-shadow",
    "rounded", "sharp", "tilted", "interactive"
]

NAVIGATION_STYLES = [
    "top-fixed", "top-transparent", "side-vertical",
    "center-minimal", "split-nav", "floating",
    "bottom-fixed", "hamburger-menu", "mega-menu"
]

SECTION_TYPES = [
    "features-grid", "testimonials", "pricing-table",
    "stats-counter", "timeline", "accordion",
    "tabs", "gallery", "team-members", "faq",
    "contact-form", "newsletter", "cta-banner",
    "process-steps", "logo-cloud", "blog-posts"
]

COLOR_PALETTES = [
    {"primary": "#667eea", "secondary": "#764ba2", "accent": "#f093fb", "bg": "#ffffff", "text": "#1a202c"},
    {"primary": "#f093fb", "secondary": "#f5576c", "accent": "#fbbf24", "bg": "#fafafa", "text": "#111827"},
    {"primary": "#4facfe", "secondary": "#00f2fe", "accent": "#43e97b", "bg": "#f0f9ff", "text": "#0c4a6e"},
    {"primary": "#43e97b", "secondary": "#38f9d7", "accent": "#667eea", "bg": "#ecfdf5", "text": "#064e3b"},
    {"primary": "#fa709a", "secondary": "#fee140", "accent": "#30cfd0", "bg": "#fff7ed", "text": "#7c2d12"},
    {"primary": "#30cfd0", "secondary": "#330867", "accent": "#f093fb", "bg": "#ecfeff", "text": "#164e63"},
    {"primary": "#a8edea", "secondary": "#fed6e3", "accent": "#fbbf24", "bg": "#f0fdfa", "text": "#134e4a"},
    {"primary": "#ff9a9e", "secondary": "#fecfef", "accent": "#c084fc", "bg": "#fdf4ff", "text": "#701a75"},
    {"primary": "#ffecd2", "secondary": "#fcb69f", "accent": "#f97316", "bg": "#fffbeb", "text": "#78350f"},
    {"primary": "#ff6e7f", "secondary": "#bfe9ff", "accent": "#06b6d4", "bg": "#f0f9ff", "text": "#0c4a6e"},
    {"primary": "#e0c3fc", "secondary": "#8ec5fc", "accent": "#667eea", "bg": "#faf5ff", "text": "#581c87"},
    {"primary": "#f5576c", "secondary": "#ffa947", "accent": "#fbbf24", "bg": "#fef2f2", "text": "#7f1d1d"},
    {"primary": "#fdcbf1", "secondary": "#e6dee9", "accent": "#a78bfa", "bg": "#fdf4ff", "text": "#6b21a8"},
    {"primary": "#a1c4fd", "secondary": "#c2e9fb", "accent": "#38bdf8", "bg": "#f0f9ff", "text": "#075985"},
    {"primary": "#d299c2", "secondary": "#fef9d7", "accent": "#facc15", "bg": "#fefce8", "text": "#713f12"},
    {"primary": "#667eea", "secondary": "#fbbf24", "accent": "#f97316", "bg": "#fffbeb", "text": "#1e293b"},
    {"primary": "#8b5cf6", "secondary": "#ec4899", "accent": "#f59e0b", "bg": "#faf5ff", "text": "#312e81"},
    {"primary": "#06b6d4", "secondary": "#6366f1", "accent": "#8b5cf6", "bg": "#f0fdfa", "text": "#0f172a"},
    {"primary": "#10b981", "secondary": "#3b82f6", "accent": "#f59e0b", "bg": "#ecfdf5", "text": "#1e3a8a"},
    {"primary": "#f43f5e", "secondary": "#fb923c", "accent": "#fbbf24", "bg": "#fff1f2", "text": "#881337"},
]

TYPOGRAPHY_STYLES = [
    {"heading": "'Inter', sans-serif", "body": "'Inter', sans-serif", "weight": "700"},
    {"heading": "'Poppins', sans-serif", "body": "'Open Sans', sans-serif", "weight": "800"},
    {"heading": "'Montserrat', sans-serif", "body": "'Roboto', sans-serif", "weight": "900"},
    {"heading": "'Space Grotesk', sans-serif", "body": "'Space Grotesk', sans-serif", "weight": "700"},
    {"heading": "'DM Sans', sans-serif", "body": "'DM Sans', sans-serif", "weight": "600"},
    {"heading": "'Plus Jakarta Sans', sans-serif", "body": "'Plus Jakarta Sans', sans-serif", "weight": "800"},
]

SPACING_SCALES = [
    {"section": "80px", "element": "40px", "gap": "24px"},
    {"section": "100px", "element": "50px", "gap": "30px"},
    {"section": "120px", "element": "60px", "gap": "40px"},
    {"section": "60px", "element": "30px", "gap": "20px"},
]


class DynamicDesignGenerator:
    """매번 완전히 다른 구조를 동적으로 생성"""
    
    def __init__(self):
        self.used_hashes: Set[str] = set()
        self.design_count = 0
        
    def get_structure_hash(self, html: str) -> str:
        """구조 해시 생성"""
        import re
        # DOM 구조와 CSS 그리드/플렉스 패턴 추출
        tags = re.findall(r'<(\w+)', html)
        grid_patterns = re.findall(r'grid-template-columns:[^;]+|flex-direction:[^;]+|display:\s*(?:grid|flex)', html)
        sections = re.findall(r'class="(hero|features|pricing|testimonial|stats|timeline|gallery|contact)', html)
        combined = ''.join(tags) + ''.join(grid_patterns) + ''.join(sections)
        return hashlib.md5(combined.encode()).hexdigest()
    
    def is_unique(self, html: str) -> bool:
        """구조 고유성 검증"""
        hash_val = self.get_structure_hash(html)
        if hash_val in self.used_hashes:
            return False
        self.used_hashes.add(hash_val)
        return True
    
    def generate_landing_page(self) -> str:
        """완전히 랜덤한 랜딩 페이지 생성"""
        
        # 랜덤 선택
        layout = random.choice(LAYOUT_TYPES)
        hero = random.choice(HERO_STYLES)
        nav = random.choice(NAVIGATION_STYLES)
        card = random.choice(CARD_STYLES)
        colors = random.choice(COLOR_PALETTES)
        typo = random.choice(TYPOGRAPHY_STYLES)
        spacing = random.choice(SPACING_SCALES)
        
        # 랜덤 섹션 조합 (3-5개)
        sections = random.sample(SECTION_TYPES, random.randint(3, 5))
        
        # 레이아웃별 CSS
        layout_css = self._get_layout_css(layout, spacing)
        hero_css = self._get_hero_css(hero, colors, typo)
        nav_css = self._get_nav_css(nav, colors)
        card_css = self._get_card_css(card, colors)
        
        # HTML 생성
        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Unique Design #{self.design_count}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ 
            font-family: {typo['body']}; 
            background: {colors['bg']}; 
            color: {colors['text']}; 
        }}
        
        {nav_css}
        {hero_css}
        {layout_css}
        {card_css}
        
        .section {{ padding: {spacing['section']} {spacing['element']}; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        h1 {{ font-family: {typo['heading']}; font-weight: {typo['weight']}; }}
        h2 {{ font-family: {typo['heading']}; font-weight: {typo['weight']}; }}
        h3 {{ font-family: {typo['heading']}; font-weight: 600; }}
        
        .btn {{
            padding: 16px 40px;
            border-radius: {random.choice(['8px', '12px', '24px', '4px', '50px'])};
            font-weight: 700;
            border: none;
            cursor: pointer;
            transition: all 0.3s;
        }}
        .btn-primary {{ background: {colors['primary']}; color: white; }}
        .btn-secondary {{ background: {colors['secondary']}; color: white; }}
        .btn:hover {{ transform: translateY(-2px); opacity: 0.9; }}
    </style>
</head>
<body>
    {self._generate_nav(nav, colors)}
    {self._generate_hero(hero, layout, colors, typo, spacing)}
    {self._generate_sections(sections, layout, colors, card, spacing)}
</body>
</html>"""
        
        self.design_count += 1
        return html
    
    def _get_layout_css(self, layout: str, spacing: dict) -> str:
        """레이아웃별 CSS"""
        css_map = {
            "grid-2-col": f".grid-container {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: {spacing['gap']}; }}",
            "grid-3-col": f".grid-container {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: {spacing['gap']}; }}",
            "grid-4-col": f".grid-container {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: {spacing['gap']}; }}",
            "flex-row": f".grid-container {{ display: flex; flex-direction: row; gap: {spacing['gap']}; flex-wrap: wrap; }}",
            "flex-column": f".grid-container {{ display: flex; flex-direction: column; gap: {spacing['gap']}; }}",
            "masonry": f".grid-container {{ column-count: 3; column-gap: {spacing['gap']}; }}",
            "split-screen": f".grid-container {{ display: grid; grid-template-columns: 1fr 1fr; min-height: 100vh; }}",
            "sidebar-left": f".grid-container {{ display: grid; grid-template-columns: 300px 1fr; gap: {spacing['gap']}; }}",
            "sidebar-right": f".grid-container {{ display: grid; grid-template-columns: 1fr 300px; gap: {spacing['gap']}; }}",
            "centered": f".grid-container {{ max-width: 1200px; margin: 0 auto; text-align: center; }}",
            "full-width": f".grid-container {{ width: 100%; }}",
            "asymmetric": f".grid-container {{ display: grid; grid-template-columns: 2fr 1fr; gap: {spacing['gap']}; }}",
            "overlapping": f".grid-container {{ position: relative; display: grid; gap: -{spacing['element']}; }}"
        }
        return css_map.get(layout, css_map["grid-3-col"])
    
    def _get_hero_css(self, hero: str, colors: dict, typo: dict) -> str:
        """히어로 스타일별 CSS"""
        base = f"""
        .hero {{
            min-height: {random.choice(['80vh', '100vh', '60vh', '70vh'])};
            display: flex;
            align-items: center;
            justify-content: center;
            position: relative;
        }}
        .hero h1 {{
            font-size: clamp(40px, 8vw, {random.choice(['80px', '96px', '72px', '64px'])});
            margin-bottom: {random.choice(['24px', '32px', '40px'])};
        }}
        """
        
        hero_styles = {
            "centered-text": f"{base} .hero {{ text-align: center; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); color: white; }}",
            "split-content": f"{base} .hero {{ background: white; }} .hero .container {{ display: grid; grid-template-columns: 1fr 1fr; gap: 60px; }}",
            "fullscreen-bg": f"{base} .hero {{ background: linear-gradient(135deg, {colors['primary']}dd 0%, {colors['secondary']}dd 100%); color: white; }}",
            "minimal": f"{base} .hero {{ background: {colors['bg']}; padding: 100px 40px; }}",
            "bold-typography": f"{base} .hero {{ background: {colors['primary']}; color: white; text-align: center; }}",
            "image-left": f"{base} .hero .container {{ display: grid; grid-template-columns: 500px 1fr; gap: 60px; align-items: center; }}",
            "image-right": f"{base} .hero .container {{ display: grid; grid-template-columns: 1fr 500px; gap: 60px; align-items: center; }}",
            "diagonal-split": f"{base} .hero {{ background: linear-gradient(45deg, {colors['primary']} 50%, {colors['secondary']} 50%); color: white; }}",
            "curved-bottom": f"{base} .hero {{ background: {colors['primary']}; color: white; border-radius: 0 0 50% 50% / 0 0 5% 5%; }}",
            "gradient-overlay": f"{base} .hero {{ background: linear-gradient(to right, {colors['primary']}ee, {colors['secondary']}ee); color: white; }}",
            "pattern-bg": f"{base} .hero {{ background: repeating-linear-gradient(45deg, {colors['primary']}, {colors['primary']} 10px, {colors['secondary']} 10px, {colors['secondary']} 20px); color: white; }}",
            "video-bg": f"{base} .hero {{ background: linear-gradient(135deg, {colors['primary']}cc 0%, {colors['secondary']}cc 100%); color: white; }}"
        }
        return hero_styles.get(hero, hero_styles["centered-text"])
    
    def _get_nav_css(self, nav: str, colors: dict) -> str:
        """네비게이션 스타일"""
        nav_styles = {
            "top-fixed": f"nav {{ position: fixed; top: 0; left: 0; right: 0; background: white; padding: 20px 60px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); z-index: 100; display: flex; justify-content: space-between; }}",
            "top-transparent": f"nav {{ position: absolute; top: 0; left: 0; right: 0; background: rgba(255,255,255,0.1); backdrop-filter: blur(10px); padding: 20px 60px; z-index: 100; display: flex; justify-content: space-between; }}",
            "side-vertical": f"nav {{ position: fixed; left: 0; top: 0; bottom: 0; width: 280px; background: {colors['primary']}; color: white; padding: 40px 0; }}",
            "center-minimal": f"nav {{ padding: 30px 60px; text-align: center; background: transparent; }}",
            "split-nav": f"nav {{ display: grid; grid-template-columns: 1fr auto 1fr; padding: 20px 60px; background: white; }}",
            "floating": f"nav {{ position: fixed; top: 20px; left: 50%; transform: translateX(-50%); background: white; padding: 15px 40px; border-radius: 50px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); z-index: 100; }}",
            "bottom-fixed": f"nav {{ position: fixed; bottom: 0; left: 0; right: 0; background: white; padding: 20px 60px; box-shadow: 0 -2px 10px rgba(0,0,0,0.1); z-index: 100; }}",
            "hamburger-menu": f"nav {{ padding: 20px 60px; background: white; display: flex; justify-content: space-between; align-items: center; }}",
            "mega-menu": f"nav {{ background: white; border-bottom: 1px solid #e0e0e0; }} nav .container {{ display: flex; justify-content: space-between; padding: 20px 60px; }}"
        }
        return nav_styles.get(nav, nav_styles["top-fixed"])
    
    def _get_card_css(self, card: str, colors: dict) -> str:
        """카드 스타일"""
        card_styles = {
            "flat": f".card {{ background: white; padding: 40px; }}",
            "elevated": f".card {{ background: white; padding: 40px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); border-radius: 16px; }}",
            "bordered": f".card {{ background: white; padding: 40px; border: 2px solid {colors['primary']}; border-radius: 12px; }}",
            "gradient": f".card {{ background: linear-gradient(135deg, {colors['primary']}20 0%, {colors['secondary']}20 100%); padding: 40px; border-radius: 16px; }}",
            "glass": f".card {{ background: rgba(255,255,255,0.7); backdrop-filter: blur(10px); padding: 40px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.5); }}",
            "neumorphic": f".card {{ background: {colors['bg']}; padding: 40px; border-radius: 20px; box-shadow: 8px 8px 16px #d1d9e6, -8px -8px 16px #ffffff; }}",
            "minimal": f".card {{ background: transparent; padding: 40px; border-bottom: 1px solid #e0e0e0; }}",
            "bold-shadow": f".card {{ background: white; padding: 40px; box-shadow: 20px 20px 0px {colors['primary']}40; border-radius: 12px; }}",
            "rounded": f".card {{ background: white; padding: 40px; border-radius: 30px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}",
            "sharp": f".card {{ background: white; padding: 40px; border-radius: 0; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}",
            "tilted": f".card {{ background: white; padding: 40px; border-radius: 12px; transform: rotate(-1deg); box-shadow: 0 10px 30px rgba(0,0,0,0.1); }}",
            "interactive": f".card {{ background: white; padding: 40px; border-radius: 16px; transition: all 0.3s; cursor: pointer; }} .card:hover {{ transform: translateY(-10px); box-shadow: 0 20px 50px rgba(0,0,0,0.15); }}"
        }
        return card_styles.get(card, card_styles["elevated"])
    
    def _generate_nav(self, style: str, colors: dict) -> str:
        """네비게이션 HTML"""
        return f"""
        <nav>
            <div style="font-size: 24px; font-weight: 800; color: {colors['primary']};">Brand</div>
            <div style="display: flex; gap: 40px;">
                <a href="#" style="text-decoration: none; color: {colors['text']}; font-weight: 600;">Home</a>
                <a href="#" style="text-decoration: none; color: {colors['text']}; font-weight: 600;">Features</a>
                <a href="#" style="text-decoration: none; color: {colors['text']}; font-weight: 600;">Pricing</a>
                <a href="#" style="text-decoration: none; color: {colors['text']}; font-weight: 600;">Contact</a>
            </div>
        </nav>
        """
    
    def _generate_hero(self, style: str, layout: str, colors: dict, typo: dict, spacing: dict) -> str:
        """히어로 섹션 HTML"""
        return f"""
        <section class="hero">
            <div class="container" style="padding: 0 {spacing['element']};">
                <div>
                    <h1>Transform Your Business Today</h1>
                    <p style="font-size: clamp(18px, 2vw, 24px); margin-bottom: {spacing['element']}; opacity: 0.9;">
                        Innovative solutions for modern challenges. Scale your business with cutting-edge technology.
                    </p>
                    <div style="display: flex; gap: 20px; flex-wrap: wrap; {'justify-content: center;' if style == 'centered-text' else ''}">
                        <button class="btn btn-primary">Get Started</button>
                        <button class="btn btn-secondary">Learn More</button>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def _generate_sections(self, sections: List[str], layout: str, colors: dict, card: str, spacing: dict) -> str:
        """섹션들 생성"""
        html_parts = []
        
        for section_type in sections:
            if section_type == "features-grid":
                html_parts.append(self._section_features(layout, colors, card, spacing))
            elif section_type == "pricing-table":
                html_parts.append(self._section_pricing(colors, card, spacing))
            elif section_type == "testimonials":
                html_parts.append(self._section_testimonials(layout, colors, card, spacing))
            elif section_type == "stats-counter":
                html_parts.append(self._section_stats(layout, colors, spacing))
            elif section_type == "contact-form":
                html_parts.append(self._section_contact(colors, spacing))
        
        return '\n'.join(html_parts)
    
    def _section_features(self, layout: str, colors: dict, card: str, spacing: dict) -> str:
        num_features = random.choice([3, 4, 6])
        grid_cols = "repeat(3, 1fr)" if num_features % 3 == 0 else "repeat(auto-fit, minmax(300px, 1fr))"
        
        return f"""
        <section class="section" style="background: {random.choice([colors['bg'], '#fafafa', '#f9fafb'])};">
            <div class="container">
                <h2 style="text-align: center; font-size: clamp(32px, 5vw, 48px); margin-bottom: {spacing['element']};">
                    Our Features
                </h2>
                <div style="display: grid; grid-template-columns: {grid_cols}; gap: {spacing['gap']};">
                    {''.join([f'<div class="card"><div style="font-size: 48px; margin-bottom: 20px;">{random.choice(["🚀", "💎", "⚡", "🎯", "🔒", "🌟"])}</div><h3 style="font-size: 24px; margin-bottom: 12px;">Feature {i+1}</h3><p style="color: #666; line-height: 1.7;">Powerful tools designed for success.</p></div>' for i in range(num_features)])}
                </div>
            </div>
        </section>
        """
    
    def _section_pricing(self, colors: dict, card: str, spacing: dict) -> str:
        return f"""
        <section class="section">
            <div class="container">
                <h2 style="text-align: center; font-size: clamp(32px, 5vw, 48px); margin-bottom: {spacing['element']};">
                    Pricing Plans
                </h2>
                <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: {spacing['gap']}; max-width: 1200px; margin: 0 auto;">
                    <div class="card" style="text-align: center;">
                        <h3 style="font-size: 24px; margin-bottom: 16px;">Starter</h3>
                        <div style="font-size: 48px; font-weight: 900; margin: 20px 0;">$29</div>
                        <button class="btn btn-secondary" style="width: 100%;">Choose Plan</button>
                    </div>
                    <div class="card" style="text-align: center; border: 3px solid {colors['primary']};">
                        <div style="background: {colors['primary']}; color: white; padding: 8px; margin: -40px -40px 20px -40px; font-weight: 700;">POPULAR</div>
                        <h3 style="font-size: 24px; margin-bottom: 16px;">Pro</h3>
                        <div style="font-size: 48px; font-weight: 900; margin: 20px 0;">$79</div>
                        <button class="btn btn-primary" style="width: 100%;">Choose Plan</button>
                    </div>
                    <div class="card" style="text-align: center;">
                        <h3 style="font-size: 24px; margin-bottom: 16px;">Enterprise</h3>
                        <div style="font-size: 48px; font-weight: 900; margin: 20px 0;">$199</div>
                        <button class="btn btn-secondary" style="width: 100%;">Choose Plan</button>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def _section_testimonials(self, layout: str, colors: dict, card: str, spacing: dict) -> str:
        return f"""
        <section class="section" style="background: {colors['bg']};">
            <div class="container">
                <h2 style="text-align: center; font-size: clamp(32px, 5vw, 48px); margin-bottom: {spacing['element']};">
                    What Clients Say
                </h2>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); gap: {spacing['gap']};">
                    <div class="card">
                        <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; color: #555;">"Amazing product! Transformed our workflow completely."</p>
                        <div style="font-weight: 700;">— John Doe, CEO</div>
                    </div>
                    <div class="card">
                        <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; color: #555;">"Best investment we've made for our business."</p>
                        <div style="font-weight: 700;">— Jane Smith, Founder</div>
                    </div>
                    <div class="card">
                        <p style="font-size: 18px; line-height: 1.8; margin-bottom: 20px; color: #555;">"Incredible support and amazing features."</p>
                        <div style="font-weight: 700;">— Mike Johnson, CTO</div>
                    </div>
                </div>
            </div>
        </section>
        """
    
    def _section_stats(self, layout: str, colors: dict, spacing: dict) -> str:
        stats_count = random.choice([3, 4])
        return f"""
        <section class="section" style="background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); color: white;">
            <div class="container">
                <div style="display: grid; grid-template-columns: repeat({stats_count}, 1fr); gap: {spacing['gap']}; text-align: center;">
                    <div><div style="font-size: 56px; font-weight: 900;">10K+</div><div style="font-size: 18px; opacity: 0.9;">Active Users</div></div>
                    <div><div style="font-size: 56px; font-weight: 900;">98%</div><div style="font-size: 18px; opacity: 0.9;">Satisfaction</div></div>
                    <div><div style="font-size: 56px; font-weight: 900;">24/7</div><div style="font-size: 18px; opacity: 0.9;">Support</div></div>
                    {f'<div><div style="font-size: 56px; font-weight: 900;">150+</div><div style="font-size: 18px; opacity: 0.9;">Countries</div></div>' if stats_count == 4 else ''}
                </div>
            </div>
        </section>
        """
    
    def _section_contact(self, colors: dict, spacing: dict) -> str:
        return f"""
        <section class="section">
            <div class="container" style="max-width: 600px;">
                <h2 style="text-align: center; font-size: clamp(32px, 5vw, 48px); margin-bottom: {spacing['element']};">
                    Get In Touch
                </h2>
                <div style="display: flex; flex-direction: column; gap: 20px;">
                    <input type="text" placeholder="Your Name" style="padding: 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px;">
                    <input type="email" placeholder="Your Email" style="padding: 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px;">
                    <textarea placeholder="Your Message" rows="5" style="padding: 16px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 16px; font-family: inherit;"></textarea>
                    <button class="btn btn-primary" style="width: 100%;">Send Message</button>
                </div>
            </div>
        </section>
        """
    
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
        print(f"✅ Uploaded: {public_url}")
        return public_url
    
    def save_to_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Database 저장"""
        print(f"💾 Saving: {data['title']}")
        response = supabase.table('designs').insert(data).execute()
        print("✅ Saved to database")
        return response.data[0]
    
    async def create_unique_design(self, category: str = "Landing Page", max_attempts: int = 10) -> Dict[str, Any]:
        """고유한 디자인 생성"""
        
        print(f"\n{'='*70}")
        print(f"🎨 Creating unique {category} design #{self.design_count + 1}")
        print(f"{'='*70}\n")
        
        for attempt in range(max_attempts):
            print(f"🔄 Attempt {attempt + 1}/{max_attempts}")
            
            # 새로운 구조 생성
            html_code = self.generate_landing_page()
            
            # 고유성 검증
            if self.is_unique(html_code):
                print("✅ Unique structure generated")
                break
            else:
                print("⚠️ Duplicate detected, regenerating...")
        else:
            raise Exception("Failed to generate unique structure")
        
        # 스크린샷
        screenshot = await self.capture_screenshot(html_code)
        
        # 업로드
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_landing_{self.design_count}.png"
        image_url = self.upload_to_storage(screenshot, filename)
        
        # DB 저장
        design_data = {
            "title": f"Unique Design #{self.design_count} - {datetime.now().strftime('%B %d, %Y')}",
            "description": f"Dynamically generated unique design with hash: {self.get_structure_hash(html_code)[:12]}",
            "image_url": image_url,
            "category": category,
            "code": html_code,
            "prompt": f"Dynamic structure #{self.design_count}",
        }
        
        result = self.save_to_database(design_data)
        
        print(f"\n🎉 Design created successfully!")
        print(f"ID: {result['id']}")
        print(f"Hash: {self.get_structure_hash(html_code)[:12]}...")
        print(f"URL: {result['image_url']}\n")
        
        return result


async def main():
    """메인 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate dynamically unique designs")
    parser.add_argument('--count', type=int, default=1, help='Number of designs')
    args = parser.parse_args()
    
    generator = DynamicDesignGenerator()
    
    for i in range(args.count):
        try:
            await generator.create_unique_design()
            
            if i < args.count - 1:
                print("⏳ Waiting before next generation...\n")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue
    
    print(f"\n{'='*70}")
    print(f"🎉 Completed! Generated {generator.design_count} unique designs")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(main())
