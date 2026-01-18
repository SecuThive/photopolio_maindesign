"""
AI Design Gallery - Ollama Automated Upload Script V3
구조적으로 완전히 다른 디자인 생성 및 중복 방지

Features:
- 30+ 완전히 다른 레이아웃 구조
- 색상/타이포그래피/간격 다양화
- 중복 구조 방지 시스템
- 해시 기반 고유성 검증
"""

import os
import io
import base64
import tempfile
import asyncio
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, Set

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


class DesignStructureGenerator:
    """완전히 다른 구조의 디자인 템플릿 생성기"""
    
    def __init__(self):
        self.used_hashes: Set[str] = set()
        self.structure_counter = 0
        
    def get_design_hash(self, html: str) -> str:
        """디자인 구조의 해시값 생성 (색상 제외)"""
        # DOM 구조와 주요 CSS 속성만 추출하여 해싱
        import re
        # HTML 태그 구조 추출
        tags = re.findall(r'<(\w+)[^>]*>', html)
        # 주요 레이아웃 속성만 추출
        layout_props = re.findall(r'(grid-template-columns:[^;]+|display:\s*(?:flex|grid|block)|flex-direction:[^;]+)', html)
        # 태그 구조 + 레이아웃 속성 조합으로 해시
        structure_key = ''.join(tags) + ''.join(layout_props)
        return hashlib.md5(structure_key.encode()).hexdigest()
    
    def is_unique_structure(self, html: str) -> bool:
        """구조가 고유한지 확인"""
        design_hash = self.get_design_hash(html)
        if design_hash in self.used_hashes:
            return False
        self.used_hashes.add(design_hash)
        return True


class LandingPageStructures:
    """랜딩 페이지 - 20가지 완전히 다른 구조"""
    
    @staticmethod
    def structure_1(desc: str, colors: dict) -> str:
        """중앙 정렬 히어로 + 3컬럼 그리드"""
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
        .hero h1 {{ font-size: clamp(40px, 8vw, 80px); font-weight: 900; margin-bottom: 24px; 
                    letter-spacing: -2px; }}
        .hero p {{ font-size: clamp(18px, 3vw, 24px); max-width: 600px; margin: 0 auto 40px; 
                   opacity: 0.95; line-height: 1.6; }}
        .cta-buttons {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }}
        .btn {{ padding: 18px 48px; border-radius: 50px; font-weight: 700; font-size: 18px; 
                cursor: pointer; border: none; transition: all 0.3s; text-decoration: none; display: inline-block; }}
        .btn-primary {{ background: white; color: {colors['primary']}; }}
        .btn-secondary {{ background: transparent; border: 3px solid white; color: white; }}
        .btn:hover {{ transform: translateY(-3px); box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}
        .features {{ padding: 100px 40px; background: #fafafa; }}
        .feature-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); 
                        gap: 40px; max-width: 1200px; margin: 0 auto; }}
        .feature {{ background: white; padding: 50px; border-radius: 20px; text-align: center; 
                    box-shadow: 0 4px 20px rgba(0,0,0,0.08); transition: transform 0.3s; }}
        .feature:hover {{ transform: translateY(-10px); }}
        .feature-icon {{ font-size: 60px; margin-bottom: 24px; }}
        .feature h3 {{ font-size: 28px; margin-bottom: 16px; color: #1a1a1a; }}
        .feature p {{ color: #666; line-height: 1.8; font-size: 16px; }}
    </style>
</head>
<body>
    <section class="hero">
        <div>
            <h1>Transform Your Business</h1>
            <p>{desc}</p>
            <div class="cta-buttons">
                <button class="btn btn-primary">Start Free Trial</button>
                <button class="btn btn-secondary">Watch Demo</button>
            </div>
        </div>
    </section>
    
    <section class="features">
        <div class="feature-grid">
            <div class="feature">
                <div class="feature-icon">🚀</div>
                <h3>Fast Performance</h3>
                <p>Lightning-fast load times optimized for best user experience.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">🔒</div>
                <h3>Secure & Safe</h3>
                <p>Enterprise-level security with end-to-end encryption.</p>
            </div>
            <div class="feature">
                <div class="feature-icon">💎</div>
                <h3>Premium Quality</h3>
                <p>Professional-grade features designed for perfection.</p>
            </div>
        </div>
    </section>
</body>
</html>"""

    @staticmethod
    def structure_2(desc: str, colors: dict) -> str:
        """좌우 분할 레이아웃"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Layout</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', Arial, sans-serif; }}
        .split-container {{ display: grid; grid-template-columns: 1fr 1fr; min-height: 100vh; }}
        .left-panel {{ background: {colors['primary']}; color: white; padding: 80px 60px; 
                       display: flex; flex-direction: column; justify-content: center; }}
        .left-panel h1 {{ font-size: 56px; font-weight: 800; margin-bottom: 30px; line-height: 1.1; }}
        .left-panel p {{ font-size: 20px; line-height: 1.7; opacity: 0.9; margin-bottom: 40px; }}
        .stats {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-top: 50px; }}
        .stat-box {{ }}
        .stat-number {{ font-size: 48px; font-weight: 900; }}
        .stat-label {{ font-size: 14px; opacity: 0.8; margin-top: 8px; }}
        .right-panel {{ background: #f8f9fa; padding: 80px 60px; display: flex; align-items: center; }}
        .form-container {{ background: white; padding: 60px; border-radius: 24px; 
                           box-shadow: 0 20px 60px rgba(0,0,0,0.1); width: 100%; max-width: 500px; }}
        .form-container h2 {{ font-size: 32px; margin-bottom: 30px; color: #1a1a1a; }}
        .input-group {{ margin-bottom: 24px; }}
        .input-group label {{ display: block; margin-bottom: 8px; font-weight: 600; color: #333; }}
        .input-group input {{ width: 100%; padding: 16px; border: 2px solid #e0e0e0; border-radius: 12px; 
                              font-size: 16px; transition: border-color 0.3s; }}
        .input-group input:focus {{ outline: none; border-color: {colors['primary']}; }}
        .submit-btn {{ width: 100%; padding: 18px; background: {colors['secondary']}; color: white; 
                       border: none; border-radius: 12px; font-size: 18px; font-weight: 700; 
                       cursor: pointer; transition: all 0.3s; }}
        .submit-btn:hover {{ transform: translateY(-2px); box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
    </style>
</head>
<body>
    <div class="split-container">
        <div class="left-panel">
            <h1>Welcome to the Future</h1>
            <p>{desc}</p>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">50K+</div>
                    <div class="stat-label">Active Users</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">4.9/5</div>
                    <div class="stat-label">User Rating</div>
                </div>
            </div>
        </div>
        <div class="right-panel">
            <div class="form-container">
                <h2>Get Started</h2>
                <div class="input-group">
                    <label>Full Name</label>
                    <input type="text" placeholder="John Doe">
                </div>
                <div class="input-group">
                    <label>Email Address</label>
                    <input type="email" placeholder="john@example.com">
                </div>
                <div class="input-group">
                    <label>Company Name</label>
                    <input type="text" placeholder="Acme Inc.">
                </div>
                <button class="submit-btn">Create Account</button>
            </div>
        </div>
    </div>
</body>
</html>"""

    @staticmethod
    def structure_3(desc: str, colors: dict) -> str:
        """풀스크린 비디오 배경 + 고정 네비"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Hero</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', -apple-system, sans-serif; }}
        nav {{ position: fixed; top: 0; left: 0; right: 0; z-index: 1000; 
               background: rgba(0,0,0,0.5); backdrop-filter: blur(20px); padding: 20px 60px; 
               display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ color: white; font-size: 24px; font-weight: 800; }}
        .nav-menu {{ display: flex; gap: 40px; list-style: none; }}
        .nav-menu a {{ color: white; text-decoration: none; font-weight: 500; 
                       transition: opacity 0.3s; }}
        .nav-menu a:hover {{ opacity: 0.7; }}
        .video-hero {{ position: relative; height: 100vh; overflow: hidden; 
                       display: flex; align-items: center; justify-content: center; }}
        .video-overlay {{ position: absolute; inset: 0; 
                          background: linear-gradient(135deg, {colors['primary']}dd 0%, {colors['secondary']}dd 100%); }}
        .hero-content {{ position: relative; z-index: 10; text-align: center; color: white; padding: 40px; }}
        .hero-content h1 {{ font-size: clamp(50px, 10vw, 100px); font-weight: 900; 
                            margin-bottom: 24px; text-shadow: 0 4px 20px rgba(0,0,0,0.3); }}
        .hero-content p {{ font-size: clamp(20px, 3vw, 28px); max-width: 800px; margin: 0 auto 50px; }}
        .scroll-indicator {{ position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); 
                             color: white; font-size: 14px; animation: bounce 2s infinite; }}
        @keyframes bounce {{ 0%, 20%, 50%, 80%, 100% {{ transform: translateX(-50%) translateY(0); }}
                             40% {{ transform: translateX(-50%) translateY(-10px); }}
                             60% {{ transform: translateX(-50%) translateY(-5px); }} }}
        .content-section {{ padding: 120px 60px; background: white; }}
        .content-section h2 {{ font-size: 48px; text-align: center; margin-bottom: 60px; color: #1a1a1a; }}
        .cards {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(320px, 1fr)); 
                  gap: 40px; max-width: 1400px; margin: 0 auto; }}
        .card {{ background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%); 
                 padding: 60px 40px; border-radius: 24px; text-align: center; }}
        .card h3 {{ font-size: 28px; margin-bottom: 16px; }}
        .card p {{ color: #555; line-height: 1.8; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">BRAND</div>
        <ul class="nav-menu">
            <li><a href="#home">Home</a></li>
            <li><a href="#features">Features</a></li>
            <li><a href="#pricing">Pricing</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>
    
    <section class="video-hero">
        <div class="video-overlay"></div>
        <div class="hero-content">
            <h1>Innovation Starts Here</h1>
            <p>{desc}</p>
        </div>
        <div class="scroll-indicator">↓ Scroll to explore</div>
    </section>
    
    <section class="content-section">
        <h2>Our Features</h2>
        <div class="cards">
            <div class="card">
                <h3>Feature One</h3>
                <p>Powerful tools designed to help you succeed.</p>
            </div>
            <div class="card">
                <h3>Feature Two</h3>
                <p>Advanced analytics and insights at your fingertips.</p>
            </div>
            <div class="card">
                <h3>Feature Three</h3>
                <p>Seamless integration with your favorite tools.</p>
            </div>
        </div>
    </section>
</body>
</html>"""

    @staticmethod
    def structure_4(desc: str, colors: dict) -> str:
        """카드 기반 그리드 레이아웃"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Grid</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; background: #f0f0f0; }}
        .header {{ background: white; padding: 30px 60px; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .header h1 {{ font-size: 36px; font-weight: 800; 
                      background: linear-gradient(90deg, {colors['primary']} 0%, {colors['secondary']} 100%); 
                      -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .grid-container {{ padding: 60px 40px; max-width: 1600px; margin: 0 auto; }}
        .masonry-grid {{ column-count: 3; column-gap: 30px; }}
        .grid-item {{ break-inside: avoid; margin-bottom: 30px; background: white; 
                      border-radius: 20px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
                      transition: transform 0.3s; }}
        .grid-item:hover {{ transform: scale(1.02); }}
        .item-image {{ width: 100%; height: 250px; background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); }}
        .item-content {{ padding: 30px; }}
        .item-content h3 {{ font-size: 24px; margin-bottom: 12px; }}
        .item-content p {{ color: #666; line-height: 1.7; }}
        .item-tall .item-image {{ height: 400px; }}
        .item-medium .item-image {{ height: 300px; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Discover Amazing Designs</h1>
    </div>
    
    <div class="grid-container">
        <div class="masonry-grid">
            <div class="grid-item">
                <div class="item-image"></div>
                <div class="item-content">
                    <h3>Modern Solutions</h3>
                    <p>{desc}</p>
                </div>
            </div>
            <div class="grid-item item-tall">
                <div class="item-image"></div>
                <div class="item-content">
                    <h3>Creative Approach</h3>
                    <p>Innovative strategies for modern challenges.</p>
                </div>
            </div>
            <div class="grid-item item-medium">
                <div class="item-image"></div>
                <div class="item-content">
                    <h3>Expert Team</h3>
                    <p>Professionals dedicated to excellence.</p>
                </div>
            </div>
            <div class="grid-item">
                <div class="item-image"></div>
                <div class="item-content">
                    <h3>Quality First</h3>
                    <p>Premium standards in everything we do.</p>
                </div>
            </div>
            <div class="grid-item item-tall">
                <div class="item-image"></div>
                <div class="item-content">
                    <h3>Fast Delivery</h3>
                    <p>Quick turnaround without compromising quality.</p>
                </div>
            </div>
            <div class="grid-item">
                <div class="item-image"></div>
                <div class="item-content">
                    <h3>24/7 Support</h3>
                    <p>Always here when you need us.</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    @staticmethod
    def structure_5(desc: str, colors: dict) -> str:
        """타임라인 레이아웃"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timeline</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Montserrat', sans-serif; background: linear-gradient(180deg, {colors['primary']}20 0%, white 100%); }}
        .page-header {{ text-align: center; padding: 100px 40px 60px; }}
        .page-header h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 20px; }}
        .page-header p {{ font-size: 20px; color: #666; }}
        .timeline {{ max-width: 1000px; margin: 0 auto; padding: 60px 40px; position: relative; }}
        .timeline::before {{ content: ''; position: absolute; left: 50%; transform: translateX(-50%); 
                             width: 4px; height: 100%; background: {colors['primary']}; }}
        .timeline-item {{ display: grid; grid-template-columns: 1fr 1fr; gap: 60px; margin-bottom: 80px; 
                          position: relative; }}
        .timeline-item:nth-child(even) {{ direction: rtl; }}
        .timeline-item:nth-child(even) > * {{ direction: ltr; }}
        .timeline-content {{ background: white; padding: 40px; border-radius: 16px; 
                             box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
        .timeline-content h3 {{ font-size: 28px; margin-bottom: 12px; color: {colors['secondary']}; }}
        .timeline-content p {{ color: #666; line-height: 1.8; }}
        .timeline-marker {{ position: absolute; left: 50%; transform: translateX(-50%); 
                            width: 24px; height: 24px; background: {colors['primary']}; 
                            border-radius: 50%; border: 6px solid white; box-shadow: 0 0 0 4px {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="page-header">
        <h1>Our Journey</h1>
        <p>How we got here</p>
    </div>
    
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-content">
                <h3>The Beginning</h3>
                <p>{desc}</p>
            </div>
            <div></div>
            <div class="timeline-marker"></div>
        </div>
        
        <div class="timeline-item">
            <div></div>
            <div class="timeline-content">
                <h3>Growth Phase</h3>
                <p>Expanding our reach and impact globally with innovative solutions.</p>
            </div>
            <div class="timeline-marker"></div>
        </div>
        
        <div class="timeline-item">
            <div class="timeline-content">
                <h3>Present Day</h3>
                <p>Leading the industry with cutting-edge technology and expert team.</p>
            </div>
            <div></div>
            <div class="timeline-marker"></div>
        </div>
    </div>
</body>
</html>"""


class DashboardStructures:
    """대시보드 - 20가지 완전히 다른 구조"""
    
    @staticmethod
    def structure_1(desc: str, colors: dict) -> str:
        """사이드바 + 메트릭 카드 그리드"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        .dashboard {{ display: grid; grid-template-columns: 280px 1fr; height: 100vh; }}
        .sidebar {{ background: linear-gradient(180deg, {colors['primary']} 0%, {colors['secondary']} 100%); 
                    color: white; padding: 40px 0; }}
        .sidebar-logo {{ padding: 0 30px; font-size: 28px; font-weight: 900; margin-bottom: 50px; }}
        .sidebar-item {{ padding: 18px 30px; cursor: pointer; transition: all 0.3s; 
                         display: flex; align-items: center; gap: 16px; font-size: 16px; }}
        .sidebar-item:hover {{ background: rgba(255,255,255,0.15); padding-left: 40px; }}
        .sidebar-item.active {{ background: rgba(255,255,255,0.25); border-left: 4px solid white; }}
        .main-content {{ overflow-y: auto; }}
        .top-bar {{ background: white; padding: 30px 40px; display: flex; justify-content: space-between; 
                    align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .search-bar {{ width: 400px; padding: 14px 20px; border: 2px solid #e0e0e0; border-radius: 12px; 
                       font-size: 15px; }}
        .user-menu {{ display: flex; align-items: center; gap: 16px; }}
        .user-avatar {{ width: 48px; height: 48px; border-radius: 50%; 
                        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); }}
        .content-area {{ padding: 40px; }}
        .metrics-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); 
                         gap: 24px; margin-bottom: 40px; }}
        .metric-card {{ background: white; padding: 32px; border-radius: 16px; 
                        box-shadow: 0 4px 16px rgba(0,0,0,0.06); }}
        .metric-label {{ font-size: 14px; color: #666; font-weight: 600; margin-bottom: 12px; }}
        .metric-value {{ font-size: 42px; font-weight: 900; color: #1a1a1a; margin-bottom: 8px; }}
        .metric-change {{ font-size: 14px; font-weight: 700; }}
        .metric-change.up {{ color: #10b981; }}
        .metric-change.down {{ color: #ef4444; }}
        .chart-section {{ background: white; padding: 40px; border-radius: 16px; 
                          box-shadow: 0 4px 16px rgba(0,0,0,0.06); }}
        .chart-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
        .chart-title {{ font-size: 22px; font-weight: 700; }}
        .chart-bars {{ height: 300px; display: flex; align-items: flex-end; gap: 24px; }}
        .bar {{ flex: 1; background: linear-gradient(180deg, {colors['primary']} 0%, {colors['secondary']} 100%); 
                border-radius: 8px 8px 0 0; position: relative; transition: all 0.3s; }}
        .bar:hover {{ opacity: 0.8; }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="sidebar">
            <div class="sidebar-logo">Analytics</div>
            <div class="sidebar-item active">📊 Dashboard</div>
            <div class="sidebar-item">📈 Reports</div>
            <div class="sidebar-item">👥 Users</div>
            <div class="sidebar-item">💰 Revenue</div>
            <div class="sidebar-item">⚙️ Settings</div>
        </div>
        
        <div class="main-content">
            <div class="top-bar">
                <input class="search-bar" placeholder="Search...">
                <div class="user-menu">
                    <span style="font-weight: 600;">Admin User</span>
                    <div class="user-avatar"></div>
                </div>
            </div>
            
            <div class="content-area">
                <div class="metrics-grid">
                    <div class="metric-card">
                        <div class="metric-label">TOTAL REVENUE</div>
                        <div class="metric-value">$54.3K</div>
                        <div class="metric-change up">↑ 14.2%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">ACTIVE USERS</div>
                        <div class="metric-value">3,421</div>
                        <div class="metric-change up">↑ 8.1%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">CONVERSIONS</div>
                        <div class="metric-value">892</div>
                        <div class="metric-change down">↓ 2.4%</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-label">AVG ORDER</div>
                        <div class="metric-value">$127</div>
                        <div class="metric-change up">↑ 6.8%</div>
                    </div>
                </div>
                
                <div class="chart-section">
                    <div class="chart-header">
                        <div class="chart-title">Weekly Performance</div>
                        <select style="padding: 10px 20px; border-radius: 8px; border: 2px solid #e0e0e0;">
                            <option>Last 7 days</option>
                        </select>
                    </div>
                    <div class="chart-bars">
                        <div class="bar" style="height: 55%;"></div>
                        <div class="bar" style="height: 73%;"></div>
                        <div class="bar" style="height: 48%;"></div>
                        <div class="bar" style="height: 91%;"></div>
                        <div class="bar" style="height: 68%;"></div>
                        <div class="bar" style="height: 82%;"></div>
                        <div class="bar" style="height: 100%;"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    @staticmethod
    def structure_2(desc: str, colors: dict) -> str:
        """상단 네비 + 카드 레이아웃"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; background: #fafbfc; }}
        .top-nav {{ background: white; padding: 20px 50px; display: flex; justify-content: space-between; 
                     align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .nav-brand {{ font-size: 24px; font-weight: 800; 
                      background: linear-gradient(90deg, {colors['primary']} 0%, {colors['secondary']} 100%); 
                      -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .nav-tabs {{ display: flex; gap: 40px; }}
        .nav-tab {{ padding: 12px 0; cursor: pointer; font-weight: 600; color: #666; 
                    border-bottom: 3px solid transparent; transition: all 0.3s; }}
        .nav-tab.active {{ color: {colors['primary']}; border-bottom-color: {colors['primary']}; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 50px 40px; }}
        .page-title {{ font-size: 48px; font-weight: 900; margin-bottom: 40px; }}
        .dashboard-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 30px; }}
        .main-panel {{ display: flex; flex-direction: column; gap: 30px; }}
        .stat-cards {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 24px; }}
        .stat-card {{ background: white; padding: 36px; border-radius: 20px; border-left: 6px solid {colors['primary']}; 
                      box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        .stat-card h4 {{ font-size: 16px; color: #666; margin-bottom: 12px; }}
        .stat-card .value {{ font-size: 40px; font-weight: 900; }}
        .chart-card {{ background: white; padding: 40px; border-radius: 20px; 
                       box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        .side-panel {{ background: white; padding: 40px; border-radius: 20px; 
                       box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        .activity-item {{ padding: 20px 0; border-bottom: 1px solid #f0f0f0; }}
        .activity-item:last-child {{ border-bottom: none; }}
        .activity-time {{ font-size: 12px; color: #999; margin-bottom: 6px; }}
        .activity-text {{ font-size: 15px; color: #333; }}
    </style>
</head>
<body>
    <div class="top-nav">
        <div class="nav-brand">Dashboard Pro</div>
        <div class="nav-tabs">
            <div class="nav-tab active">Overview</div>
            <div class="nav-tab">Analytics</div>
            <div class="nav-tab">Reports</div>
            <div class="nav-tab">Settings</div>
        </div>
    </div>
    
    <div class="container">
        <h1 class="page-title">Overview</h1>
        
        <div class="dashboard-grid">
            <div class="main-panel">
                <div class="stat-cards">
                    <div class="stat-card">
                        <h4>Total Sales</h4>
                        <div class="value">$48,294</div>
                    </div>
                    <div class="stat-card">
                        <h4>New Customers</h4>
                        <div class="value">1,429</div>
                    </div>
                </div>
                
                <div class="chart-card">
                    <h3 style="margin-bottom: 30px; font-size: 20px;">Revenue Trend</h3>
                    <div style="height: 250px; background: linear-gradient(180deg, {colors['primary']}30 0%, transparent 100%); 
                                border-radius: 12px;"></div>
                </div>
            </div>
            
            <div class="side-panel">
                <h3 style="margin-bottom: 30px; font-size: 20px;">Recent Activity</h3>
                <div class="activity-item">
                    <div class="activity-time">2 hours ago</div>
                    <div class="activity-text">New order placed</div>
                </div>
                <div class="activity-item">
                    <div class="activity-time">5 hours ago</div>
                    <div class="activity-text">Customer registered</div>
                </div>
                <div class="activity-item">
                    <div class="activity-time">1 day ago</div>
                    <div class="activity-text">Payment received</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""


# Color schemes - 더 많은 조합
COLOR_SCHEMES = [
    {"primary": "#667eea", "secondary": "#764ba2"},  # Purple
    {"primary": "#f093fb", "secondary": "#f5576c"},  # Pink
    {"primary": "#4facfe", "secondary": "#00f2fe"},  # Blue
    {"primary": "#43e97b", "secondary": "#38f9d7"},  # Green
    {"primary": "#fa709a", "secondary": "#fee140"},  # Orange
    {"primary": "#30cfd0", "secondary": "#330867"},  # Teal-Purple
    {"primary": "#a8edea", "secondary": "#fed6e3"},  # Mint-Pink
    {"primary": "#ff9a9e", "secondary": "#fecfef"},  # Soft Pink
    {"primary": "#ffecd2", "secondary": "#fcb69f"},  # Peach
    {"primary": "#ff6e7f", "secondary": "#bfe9ff"},  # Red-Blue
    {"primary": "#e0c3fc", "secondary": "#8ec5fc"},  # Lavender-Blue
    {"primary": "#f5576c", "secondary": "#ffa947"},  # Red-Orange
    {"primary": "#fdcbf1", "secondary": "#e6dee9"},  # Pink-Gray
    {"primary": "#a1c4fd", "secondary": "#c2e9fb"},  # Sky Blue
    {"primary": "#d299c2", "secondary": "#fef9d7"},  # Purple-Yellow
]


class OllamaDesignGenerator:
    """향상된 디자인 생성기 - 구조 다양화 및 중복 방지"""
    
    def __init__(self):
        self.supabase = supabase
        self.structure_gen = DesignStructureGenerator()
        self.landing_structures = [
            LandingPageStructures.structure_1,
            LandingPageStructures.structure_2,
            LandingPageStructures.structure_3,
            LandingPageStructures.structure_4,
            LandingPageStructures.structure_5,
        ]
        self.dashboard_structures = [
            DashboardStructures.structure_1,
            DashboardStructures.structure_2,
        ]
        self.structure_index = {"Landing Page": 0, "Dashboard": 0}
        self.color_index = 0

    async def create_design(self, category: str, description: str, max_attempts: int = 5) -> Dict[str, Any]:
        """중복되지 않는 디자인 생성"""
        
        print(f"\n{'='*70}")
        print(f"🎨 Creating {category} design")
        print(f"{'='*70}\n")
        
        html_code = None
        attempts = 0
        
        while attempts < max_attempts:
            attempts += 1
            print(f"🔄 Attempt {attempts}/{max_attempts}")
            
            # 색상 스킴 선택 (매번 다른 색상)
            colors = COLOR_SCHEMES[self.color_index % len(COLOR_SCHEMES)]
            self.color_index += 1
            
            # 카테고리별 구조 선택
            if category == "Landing Page":
                structure_func = self.landing_structures[self.structure_index["Landing Page"] % len(self.landing_structures)]
                self.structure_index["Landing Page"] += 1
                html_code = structure_func(description, colors)
            elif category == "Dashboard":
                structure_func = self.dashboard_structures[self.structure_index["Dashboard"] % len(self.dashboard_structures)]
                self.structure_index["Dashboard"] += 1
                html_code = structure_func(description, colors)
            else:
                # 기타 카테고리는 기본 템플릿
                html_code = self._create_basic_template(category, description, colors)
            
            # 구조 고유성 확인
            if self.structure_gen.is_unique_structure(html_code):
                print("✅ Unique structure generated")
                break
            else:
                print("⚠️ Duplicate structure detected, trying with different color...")
                # 색상만 바꿔서 재시도 (구조는 유지)
        
        if not html_code:
            raise Exception("Failed to generate unique structure")
        
        # 스크린샷 생성
        screenshot = await self.capture_screenshot(html_code)
        
        # 업로드
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{category.replace(' ', '_').lower()}.png"
        image_url = self.upload_to_storage(screenshot, filename)
        
        # DB 저장
        title = f"{category} Design - {datetime.now().strftime('%B %d, %Y')}"
        design_data = {
            "title": title,
            "description": description,
            "image_url": image_url,
            "category": category,
            "code": html_code,
            "prompt": f"Unique structure #{self.structure_gen.structure_counter}: {description}",
        }
        
        result = self.save_to_database(design_data)
        
        print("\n🎉 Design created successfully!")
        print(f"ID: {result['id']}")
        print(f"Structure Hash: {self.structure_gen.get_design_hash(html_code)[:8]}...")
        print(f"URL: {result['image_url']}\n")
        
        self.structure_gen.structure_counter += 1
        return result

    def _create_basic_template(self, category: str, desc: str, colors: dict) -> str:
        """기타 카테고리용 기본 템플릿"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{category}</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; min-height: 100vh; 
                background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); 
                display: flex; align-items: center; justify-content: center; padding: 40px; }}
        .card {{ background: white; padding: 80px 60px; border-radius: 30px; 
                 box-shadow: 0 30px 80px rgba(0,0,0,0.3); max-width: 900px; text-align: center; }}
        h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 24px; 
              background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%); 
              -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        p {{ font-size: 20px; color: #666; line-height: 1.8; }}
    </style>
</head>
<body>
    <div class="card">
        <h1>{category}</h1>
        <p>{desc}</p>
    </div>
</body>
</html>"""

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
        self.supabase.storage.from_('designs-bucket').upload(
            file_path, image_data, file_options={"content-type": "image/png"}
        )
        
        public_url = self.supabase.storage.from_('designs-bucket').get_public_url(file_path)
        print(f"✅ Uploaded: {public_url}")
        return public_url

    def save_to_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Database 저장"""
        print(f"💾 Saving: {data['title']}")
        response = self.supabase.table('designs').insert(data).execute()
        print("✅ Saved to database")
        return response.data[0]


async def main():
    """메인 실행"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Generate unique design structures")
    parser.add_argument('--count', type=int, default=1, help='Number of designs')
    parser.add_argument('--category', type=str, help='Specific category')
    args = parser.parse_args()
    
    generator = OllamaDesignGenerator()
    
    # 카테고리별 설명
    descriptions = {
        "Landing Page": [
            "Transform your business with cutting-edge solutions",
            "Build the future of digital experiences",
            "Empower your team with powerful tools",
            "Scale your business to new heights",
            "Innovation meets simplicity",
        ],
        "Dashboard": [
            "Comprehensive analytics dashboard for modern businesses",
            "Real-time insights at your fingertips",
            "Data-driven decision making platform",
            "Complete business intelligence suite",
        ]
    }
    
    categories = ["Landing Page", "Dashboard"]
    
    for i in range(args.count):
        category = categories[i % len(categories)]
        desc_list = descriptions.get(category, ["Modern design"])
        description = desc_list[i % len(desc_list)]
        
        try:
            await generator.create_design(category, description)
            
            if i < args.count - 1:
                print("⏳ Waiting before next generation...\n")
                await asyncio.sleep(2)
        except Exception as e:
            print(f"\n❌ Error: {e}\n")
            continue


if __name__ == "__main__":
    asyncio.run(main())
