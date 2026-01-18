"""
Enhanced AI Design Gallery - 카테고리별 정확한 디자인 생성
DESIGN_CATEGORIES.md의 가이드라인을 따라 각 카테고리에 맞는 디자인 생성

개선 사항:
1. 각 카테고리의 필수 요소 포함
2. 더 상세한 디자인 구조
3. 카테고리별 특징을 명확히 반영
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

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    raise ValueError("Missing required environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# 색상 팔레트 (8개로 확장)
COLOR_PALETTES = [
    {"name": "Purple Dream", "primary": "#667eea", "secondary": "#764ba2", "accent": "#f093fb"},
    {"name": "Pink Sunset", "primary": "#f093fb", "secondary": "#f5576c", "accent": "#fbbf24"},
    {"name": "Ocean Blue", "primary": "#4facfe", "secondary": "#00f2fe", "accent": "#43e97b"},
    {"name": "Green Forest", "primary": "#11998e", "secondary": "#38ef7d", "accent": "#7bed9f"},
    {"name": "Orange Fire", "primary": "#fc4a1a", "secondary": "#f7b733", "accent": "#ee5a24"},
    {"name": "Violet Night", "primary": "#8e2de2", "secondary": "#4a00e0", "accent": "#c471ed"},
    {"name": "Red Passion", "primary": "#eb3349", "secondary": "#f45c43", "accent": "#fa8072"},
    {"name": "Blue Steel", "primary": "#2c3e50", "secondary": "#3498db", "accent": "#74b9ff"},
]

CATEGORIES = ["Landing Page", "Dashboard", "E-commerce", "Portfolio", "Blog", "Components"]


class EnhancedDesignGenerator:
    """카테고리별 정확한 디자인을 생성하는 클래스"""
    
    def __init__(self):
        self.used_hashes: Set[str] = set()
        self.design_count = 0
        self.current_method_name = ""  # 현재 생성 중인 메서드 이름
    
    def get_design_name(self, method_name: str) -> str:
        """구조별로 의미있는 디자인 이름 반환"""
        design_names = {
            # Landing Page (30개)
            '_landing_hero_with_features': 'Modern SaaS Landing',
            '_landing_split_with_form': 'Split Screen Signup',
            '_landing_video_background': 'Video Hero Landing',
            '_landing_product_showcase': 'Product Spotlight',
            '_landing_saas_minimal': 'Minimal Tech Platform',
            '_landing_app_download': 'App Download Page',
            '_landing_event_conference': 'Event Conference',
            '_landing_agency_creative': 'Creative Agency',
            '_landing_newsletter_subscription': 'Newsletter Signup',
            '_landing_waitlist_launch': 'Product Waitlist',
            '_landing_startup_pitch': 'Startup Pitch Deck',
            '_landing_mobile_first': 'Mobile First Design',
            '_landing_pricing_focus': 'Pricing Focused Landing',
            '_landing_testimonial_heavy': 'Testimonial Showcase',
            '_landing_feature_comparison': 'Feature Comparison',
            '_landing_animation_hero': 'Animated Hero Section',
            '_landing_two_column_benefits': 'Two Column Benefits',
            '_landing_video_testimonials': 'Video Testimonials',
            '_landing_trusted_by_logos': 'Trusted By Brands',
            '_landing_countdown_launch': 'Countdown Launch',
            '_landing_free_trial_emphasis': 'Free Trial Emphasis',
            '_landing_integration_showcase': 'Integration Showcase',
            '_landing_security_focused': 'Security Focused',
            '_landing_case_study_proof': 'Case Study Proof',
            '_landing_calculator_tool': 'ROI Calculator',
            '_landing_comparison_table': 'Comparison Table',
            '_landing_demo_request': 'Demo Request',
            '_landing_resource_download': 'Resource Download',
            '_landing_webinar_registration': 'Webinar Registration',
            '_landing_partner_program': 'Partner Program',
            
            # Dashboard (30개)
            '_dashboard_analytics_sidebar': 'Analytics Dashboard',
            '_dashboard_metrics_top_nav': 'Metrics Overview',
            '_dashboard_crm': 'CRM Pipeline',
            '_dashboard_ecommerce_stats': 'E-commerce Insights',
            '_dashboard_project_management': 'Project Tracker',
            '_dashboard_sales_analytics': 'Sales Analytics Board',
            '_dashboard_user_admin': 'User Admin Panel',
            '_dashboard_financial_overview': 'Financial Overview',
            '_dashboard_social_media_metrics': 'Social Media Metrics',
            '_dashboard_inventory_management': 'Inventory Manager',
            '_dashboard_realtime_monitoring': 'Real-time Monitoring',
            '_dashboard_team_collaboration': 'Team Collaboration',
            '_dashboard_sales_funnel': 'Sales Funnel Tracker',
            '_dashboard_marketing_campaign': 'Marketing Campaign',
            '_dashboard_customer_support': 'Customer Support Hub',
            '_dashboard_email_analytics': 'Email Analytics',
            '_dashboard_appointment_scheduling': 'Appointment Scheduler',
            '_dashboard_task_management': 'Task Management',
            '_dashboard_goal_tracking': 'Goal Tracking',
            '_dashboard_performance_review': 'Performance Review',
            '_dashboard_lead_management': 'Lead Management',
            '_dashboard_content_calendar': 'Content Calendar',
            '_dashboard_bug_tracking': 'Bug Tracking System',
            '_dashboard_time_tracking': 'Time Tracking',
            '_dashboard_resource_allocation': 'Resource Allocation',
            '_dashboard_budget_planning': 'Budget Planning',
            '_dashboard_survey_results': 'Survey Results',
            '_dashboard_network_monitoring': 'Network Monitoring',
            '_dashboard_server_status': 'Server Status',
            '_dashboard_api_analytics': 'API Analytics',
            
            # E-commerce (30개)
            '_ecommerce_product_grid': 'Product Gallery',
            '_ecommerce_product_detail': 'Product Showcase',
            '_ecommerce_cart': 'Shopping Cart',
            '_ecommerce_checkout': 'Checkout Flow',
            '_ecommerce_category': 'Category Browser',
            '_ecommerce_wishlist': 'Wishlist Manager',
            '_ecommerce_order_tracking': 'Order Tracker',
            '_ecommerce_search_results': 'Search Results',
            '_ecommerce_customer_reviews': 'Customer Reviews',
            '_ecommerce_product_comparison': 'Product Comparison',
            '_ecommerce_bundle_deals': 'Bundle Deals',
            '_ecommerce_flash_sale': 'Flash Sale',
            '_ecommerce_gift_cards': 'Gift Cards',
            '_ecommerce_subscription_plans': 'Subscription Plans',
            '_ecommerce_size_guide': 'Size Guide',
            '_ecommerce_store_locator': 'Store Locator',
            '_ecommerce_brand_story': 'Brand Story',
            '_ecommerce_wholesale_portal': 'Wholesale Portal',
            '_ecommerce_affiliate_dashboard': 'Affiliate Dashboard',
            '_ecommerce_returns_portal': 'Returns Portal',
            '_ecommerce_loyalty_program': 'Loyalty Program',
            '_ecommerce_preorder_page': 'Pre-order Page',
            '_ecommerce_waitlist': 'Sold Out Waitlist',
            '_ecommerce_deal_of_day': 'Deal of the Day',
            '_ecommerce_clearance': 'Clearance Section',
            '_ecommerce_new_arrivals': 'New Arrivals',
            '_ecommerce_best_sellers': 'Best Sellers',
            '_ecommerce_customer_account': 'Customer Account',
            '_ecommerce_payment_methods': 'Payment Methods',
            '_ecommerce_shipping_calculator': 'Shipping Calculator',
            
            # Portfolio (30개)
            '_portfolio_masonry': 'Masonry Portfolio',
            '_portfolio_minimal': 'Minimal Portfolio',
            '_portfolio_grid': 'Portfolio Grid',
            '_portfolio_case_study': 'Case Study',
            '_portfolio_timeline': 'Timeline Portfolio',
            '_portfolio_photography': 'Photography Portfolio',
            '_portfolio_developer': 'Developer Portfolio',
            '_portfolio_designer_resume': 'Designer Resume',
            '_portfolio_video_creator': 'Video Creator Portfolio',
            '_portfolio_freelancer': 'Freelancer Portfolio',
            '_portfolio_architect': 'Architect Portfolio',
            '_portfolio_writer': 'Writer Portfolio',
            '_portfolio_musician': 'Musician Portfolio',
            '_portfolio_artist': 'Artist Portfolio',
            '_portfolio_ux_researcher': 'UX Researcher',
            '_portfolio_product_manager': 'Product Manager',
            '_portfolio_marketing_specialist': 'Marketing Specialist',
            '_portfolio_data_analyst': 'Data Analyst',
            '_portfolio_consultant': 'Consultant Portfolio',
            '_portfolio_coach': 'Coach Portfolio',
            '_portfolio_speaker': 'Speaker Portfolio',
            '_portfolio_podcaster': 'Podcaster Portfolio',
            '_portfolio_youtuber': 'YouTuber Portfolio',
            '_portfolio_influencer': 'Influencer Portfolio',
            '_portfolio_photographer_pro': 'Professional Photographer',
            '_portfolio_illustrator': 'Illustrator Portfolio',
            '_portfolio_3d_artist': '3D Artist Portfolio',
            '_portfolio_motion_designer': 'Motion Designer',
            '_portfolio_brand_strategist': 'Brand Strategist',
            '_portfolio_content_creator': 'Content Creator',
            
            # Blog (30개)
            '_blog_grid': 'Blog Grid',
            '_blog_magazine': 'Magazine Layout',
            '_blog_list': 'Blog List',
            '_blog_featured': 'Featured Article',
            '_blog_sidebar': 'Blog with Sidebar',
            '_blog_personal': 'Personal Blog',
            '_blog_tech_news': 'Tech News Blog',
            '_blog_food_recipe': 'Food & Recipe Blog',
            '_blog_travel': 'Travel Blog',
            '_blog_minimal_medium': 'Minimal Medium Style',
            '_blog_interview_series': 'Interview Series',
            '_blog_tutorial_hub': 'Tutorial Hub',
            '_blog_news_aggregator': 'News Aggregator',
            '_blog_opinion_editorial': 'Opinion Editorial',
            '_blog_roundup_posts': 'Roundup Posts',
            '_blog_comparison_posts': 'Comparison Posts',
            '_blog_how_to_guides': 'How-to Guides',
            '_blog_industry_reports': 'Industry Reports',
            '_blog_guest_posts': 'Guest Posts',
            '_blog_series_saga': 'Series & Saga',
            '_blog_podcast_transcripts': 'Podcast Transcripts',
            '_blog_video_blog': 'Video Blog',
            '_blog_photo_essay': 'Photo Essay',
            '_blog_infographic_blog': 'Infographic Blog',
            '_blog_qa_format': 'Q&A Format',
            '_blog_review_blog': 'Review Blog',
            '_blog_lifestyle': 'Lifestyle Blog',
            '_blog_business': 'Business Blog',
            '_blog_educational': 'Educational Blog',
            '_blog_entertainment': 'Entertainment Blog',
            
            # Components (30개)
            '_components_showcase': 'Component Showcase',
            '_components_library': 'UI Library',
            '_components_design_system': 'Design System',
            '_components_pattern_library': 'Pattern Library',
            '_components_interactive_demo': 'Interactive Demo',
            '_components_form_elements': 'Form Elements Library',
            '_components_navigation_menus': 'Navigation Menus',
            '_components_card_layouts': 'Card Layouts',
            '_components_modal_dialogs': 'Modal Dialogs',
            '_components_pricing_tables': 'Pricing Tables',
            '_components_alerts_notifications': 'Alerts & Notifications',
            '_components_badges_labels': 'Badges & Labels',
            '_components_breadcrumbs': 'Breadcrumbs',
            '_components_buttons_collection': 'Buttons Collection',
            '_components_checkboxes_radios': 'Checkboxes & Radios',
            '_components_dropdown_menus': 'Dropdown Menus',
            '_components_file_upload': 'File Upload',
            '_components_icons_library': 'Icons Library',
            '_components_input_fields': 'Input Fields',
            '_components_loading_states': 'Loading States',
            '_components_pagination': 'Pagination',
            '_components_progress_bars': 'Progress Bars',
            '_components_search_bars': 'Search Bars',
            '_components_sliders_range': 'Sliders & Range',
            '_components_tabs_pills': 'Tabs & Pills',
            '_components_tags_chips': 'Tags & Chips',
            '_components_toggles_switches': 'Toggles & Switches',
            '_components_tooltips': 'Tooltips',
            '_components_avatars': 'Avatars',
            '_components_empty_states': 'Empty States'
        }
        return design_names.get(method_name, "Creative Design")
    
    def get_structure_hash(self, html: str) -> str:
        """구조 해시 (색상 제외)"""
        import re
        normalized = re.sub(r'#[0-9a-fA-F]{3,6}', 'COLOR', html)
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
    
    # ===== Landing Page (30가지 구조) =====
    def generate_landing_page(self, colors: dict) -> str:
        """
        랜딩 페이지 생성
        필수 요소: Hero, CTA, Features, Social Proof
        """
        layouts = [
            self._landing_hero_with_features,
            self._landing_split_with_form,
            self._landing_video_background,
            self._landing_product_showcase,
            self._landing_saas_minimal,
            self._landing_app_download,
            self._landing_event_conference,
            self._landing_agency_creative,
            self._landing_newsletter_subscription,
            self._landing_waitlist_launch,
            self._landing_startup_pitch,
            self._landing_mobile_first,
            self._landing_pricing_focus,
            self._landing_testimonial_heavy,
            self._landing_feature_comparison,
            self._landing_animation_hero,
            self._landing_two_column_benefits,
            self._landing_video_testimonials,
            self._landing_trusted_by_logos,
            self._landing_countdown_launch,
            self._landing_free_trial_emphasis,
            self._landing_integration_showcase,
            self._landing_security_focused,
            self._landing_case_study_proof,
            self._landing_calculator_tool,
            self._landing_comparison_table,
            self._landing_demo_request,
            self._landing_resource_download,
            self._landing_webinar_registration,
            self._landing_partner_program,
        ]
        chosen_method = random.choice(layouts)
        self.current_method_name = chosen_method.__name__
        return chosen_method(colors)
    
    def _landing_hero_with_features(self, colors: dict) -> str:
        """Hero 섹션 + Features 그리드 + Social Proof"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modern SaaS Platform</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; }}
        
        /* Navigation */
        nav {{ position: fixed; top: 0; width: 100%; background: rgba(255,255,255,0.95); 
               backdrop-filter: blur(10px); padding: 20px 60px; display: flex; 
               justify-content: space-between; z-index: 1000; box-shadow: 0 2px 10px rgba(0,0,0,0.05); }}
        .logo {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; }}
        .nav-links {{ display: flex; gap: 40px; align-items: center; }}
        .nav-links a {{ text-decoration: none; color: #333; font-weight: 600; }}
        .nav-cta {{ padding: 12px 32px; background: {colors['primary']}; color: white; 
                   border-radius: 8px; font-weight: 700; }}
        
        /* Hero Section */
        .hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; 
                 background: linear-gradient(135deg, {colors['primary']}15 0%, {colors['secondary']}15 100%); 
                 text-align: center; padding: 120px 40px 80px; }}
        .hero-content {{ max-width: 900px; }}
        .hero h1 {{ font-size: clamp(48px, 8vw, 84px); font-weight: 900; margin-bottom: 24px; 
                   line-height: 1.1; color: #1a1a1a; }}
        .hero p {{ font-size: clamp(20px, 3vw, 28px); color: #666; margin-bottom: 40px; line-height: 1.6; }}
        .cta-group {{ display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; }}
        .btn-primary {{ padding: 20px 48px; background: {colors['primary']}; color: white; border: none; 
                       border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; 
                       transition: all 0.3s; box-shadow: 0 4px 20px {colors['primary']}40; }}
        .btn-primary:hover {{ transform: translateY(-3px); box-shadow: 0 8px 30px {colors['primary']}50; }}
        .btn-secondary {{ padding: 20px 48px; background: transparent; border: 3px solid {colors['primary']}; 
                         color: {colors['primary']}; border-radius: 12px; font-size: 18px; 
                         font-weight: 700; cursor: pointer; transition: all 0.3s; }}
        
        /* Social Proof */
        .social-proof {{ margin-top: 60px; }}
        .social-proof p {{ font-size: 14px; color: #999; margin-bottom: 20px; }}
        .companies {{ display: flex; gap: 40px; justify-content: center; align-items: center; opacity: 0.5; }}
        .companies div {{ font-size: 24px; font-weight: 900; color: #666; }}
        
        /* Features Section */
        .features {{ padding: 120px 60px; background: white; }}
        .features h2 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 70px; }}
        .feature-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); 
                        gap: 50px; max-width: 1400px; margin: 0 auto; }}
        .feature-card {{ text-align: center; padding: 50px 30px; border-radius: 20px; 
                        transition: all 0.3s; background: #fafafa; }}
        .feature-card:hover {{ transform: translateY(-10px); box-shadow: 0 20px 50px rgba(0,0,0,0.1); }}
        .feature-icon {{ font-size: 72px; margin-bottom: 24px; }}
        .feature-card h3 {{ font-size: 28px; margin-bottom: 16px; font-weight: 800; }}
        .feature-card p {{ font-size: 18px; color: #666; line-height: 1.7; }}
        
        /* Stats Section */
        .stats {{ padding: 100px 60px; background: {colors['primary']}; color: white; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 60px; 
                      max-width: 1400px; margin: 0 auto; text-align: center; }}
        .stat-number {{ font-size: 64px; font-weight: 900; margin-bottom: 12px; }}
        .stat-label {{ font-size: 18px; opacity: 0.9; }}
        
        /* CTA Section */
        .cta-section {{ padding: 120px 60px; text-align: center; 
                        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); color: white; }}
        .cta-section h2 {{ font-size: 56px; font-weight: 900; margin-bottom: 30px; }}
        .cta-section p {{ font-size: 24px; margin-bottom: 40px; opacity: 0.95; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">ProductName</div>
        <div class="nav-links">
            <a href="#features">Features</a>
            <a href="#pricing">Pricing</a>
            <a href="#about">About</a>
            <a href="#" class="nav-cta">Get Started →</a>
        </div>
    </nav>
    
    <section class="hero">
        <div class="hero-content">
            <h1>Transform Your Business with AI</h1>
            <p>Automate workflows, increase productivity, and scale your business with our cutting-edge platform</p>
            <div class="cta-group">
                <button class="btn-primary">Start Free Trial</button>
                <button class="btn-secondary">Watch Demo</button>
            </div>
            <div class="social-proof">
                <p>TRUSTED BY LEADING COMPANIES</p>
                <div class="companies">
                    <div>ACME</div>
                    <div>TECH</div>
                    <div>GROW</div>
                    <div>SCALE</div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="features" id="features">
        <h2>Everything You Need to Succeed</h2>
        <div class="feature-grid">
            <div class="feature-card">
                <div class="feature-icon">🚀</div>
                <h3>Lightning Fast</h3>
                <p>Optimized performance that delivers results in milliseconds, not minutes</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔒</div>
                <h3>Enterprise Security</h3>
                <p>Bank-level encryption and compliance with industry standards</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3>Advanced Analytics</h3>
                <p>Deep insights into your data with real-time reporting dashboards</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🤝</div>
                <h3>Seamless Integration</h3>
                <p>Connect with 100+ tools and platforms you already use</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3>AI-Powered</h3>
                <p>Machine learning algorithms that adapt to your workflow</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">💬</div>
                <h3>24/7 Support</h3>
                <p>Expert team ready to help you succeed, anytime, anywhere</p>
            </div>
        </div>
    </section>
    
    <section class="stats">
        <div class="stats-grid">
            <div>
                <div class="stat-number">10M+</div>
                <div class="stat-label">Active Users</div>
            </div>
            <div>
                <div class="stat-number">99.9%</div>
                <div class="stat-label">Uptime</div>
            </div>
            <div>
                <div class="stat-number">150+</div>
                <div class="stat-label">Countries</div>
            </div>
            <div>
                <div class="stat-number">4.9★</div>
                <div class="stat-label">Rating</div>
            </div>
        </div>
    </section>
    
    <section class="cta-section">
        <h2>Ready to Get Started?</h2>
        <p>Join thousands of businesses already growing with our platform</p>
        <button class="btn-primary" style="background: white; color: {colors['primary']};">
            Start Your Free Trial →
        </button>
    </section>
</body>
</html>"""

    def _landing_split_with_form(self, colors: dict) -> str:
        """Split Screen: 좌측 텍스트 + 우측 가입 폼"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get Started Today</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', -apple-system, sans-serif; }}
        
        .split-container {{ display: grid; grid-template-columns: 1.2fr 1fr; min-height: 100vh; }}
        
        /* Left Side */
        .left {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                 color: white; padding: 100px 80px; display: flex; flex-direction: column; 
                 justify-content: center; }}
        .left h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 30px; line-height: 1.1; }}
        .left p {{ font-size: 22px; line-height: 1.8; margin-bottom: 50px; opacity: 0.95; }}
        
        .benefits {{ display: flex; flex-direction: column; gap: 24px; }}
        .benefit {{ display: flex; gap: 20px; align-items: flex-start; }}
        .benefit-icon {{ font-size: 32px; }}
        .benefit-text h3 {{ font-size: 20px; margin-bottom: 8px; }}
        .benefit-text p {{ font-size: 16px; opacity: 0.9; }}
        
        .testimonial {{ margin-top: 60px; padding: 30px; background: rgba(255,255,255,0.15); 
                       backdrop-filter: blur(10px); border-radius: 16px; }}
        .testimonial p {{ font-size: 18px; line-height: 1.7; margin-bottom: 16px; }}
        .author {{ font-size: 14px; font-weight: 700; opacity: 0.9; }}
        
        /* Right Side - Form */
        .right {{ background: #fafafa; padding: 100px 70px; display: flex; 
                  align-items: center; justify-content: center; }}
        .form-container {{ background: white; padding: 60px 50px; border-radius: 24px; 
                          width: 100%; max-width: 500px; box-shadow: 0 30px 80px rgba(0,0,0,0.12); }}
        .form-container h2 {{ font-size: 36px; margin-bottom: 12px; font-weight: 900; }}
        .form-container .subtitle {{ font-size: 16px; color: #666; margin-bottom: 40px; }}
        
        .form-group {{ margin-bottom: 24px; }}
        .form-label {{ font-size: 14px; font-weight: 700; margin-bottom: 8px; display: block; color: #333; }}
        .form-input {{ width: 100%; padding: 16px 20px; border: 2px solid #e0e0e0; border-radius: 12px; 
                      font-size: 16px; transition: all 0.3s; }}
        .form-input:focus {{ outline: none; border-color: {colors['primary']}; 
                            box-shadow: 0 0 0 3px {colors['primary']}20; }}
        
        .submit-btn {{ width: 100%; padding: 18px; background: {colors['primary']}; color: white; 
                      border: none; border-radius: 12px; font-size: 18px; font-weight: 700; 
                      cursor: pointer; transition: all 0.3s; margin-top: 10px; }}
        .submit-btn:hover {{ background: {colors['secondary']}; transform: translateY(-2px); 
                            box-shadow: 0 8px 20px {colors['primary']}40; }}
        
        .divider {{ text-align: center; margin: 30px 0; color: #999; font-size: 14px; }}
        
        .social-login {{ display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }}
        .social-btn {{ padding: 14px; border: 2px solid #e0e0e0; background: white; border-radius: 10px; 
                      font-weight: 600; cursor: pointer; transition: all 0.3s; }}
        .social-btn:hover {{ border-color: {colors['primary']}; background: {colors['primary']}10; }}
        
        .terms {{ font-size: 13px; color: #999; text-align: center; margin-top: 24px; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="split-container">
        <div class="left">
            <h1>Join 50,000+ Growing Businesses</h1>
            <p>Everything you need to scale your business, automate workflows, and drive growth in one powerful platform.</p>
            
            <div class="benefits">
                <div class="benefit">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <h3>No Credit Card Required</h3>
                        <p>Start your 14-day free trial instantly</p>
                    </div>
                </div>
                <div class="benefit">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <h3>Setup in Minutes</h3>
                        <p>Easy onboarding process with guided tours</p>
                    </div>
                </div>
                <div class="benefit">
                    <div class="benefit-icon">✅</div>
                    <div class="benefit-text">
                        <h3>Cancel Anytime</h3>
                        <p>No long-term contracts or commitments</p>
                    </div>
                </div>
            </div>
            
            <div class="testimonial">
                <p>"This platform helped us increase our revenue by 300% in just 6 months. The ROI was immediate and measurable."</p>
                <div class="author">— Sarah Johnson, CEO at TechCorp</div>
            </div>
        </div>
        
        <div class="right">
            <div class="form-container">
                <h2>Create Account</h2>
                <p class="subtitle">Get started with your free trial today</p>
                
                <div class="form-group">
                    <label class="form-label">Full Name</label>
                    <input type="text" class="form-input" placeholder="John Doe">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <input type="email" class="form-input" placeholder="john@company.com">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Company Name</label>
                    <input type="text" class="form-input" placeholder="Company Inc.">
                </div>
                
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-input" placeholder="••••••••">
                </div>
                
                <button class="submit-btn">Get Started Free →</button>
                
                <div class="divider">OR CONTINUE WITH</div>
                
                <div class="social-login">
                    <button class="social-btn">🔵 Google</button>
                    <button class="social-btn">📘 Facebook</button>
                </div>
                
                <p class="terms">
                    By creating an account, you agree to our<br>
                    <strong>Terms of Service</strong> and <strong>Privacy Policy</strong>
                </p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _landing_video_background(self, colors: dict) -> str:
        """Video Background Hero + Product Features"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Next Generation Platform</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', -apple-system, sans-serif; color: #1a1a1a; }}
        
        /* Fixed Navigation */
        nav {{ position: fixed; top: 0; width: 100%; z-index: 1000; 
               background: rgba(0,0,0,0.6); backdrop-filter: blur(20px); }}
        .nav-content {{ display: flex; justify-content: space-between; align-items: center; 
                       padding: 24px 60px; max-width: 1800px; margin: 0 auto; }}
        .brand {{ font-size: 28px; font-weight: 900; color: white; }}
        .nav-menu {{ display: flex; gap: 50px; }}
        .nav-menu a {{ color: white; text-decoration: none; font-weight: 600; font-size: 16px; }}
        .nav-cta {{ padding: 12px 30px; background: white; color: #1a1a1a; border-radius: 8px; 
                   font-weight: 700; }}
        
        /* Hero with Video Background */
        .hero-video {{ position: relative; height: 100vh; display: flex; align-items: center; 
                      justify-content: center; overflow: hidden; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .hero-overlay {{ position: absolute; inset: 0; background: rgba(0,0,0,0.4); }}
        .hero-content {{ position: relative; z-index: 10; text-align: center; color: white; 
                        padding: 0 40px; max-width: 1100px; }}
        .hero-content h1 {{ font-size: clamp(56px, 10vw, 120px); font-weight: 900; margin-bottom: 30px; 
                           line-height: 1; letter-spacing: -2px; }}
        .hero-content p {{ font-size: clamp(20px, 3vw, 32px); margin-bottom: 50px; opacity: 0.95; }}
        .hero-cta {{ display: inline-block; padding: 24px 60px; background: white; color: {colors['primary']}; 
                    border-radius: 14px; font-size: 20px; font-weight: 900; text-decoration: none; 
                    transition: all 0.3s; box-shadow: 0 10px 40px rgba(0,0,0,0.3); }}
        .hero-cta:hover {{ transform: translateY(-5px); box-shadow: 0 20px 60px rgba(0,0,0,0.4); }}
        
        .scroll-indicator {{ position: absolute; bottom: 40px; left: 50%; transform: translateX(-50%); 
                            color: white; font-size: 14px; animation: bounce 2s infinite; }}
        @keyframes bounce {{ 0%, 100% {{ transform: translateX(-50%) translateY(0); }} 
                            50% {{ transform: translateX(-50%) translateY(-15px); }} }}
        
        /* Features Section */
        .features {{ padding: 140px 60px; background: white; }}
        .section-header {{ text-align: center; margin-bottom: 100px; }}
        .section-header h2 {{ font-size: 64px; font-weight: 900; margin-bottom: 24px; }}
        .section-header p {{ font-size: 22px; color: #666; }}
        
        .feature-showcase {{ max-width: 1400px; margin: 0 auto; }}
        .feature-row {{ display: grid; grid-template-columns: 1fr 1fr; gap: 100px; 
                       align-items: center; margin-bottom: 120px; }}
        .feature-row:nth-child(even) {{ direction: rtl; }}
        .feature-row:nth-child(even) > * {{ direction: ltr; }}
        
        .feature-visual {{ aspect-ratio: 1.4; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                          border-radius: 24px; box-shadow: 0 30px 80px rgba(0,0,0,0.15); }}
        .feature-content h3 {{ font-size: 48px; font-weight: 900; margin-bottom: 24px; }}
        .feature-content p {{ font-size: 20px; color: #666; line-height: 1.8; margin-bottom: 30px; }}
        .feature-list {{ display: flex; flex-direction: column; gap: 16px; }}
        .feature-item {{ display: flex; gap: 16px; align-items: center; font-size: 18px; }}
        .feature-item::before {{ content: "✓"; color: {colors['accent']}; font-size: 24px; font-weight: 900; }}
        
        /* Pricing Section */
        .pricing {{ padding: 140px 60px; background: linear-gradient(180deg, #fafafa 0%, white 100%); }}
        .pricing-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; 
                        max-width: 1400px; margin: 0 auto; }}
        .pricing-card {{ background: white; padding: 60px 40px; border-radius: 24px; text-align: center; 
                        border: 3px solid #e0e0e0; transition: all 0.3s; }}
        .pricing-card.featured {{ border-color: {colors['primary']}; transform: scale(1.05); 
                                 box-shadow: 0 30px 80px {colors['primary']}30; }}
        .pricing-card:hover {{ transform: translateY(-10px); box-shadow: 0 30px 60px rgba(0,0,0,0.15); }}
        .plan-name {{ font-size: 24px; font-weight: 800; margin-bottom: 16px; color: #666; }}
        .plan-price {{ font-size: 72px; font-weight: 900; margin-bottom: 8px; color: #1a1a1a; }}
        .plan-period {{ font-size: 18px; color: #999; margin-bottom: 40px; }}
        .plan-features {{ text-align: left; margin-bottom: 40px; }}
        .plan-feature {{ padding: 16px 0; border-bottom: 1px solid #f0f0f0; font-size: 16px; }}
        .plan-btn {{ width: 100%; padding: 18px; background: {colors['primary']}; color: white; 
                    border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; }}
        .plan-btn.secondary {{ background: transparent; border: 2px solid {colors['primary']}; 
                              color: {colors['primary']}; }}
    </style>
</head>
<body>
    <nav>
        <div class="nav-content">
            <div class="brand">FUTURE</div>
            <div class="nav-menu">
                <a href="#features">Features</a>
                <a href="#pricing">Pricing</a>
                <a href="#about">About</a>
                <a href="#" class="nav-cta">Sign Up</a>
            </div>
        </div>
    </nav>
    
    <section class="hero-video">
        <div class="hero-overlay"></div>
        <div class="hero-content">
            <h1>The Future of Work</h1>
            <p>Empower your team with AI-driven tools that transform how you work</p>
            <a href="#" class="hero-cta">Get Started →</a>
        </div>
        <div class="scroll-indicator">↓ Scroll to explore</div>
    </section>
    
    <section class="features" id="features">
        <div class="section-header">
            <h2>Built for Modern Teams</h2>
            <p>Everything you need to collaborate, automate, and scale</p>
        </div>
        
        <div class="feature-showcase">
            <div class="feature-row">
                <div class="feature-visual"></div>
                <div class="feature-content">
                    <h3>Intelligent Automation</h3>
                    <p>Let AI handle repetitive tasks while you focus on what matters most. Our smart workflows adapt to your business needs.</p>
                    <div class="feature-list">
                        <div class="feature-item">Automated task routing</div>
                        <div class="feature-item">Smart scheduling</div>
                        <div class="feature-item">Predictive analytics</div>
                    </div>
                </div>
            </div>
            
            <div class="feature-row">
                <div class="feature-visual"></div>
                <div class="feature-content">
                    <h3>Real-Time Collaboration</h3>
                    <p>Work together seamlessly with your team, no matter where they are. Share files, communicate, and stay in sync.</p>
                    <div class="feature-list">
                        <div class="feature-item">Live co-editing</div>
                        <div class="feature-item">Video conferencing</div>
                        <div class="feature-item">Instant messaging</div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="pricing" id="pricing">
        <div class="section-header">
            <h2>Simple, Transparent Pricing</h2>
            <p>Choose the plan that's right for your team</p>
        </div>
        
        <div class="pricing-grid">
            <div class="pricing-card">
                <div class="plan-name">STARTER</div>
                <div class="plan-price">$29</div>
                <div class="plan-period">per month</div>
                <div class="plan-features">
                    <div class="plan-feature">Up to 10 users</div>
                    <div class="plan-feature">10GB storage</div>
                    <div class="plan-feature">Basic features</div>
                    <div class="plan-feature">Email support</div>
                </div>
                <button class="plan-btn secondary">Choose Plan</button>
            </div>
            
            <div class="pricing-card featured">
                <div class="plan-name">PROFESSIONAL</div>
                <div class="plan-price">$99</div>
                <div class="plan-period">per month</div>
                <div class="plan-features">
                    <div class="plan-feature">Up to 50 users</div>
                    <div class="plan-feature">100GB storage</div>
                    <div class="plan-feature">Advanced features</div>
                    <div class="plan-feature">Priority support</div>
                </div>
                <button class="plan-btn">Choose Plan</button>
            </div>
            
            <div class="pricing-card">
                <div class="plan-name">ENTERPRISE</div>
                <div class="plan-price">$299</div>
                <div class="plan-period">per month</div>
                <div class="plan-features">
                    <div class="plan-feature">Unlimited users</div>
                    <div class="plan-feature">1TB storage</div>
                    <div class="plan-feature">Custom features</div>
                    <div class="plan-feature">Dedicated support</div>
                </div>
                <button class="plan-btn secondary">Contact Sales</button>
            </div>
        </div>
    </section>
</body>
</html>"""

    def _landing_product_showcase(self, colors: dict) -> str:
        """Product Showcase with Interactive Elements"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Product Showcase</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', sans-serif; }}
        
        /* Hero Product */
        .hero-product {{ min-height: 100vh; display: grid; grid-template-columns: 1fr 1fr; 
                        align-items: center; padding: 80px 100px; gap: 80px; background: #fafafa; }}
        .product-info h1 {{ font-size: 72px; font-weight: 900; margin-bottom: 30px; line-height: 1.1; }}
        .product-info .tagline {{ font-size: 28px; color: {colors['primary']}; font-weight: 800; 
                                 margin-bottom: 24px; }}
        .product-info p {{ font-size: 20px; color: #666; line-height: 1.8; margin-bottom: 40px; }}
        .product-price {{ font-size: 56px; font-weight: 900; color: {colors['primary']}; margin-bottom: 40px; }}
        .buy-btn {{ padding: 24px 60px; background: {colors['primary']}; color: white; border: none; 
                   border-radius: 14px; font-size: 20px; font-weight: 900; cursor: pointer; 
                   box-shadow: 0 10px 40px {colors['primary']}40; transition: all 0.3s; }}
        .buy-btn:hover {{ transform: translateY(-3px); box-shadow: 0 15px 50px {colors['primary']}50; }}
        
        .product-visual {{ aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                          border-radius: 32px; box-shadow: 0 40px 100px rgba(0,0,0,0.2); }}
        
        /* Features Grid */
        .highlights {{ padding: 120px 100px; background: white; }}
        .highlights h2 {{ font-size: 56px; text-align: center; margin-bottom: 80px; font-weight: 900; }}
        .highlights-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 50px; }}
        .highlight {{ text-align: center; }}
        .highlight-icon {{ font-size: 64px; margin-bottom: 20px; }}
        .highlight h3 {{ font-size: 20px; font-weight: 800; margin-bottom: 12px; }}
        .highlight p {{ font-size: 16px; color: #666; }}
        
        /* Specs Section */
        .specs {{ padding: 120px 100px; background: #1a1a1a; color: white; }}
        .specs-content {{ max-width: 1400px; margin: 0 auto; }}
        .specs h2 {{ font-size: 56px; margin-bottom: 60px; font-weight: 900; }}
        .specs-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 60px; }}
        .spec-row {{ display: flex; justify-content: space-between; padding: 30px 0; 
                    border-bottom: 1px solid #333; }}
        .spec-label {{ font-size: 20px; color: #999; }}
        .spec-value {{ font-size: 20px; font-weight: 700; }}
        
        /* Gallery */
        .gallery {{ padding: 120px 100px; background: white; }}
        .gallery h2 {{ font-size: 56px; text-align: center; margin-bottom: 80px; font-weight: 900; }}
        .gallery-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; }}
        .gallery-item {{ aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}50, {colors['accent']}50); 
                        border-radius: 20px; }}
    </style>
</head>
<body>
    <section class="hero-product">
        <div class="product-info">
            <div class="tagline">INTRODUCING</div>
            <h1>The Ultimate Product</h1>
            <p>Experience the perfect blend of design, performance, and innovation. Crafted with precision for those who demand the best.</p>
            <div class="product-price">$1,299</div>
            <button class="buy-btn">Buy Now</button>
        </div>
        <div class="product-visual"></div>
    </section>
    
    <section class="highlights">
        <h2>Why You'll Love It</h2>
        <div class="highlights-grid">
            <div class="highlight">
                <div class="highlight-icon">⚡</div>
                <h3>Ultra Fast</h3>
                <p>10x faster than competition</p>
            </div>
            <div class="highlight">
                <div class="highlight-icon">🎯</div>
                <h3>Precision</h3>
                <p>Engineered to perfection</p>
            </div>
            <div class="highlight">
                <div class="highlight-icon">🌟</div>
                <h3>Premium</h3>
                <p>Luxury materials</p>
            </div>
            <div class="highlight">
                <div class="highlight-icon">♻️</div>
                <h3>Sustainable</h3>
                <p>Eco-friendly design</p>
            </div>
        </div>
    </section>
    
    <section class="specs">
        <div class="specs-content">
            <h2>Technical Specifications</h2>
            <div class="specs-grid">
                <div>
                    <div class="spec-row">
                        <div class="spec-label">Processor</div>
                        <div class="spec-value">Next-Gen Chip</div>
                    </div>
                    <div class="spec-row">
                        <div class="spec-label">Memory</div>
                        <div class="spec-value">32GB RAM</div>
                    </div>
                    <div class="spec-row">
                        <div class="spec-label">Storage</div>
                        <div class="spec-value">1TB SSD</div>
                    </div>
                </div>
                <div>
                    <div class="spec-row">
                        <div class="spec-label">Display</div>
                        <div class="spec-value">Retina 4K</div>
                    </div>
                    <div class="spec-row">
                        <div class="spec-label">Battery</div>
                        <div class="spec-value">24-hour life</div>
                    </div>
                    <div class="spec-row">
                        <div class="spec-label">Weight</div>
                        <div class="spec-value">1.2 kg</div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="gallery">
        <h2>Gallery</h2>
        <div class="gallery-grid">
            <div class="gallery-item"></div>
            <div class="gallery-item"></div>
            <div class="gallery-item"></div>
        </div>
    </section>
</body>
</html>"""

    def _landing_saas_minimal(self, colors: dict) -> str:
        """Minimal SaaS Landing with Pricing"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SaaS Platform</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; color: #1a1a1a; }}
        
        /* Minimal Hero */
        .hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; 
                 padding: 100px 40px; text-align: center; }}
        .hero-content {{ max-width: 900px; }}
        .hero h1 {{ font-size: clamp(64px, 10vw, 120px); font-weight: 900; margin-bottom: 30px; 
                   letter-spacing: -3px; }}
        .hero h1 .gradient {{ background: linear-gradient(90deg, {colors['primary']}, {colors['secondary']}); 
                             -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        .hero p {{ font-size: 26px; color: #666; margin-bottom: 50px; line-height: 1.6; }}
        .hero-cta {{ padding: 20px 50px; background: #1a1a1a; color: white; border: none; 
                    border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; 
                    transition: all 0.3s; }}
        .hero-cta:hover {{ transform: scale(1.05); }}
        
        /* Simple Features */
        .simple-features {{ padding: 120px 60px; background: #fafafa; }}
        .features-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 60px; 
                         max-width: 1400px; margin: 0 auto; }}
        .simple-feature {{ text-align: center; }}
        .simple-feature h3 {{ font-size: 32px; font-weight: 900; margin-bottom: 16px; }}
        .simple-feature p {{ font-size: 18px; color: #666; line-height: 1.7; }}
        
        /* Minimal Pricing */
        .minimal-pricing {{ padding: 120px 60px; background: white; }}
        .minimal-pricing h2 {{ font-size: 64px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .price-cards {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; 
                       max-width: 900px; margin: 0 auto; }}
        .price-card {{ padding: 60px 50px; border: 3px solid #e0e0e0; border-radius: 24px; 
                      text-align: center; transition: all 0.3s; }}
        .price-card:hover {{ border-color: {colors['primary']}; }}
        .price-card h3 {{ font-size: 20px; font-weight: 800; margin-bottom: 20px; color: #666; }}
        .price-card .amount {{ font-size: 72px; font-weight: 900; margin-bottom: 40px; }}
        .price-card ul {{ list-style: none; text-align: left; margin-bottom: 40px; }}
        .price-card li {{ padding: 12px 0; font-size: 16px; }}
        .price-card button {{ width: 100%; padding: 18px; background: {colors['primary']}; color: white; 
                             border: none; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; }}
    </style>
</head>
<body>
    <section class="hero">
        <div class="hero-content">
            <h1><span class="gradient">Simplify</span> Everything</h1>
            <p>One platform to manage your entire business. No complexity, just results.</p>
            <button class="hero-cta">Start Free Trial →</button>
        </div>
    </section>
    
    <section class="simple-features">
        <div class="features-grid">
            <div class="simple-feature">
                <h3>1. Setup</h3>
                <p>Get started in minutes with our guided onboarding</p>
            </div>
            <div class="simple-feature">
                <h3>2. Automate</h3>
                <p>Let AI handle your workflows automatically</p>
            </div>
            <div class="simple-feature">
                <h3>3. Scale</h3>
                <p>Grow your business without limits</p>
            </div>
        </div>
    </section>
    
    <section class="minimal-pricing">
        <h2>Simple Pricing</h2>
        <div class="price-cards">
            <div class="price-card">
                <h3>STARTER</h3>
                <div class="amount">$49</div>
                <ul>
                    <li>✓ All core features</li>
                    <li>✓ Up to 10 users</li>
                    <li>✓ Email support</li>
                    <li>✓ 50GB storage</li>
                </ul>
                <button>Get Started</button>
            </div>
            <div class="price-card">
                <h3>BUSINESS</h3>
                <div class="amount">$149</div>
                <ul>
                    <li>✓ Everything in Starter</li>
                    <li>✓ Unlimited users</li>
                    <li>✓ Priority support</li>
                    <li>✓ 500GB storage</li>
                </ul>
                <button>Get Started</button>
            </div>
        </div>
    </section>
</body>
</html>"""

    def _landing_app_download(self, colors: dict) -> str:
        """App Download Landing Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>App Download</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        
        .app-hero {{ min-height: 100vh; display: grid; grid-template-columns: 1fr 1fr; align-items: center; 
                     padding: 80px 100px; gap: 80px; }}
        .hero-left h1 {{ font-size: 72px; font-weight: 900; color: white; margin-bottom: 30px; line-height: 1.1; }}
        .hero-left p {{ font-size: 22px; color: rgba(255,255,255,0.9); margin-bottom: 50px; }}
        .download-buttons {{ display: flex; gap: 20px; margin-bottom: 50px; }}
        .download-btn {{ padding: 18px 40px; background: white; color: {colors['primary']}; 
                        border-radius: 12px; font-weight: 700; font-size: 16px; display: flex; 
                        align-items: center; gap: 12px; cursor: pointer; transition: all 0.3s; }}
        .download-btn:hover {{ transform: translateY(-3px); box-shadow: 0 20px 40px rgba(0,0,0,0.2); }}
        .stats {{ display: flex; gap: 50px; }}
        .stat-item h3 {{ font-size: 48px; font-weight: 900; color: white; }}
        .stat-item p {{ color: rgba(255,255,255,0.8); font-size: 14px; }}
        .phone-mockup {{ background: white; border-radius: 40px; padding: 20px; box-shadow: 0 40px 80px rgba(0,0,0,0.3); }}
        .screen {{ background: linear-gradient(180deg, #f8f9fa, #e9ecef); height: 700px; border-radius: 30px; 
                   padding: 40px; text-align: center; }}
        
        .features-section {{ padding: 100px; background: white; }}
        .features-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 60px; }}
        .feature-box {{ text-align: center; padding: 40px; }}
        .feature-icon {{ width: 80px; height: 80px; background: {colors['accent']}; border-radius: 20px; 
                        margin: 0 auto 30px; display: flex; align-items: center; justify-content: center; 
                        font-size: 36px; }}
        .feature-box h3 {{ font-size: 24px; font-weight: 700; margin-bottom: 16px; }}
        .feature-box p {{ color: #666; line-height: 1.7; }}
    </style>
</head>
<body>
    <section class="app-hero">
        <div class="hero-left">
            <h1>Your Life, Simplified</h1>
            <p>Everything you need in one beautiful app. Available now on iOS and Android.</p>
            <div class="download-buttons">
                <button class="download-btn">
                    <span style="font-size: 24px;">📱</span> App Store
                </button>
                <button class="download-btn">
                    <span style="font-size: 24px;">🤖</span> Google Play
                </button>
            </div>
            <div class="stats">
                <div class="stat-item">
                    <h3>5M+</h3>
                    <p>Downloads</p>
                </div>
                <div class="stat-item">
                    <h3>4.9★</h3>
                    <p>Rating</p>
                </div>
                <div class="stat-item">
                    <h3>50k+</h3>
                    <p>Reviews</p>
                </div>
            </div>
        </div>
        <div class="phone-mockup">
            <div class="screen">
                <h2 style="margin-top: 200px; font-size: 32px;">Beautiful Interface</h2>
                <p style="margin-top: 20px; color: #666;">Designed for everyone</p>
            </div>
        </div>
    </section>
    
    <section class="features-section">
        <div class="features-grid">
            <div class="feature-box">
                <div class="feature-icon">⚡</div>
                <h3>Lightning Fast</h3>
                <p>Optimized performance for smooth experience</p>
            </div>
            <div class="feature-box">
                <div class="feature-icon">🔒</div>
                <h3>Secure & Private</h3>
                <p>Your data is encrypted and protected</p>
            </div>
            <div class="feature-box">
                <div class="feature-icon">🌐</div>
                <h3>Works Offline</h3>
                <p>Access your content anywhere, anytime</p>
            </div>
        </div>
    </section>
</body>
</html>"""

    def _landing_event_conference(self, colors: dict) -> str:
        """Event/Conference Landing Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech Conference 2026</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; color: white; }}
        
        .event-hero {{ min-height: 100vh; padding: 120px 100px; text-align: center; 
                      background: linear-gradient(180deg, {colors['primary']}, {colors['secondary']}); }}
        .event-date {{ font-size: 18px; letter-spacing: 4px; margin-bottom: 30px; opacity: 0.9; }}
        .event-hero h1 {{ font-size: 96px; font-weight: 900; margin-bottom: 30px; line-height: 1; }}
        .event-hero .subtitle {{ font-size: 32px; margin-bottom: 50px; opacity: 0.95; }}
        .event-cta {{ padding: 24px 60px; background: white; color: {colors['primary']}; 
                     border: none; border-radius: 50px; font-size: 20px; font-weight: 800; 
                     cursor: pointer; transition: all 0.3s; }}
        .event-cta:hover {{ transform: scale(1.05); }}
        
        .speakers-section {{ padding: 100px; background: white; color: #0a0a0a; }}
        .speakers-section h2 {{ font-size: 64px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .speakers-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; }}
        .speaker-card {{ text-align: center; }}
        .speaker-avatar {{ width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}, {colors['accent']}); 
                          border-radius: 20px; margin-bottom: 20px; }}
        .speaker-card h3 {{ font-size: 22px; font-weight: 700; margin-bottom: 8px; }}
        .speaker-card p {{ color: #666; font-size: 14px; }}
        
        .schedule-section {{ padding: 100px; background: #f8f9fa; color: #0a0a0a; }}
        .schedule-section h2 {{ font-size: 64px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .schedule-timeline {{ max-width: 900px; margin: 0 auto; }}
        .schedule-item {{ display: flex; gap: 40px; padding: 40px 0; border-bottom: 2px solid #e0e0e0; }}
        .schedule-time {{ font-size: 24px; font-weight: 700; min-width: 150px; color: {colors['primary']}; }}
        .schedule-content h3 {{ font-size: 28px; font-weight: 700; margin-bottom: 12px; }}
        .schedule-content p {{ color: #666; font-size: 16px; }}
    </style>
</head>
<body>
    <section class="event-hero">
        <div class="event-date">MARCH 15-17, 2026 • SAN FRANCISCO</div>
        <h1>TECH SUMMIT</h1>
        <div class="subtitle">The Future of Innovation</div>
        <button class="event-cta">Register Now - $299</button>
    </section>
    
    <section class="speakers-section">
        <h2>Featured Speakers</h2>
        <div class="speakers-grid">
            <div class="speaker-card">
                <div class="speaker-avatar"></div>
                <h3>Sarah Chen</h3>
                <p>CEO, TechCorp</p>
            </div>
            <div class="speaker-card">
                <div class="speaker-avatar"></div>
                <h3>Michael Park</h3>
                <p>CTO, InnovateLab</p>
            </div>
            <div class="speaker-card">
                <div class="speaker-avatar"></div>
                <h3>Lisa Zhang</h3>
                <p>Founder, StartupX</p>
            </div>
            <div class="speaker-card">
                <div class="speaker-avatar"></div>
                <h3>David Kim</h3>
                <p>VP, CloudSystems</p>
            </div>
        </div>
    </section>
    
    <section class="schedule-section">
        <h2>Schedule</h2>
        <div class="schedule-timeline">
            <div class="schedule-item">
                <div class="schedule-time">9:00 AM</div>
                <div class="schedule-content">
                    <h3>Opening Keynote</h3>
                    <p>The Future of AI in Business</p>
                </div>
            </div>
            <div class="schedule-item">
                <div class="schedule-time">11:00 AM</div>
                <div class="schedule-content">
                    <h3>Panel Discussion</h3>
                    <p>Building Scalable Systems</p>
                </div>
            </div>
            <div class="schedule-item">
                <div class="schedule-time">2:00 PM</div>
                <div class="schedule-content">
                    <h3>Workshop</h3>
                    <p>Hands-on Machine Learning</p>
                </div>
            </div>
        </div>
    </section>
</body>
</html>"""

    def _landing_agency_creative(self, colors: dict) -> str:
        """Creative Agency Landing Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Creative Agency</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; color: #0a0a0a; }}
        
        .agency-hero {{ min-height: 100vh; display: flex; align-items: center; padding: 100px; }}
        .agency-hero h1 {{ font-size: 160px; font-weight: 900; line-height: 0.9; letter-spacing: -5px; }}
        .agency-hero .word {{ display: block; }}
        .agency-hero .highlight {{ color: {colors['primary']}; }}
        
        .work-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); }}
        .work-item {{ aspect-ratio: 16/10; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                     position: relative; overflow: hidden; cursor: pointer; }}
        .work-item:hover .work-overlay {{ opacity: 1; }}
        .work-overlay {{ position: absolute; inset: 0; background: rgba(0,0,0,0.8); opacity: 0; 
                        transition: opacity 0.3s; display: flex; align-items: center; justify-content: center; 
                        flex-direction: column; color: white; }}
        .work-overlay h3 {{ font-size: 48px; font-weight: 900; margin-bottom: 16px; }}
        .work-overlay p {{ font-size: 18px; }}
        
        .services-section {{ padding: 150px 100px; background: #0a0a0a; color: white; }}
        .services-section h2 {{ font-size: 96px; font-weight: 900; margin-bottom: 100px; }}
        .services-list {{ display: grid; gap: 60px; }}
        .service-item {{ display: flex; justify-content: space-between; align-items: center; 
                        padding-bottom: 60px; border-bottom: 2px solid #333; }}
        .service-item h3 {{ font-size: 64px; font-weight: 900; }}
        .service-item .number {{ font-size: 24px; color: {colors['accent']}; }}
        
        .cta-section {{ padding: 150px 100px; text-align: center; background: {colors['primary']}; color: white; }}
        .cta-section h2 {{ font-size: 96px; font-weight: 900; margin-bottom: 50px; }}
        .cta-section button {{ padding: 30px 80px; background: white; color: {colors['primary']}; 
                               border: none; font-size: 24px; font-weight: 900; cursor: pointer; 
                               border-radius: 60px; }}
    </style>
</head>
<body>
    <section class="agency-hero">
        <h1>
            <span class="word">We Create</span>
            <span class="word highlight">Experiences</span>
            <span class="word">That Matter</span>
        </h1>
    </section>
    
    <section class="work-grid">
        <div class="work-item">
            <div class="work-overlay">
                <h3>Brand Identity</h3>
                <p>TechCorp Redesign</p>
            </div>
        </div>
        <div class="work-item" style="background: linear-gradient(135deg, {colors['secondary']}, {colors['accent']});">
            <div class="work-overlay">
                <h3>Web Design</h3>
                <p>E-commerce Platform</p>
            </div>
        </div>
        <div class="work-item" style="background: linear-gradient(135deg, {colors['accent']}, {colors['primary']});">
            <div class="work-overlay">
                <h3>Mobile App</h3>
                <p>Fitness Tracker</p>
            </div>
        </div>
        <div class="work-item" style="background: linear-gradient(135deg, {colors['primary']}, {colors['accent']});">
            <div class="work-overlay">
                <h3>Marketing</h3>
                <p>Campaign Strategy</p>
            </div>
        </div>
    </section>
    
    <section class="services-section">
        <h2>Services</h2>
        <div class="services-list">
            <div class="service-item">
                <h3>Branding</h3>
                <div class="number">01</div>
            </div>
            <div class="service-item">
                <h3>Digital Design</h3>
                <div class="number">02</div>
            </div>
            <div class="service-item">
                <h3>Development</h3>
                <div class="number">03</div>
            </div>
            <div class="service-item">
                <h3>Strategy</h3>
                <div class="number">04</div>
            </div>
        </div>
    </section>
    
    <section class="cta-section">
        <h2>Let's Work Together</h2>
        <button>Start a Project</button>
    </section>
</body>
</html>"""

    def _landing_newsletter_subscription(self, colors: dict) -> str:
        """Newsletter Subscription Landing Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Newsletter Signup</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        
        .newsletter-hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; 
                           padding: 100px 60px; text-align: center; }}
        .newsletter-content {{ max-width: 800px; }}
        .newsletter-content h1 {{ font-size: 88px; font-weight: 900; margin-bottom: 30px; line-height: 1.1; }}
        .newsletter-content .highlight {{ color: {colors['primary']}; }}
        .newsletter-content p {{ font-size: 24px; color: #666; margin-bottom: 60px; line-height: 1.6; }}
        .signup-form {{ display: flex; gap: 20px; max-width: 600px; margin: 0 auto 40px; }}
        .signup-form input {{ flex: 1; padding: 24px 30px; border: 2px solid #e0e0e0; 
                             border-radius: 12px; font-size: 18px; }}
        .signup-form button {{ padding: 24px 50px; background: {colors['primary']}; color: white; 
                              border: none; border-radius: 12px; font-size: 18px; font-weight: 700; 
                              cursor: pointer; transition: all 0.3s; }}
        .signup-form button:hover {{ background: {colors['secondary']}; }}
        .trust-badges {{ display: flex; gap: 40px; justify-content: center; align-items: center; }}
        .trust-badge {{ color: #999; font-size: 14px; }}
        
        .benefits-section {{ padding: 120px 100px; background: white; }}
        .benefits-section h2 {{ font-size: 64px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .benefits-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 60px; }}
        .benefit-card {{ text-align: center; padding: 50px 30px; background: #f8f9fa; border-radius: 20px; }}
        .benefit-icon {{ width: 100px; height: 100px; background: {colors['accent']}; border-radius: 50%; 
                        margin: 0 auto 30px; display: flex; align-items: center; justify-content: center; 
                        font-size: 48px; }}
        .benefit-card h3 {{ font-size: 28px; font-weight: 700; margin-bottom: 16px; }}
        .benefit-card p {{ color: #666; line-height: 1.7; font-size: 16px; }}
        
        .social-proof {{ padding: 120px 100px; background: {colors['primary']}; color: white; text-align: center; }}
        .social-proof h2 {{ font-size: 72px; font-weight: 900; margin-bottom: 60px; }}
        .testimonials-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; max-width: 1200px; margin: 0 auto; }}
        .testimonial-card {{ background: rgba(255,255,255,0.1); padding: 50px; border-radius: 20px; text-align: left; }}
        .testimonial-card p {{ font-size: 20px; margin-bottom: 30px; line-height: 1.6; }}
        .testimonial-card .author {{ font-weight: 700; }}
    </style>
</head>
<body>
    <section class="newsletter-hero">
        <div class="newsletter-content">
            <h1>Join <span class="highlight">10,000+</span> Readers</h1>
            <p>Get weekly insights on design, technology, and innovation delivered to your inbox.</p>
            <form class="signup-form">
                <input type="email" placeholder="Enter your email">
                <button type="submit">Subscribe Free</button>
            </form>
            <div class="trust-badges">
                <div class="trust-badge">🔒 No spam, ever</div>
                <div class="trust-badge">✉️ Weekly newsletter</div>
                <div class="trust-badge">✨ Unsubscribe anytime</div>
            </div>
        </div>
    </section>
    
    <section class="benefits-section">
        <h2>What You'll Get</h2>
        <div class="benefits-grid">
            <div class="benefit-card">
                <div class="benefit-icon">📚</div>
                <h3>Expert Insights</h3>
                <p>Learn from industry leaders and stay ahead of trends</p>
            </div>
            <div class="benefit-card">
                <div class="benefit-icon">💡</div>
                <h3>Actionable Tips</h3>
                <p>Practical advice you can apply immediately</p>
            </div>
            <div class="benefit-card">
                <div class="benefit-icon">🚀</div>
                <h3>Exclusive Content</h3>
                <p>Access subscriber-only resources and guides</p>
            </div>
        </div>
    </section>
    
    <section class="social-proof">
        <h2>What Readers Say</h2>
        <div class="testimonials-grid">
            <div class="testimonial-card">
                <p>"The best newsletter I've ever subscribed to. Full of actionable insights!"</p>
                <div class="author">— Sarah K., Product Designer</div>
            </div>
            <div class="testimonial-card">
                <p>"I look forward to every issue. It's transformed how I approach my work."</p>
                <div class="author">— Michael T., Developer</div>
            </div>
        </div>
    </section>
</body>
</html>"""

    def _landing_waitlist_launch(self, colors: dict) -> str:
        """Product Waitlist/Launch Landing Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Join the Waitlist</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; color: white; }}
        
        .countdown-section {{ padding: 40px 100px; background: {colors['primary']}; text-align: center; }}
        .countdown-section p {{ font-size: 16px; letter-spacing: 2px; }}
        
        .waitlist-hero {{ min-height: 90vh; display: flex; align-items: center; justify-content: center; 
                         padding: 100px 60px; text-align: center; }}
        .waitlist-content {{ max-width: 900px; }}
        .launch-badge {{ display: inline-block; padding: 12px 30px; background: {colors['accent']}; 
                        border-radius: 50px; margin-bottom: 40px; font-size: 14px; font-weight: 700; 
                        letter-spacing: 2px; }}
        .waitlist-content h1 {{ font-size: 108px; font-weight: 900; margin-bottom: 30px; line-height: 1; }}
        .waitlist-content p {{ font-size: 28px; color: #999; margin-bottom: 60px; }}
        .waitlist-form {{ display: flex; gap: 20px; max-width: 700px; margin: 0 auto 40px; }}
        .waitlist-form input {{ flex: 1; padding: 28px 35px; background: #1a1a1a; border: 2px solid #333; 
                               color: white; border-radius: 14px; font-size: 18px; }}
        .waitlist-form input::placeholder {{ color: #666; }}
        .waitlist-form button {{ padding: 28px 60px; background: {colors['primary']}; color: white; 
                                border: none; border-radius: 14px; font-size: 18px; font-weight: 800; 
                                cursor: pointer; transition: all 0.3s; }}
        .waitlist-form button:hover {{ background: {colors['secondary']}; transform: translateY(-2px); }}
        .waitlist-count {{ font-size: 18px; color: #666; }}
        .waitlist-count span {{ color: {colors['accent']}; font-weight: 700; }}
        
        .features-preview {{ padding: 120px 100px; background: #0f0f0f; }}
        .features-preview h2 {{ font-size: 72px; font-weight: 900; text-align: center; margin-bottom: 100px; }}
        .features-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 80px; }}
        .feature-preview {{ display: flex; align-items: flex-start; gap: 30px; }}
        .feature-number {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; }}
        .feature-preview h3 {{ font-size: 32px; font-weight: 700; margin-bottom: 16px; }}
        .feature-preview p {{ color: #999; line-height: 1.7; font-size: 18px; }}
        
        .cta-footer {{ padding: 100px; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                      text-align: center; }}
        .cta-footer h2 {{ font-size: 64px; font-weight: 900; margin-bottom: 30px; }}
        .cta-footer p {{ font-size: 20px; margin-bottom: 50px; opacity: 0.9; }}
        .cta-footer button {{ padding: 28px 70px; background: white; color: {colors['primary']}; 
                             border: none; border-radius: 50px; font-size: 20px; font-weight: 800; 
                             cursor: pointer; }}
    </style>
</head>
<body>
    <div class="countdown-section">
        <p>LAUNCHING IN 30 DAYS</p>
    </div>
    
    <section class="waitlist-hero">
        <div class="waitlist-content">
            <div class="launch-badge">COMING SOON</div>
            <h1>The Future<br>Is Almost Here</h1>
            <p>Be the first to experience the next generation of productivity</p>
            <form class="waitlist-form">
                <input type="email" placeholder="Enter your email">
                <button type="submit">Join Waitlist</button>
            </form>
            <div class="waitlist-count"><span>12,847</span> people already joined</div>
        </div>
    </section>
    
    <section class="features-preview">
        <h2>What's Coming</h2>
        <div class="features-grid">
            <div class="feature-preview">
                <div class="feature-number">01</div>
                <div>
                    <h3>AI-Powered Automation</h3>
                    <p>Let artificial intelligence handle your repetitive tasks automatically</p>
                </div>
            </div>
            <div class="feature-preview">
                <div class="feature-number">02</div>
                <div>
                    <h3>Real-time Collaboration</h3>
                    <p>Work seamlessly with your team from anywhere in the world</p>
                </div>
            </div>
            <div class="feature-preview">
                <div class="feature-number">03</div>
                <div>
                    <h3>Advanced Analytics</h3>
                    <p>Get deep insights into your workflow and productivity patterns</p>
                </div>
            </div>
            <div class="feature-preview">
                <div class="feature-number">04</div>
                <div>
                    <h3>Enterprise Security</h3>
                    <p>Bank-level encryption to keep your data safe and secure</p>
                </div>
            </div>
        </div>
    </section>
    
    <section class="cta-footer">
        <h2>Don't Miss Out</h2>
        <p>Early members get lifetime 50% discount</p>
        <button>Secure Your Spot →</button>
    </section>
</body>
</html>"""

    def _landing_startup_pitch(self, colors: dict) -> str:
        """Startup Pitch Landing Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Startup Pitch</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        
        .pitch-hero {{ min-height: 90vh; display: flex; align-items: center; justify-content: center; 
                      background: linear-gradient(135deg, {colors['primary']}10, {colors['secondary']}10); 
                      padding: 80px 40px; text-align: center; }}
        .pitch-content {{ max-width: 1000px; }}
        .pitch-badge {{ display: inline-block; padding: 8px 20px; background: {colors['accent']}; 
                       color: white; border-radius: 30px; font-weight: 700; margin-bottom: 24px; }}
        .pitch-title {{ font-size: 72px; font-weight: 900; margin-bottom: 24px; line-height: 1.1; }}
        .pitch-subtitle {{ font-size: 28px; color: #666; margin-bottom: 40px; }}
        
        .pitch-cta {{ display: flex; gap: 20px; justify-content: center; margin-bottom: 60px; }}
        .btn {{ padding: 18px 48px; font-size: 18px; font-weight: 700; border-radius: 12px; 
               cursor: pointer; transition: transform 0.3s; }}
        .btn-primary {{ background: {colors['primary']}; color: white; border: none; }}
        .btn-secondary {{ background: transparent; border: 3px solid {colors['primary']}; 
                         color: {colors['primary']}; }}
        .btn:hover {{ transform: translateY(-3px); }}
        
        .traction {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; 
                    max-width: 900px; margin: 0 auto; }}
        .traction-item {{ text-align: center; }}
        .traction-number {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; }}
        .traction-label {{ font-size: 14px; color: #666; margin-top: 8px; }}
        
        .problem-solution {{ padding: 120px 60px; background: white; }}
        .section-title {{ font-size: 48px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .ps-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 80px; max-width: 1200px; margin: 0 auto; }}
        .ps-card {{ padding: 60px; border-radius: 24px; }}
        .problem {{ background: #ffebee; }}
        .solution {{ background: #e8f5e9; }}
        .ps-card h3 {{ font-size: 32px; margin-bottom: 24px; }}
        .ps-card ul {{ list-style: none; font-size: 18px; line-height: 2; }}
        .ps-card li:before {{ content: "•"; margin-right: 12px; color: {colors['primary']}; font-weight: 900; }}
        
        .team {{ padding: 120px 60px; background: #f8f9fa; }}
        .team-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 40px; 
                     max-width: 1200px; margin: 0 auto; }}
        .team-card {{ text-align: center; }}
        .team-avatar {{ width: 120px; height: 120px; border-radius: 50%; background: {colors['primary']}20; 
                       margin: 0 auto 16px; }}
        .team-name {{ font-size: 20px; font-weight: 700; margin-bottom: 4px; }}
        .team-role {{ font-size: 14px; color: #666; }}
    </style>
</head>
<body>
    <section class="pitch-hero">
        <div class="pitch-content">
            <span class="pitch-badge">Backed by Y Combinator</span>
            <h1 class="pitch-title">Revolutionizing How Teams Work</h1>
            <p class="pitch-subtitle">The all-in-one workspace that combines project management, docs, and communication</p>
            
            <div class="pitch-cta">
                <button class="btn btn-primary">Request Demo</button>
                <button class="btn btn-secondary">View Deck</button>
            </div>
            
            <div class="traction">
                <div class="traction-item">
                    <div class="traction-number">$2M</div>
                    <div class="traction-label">ARR</div>
                </div>
                <div class="traction-item">
                    <div class="traction-number">500+</div>
                    <div class="traction-label">Companies</div>
                </div>
                <div class="traction-item">
                    <div class="traction-number">150%</div>
                    <div class="traction-label">YoY Growth</div>
                </div>
                <div class="traction-item">
                    <div class="traction-number">95%</div>
                    <div class="traction-label">Retention</div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="problem-solution">
        <h2 class="section-title">The Problem & Our Solution</h2>
        <div class="ps-grid">
            <div class="ps-card problem">
                <h3>The Problem</h3>
                <ul>
                    <li>Teams use 10+ disconnected tools</li>
                    <li>Information scattered everywhere</li>
                    <li>Productivity lost in context switching</li>
                    <li>$2,500 wasted per employee/year</li>
                </ul>
            </div>
            <div class="ps-card solution">
                <h3>Our Solution</h3>
                <ul>
                    <li>One unified workspace</li>
                    <li>All information in one place</li>
                    <li>Seamless context preservation</li>
                    <li>40% increase in productivity</li>
                </ul>
            </div>
        </div>
    </section>
    
    <section class="team">
        <h2 class="section-title">Our Team</h2>
        <div class="team-grid">
            <div class="team-card">
                <div class="team-avatar"></div>
                <div class="team-name">Alex Chen</div>
                <div class="team-role">CEO, Ex-Google</div>
            </div>
            <div class="team-card">
                <div class="team-avatar"></div>
                <div class="team-name">Sarah Kim</div>
                <div class="team-role">CTO, Ex-Meta</div>
            </div>
            <div class="team-card">
                <div class="team-avatar"></div>
                <div class="team-name">Mike Johnson</div>
                <div class="team-role">CPO, Ex-Airbnb</div>
            </div>
            <div class="team-card">
                <div class="team-avatar"></div>
                <div class="team-name">Lisa Wang</div>
                <div class="team-role">Head of Growth, Ex-Stripe</div>
            </div>
        </div>
    </section>
</body>
</html>"""

    def _landing_mobile_first(self, colors: dict) -> str:
        """Mobile First Design Landing"""
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
        
        .download-buttons {{ display: flex; gap: 16px; justify-content: center; margin-bottom: 40px; }}
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

    def _landing_pricing_focus(self, colors: dict) -> str:
        """Pricing Focused Landing"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple, Transparent Pricing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        
        .pricing-header {{ padding: 100px 40px 60px; text-align: center; background: white; }}
        .pricing-header h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 16px; }}
        .pricing-header p {{ font-size: 24px; color: #666; }}
        
        .billing-toggle {{ display: flex; justify-content: center; align-items: center; gap: 16px; 
                          margin: 40px 0; }}
        .toggle-label {{ font-size: 18px; font-weight: 600; }}
        .toggle-label.active {{ color: {colors['primary']}; }}
        .toggle-switch {{ width: 60px; height: 32px; background: #ddd; border-radius: 16px; 
                         position: relative; cursor: pointer; }}
        .toggle-slider {{ width: 28px; height: 28px; background: white; border-radius: 50%; 
                         position: absolute; top: 2px; left: 2px; transition: 0.3s; }}
        
        .pricing-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; 
                        max-width: 1200px; margin: 0 auto; padding: 60px 40px; }}
        .pricing-card {{ background: white; border-radius: 24px; padding: 48px 40px; 
                        border: 3px solid #e0e0e0; transition: all 0.3s; }}
        .pricing-card:hover {{ border-color: {colors['primary']}; transform: translateY(-8px); 
                              box-shadow: 0 20px 60px rgba(0,0,0,0.1); }}
        .pricing-card.featured {{ border-color: {colors['primary']}; background: {colors['primary']}05; }}
        
        .plan-name {{ font-size: 24px; font-weight: 700; margin-bottom: 8px; }}
        .plan-price {{ font-size: 56px; font-weight: 900; margin-bottom: 8px; }}
        .plan-price span {{ font-size: 24px; }}
        .plan-period {{ color: #666; margin-bottom: 32px; }}
        
        .features-list {{ list-style: none; margin-bottom: 40px; }}
        .features-list li {{ padding: 12px 0; border-bottom: 1px solid #f0f0f0; }}
        .features-list li:before {{ content: "✓"; margin-right: 12px; color: {colors['primary']}; 
                                   font-weight: 900; }}
        
        .select-btn {{ width: 100%; padding: 18px; background: {colors['primary']}; color: white; 
                      border: none; border-radius: 12px; font-size: 18px; font-weight: 700; 
                      cursor: pointer; transition: all 0.3s; }}
        .select-btn:hover {{ background: {colors['secondary']}; }}
        
        .faq {{ padding: 100px 40px; background: white; }}
        .faq h2 {{ font-size: 48px; font-weight: 900; text-align: center; margin-bottom: 60px; }}
        .faq-list {{ max-width: 800px; margin: 0 auto; }}
        .faq-item {{ padding: 24px 0; border-bottom: 1px solid #e0e0e0; }}
        .faq-question {{ font-size: 20px; font-weight: 700; margin-bottom: 12px; }}
        .faq-answer {{ color: #666; line-height: 1.8; }}
    </style>
</head>
<body>
    <div class="pricing-header">
        <h1>Simple, Transparent Pricing</h1>
        <p>Choose the plan that's right for you</p>
        
        <div class="billing-toggle">
            <span class="toggle-label">Monthly</span>
            <div class="toggle-switch">
                <div class="toggle-slider"></div>
            </div>
            <span class="toggle-label active">Annual <span style="color: {colors['accent']};">(Save 20%)</span></span>
        </div>
    </div>
    
    <div class="pricing-grid">
        <div class="pricing-card">
            <div class="plan-name">Starter</div>
            <div class="plan-price"><span>$</span>9</div>
            <div class="plan-period">per month, billed annually</div>
            <ul class="features-list">
                <li>Up to 5 team members</li>
                <li>10 GB storage</li>
                <li>Basic support</li>
                <li>Core features</li>
            </ul>
            <button class="select-btn">Get Started</button>
        </div>
        
        <div class="pricing-card featured">
            <div class="plan-name">Professional</div>
            <div class="plan-price"><span>$</span>29</div>
            <div class="plan-period">per month, billed annually</div>
            <ul class="features-list">
                <li>Up to 20 team members</li>
                <li>100 GB storage</li>
                <li>Priority support</li>
                <li>Advanced features</li>
                <li>Custom integrations</li>
                <li>Advanced analytics</li>
            </ul>
            <button class="select-btn">Get Started</button>
        </div>
        
        <div class="pricing-card">
            <div class="plan-name">Enterprise</div>
            <div class="plan-price"><span>$</span>99</div>
            <div class="plan-period">per month, billed annually</div>
            <ul class="features-list">
                <li>Unlimited team members</li>
                <li>Unlimited storage</li>
                <li>24/7 phone support</li>
                <li>All features</li>
                <li>Dedicated account manager</li>
                <li>Custom contracts & SLA</li>
                <li>Advanced security</li>
            </ul>
            <button class="select-btn">Contact Sales</button>
        </div>
    </div>
    
    <div class="faq">
        <h2>Frequently Asked Questions</h2>
        <div class="faq-list">
            <div class="faq-item">
                <div class="faq-question">Can I change plans later?</div>
                <div class="faq-answer">Yes, you can upgrade or downgrade your plan at any time. Changes take effect immediately.</div>
            </div>
            <div class="faq-item">
                <div class="faq-question">What payment methods do you accept?</div>
                <div class="faq-answer">We accept all major credit cards, PayPal, and wire transfers for enterprise plans.</div>
            </div>
            <div class="faq-item">
                <div class="faq-question">Is there a free trial?</div>
                <div class="faq-answer">Yes, all plans come with a 14-day free trial. No credit card required.</div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _landing_testimonial_heavy(self, colors: dict) -> str:
        """Testimonial Heavy Landing"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Loved by Thousands</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; }}
        
        .hero {{ padding: 100px 40px; text-align: center; background: linear-gradient(180deg, white, {colors['primary']}10); }}
        .hero h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 24px; }}
        .hero p {{ font-size: 28px; color: #666; margin-bottom: 40px; }}
        .hero-cta {{ padding: 20px 60px; background: {colors['primary']}; color: white; border: none; 
                    border-radius: 12px; font-size: 20px; font-weight: 700; cursor: pointer; }}
        
        .stats {{ display: flex; justify-content: center; gap: 80px; margin: 60px 0; }}
        .stat-item {{ text-align: center; }}
        .stat-number {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; }}
        .stat-label {{ color: #666; margin-top: 8px; }}
        
        .testimonials {{ padding: 100px 40px; background: white; }}
        .testimonials h2 {{ font-size: 48px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .testimonial-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; 
                            max-width: 1400px; margin: 0 auto; }}
        .testimonial-card {{ padding: 40px; background: #f8f9fa; border-radius: 16px; }}
        .testimonial-stars {{ color: #ffc107; font-size: 24px; margin-bottom: 16px; }}
        .testimonial-text {{ font-size: 18px; line-height: 1.7; margin-bottom: 24px; color: #333; }}
        .testimonial-author {{ display: flex; align-items: center; gap: 16px; }}
        .author-avatar {{ width: 50px; height: 50px; border-radius: 50%; background: {colors['primary']}; }}
        .author-name {{ font-weight: 700; }}
        .author-title {{ font-size: 14px; color: #666; }}
        
        .video-testimonials {{ padding: 100px 40px; background: #f8f9fa; }}
        .video-testimonials h2 {{ font-size: 48px; font-weight: 900; text-align: center; margin-bottom: 60px; }}
        .video-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; max-width: 1200px; margin: 0 auto; }}
        .video-card {{ background: #ddd; aspect-ratio: 16/9; border-radius: 16px; position: relative; }}
        .play-btn {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                    font-size: 64px; color: white; }}
        
        .cta-final {{ padding: 100px 40px; text-align: center; background: {colors['primary']}; color: white; }}
        .cta-final h2 {{ font-size: 48px; font-weight: 900; margin-bottom: 24px; }}
        .cta-final p {{ font-size: 24px; margin-bottom: 40px; opacity: 0.95; }}
        .cta-final button {{ padding: 20px 60px; background: white; color: {colors['primary']}; 
                            border: none; border-radius: 12px; font-size: 20px; font-weight: 700; cursor: pointer; }}
    </style>
</head>
<body>
    <section class="hero">
        <h1>Join 50,000+ Happy Users</h1>
        <p>See why teams love using our platform</p>
        <button class="hero-cta">Start Free Trial</button>
        
        <div class="stats">
            <div class="stat-item">
                <div class="stat-number">4.9/5</div>
                <div class="stat-label">Average Rating</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">10,000+</div>
                <div class="stat-label">5-Star Reviews</div>
            </div>
            <div class="stat-item">
                <div class="stat-number">98%</div>
                <div class="stat-label">Would Recommend</div>
            </div>
        </div>
    </section>
    
    <section class="testimonials">
        <h2>What Our Customers Say</h2>
        <div class="testimonial-grid">
            <div class="testimonial-card">
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"This tool has completely transformed how our team works. We're 3x more productive and communication has never been better."</p>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div>
                        <div class="author-name">Sarah Johnson</div>
                        <div class="author-title">CEO, TechCorp</div>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"Best investment we've made this year. The ROI was clear within the first month. Highly recommend!"</p>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div>
                        <div class="author-name">Michael Chen</div>
                        <div class="author-title">Product Manager, StartupXYZ</div>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"Simple, powerful, and exactly what we needed. The support team is also incredibly helpful."</p>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div>
                        <div class="author-name">Emma Davis</div>
                        <div class="author-title">Director of Ops, Enterprise Inc</div>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"Game changer for remote teams. We can't imagine working without it now."</p>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div>
                        <div class="author-name">Alex Kim</div>
                        <div class="author-title">Head of Engineering, DevShop</div>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"Worth every penny. Saves us hours every week and keeps everyone aligned."</p>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div>
                        <div class="author-name">Lisa Wang</div>
                        <div class="author-title">Marketing Director, GrowthCo</div>
                    </div>
                </div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-stars">★★★★★</div>
                <p class="testimonial-text">"Finally, a tool that actually delivers on its promises. Customer success team is top-notch."</p>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div>
                        <div class="author-name">James Brown</div>
                        <div class="author-title">COO, SaaS Company</div>
                    </div>
                </div>
            </div>
        </div>
    </section>
    
    <section class="video-testimonials">
        <h2>Hear From Real Customers</h2>
        <div class="video-grid">
            <div class="video-card">
                <span class="play-btn">▶</span>
            </div>
            <div class="video-card">
                <span class="play-btn">▶</span>
            </div>
        </div>
    </section>
    
    <section class="cta-final">
        <h2>Ready to Join Them?</h2>
        <p>Start your free 14-day trial today</p>
        <button>Get Started Free</button>
    </section>
</body>
</html>"""

    def _landing_feature_comparison(self, colors: dict) -> str:
        """Feature Comparison Landing"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Feature Comparison</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        
        .comparison-hero {{ padding: 80px 40px; text-align: center; background: white; }}
        .comparison-hero h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 16px; }}
        .comparison-hero p {{ font-size: 24px; color: #666; margin-bottom: 40px; }}
        
        .comparison-table {{ max-width: 1200px; margin: 60px auto; padding: 0 40px; }}
        .table-container {{ background: white; border-radius: 24px; overflow: hidden; 
                           box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead th {{ padding: 24px; background: {colors['primary']}; color: white; font-size: 20px; 
                   font-weight: 700; text-align: left; }}
        thead th:first-child {{ text-align: left; }}
        tbody td {{ padding: 20px; border-bottom: 1px solid #f0f0f0; }}
        tbody tr:hover {{ background: #f8f9fa; }}
        .feature-name {{ font-weight: 600; }}
        .check {{ color: {colors['primary']}; font-size: 24px; font-weight: 900; }}
        .cross {{ color: #ccc; font-size: 24px; }}
        
        .cta-section {{ padding: 100px 40px; text-align: center; 
                       background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); color: white; }}
        .cta-section h2 {{ font-size: 48px; font-weight: 900; margin-bottom: 24px; }}
        .cta-section button {{ padding: 20px 60px; background: white; color: {colors['primary']}; 
                              border: none; border-radius: 12px; font-size: 20px; font-weight: 700; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="comparison-hero">
        <h1>Why Choose Us?</h1>
        <p>See how we compare to the competition</p>
    </div>
    
    <div class="comparison-table">
        <div class="table-container">
            <table>
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Us</th>
                        <th>Competitor A</th>
                        <th>Competitor B</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td class="feature-name">Unlimited Projects</td>
                        <td><span class="check">✓</span></td>
                        <td><span class="cross">✗</span></td>
                        <td><span class="check">✓</span></td>
                    </tr>
                    <tr>
                        <td class="feature-name">Advanced Analytics</td>
                        <td><span class="check">✓</span></td>
                        <td><span class="check">✓</span></td>
                        <td><span class="cross">✗</span></td>
                    </tr>
                    <tr>
                        <td class="feature-name">24/7 Support</td>
                        <td><span class="check">✓</span></td>
                        <td><span class="cross">✗</span></td>
                        <td><span class="cross">✗</span></td>
                    </tr>
                    <tr>
                        <td class="feature-name">Custom Integrations</td>
                        <td><span class="check">✓</span></td>
                        <td><span class="check">✓</span></td>
                        <td><span class="check">✓</span></td>
                    </tr>
                    <tr>
                        <td class="feature-name">White Label Options</td>
                        <td><span class="check">✓</span></td>
                        <td><span class="cross">✗</span></td>
                        <td><span class="cross">✗</span></td>
                    </tr>
                    <tr>
                        <td class="feature-name">API Access</td>
                        <td><span class="check">✓</span></td>
                        <td><span class="check">✓</span></td>
                        <td><span class="cross">✗</span></td>
                    </tr>
                    <tr>
                        <td class="feature-name">Price (monthly)</td>
                        <td><strong>$29</strong></td>
                        <td>$49</td>
                        <td>$39</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
    
    <section class="cta-section">
        <h2>Ready to Get Started?</h2>
        <button>Start Your Free Trial</button>
    </section>
</body>
</html>"""

    def _landing_animation_hero(self, colors: dict) -> str:
        """Animated Hero Section Landing"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Animated Hero Landing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; overflow-x: hidden; }}
        
        @keyframes float {{ 0%, 100% {{ transform: translateY(0); }} 50% {{ transform: translateY(-20px); }} }}
        @keyframes gradient {{ 0% {{ background-position: 0% 50%; }} 50% {{ background-position: 100% 50%; }} 100% {{ background-position: 0% 50%; }} }}
        @keyframes fadeInUp {{ from {{ opacity: 0; transform: translateY(30px); }} to {{ opacity: 1; transform: translateY(0); }} }}
        
        .animated-hero {{ min-height: 100vh; display: flex; align-items: center; justify-content: center; 
                         background: linear-gradient(-45deg, {colors['primary']}, {colors['secondary']}, {colors['accent']}, {colors['primary']}); 
                         background-size: 400% 400%; animation: gradient 15s ease infinite; position: relative; overflow: hidden; }}
        
        .floating-shapes {{ position: absolute; width: 100%; height: 100%; pointer-events: none; }}
        .shape {{ position: absolute; background: rgba(255,255,255,0.1); border-radius: 50%; }}
        .shape1 {{ width: 300px; height: 300px; top: 10%; left: 10%; animation: float 6s ease-in-out infinite; }}
        .shape2 {{ width: 200px; height: 200px; bottom: 20%; right: 15%; animation: float 8s ease-in-out infinite 1s; }}
        .shape3 {{ width: 150px; height: 150px; top: 60%; left: 70%; animation: float 7s ease-in-out infinite 2s; }}
        
        .hero-content {{ position: relative; z-index: 10; text-align: center; color: white; max-width: 1000px; 
                        padding: 40px; animation: fadeInUp 1s ease; }}
        .hero-content h1 {{ font-size: 72px; font-weight: 900; margin-bottom: 24px; line-height: 1.1; }}
        .hero-content p {{ font-size: 28px; margin-bottom: 40px; opacity: 0.95; }}
        
        .animated-cta {{ display: inline-flex; gap: 20px; }}
        .cta-btn {{ padding: 20px 48px; font-size: 18px; font-weight: 700; border-radius: 12px; 
                   cursor: pointer; transition: all 0.3s; border: none; }}
        .cta-primary {{ background: white; color: {colors['primary']}; }}
        .cta-secondary {{ background: transparent; border: 3px solid white; color: white; }}
        .cta-btn:hover {{ transform: translateY(-3px) scale(1.05); }}
        
        .features-animated {{ padding: 120px 40px; background: white; }}
        .features-animated h2 {{ font-size: 48px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .features-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 60px; max-width: 1200px; margin: 0 auto; }}
        .feature-box {{ text-align: center; animation: fadeInUp 1s ease forwards; opacity: 0; }}
        .feature-box:nth-child(1) {{ animation-delay: 0.2s; }}
        .feature-box:nth-child(2) {{ animation-delay: 0.4s; }}
        .feature-box:nth-child(3) {{ animation-delay: 0.6s; }}
        .feature-icon {{ font-size: 64px; margin-bottom: 24px; }}
        .feature-box h3 {{ font-size: 28px; margin-bottom: 16px; }}
        .feature-box p {{ font-size: 18px; color: #666; line-height: 1.7; }}
    </style>
</head>
<body>
    <section class="animated-hero">
        <div class="floating-shapes">
            <div class="shape shape1"></div>
            <div class="shape shape2"></div>
            <div class="shape shape3"></div>
        </div>
        
        <div class="hero-content">
            <h1>The Future of Productivity</h1>
            <p>Experience a new way to work with stunning animations and seamless interactions</p>
            
            <div class="animated-cta">
                <button class="cta-btn cta-primary">Get Started</button>
                <button class="cta-btn cta-secondary">Watch Demo</button>
            </div>
        </div>
    </section>
    
    <section class="features-animated">
        <h2>Why You'll Love It</h2>
        <div class="features-grid">
            <div class="feature-box">
                <div class="feature-icon">⚡</div>
                <h3>Lightning Fast</h3>
                <p>Optimized performance that feels instant</p>
            </div>
            <div class="feature-box">
                <div class="feature-icon">🎨</div>
                <h3>Beautiful Design</h3>
                <p>Stunning visuals that delight users</p>
            </div>
            <div class="feature-box">
                <div class="feature-icon">🚀</div>
                <h3>Easy to Use</h3>
                <p>Intuitive interface anyone can master</p>
            </div>
        </div>
    </section>
</body>
</html>"""

    # Adding more Landing methods continues...
    # Due to character limits, I'll create a more compact approach for the remaining methods
    
    def _landing_two_column_benefits(self, colors: dict) -> str:
        """Two Column Benefits Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Two Column Benefits</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.hero {{padding:100px 40px;text-align:center;background:{colors['primary']};color:white;}}
.hero h1 {{font-size:56px;font-weight:900;margin-bottom:24px;}}
.hero p {{font-size:24px;margin-bottom:40px;opacity:0.95;}}
.hero button {{padding:20px 48px;background:white;color:{colors['primary']};border:none;border-radius:12px;font-size:18px;font-weight:700;cursor:pointer;}}
.benefits {{padding:120px 40px;}} .benefits-grid {{display:grid;grid-template-columns:repeat(2,1fr);gap:60px;max-width:1200px;margin:0 auto;}}
.benefit-item {{display:flex;gap:24px;align-items:start;}} .benefit-icon {{font-size:48px;}}
.benefit-item h3 {{font-size:24px;margin-bottom:12px;}} .benefit-item p {{color:#666;line-height:1.7;}}</style></head>
<body><section class="hero"><h1>Everything You Need to Succeed</h1><p>Powerful features designed for modern teams</p><button>Start Free Trial</button></section>
<section class="benefits"><div class="benefits-grid">
<div class="benefit-item"><span class="benefit-icon">📊</span><div><h3>Advanced Analytics</h3><p>Get deep insights into your data with powerful analytics tools</p></div></div>
<div class="benefit-item"><span class="benefit-icon">🔄</span><div><h3>Auto Sync</h3><p>Your data automatically syncs across all devices in real-time</p></div></div>
<div class="benefit-item"><span class="benefit-icon">🔒</span><div><h3>Enterprise Security</h3><p>Bank-level encryption keeps your data safe and secure</p></div></div>
<div class="benefit-item"><span class="benefit-icon">🌐</span><div><h3>Global CDN</h3><p>Lightning-fast performance worldwide with our global infrastructure</p></div></div>
<div class="benefit-item"><span class="benefit-icon">📱</span><div><h3>Mobile Apps</h3><p>Native iOS and Android apps for working on the go</p></div></div>
<div class="benefit-item"><span class="benefit-icon">🎨</span><div><h3>Customizable</h3><p>Tailor the platform to match your exact workflow needs</p></div></div>
</div></section></body></html>"""

    def _landing_video_testimonials(self, colors: dict) -> str:
        """Video Testimonials Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Video Testimonials</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;background:#f8f9fa;}}
.hero {{padding:80px 40px;text-align:center;background:white;}} .hero h1 {{font-size:56px;font-weight:900;margin-bottom:16px;}}
.hero p {{font-size:24px;color:#666;}} .video-section {{padding:100px 40px;}}
.video-grid {{display:grid;grid-template-columns:repeat(2,1fr);gap:40px;max-width:1200px;margin:0 auto;}}
.video-card {{background:#ddd;aspect-ratio:16/9;border-radius:16px;position:relative;cursor:pointer;}}
.video-card:hover {{transform:scale(1.02);transition:0.3s;}} .play-icon {{position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);font-size:72px;color:white;}}
.customer-info {{margin-top:16px;}} .customer-name {{font-weight:700;font-size:18px;}}
.customer-title {{color:#666;font-size:14px;}}</style></head>
<body><section class="hero"><h1>Hear From Our Customers</h1><p>Real stories from real users</p></section>
<section class="video-section"><div class="video-grid">
<div><div class="video-card"><span class="play-icon">▶</span></div>
<div class="customer-info"><div class="customer-name">Sarah Johnson</div><div class="customer-title">CEO at TechCorp</div></div></div>
<div><div class="video-card"><span class="play-icon">▶</span></div>
<div class="customer-info"><div class="customer-name">Michael Chen</div><div class="customer-title">Product Lead at StartupXYZ</div></div></div>
<div><div class="video-card"><span class="play-icon">▶</span></div>
<div class="customer-info"><div class="customer-name">Emma Davis</div><div class="customer-title">Director at Enterprise Inc</div></div></div>
<div><div class="video-card"><span class="play-icon">▶</span></div>
<div class="customer-info"><div class="customer-name">Alex Kim</div><div class="customer-title">Head of Engineering</div></div></div>
</div></section></body></html>"""

    def _landing_trusted_by_logos(self, colors: dict) -> str:
        """Trusted By Logos Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Trusted By</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.hero {{padding:100px 40px;text-align:center;background:{colors['primary']};color:white;}}
.hero h1 {{font-size:64px;font-weight:900;margin-bottom:24px;}} .hero p {{font-size:28px;margin-bottom:40px;opacity:0.95;}}
.hero button {{padding:20px 60px;background:white;color:{colors['primary']};border:none;border-radius:12px;font-size:20px;font-weight:700;cursor:pointer;}}
.trusted {{padding:60px 40px;background:white;}} .trusted h3 {{text-align:center;color:#999;font-size:14px;margin-bottom:40px;letter-spacing:2px;}}
.logos {{display:grid;grid-template-columns:repeat(6,1fr);gap:40px;max-width:1200px;margin:0 auto;align-items:center;}}
.logo {{height:60px;background:#e0e0e0;border-radius:8px;}} .features {{padding:120px 40px;background:#f8f9fa;}}
.features h2 {{font-size:48px;font-weight:900;text-align:center;margin-bottom:80px;}}
.features-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:60px;max-width:1200px;margin:0 auto;}}
.feature-card {{text-align:center;}} .feature-icon {{font-size:64px;margin-bottom:24px;}}
.feature-card h3 {{font-size:24px;margin-bottom:16px;}} .feature-card p {{color:#666;line-height:1.7;}}</style></head>
<body><section class="hero"><h1>Trusted by Industry Leaders</h1><p>Join thousands of companies already using our platform</p><button>Get Started Free</button></section>
<section class="trusted"><h3>TRUSTED BY</h3><div class="logos">
<div class="logo"></div><div class="logo"></div><div class="logo"></div><div class="logo"></div><div class="logo"></div><div class="logo"></div></div></section>
<section class="features"><h2>Why Companies Choose Us</h2><div class="features-grid">
<div class="feature-card"><div class="feature-icon">🏆</div><h3>Industry Leading</h3><p>The #1 platform in our category</p></div>
<div class="feature-card"><div class="feature-icon">⚡</div><h3>Fast & Reliable</h3><p>99.99% uptime guarantee</p></div>
<div class="feature-card"><div class="feature-icon">🔒</div><h3>Enterprise Secure</h3><p>SOC 2 Type II certified</p></div>
</div></section></body></html>"""

    def _landing_countdown_launch(self, colors: dict) -> str:
        """Countdown Launch Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Countdown Launch</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;background:#000;color:white;}}
.countdown-hero {{min-height:100vh;display:flex;align-items:center;justify-content:center;text-align:center;padding:40px;}}
.countdown-content {{max-width:800px;}} .launch-badge {{display:inline-block;padding:8px 24px;background:{colors['accent']};border-radius:30px;margin-bottom:24px;font-weight:700;}}
.countdown-content h1 {{font-size:64px;font-weight:900;margin-bottom:24px;}} .countdown-content p {{font-size:24px;opacity:0.8;margin-bottom:60px;}}
.countdown {{display:flex;gap:32px;justify-content:center;margin-bottom:60px;}} .countdown-item {{text-align:center;}}
.countdown-number {{font-size:64px;font-weight:900;background:{colors['primary']};padding:24px 32px;border-radius:16px;}}
.countdown-label {{margin-top:12px;font-size:14px;opacity:0.8;}} .notify-form {{display:flex;gap:16px;max-width:500px;margin:0 auto;}}
.notify-input {{flex:1;padding:18px 24px;border:2px solid #333;background:#111;color:white;border-radius:12px;font-size:16px;}}
.notify-btn {{padding:18px 40px;background:{colors['primary']};border:none;border-radius:12px;font-weight:700;cursor:pointer;color:white;}}</style></head>
<body><section class="countdown-hero"><div class="countdown-content">
<span class="launch-badge">LAUNCHING SOON</span><h1>Something Amazing Is Coming</h1><p>Be the first to know when we launch and get exclusive early access</p>
<div class="countdown"><div class="countdown-item"><div class="countdown-number">07</div><div class="countdown-label">Days</div></div>
<div class="countdown-item"><div class="countdown-number">14</div><div class="countdown-label">Hours</div></div>
<div class="countdown-item"><div class="countdown-number">32</div><div class="countdown-label">Minutes</div></div>
<div class="countdown-item"><div class="countdown-number">18</div><div class="countdown-label">Seconds</div></div></div>
<form class="notify-form"><input type="email" class="notify-input" placeholder="Enter your email">
<button class="notify-btn">Notify Me</button></form></div></section></body></html>"""

    def _landing_free_trial_emphasis(self, colors: dict) -> str:
        """Free Trial Emphasis Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Free Trial</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.trial-hero {{padding:100px 40px;text-align:center;background:linear-gradient(135deg,{colors['primary']},{colors['secondary']});color:white;}}
.trial-badge {{display:inline-block;padding:12px 32px;background:rgba(255,255,255,0.2);backdrop-filter:blur(10px);border-radius:30px;margin-bottom:24px;font-weight:700;font-size:18px;}}
.trial-hero h1 {{font-size:72px;font-weight:900;margin-bottom:24px;}} .trial-hero p {{font-size:28px;margin-bottom:40px;opacity:0.95;}}
.trial-cta {{padding:24px 64px;background:white;color:{colors['primary']};border:none;border-radius:12px;font-size:22px;font-weight:700;cursor:pointer;margin-bottom:24px;}}
.no-cc {{font-size:14px;opacity:0.9;}} .benefits {{padding:100px 40px;background:white;}}
.benefits h2 {{font-size:48px;font-weight:900;text-align:center;margin-bottom:80px;}}
.benefits-list {{max-width:600px;margin:0 auto;}} .benefit {{display:flex;gap:24px;padding:24px;margin-bottom:16px;background:#f8f9fa;border-radius:16px;}}
.benefit-icon {{font-size:40px;}} .benefit h3 {{font-size:22px;margin-bottom:8px;}} .benefit p {{color:#666;}}</style></head>
<body><section class="trial-hero"><div><span class="trial-badge">14-DAY FREE TRIAL</span>
<h1>Try It Free for 14 Days</h1><p>No credit card required. Cancel anytime.</p>
<button class="trial-cta">Start Your Free Trial</button><p class="no-cc">✓ No credit card required</p></div></section>
<section class="benefits"><h2>What's Included in Your Trial</h2><div class="benefits-list">
<div class="benefit"><span class="benefit-icon">✓</span><div><h3>Full Access</h3><p>Access all features with no limitations during your trial</p></div></div>
<div class="benefit"><span class="benefit-icon">✓</span><div><h3>Premium Support</h3><p>Get priority support from our expert team</p></div></div>
<div class="benefit"><span class="benefit-icon">✓</span><div><h3>Easy Setup</h3><p>Get started in minutes with our guided onboarding</p></div></div>
<div class="benefit"><span class="benefit-icon">✓</span><div><h3>No Commitment</h3><p>Cancel anytime, no questions asked</p></div></div>
</div></section></body></html>"""

    def _landing_integration_showcase(self, colors: dict) -> str:
        """Integration Showcase Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Integrations</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.integrations-hero {{padding:100px 40px;text-align:center;background:white;}}
.integrations-hero h1 {{font-size:56px;font-weight:900;margin-bottom:16px;}}
.integrations-hero p {{font-size:24px;color:#666;margin-bottom:60px;}}
.integration-grid {{display:grid;grid-template-columns:repeat(6,1fr);gap:24px;max-width:1000px;margin:0 auto;}}
.integration-card {{aspect-ratio:1;background:#f8f9fa;border-radius:16px;display:flex;align-items:center;justify-content:center;font-size:40px;transition:0.3s;cursor:pointer;}}
.integration-card:hover {{transform:translateY(-8px);background:{colors['primary']}10;}}
.categories {{padding:120px 40px;background:#f8f9fa;}}
.categories h2 {{font-size:48px;font-weight:900;text-align:center;margin-bottom:60px;}}
.category-list {{display:grid;grid-template-columns:repeat(4,1fr);gap:32px;max-width:1200px;margin:0 auto;}}
.category-item {{text-align:center;padding:40px;background:white;border-radius:16px;}}
.category-icon {{font-size:48px;margin-bottom:16px;}}
.category-item h3 {{font-size:20px;margin-bottom:8px;}}
.category-item p {{color:#666;font-size:14px;}}</style></head>
<body><section class="integrations-hero"><h1>Connects With Your Favorite Tools</h1>
<p>Seamlessly integrate with 100+ popular apps and services</p>
<div class="integration-grid">
<div class="integration-card">📧</div><div class="integration-card">💬</div><div class="integration-card">📊</div>
<div class="integration-card">🗂️</div><div class="integration-card">📅</div><div class="integration-card">🎨</div>
<div class="integration-card">📝</div><div class="integration-card">💳</div><div class="integration-card">🔔</div>
<div class="integration-card">🎯</div><div class="integration-card">📈</div><div class="integration-card">🛠️</div>
</div></section>
<section class="categories"><h2>Integration Categories</h2><div class="category-list">
<div class="category-item"><div class="category-icon">📧</div><h3>Email & Communication</h3><p>Gmail, Outlook, Slack</p></div>
<div class="category-item"><div class="category-icon">📊</div><h3>Analytics & Reporting</h3><p>Google Analytics, Mixpanel</p></div>
<div class="category-item"><div class="category-icon">💳</div><h3>Payment Processing</h3><p>Stripe, PayPal, Square</p></div>
<div class="category-item"><div class="category-icon">🗂️</div><h3>File Storage</h3><p>Dropbox, Google Drive</p></div>
</div></section></body></html>"""

    def _landing_security_focused(self, colors: dict) -> str:
        """Security Focused Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Enterprise Security</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.security-hero {{padding:100px 40px;text-align:center;background:#000;color:white;}}
.security-badge {{display:inline-block;padding:8px 20px;background:{colors['accent']};border-radius:30px;margin-bottom:24px;font-weight:700;}}
.security-hero h1 {{font-size:64px;font-weight:900;margin-bottom:24px;}}
.security-hero p {{font-size:24px;opacity:0.9;margin-bottom:40px;}}
.certifications {{display:flex;gap:40px;justify-content:center;margin-top:60px;}}
.cert {{padding:24px 40px;background:#111;border-radius:12px;font-size:18px;font-weight:700;}}
.security-features {{padding:120px 40px;background:white;}}
.security-features h2 {{font-size:48px;font-weight:900;text-align:center;margin-bottom:80px;}}
.security-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:60px;max-width:1200px;margin:0 auto;}}
.security-item {{text-align:center;}} .security-icon {{font-size:64px;margin-bottom:24px;}}
.security-item h3 {{font-size:24px;margin-bottom:16px;}} .security-item p {{color:#666;line-height:1.7;}}</style></head>
<body><section class="security-hero"><span class="security-badge">ENTERPRISE GRADE</span>
<h1>Bank-Level Security</h1><p>Your data is protected with industry-leading security measures</p>
<button style="padding:20px 60px;background:white;color:#000;border:none;border-radius:12px;font-size:20px;font-weight:700;cursor:pointer;">Learn More</button>
<div class="certifications"><div class="cert">SOC 2 Type II</div><div class="cert">ISO 27001</div><div class="cert">GDPR Compliant</div></div></section>
<section class="security-features"><h2>How We Protect Your Data</h2><div class="security-grid">
<div class="security-item"><div class="security-icon">🔐</div><h3>End-to-End Encryption</h3><p>AES-256 encryption for data at rest and in transit</p></div>
<div class="security-item"><div class="security-icon">🛡️</div><h3>Advanced Threat Detection</h3><p>Real-time monitoring and automatic threat response</p></div>
<div class="security-item"><div class="security-icon">👁️</div><h3>Access Controls</h3><p>Granular permissions and role-based access</p></div>
<div class="security-item"><div class="security-icon">📍</div><h3>Audit Logs</h3><p>Complete activity tracking and compliance reporting</p></div>
<div class="security-item"><div class="security-icon">🔄</div><h3>Regular Backups</h3><p>Automated backups with point-in-time recovery</p></div>
<div class="security-item"><div class="security-icon">🌐</div><h3>DDoS Protection</h3><p>Enterprise-grade protection against attacks</p></div>
</div></section></body></html>"""

    def _landing_case_study_proof(self, colors: dict) -> str:
        """Case Study Proof Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Case Studies</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;background:#f8f9fa;}}
.case-hero {{padding:80px 40px;text-align:center;background:white;}}
.case-hero h1 {{font-size:56px;font-weight:900;margin-bottom:16px;}}
.case-hero p {{font-size:24px;color:#666;}}
.case-studies {{padding:80px 40px;}}
.case-grid {{display:grid;gap:60px;max-width:1200px;margin:0 auto;}}
.case-study {{background:white;border-radius:24px;overflow:hidden;display:grid;grid-template-columns:1fr 1fr;}}
.case-image {{background:{colors['primary']}20;min-height:400px;}}
.case-content {{padding:60px;display:flex;flex-direction:column;justify-content:center;}}
.case-logo {{font-size:32px;font-weight:900;margin-bottom:24px;}}
.case-result {{font-size:48px;font-weight:900;color:{colors['primary']};margin-bottom:16px;}}
.case-description {{font-size:18px;color:#666;line-height:1.7;margin-bottom:32px;}}
.case-cta {{display:inline-block;padding:16px 32px;background:{colors['primary']};color:white;border-radius:12px;text-decoration:none;font-weight:700;}}</style></head>
<body><section class="case-hero"><h1>Customer Success Stories</h1><p>See how companies are achieving amazing results</p></section>
<section class="case-studies"><div class="case-grid">
<div class="case-study"><div class="case-image"></div>
<div class="case-content"><div class="case-logo">TechCorp</div>
<div class="case-result">300% ROI in 6 months</div>
<p class="case-description">Learn how TechCorp increased productivity and saved $500K annually by implementing our platform across their organization.</p>
<a href="#" class="case-cta">Read Full Story →</a></div></div>
<div class="case-study"><div class="case-content"><div class="case-logo">StartupXYZ</div>
<div class="case-result">10x Faster Deployment</div>
<p class="case-description">Discover how StartupXYZ reduced their deployment time from days to hours, enabling them to ship features faster than ever.</p>
<a href="#" class="case-cta">Read Full Story →</a></div>
<div class="case-image"></div></div>
</div></section></body></html>"""

    def _landing_calculator_tool(self, colors: dict) -> str:
        """ROI Calculator Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>ROI Calculator</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.calculator-hero {{padding:80px 40px;text-align:center;background:{colors['primary']};color:white;}}
.calculator-hero h1 {{font-size:56px;font-weight:900;margin-bottom:16px;}}
.calculator-hero p {{font-size:24px;opacity:0.95;}}
.calculator-section {{padding:80px 40px;background:white;}}
.calculator-container {{max-width:800px;margin:0 auto;background:#f8f9fa;padding:60px;border-radius:24px;}}
.calculator-container h2 {{font-size:32px;margin-bottom:40px;}}
.input-group {{margin-bottom:32px;}}
.input-label {{font-size:16px;font-weight:600;margin-bottom:8px;display:block;}}
.input-field {{width:100%;padding:16px;border:2px solid #e0e0e0;border-radius:12px;font-size:18px;}}
.result-box {{background:{colors['primary']};color:white;padding:40px;border-radius:16px;text-align:center;margin-top:40px;}}
.result-label {{font-size:16px;opacity:0.9;margin-bottom:8px;}}
.result-value {{font-size:64px;font-weight:900;}}
.calc-btn {{width:100%;padding:18px;background:{colors['secondary']};color:white;border:none;border-radius:12px;font-size:18px;font-weight:700;cursor:pointer;margin-top:24px;}}</style></head>
<body><section class="calculator-hero"><h1>Calculate Your ROI</h1><p>See how much you could save with our platform</p></section>
<section class="calculator-section"><div class="calculator-container">
<h2>Enter Your Information</h2>
<div class="input-group"><label class="input-label">Number of Employees</label>
<input type="number" class="input-field" placeholder="50" value="50"></div>
<div class="input-group"><label class="input-label">Average Hourly Rate ($)</label>
<input type="number" class="input-field" placeholder="50" value="50"></div>
<div class="input-group"><label class="input-label">Hours Wasted Per Week</label>
<input type="number" class="input-field" placeholder="10" value="10"></div>
<button class="calc-btn">Calculate Savings</button>
<div class="result-box"><div class="result-label">Your Annual Savings</div>
<div class="result-value">$1.3M</div>
<p style="margin-top:16px;opacity:0.9;">Based on industry averages and your inputs</p></div>
</div></section></body></html>"""

    def _landing_comparison_table(self, colors: dict) -> str:
        """Comparison Table Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Compare Plans</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;background:#f8f9fa;}}
.compare-hero {{padding:80px 40px;text-align:center;background:white;}}
.compare-hero h1 {{font-size:56px;font-weight:900;margin-bottom:16px;}}
.compare-hero p {{font-size:24px;color:#666;}}
.comparison {{padding:80px 40px;}}
.comparison-table {{max-width:1200px;margin:0 auto;background:white;border-radius:24px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.08);}}
table {{width:100%;border-collapse:collapse;}}
thead th {{padding:32px 24px;background:{colors['primary']};color:white;font-size:20px;font-weight:700;}}
tbody td {{padding:24px;border-bottom:1px solid #f0f0f0;text-align:center;}}
tbody td:first-child {{text-align:left;font-weight:600;}}
.check {{color:{colors['primary']};font-size:24px;font-weight:900;}}
.price {{font-size:32px;font-weight:900;color:{colors['primary']};}}</style></head>
<body><section class="compare-hero"><h1>Compare Our Plans</h1><p>Find the perfect plan for your needs</p></section>
<section class="comparison"><table class="comparison-table">
<thead><tr><th>Feature</th><th>Basic</th><th>Pro</th><th>Enterprise</th></tr></thead>
<tbody>
<tr><td>Monthly Price</td><td class="price">$9</td><td class="price">$29</td><td class="price">$99</td></tr>
<tr><td>Team Members</td><td>5</td><td>20</td><td>Unlimited</td></tr>
<tr><td>Storage</td><td>10 GB</td><td>100 GB</td><td>Unlimited</td></tr>
<tr><td>Projects</td><td>10</td><td>Unlimited</td><td>Unlimited</td></tr>
<tr><td>Analytics</td><td>Basic</td><td>Advanced</td><td>Advanced</td></tr>
<tr><td>API Access</td><td>-</td><td><span class="check">✓</span></td><td><span class="check">✓</span></td></tr>
<tr><td>Priority Support</td><td>-</td><td><span class="check">✓</span></td><td><span class="check">✓</span></td></tr>
<tr><td>Custom Integrations</td><td>-</td><td>-</td><td><span class="check">✓</span></td></tr>
</tbody></table></section></body></html>"""

    def _landing_demo_request(self, colors: dict) -> str:
        """Demo Request Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Request Demo</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.demo-page {{display:grid;grid-template-columns:1fr 1fr;min-height:100vh;}}
.demo-left {{background:linear-gradient(135deg,{colors['primary']},{colors['secondary']});color:white;padding:80px 60px;display:flex;flex-direction:column;justify-content:center;}}
.demo-left h1 {{font-size:56px;font-weight:900;margin-bottom:24px;}}
.demo-left p {{font-size:24px;margin-bottom:60px;opacity:0.95;}}
.demo-benefits {{list-style:none;}}
.demo-benefits li {{padding:16px 0;font-size:20px;display:flex;align-items:center;gap:16px;}}
.demo-benefits li:before {{content:"✓";font-size:24px;font-weight:900;}}
.demo-right {{background:white;padding:80px 60px;display:flex;align-items:center;}}
.demo-form {{width:100%;max-width:500px;}}
.demo-form h2 {{font-size:32px;margin-bottom:32px;}}
.form-group {{margin-bottom:24px;}}
.form-label {{display:block;font-weight:600;margin-bottom:8px;}}
.form-input {{width:100%;padding:16px;border:2px solid #e0e0e0;border-radius:12px;font-size:16px;}}
.form-input:focus {{outline:none;border-color:{colors['primary']};}}
.demo-btn {{width:100%;padding:18px;background:{colors['primary']};color:white;border:none;border-radius:12px;font-size:18px;font-weight:700;cursor:pointer;margin-top:16px;}}</style></head>
<body><div class="demo-page">
<div class="demo-left"><h1>See It In Action</h1><p>Schedule a personalized demo with our team</p>
<ul class="demo-benefits">
<li>30-minute personalized walkthrough</li>
<li>See how it works for your use case</li>
<li>Get all your questions answered</li>
<li>No obligation or commitment required</li>
</ul></div>
<div class="demo-right"><form class="demo-form">
<h2>Request Your Demo</h2>
<div class="form-group"><label class="form-label">Full Name</label>
<input type="text" class="form-input" placeholder="John Doe"></div>
<div class="form-group"><label class="form-label">Work Email</label>
<input type="email" class="form-input" placeholder="john@company.com"></div>
<div class="form-group"><label class="form-label">Company Name</label>
<input type="text" class="form-input" placeholder="Acme Inc"></div>
<div class="form-group"><label class="form-label">Phone Number</label>
<input type="tel" class="form-input" placeholder="+1 (555) 000-0000"></div>
<button type="submit" class="demo-btn">Schedule Demo</button>
</form></div></div></body></html>"""

    def _landing_resource_download(self, colors: dict) -> str:
        """Resource Download Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Download Guide</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.resource-hero {{padding:100px 40px;background:{colors['primary']};color:white;text-align:center;}}
.resource-hero h1 {{font-size:56px;font-weight:900;margin-bottom:16px;}}
.resource-hero p {{font-size:24px;opacity:0.95;}}
.download-section {{padding:80px 40px;background:white;}}
.download-container {{max-width:1000px;margin:0 auto;display:grid;grid-template-columns:1fr 1fr;gap:60px;align-items:center;}}
.resource-preview {{background:#f8f9fa;aspect-ratio:8.5/11;border-radius:16px;box-shadow:0 20px 60px rgba(0,0,0,0.15);}}
.download-form {{max-width:450px;}}
.download-form h2 {{font-size:36px;margin-bottom:16px;}}
.download-form p {{color:#666;margin-bottom:32px;line-height:1.7;}}
.form-group {{margin-bottom:20px;}}
.form-label {{display:block;font-weight:600;margin-bottom:8px;}}
.form-input {{width:100%;padding:16px;border:2px solid #e0e0e0;border-radius:12px;font-size:16px;}}
.download-btn {{width:100%;padding:18px;background:{colors['primary']};color:white;border:none;border-radius:12px;font-size:18px;font-weight:700;cursor:pointer;}}
.trust-badge {{text-align:center;margin-top:16px;color:#666;font-size:14px;}}</style></head>
<body><section class="resource-hero"><h1>Free Ultimate Guide</h1><p>Everything you need to know in one comprehensive resource</p></section>
<section class="download-section"><div class="download-container">
<div class="resource-preview"></div>
<div class="download-form"><h2>Download Your Free Copy</h2>
<p>Get instant access to our comprehensive 50-page guide with proven strategies and actionable insights.</p>
<form><div class="form-group"><label class="form-label">First Name</label>
<input type="text" class="form-input" placeholder="John"></div>
<div class="form-group"><label class="form-label">Email Address</label>
<input type="email" class="form-input" placeholder="john@example.com"></div>
<button type="submit" class="download-btn">Download Free Guide</button>
<p class="trust-badge">🔒 We respect your privacy. Unsubscribe anytime.</p>
</form></div></div></section></body></html>"""

    def _landing_webinar_registration(self, colors: dict) -> str:
        """Webinar Registration Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Webinar Registration</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;background:#f8f9fa;}}
.webinar-hero {{padding:80px 40px;text-align:center;background:white;}}
.live-badge {{display:inline-block;padding:8px 20px;background:#e74c3c;color:white;border-radius:30px;margin-bottom:24px;font-weight:700;animation:pulse 2s infinite;}}
@keyframes pulse {{0%,100% {{opacity:1;}} 50% {{opacity:0.7;}}}}
.webinar-hero h1 {{font-size:56px;font-weight:900;margin-bottom:16px;}}
.webinar-date {{font-size:24px;color:{colors['primary']};font-weight:700;margin-bottom:40px;}}
.registration-section {{padding:80px 40px;}}
.reg-container {{max-width:1200px;margin:0 auto;display:grid;grid-template-columns:2fr 1fr;gap:60px;}}
.webinar-details h2 {{font-size:36px;margin-bottom:24px;}}
.webinar-details p {{font-size:18px;color:#666;line-height:1.8;margin-bottom:32px;}}
.topics {{list-style:none;}}
.topics li {{padding:16px 0;font-size:18px;border-bottom:1px solid #e0e0e0;display:flex;gap:16px;}}
.topics li:before {{content:"✓";color:{colors['primary']};font-weight:900;}}
.reg-form {{background:white;padding:40px;border-radius:24px;box-shadow:0 4px 20px rgba(0,0,0,0.08);}}
.reg-form h3 {{font-size:24px;margin-bottom:24px;}}
.form-group {{margin-bottom:20px;}}
.form-input {{width:100%;padding:16px;border:2px solid #e0e0e0;border-radius:12px;font-size:16px;}}
.reg-btn {{width:100%;padding:18px;background:{colors['primary']};color:white;border:none;border-radius:12px;font-size:18px;font-weight:700;cursor:pointer;}}</style></head>
<body><section class="webinar-hero"><span class="live-badge">🔴 LIVE WEBINAR</span>
<h1>Master Modern Design Systems</h1>
<p class="webinar-date">📅 Thursday, February 15, 2024 at 2:00 PM EST</p></section>
<section class="registration-section"><div class="reg-container">
<div class="webinar-details"><h2>What You'll Learn</h2>
<p>Join our expert panel for an in-depth discussion on building scalable design systems that work for teams of all sizes.</p>
<ul class="topics">
<li>Setting up a design system from scratch</li>
<li>Component architecture best practices</li>
<li>Scaling across multiple platforms</li>
<li>Collaboration between design and development</li>
<li>Real-world case studies and examples</li>
</ul></div>
<div class="reg-form"><h3>Register Now</h3>
<form><div class="form-group"><input type="text" class="form-input" placeholder="Full Name"></div>
<div class="form-group"><input type="email" class="form-input" placeholder="Email Address"></div>
<div class="form-group"><input type="text" class="form-input" placeholder="Job Title"></div>
<button type="submit" class="reg-btn">Reserve Your Spot</button>
<p style="text-align:center;margin-top:16px;font-size:14px;color:#666;">Limited to 500 attendees</p>
</form></div></div></section></body></html>"""

    def _landing_partner_program(self, colors: dict) -> str:
        """Partner Program Landing"""
        return f"""<!DOCTYPE html>
<html><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>Partner Program</title>
<style>* {{margin:0;padding:0;box-sizing:border-box;}} body {{font-family:'Inter',sans-serif;}}
.partner-hero {{padding:100px 40px;text-align:center;background:linear-gradient(135deg,{colors['primary']},{colors['secondary']});color:white;}}
.partner-hero h1 {{font-size:64px;font-weight:900;margin-bottom:24px;}}
.partner-hero p {{font-size:28px;margin-bottom:40px;opacity:0.95;}}
.partner-hero button {{padding:20px 60px;background:white;color:{colors['primary']};border:none;border-radius:12px;font-size:20px;font-weight:700;cursor:pointer;}}
.benefits {{padding:120px 40px;background:white;}}
.benefits h2 {{font-size:48px;font-weight:900;text-align:center;margin-bottom:80px;}}
.benefits-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:60px;max-width:1200px;margin:0 auto;}}
.benefit-card {{text-align:center;}}
.benefit-icon {{font-size:72px;margin-bottom:24px;}}
.benefit-card h3 {{font-size:28px;margin-bottom:16px;}}
.benefit-card p {{color:#666;font-size:18px;line-height:1.7;}}
.tiers {{padding:120px 40px;background:#f8f9fa;}}
.tiers h2 {{font-size:48px;font-weight:900;text-align:center;margin-bottom:80px;}}
.tier-grid {{display:grid;grid-template-columns:repeat(3,1fr);gap:32px;max-width:1200px;margin:0 auto;}}
.tier-card {{background:white;padding:50px 40px;border-radius:24px;text-align:center;}}
.tier-name {{font-size:24px;font-weight:700;margin-bottom:16px;}}
.tier-commission {{font-size:56px;font-weight:900;color:{colors['primary']};margin-bottom:24px;}}
.tier-features {{list-style:none;margin-bottom:32px;}}
.tier-features li {{padding:12px 0;}}
.tier-btn {{width:100%;padding:16px;background:{colors['primary']};color:white;border:none;border-radius:12px;font-weight:700;cursor:pointer;}}</style></head>
<body><section class="partner-hero"><h1>Become a Partner</h1><p>Join our partner program and earn generous commissions</p>
<button>Apply Now</button></section>
<section class="benefits"><h2>Why Partner With Us</h2><div class="benefits-grid">
<div class="benefit-card"><div class="benefit-icon">💰</div><h3>High Commissions</h3><p>Earn up to 30% recurring commission on every sale</p></div>
<div class="benefit-card"><div class="benefit-icon">🎯</div><h3>Proven Product</h3><p>Sell a product customers love with 98% satisfaction rate</p></div>
<div class="benefit-card"><div class="benefit-icon">📊</div><h3>Real-Time Tracking</h3><p>Monitor your performance with our advanced dashboard</p></div>
<div class="benefit-card"><div class="benefit-icon">🎓</div><h3>Training & Resources</h3><p>Access comprehensive training and marketing materials</p></div>
<div class="benefit-card"><div class="benefit-icon">🤝</div><h3>Dedicated Support</h3><p>Get help from our dedicated partner success team</p></div>
<div class="benefit-card"><div class="benefit-icon">🚀</div><h3>Fast Payouts</h3><p>Receive payments quickly via your preferred method</p></div>
</div></section>
<section class="tiers"><h2>Partner Tiers</h2><div class="tier-grid">
<div class="tier-card"><div class="tier-name">Bronze</div><div class="tier-commission">20%</div>
<ul class="tier-features"><li>20% commission</li><li>Marketing materials</li><li>Email support</li></ul>
<button class="tier-btn">Start Free</button></div>
<div class="tier-card"><div class="tier-name">Silver</div><div class="tier-commission">25%</div>
<ul class="tier-features"><li>25% commission</li><li>Priority support</li><li>Co-marketing opportunities</li></ul>
<button class="tier-btn">Qualify at $5K MRR</button></div>
<div class="tier-card"><div class="tier-name">Gold</div><div class="tier-commission">30%</div>
<ul class="tier-features"><li>30% commission</li><li>Dedicated partner manager</li><li>Custom integrations</li></ul>
<button class="tier-btn">Qualify at $20K MRR</button></div>
</div></section></body></html>"""

    # ===== Dashboard (30가지 구조) =====
    def generate_dashboard(self, colors: dict) -> str:
        """
        대시보드 생성
        필수 요소: Stats Cards, Charts, Navigation, Tables, Activity Feed
        """
        layouts = [
            self._dashboard_analytics_sidebar,
            self._dashboard_metrics_top_nav,
            self._dashboard_crm,
            self._dashboard_ecommerce_stats,
            self._dashboard_project_management,
            self._dashboard_sales_analytics,
            self._dashboard_user_admin,
            self._dashboard_financial_overview,
            self._dashboard_social_media_metrics,
            self._dashboard_inventory_management,
            self._dashboard_realtime_monitoring,
            self._dashboard_team_collaboration,
            self._dashboard_sales_funnel,
            self._dashboard_marketing_campaign,
            self._dashboard_customer_support,
            self._dashboard_email_analytics,
            self._dashboard_appointment_scheduling,
            self._dashboard_task_management,
            self._dashboard_goal_tracking,
            self._dashboard_performance_review,
            self._dashboard_lead_management,
            self._dashboard_content_calendar,
            self._dashboard_bug_tracking,
            self._dashboard_time_tracking,
            self._dashboard_resource_allocation,
            self._dashboard_budget_planning,
            self._dashboard_survey_results,
            self._dashboard_network_monitoring,
            self._dashboard_server_status,
            self._dashboard_api_analytics,
        ]
        chosen_method = random.choice(layouts)
        self.current_method_name = chosen_method.__name__
        return chosen_method(colors)
    
    def _dashboard_analytics_sidebar(self, colors: dict) -> str:
        """Analytics Dashboard with Sidebar"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        .layout {{ display: grid; grid-template-columns: 280px 1fr; height: 100vh; }}
        
        /* Sidebar */
        .sidebar {{ background: linear-gradient(180deg, {colors['primary']}, {colors['secondary']}); 
                    color: white; padding: 40px 0; overflow-y: auto; }}
        .logo {{ padding: 0 30px; font-size: 28px; font-weight: 900; margin-bottom: 50px; }}
        .nav-section {{ padding: 0 20px; margin-bottom: 40px; }}
        .nav-title {{ font-size: 12px; opacity: 0.7; margin-bottom: 16px; padding: 0 10px; 
                     font-weight: 700; letter-spacing: 1px; }}
        .nav-item {{ padding: 14px 16px; margin-bottom: 4px; border-radius: 12px; cursor: pointer; 
                    transition: all 0.3s; display: flex; align-items: center; gap: 12px; }}
        .nav-item:hover {{ background: rgba(255,255,255,0.15); }}
        .nav-item.active {{ background: rgba(255,255,255,0.2); font-weight: 700; }}
        
        /* Main Content */
        .main {{ overflow-y: auto; padding: 40px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }}
        .header h1 {{ font-size: 36px; font-weight: 900; }}
        .date-range {{ padding: 12px 24px; border: 2px solid #e0e0e0; border-radius: 12px; 
                      background: white; cursor: pointer; }}
        
        /* Stats Grid */
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 40px; }}
        .stat-card {{ background: white; padding: 32px; border-radius: 16px; 
                      box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
        .stat-label {{ font-size: 14px; color: #666; margin-bottom: 12px; font-weight: 600; }}
        .stat-value {{ font-size: 42px; font-weight: 900; color: #1a1a1a; margin-bottom: 8px; }}
        .stat-change {{ font-size: 14px; font-weight: 700; }}
        .stat-change.up {{ color: #10b981; }}
        .stat-change.down {{ color: #ef4444; }}
        
        /* Charts */
        .charts {{ display: grid; grid-template-columns: 2fr 1fr; gap: 24px; margin-bottom: 40px; }}
        .chart-card {{ background: white; padding: 32px; border-radius: 16px; 
                      box-shadow: 0 2px 12px rgba(0,0,0,0.06); }}
        .chart-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
        .chart-header h3 {{ font-size: 20px; font-weight: 800; }}
        .chart-placeholder {{ height: 300px; background: linear-gradient(180deg, {colors['primary']}20 0%, transparent); 
                             border-radius: 12px; display: flex; align-items: flex-end; padding: 20px; }}
        .bar {{ width: 100%; height: 60%; background: {colors['primary']}; border-radius: 8px 8px 0 0; }}
        
        /* Activity List */
        .activity-item {{ padding: 20px 0; border-bottom: 1px solid #f0f0f0; display: flex; gap: 16px; }}
        .activity-icon {{ width: 48px; height: 48px; border-radius: 12px; display: flex; 
                         align-items: center; justify-content: center; font-size: 20px; 
                         background: {colors['primary']}20; }}
        .activity-content {{ flex: 1; }}
        .activity-title {{ font-size: 16px; font-weight: 700; margin-bottom: 4px; }}
        .activity-time {{ font-size: 14px; color: #999; }}
    </style>
</head>
<body>
    <div class="layout">
        <div class="sidebar">
            <div class="logo">Analytics Pro</div>
            <div class="nav-section">
                <div class="nav-title">MAIN</div>
                <div class="nav-item active">📊 Dashboard</div>
                <div class="nav-item">📈 Analytics</div>
                <div class="nav-item">💰 Revenue</div>
            </div>
            <div class="nav-section">
                <div class="nav-title">MANAGE</div>
                <div class="nav-item">👥 Users</div>
                <div class="nav-item">📦 Products</div>
                <div class="nav-item">🎯 Campaigns</div>
            </div>
            <div class="nav-section">
                <div class="nav-title">SYSTEM</div>
                <div class="nav-item">⚙️ Settings</div>
                <div class="nav-item">🔔 Notifications</div>
            </div>
        </div>
        
        <div class="main">
            <div class="header">
                <h1>Dashboard Overview</h1>
                <div class="date-range">📅 Last 30 days</div>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-label">TOTAL REVENUE</div>
                    <div class="stat-value">$54,329</div>
                    <div class="stat-change up">↑ 12.5% from last month</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">NEW CUSTOMERS</div>
                    <div class="stat-value">3,421</div>
                    <div class="stat-change up">↑ 8.2% from last month</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">ACTIVE USERS</div>
                    <div class="stat-value">12,847</div>
                    <div class="stat-change down">↓ 2.1% from last month</div>
                </div>
                <div class="stat-card">
                    <div class="stat-label">CONVERSION RATE</div>
                    <div class="stat-value">18.2%</div>
                    <div class="stat-change up">↑ 5.8% from last month</div>
                </div>
            </div>
            
            <div class="charts">
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>Revenue Trend</h3>
                        <select style="padding: 8px 16px; border: 2px solid #e0e0e0; border-radius: 8px;">
                            <option>Last 7 days</option>
                            <option>Last 30 days</option>
                            <option>Last 90 days</option>
                        </select>
                    </div>
                    <div class="chart-placeholder">
                        <div class="bar"></div>
                    </div>
                </div>
                
                <div class="chart-card">
                    <div class="chart-header">
                        <h3>Recent Activity</h3>
                    </div>
                    <div class="activity-item">
                        <div class="activity-icon">🛒</div>
                        <div class="activity-content">
                            <div class="activity-title">New order placed</div>
                            <div class="activity-time">2 minutes ago</div>
                        </div>
                    </div>
                    <div class="activity-item">
                        <div class="activity-icon">👤</div>
                        <div class="activity-content">
                            <div class="activity-title">User registered</div>
                            <div class="activity-time">12 minutes ago</div>
                        </div>
                    </div>
                    <div class="activity-item">
                        <div class="activity-icon">💳</div>
                        <div class="activity-content">
                            <div class="activity-title">Payment received</div>
                            <div class="activity-time">1 hour ago</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_metrics_top_nav(self, colors: dict) -> str:
        """Metrics Dashboard with Top Navigation"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Metrics Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; background: #fafbfc; }}
        
        /* Top Navigation */
        .top-nav {{ background: white; padding: 20px 60px; display: flex; 
                    justify-content: space-between; align-items: center; 
                    box-shadow: 0 1px 3px rgba(0,0,0,0.1); position: sticky; top: 0; z-index: 100; }}
        .nav-brand {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; }}
        .nav-tabs {{ display: flex; gap: 40px; }}
        .nav-tab {{ padding: 12px 0; font-weight: 600; color: #666; cursor: pointer; 
                   border-bottom: 3px solid transparent; transition: all 0.3s; }}
        .nav-tab.active {{ color: {colors['primary']}; border-bottom-color: {colors['primary']}; }}
        .nav-actions {{ display: flex; gap: 16px; }}
        .icon-btn {{ width: 40px; height: 40px; border-radius: 10px; border: 2px solid #e0e0e0; 
                    display: flex; align-items: center; justify-content: center; cursor: pointer; background: white; }}
        
        /* Container */
        .container {{ max-width: 1600px; margin: 0 auto; padding: 50px 60px; }}
        .page-header {{ margin-bottom: 40px; }}
        .page-header h1 {{ font-size: 48px; font-weight: 900; margin-bottom: 12px; }}
        .page-header p {{ font-size: 18px; color: #666; }}
        
        /* Metric Cards */
        .metrics {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-bottom: 40px; }}
        .metric {{ background: white; padding: 40px; border-radius: 20px; 
                  box-shadow: 0 2px 12px rgba(0,0,0,0.08); border-left: 6px solid {colors['primary']}; }}
        .metric:nth-child(2) {{ border-left-color: {colors['secondary']}; }}
        .metric:nth-child(3) {{ border-left-color: {colors['accent']}; }}
        .metric-label {{ font-size: 14px; font-weight: 700; color: #666; margin-bottom: 16px; 
                        text-transform: uppercase; letter-spacing: 1px; }}
        .metric-value {{ font-size: 56px; font-weight: 900; margin-bottom: 12px; }}
        .metric-trend {{ font-size: 16px; }}
        .trend-up {{ color: #10b981; font-weight: 700; }}
        .trend-down {{ color: #ef4444; font-weight: 700; }}
        
        /* Data Grid */
        .data-section {{ background: white; padding: 40px; border-radius: 20px; 
                        box-shadow: 0 2px 12px rgba(0,0,0,0.08); }}
        .data-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 30px; }}
        .data-header h2 {{ font-size: 28px; font-weight: 900; }}
        .data-table {{ width: 100%; }}
        .data-table th {{ text-align: left; padding: 16px; background: #f8f9fa; 
                         font-size: 14px; font-weight: 700; color: #666; }}
        .data-table td {{ padding: 20px 16px; border-bottom: 1px solid #f0f0f0; }}
        .data-table tr:last-child td {{ border-bottom: none; }}
        .status-badge {{ padding: 6px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; }}
        .status-success {{ background: #d1fae5; color: #065f46; }}
        .status-pending {{ background: #fef3c7; color: #92400e; }}
    </style>
</head>
<body>
    <div class="top-nav">
        <div class="nav-brand">Dashboard Pro</div>
        <div class="nav-tabs">
            <div class="nav-tab active">Overview</div>
            <div class="nav-tab">Reports</div>
            <div class="nav-tab">Team</div>
            <div class="nav-tab">Settings</div>
        </div>
        <div class="nav-actions">
            <button class="icon-btn">🔔</button>
            <button class="icon-btn">👤</button>
        </div>
    </div>
    
    <div class="container">
        <div class="page-header">
            <h1>Dashboard Overview</h1>
            <p>Track your key metrics and performance indicators</p>
        </div>
        
        <div class="metrics">
            <div class="metric">
                <div class="metric-label">Total Revenue</div>
                <div class="metric-value">$94,527</div>
                <div class="metric-trend trend-up">↑ 23.1% vs last month</div>
            </div>
            <div class="metric">
                <div class="metric-label">New Customers</div>
                <div class="metric-value">2,847</div>
                <div class="metric-trend trend-up">↑ 12.4% vs last month</div>
            </div>
            <div class="metric">
                <div class="metric-label">Conversion Rate</div>
                <div class="metric-value">18.2%</div>
                <div class="metric-trend trend-up">↑ 5.8% vs last month</div>
            </div>
        </div>
        
        <div class="data-section">
            <div class="data-header">
                <h2>Recent Transactions</h2>
                <button style="padding: 10px 24px; background: {colors['primary']}; color: white; 
                               border: none; border-radius: 10px; font-weight: 700; cursor: pointer;">
                    Export Data
                </button>
            </div>
            <table class="data-table">
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
                        <td>John Smith</td>
                        <td>$1,259.00</td>
                        <td><span class="status-badge status-success">Completed</span></td>
                        <td>Jan 18, 2026</td>
                    </tr>
                    <tr>
                        <td>#ORD-002</td>
                        <td>Sarah Johnson</td>
                        <td>$849.00</td>
                        <td><span class="status-badge status-pending">Pending</span></td>
                        <td>Jan 18, 2026</td>
                    </tr>
                    <tr>
                        <td>#ORD-003</td>
                        <td>Mike Davis</td>
                        <td>$2,149.00</td>
                        <td><span class="status-badge status-success">Completed</span></td>
                        <td>Jan 17, 2026</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_crm(self, colors: dict) -> str:
        """CRM Dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CRM Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Montserrat', sans-serif; background: #f5f7fa; }}
        .container {{ padding: 60px; max-width: 1800px; margin: 0 auto; }}
        
        /* Header */
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 50px; }}
        .header h1 {{ font-size: 48px; font-weight: 900; }}
        .header-actions {{ display: flex; gap: 16px; }}
        .btn {{ padding: 14px 32px; border-radius: 12px; font-weight: 700; cursor: pointer; border: none; }}
        .btn-primary {{ background: {colors['primary']}; color: white; }}
        .btn-secondary {{ background: white; border: 2px solid #e0e0e0; }}
        
        /* Pipeline */
        .pipeline {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 50px; }}
        .pipeline-stage {{ background: white; padding: 30px; border-radius: 20px; 
                          box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}
        .stage-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px; }}
        .stage-title {{ font-size: 16px; font-weight: 800; color: #666; }}
        .stage-count {{ background: {colors['primary']}; color: white; padding: 4px 12px; 
                       border-radius: 12px; font-size: 14px; font-weight: 700; }}
        .deal-card {{ background: #f8f9fa; padding: 20px; border-radius: 12px; margin-bottom: 12px; }}
        .deal-name {{ font-size: 16px; font-weight: 700; margin-bottom: 8px; }}
        .deal-value {{ font-size: 20px; font-weight: 900; color: {colors['primary']}; }}
        
        /* Team Performance */
        .team {{ background: white; padding: 40px; border-radius: 20px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.06); }}
        .team h2 {{ font-size: 32px; font-weight: 900; margin-bottom: 30px; }}
        .member-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }}
        .member-card {{ text-align: center; padding: 30px; background: #f8f9fa; border-radius: 16px; }}
        .avatar {{ width: 80px; height: 80px; border-radius: 50%; 
                  background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                  margin: 0 auto 16px; }}
        .member-name {{ font-size: 18px; font-weight: 800; margin-bottom: 8px; }}
        .member-role {{ font-size: 14px; color: #999; margin-bottom: 16px; }}
        .member-stat {{ font-size: 28px; font-weight: 900; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Sales Pipeline</h1>
            <div class="header-actions">
                <button class="btn btn-secondary">Filters</button>
                <button class="btn btn-primary">+ New Deal</button>
            </div>
        </div>
        
        <div class="pipeline">
            <div class="pipeline-stage">
                <div class="stage-header">
                    <div class="stage-title">LEAD</div>
                    <div class="stage-count">12</div>
                </div>
                <div class="deal-card">
                    <div class="deal-name">Acme Corp</div>
                    <div class="deal-value">$15,000</div>
                </div>
                <div class="deal-card">
                    <div class="deal-name">TechStart Inc</div>
                    <div class="deal-value">$8,500</div>
                </div>
            </div>
            
            <div class="pipeline-stage">
                <div class="stage-header">
                    <div class="stage-title">QUALIFIED</div>
                    <div class="stage-count">8</div>
                </div>
                <div class="deal-card">
                    <div class="deal-name">Global Systems</div>
                    <div class="deal-value">$32,000</div>
                </div>
            </div>
            
            <div class="pipeline-stage">
                <div class="stage-header">
                    <div class="stage-title">PROPOSAL</div>
                    <div class="stage-count">5</div>
                </div>
                <div class="deal-card">
                    <div class="deal-name">Enterprise Co</div>
                    <div class="deal-value">$125,000</div>
                </div>
            </div>
            
            <div class="pipeline-stage">
                <div class="stage-header">
                    <div class="stage-title">CLOSED WON</div>
                    <div class="stage-count">24</div>
                </div>
                <div class="deal-card">
                    <div class="deal-name">Big Client LLC</div>
                    <div class="deal-value">$50,000</div>
                </div>
            </div>
        </div>
        
        <div class="team">
            <h2>Team Performance</h2>
            <div class="member-grid">
                <div class="member-card">
                    <div class="avatar"></div>
                    <div class="member-name">Sarah Wilson</div>
                    <div class="member-role">Sales Manager</div>
                    <div class="member-stat">$285K</div>
                </div>
                <div class="member-card">
                    <div class="avatar"></div>
                    <div class="member-name">Mike Chen</div>
                    <div class="member-role">Account Executive</div>
                    <div class="member-stat">$192K</div>
                </div>
                <div class="member-card">
                    <div class="avatar"></div>
                    <div class="member-name">Emma Davis</div>
                    <div class="member-role">Sales Rep</div>
                    <div class="member-stat">$143K</div>
                </div>
                <div class="member-card">
                    <div class="avatar"></div>
                    <div class="member-name">John Park</div>
                    <div class="member-role">Sales Rep</div>
                    <div class="member-stat">$128K</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_ecommerce_stats(self, colors: dict) -> str:
        """E-commerce Stats Dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>E-commerce Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #fafafa; padding: 60px; }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        
        h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 50px; text-align: center; }}
        
        /* Overview Cards */
        .overview {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 40px; }}
        .overview-card {{ background: white; padding: 40px; border-radius: 20px; 
                         box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .overview-label {{ font-size: 14px; color: #999; margin-bottom: 12px; }}
        .overview-value {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; }}
        
        /* Charts Grid */
        .charts-grid {{ display: grid; grid-template-columns: 2fr 1fr; gap: 24px; margin-bottom: 40px; }}
        .chart-box {{ background: white; padding: 40px; border-radius: 20px; 
                     box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .chart-title {{ font-size: 24px; font-weight: 900; margin-bottom: 30px; }}
        .chart-visual {{ height: 300px; background: linear-gradient(180deg, {colors['primary']}20, transparent); 
                        border-radius: 12px; }}
        
        /* Best Sellers */
        .product-list {{ display: flex; flex-direction: column; gap: 16px; }}
        .product-item {{ display: flex; justify-content: space-between; align-items: center; 
                        padding: 20px; background: #f8f9fa; border-radius: 12px; }}
        .product-info {{ display: flex; gap: 16px; align-items: center; }}
        .product-thumb {{ width: 60px; height: 60px; border-radius: 8px; 
                         background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .product-name {{ font-size: 16px; font-weight: 700; }}
        .product-sales {{ font-size: 20px; font-weight: 900; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>E-commerce Overview</h1>
        
        <div class="overview">
            <div class="overview-card">
                <div class="overview-label">TODAY'S SALES</div>
                <div class="overview-value">$8,549</div>
            </div>
            <div class="overview-card">
                <div class="overview-label">TOTAL ORDERS</div>
                <div class="overview-value">1,284</div>
            </div>
            <div class="overview-card">
                <div class="overview-label">CUSTOMERS</div>
                <div class="overview-value">9,842</div>
            </div>
            <div class="overview-card">
                <div class="overview-label">AVG ORDER</div>
                <div class="overview-value">$127</div>
            </div>
        </div>
        
        <div class="charts-grid">
            <div class="chart-box">
                <div class="chart-title">Sales Trend (Last 30 Days)</div>
                <div class="chart-visual"></div>
            </div>
            
            <div class="chart-box">
                <div class="chart-title">Top Products</div>
                <div class="product-list">
                    <div class="product-item">
                        <div class="product-info">
                            <div class="product-thumb"></div>
                            <div class="product-name">Premium Headphones</div>
                        </div>
                        <div class="product-sales">892</div>
                    </div>
                    <div class="product-item">
                        <div class="product-info">
                            <div class="product-thumb"></div>
                            <div class="product-name">Wireless Mouse</div>
                        </div>
                        <div class="product-sales">743</div>
                    </div>
                    <div class="product-item">
                        <div class="product-info">
                            <div class="product-thumb"></div>
                            <div class="product-name">Laptop Stand</div>
                        </div>
                        <div class="product-sales">621</div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_project_management(self, colors: dict) -> str:
        """Project Management Dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Project Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; padding: 60px; }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 50px; }}
        .header h1 {{ font-size: 48px; font-weight: 900; }}
        
        /* Project Cards */
        .projects {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-bottom: 40px; }}
        .project-card {{ background: white; padding: 40px; border-radius: 24px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .project-header {{ display: flex; justify-content: space-between; align-items: start; margin-bottom: 24px; }}
        .project-name {{ font-size: 24px; font-weight: 900; }}
        .project-status {{ padding: 8px 16px; border-radius: 20px; font-size: 12px; font-weight: 700; }}
        .status-active {{ background: #d1fae5; color: #065f46; }}
        .status-pending {{ background: #fef3c7; color: #92400e; }}
        .project-progress {{ margin-bottom: 20px; }}
        .progress-label {{ font-size: 14px; color: #666; margin-bottom: 8px; }}
        .progress-bar {{ height: 8px; background: #e0e0e0; border-radius: 4px; overflow: hidden; }}
        .progress-fill {{ height: 100%; background: {colors['primary']}; }}
        .project-team {{ display: flex; gap: 8px; }}
        .team-avatar {{ width: 40px; height: 40px; border-radius: 50%; 
                       background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                       border: 3px solid white; }}
        
        /* Tasks */
        .tasks {{ background: white; padding: 40px; border-radius: 24px; 
                 box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .tasks h2 {{ font-size: 32px; font-weight: 900; margin-bottom: 30px; }}
        .task-item {{ display: flex; gap: 16px; padding: 20px; border-radius: 12px; 
                     margin-bottom: 12px; background: #f8f9fa; }}
        .task-checkbox {{ width: 24px; height: 24px; border-radius: 6px; border: 3px solid {colors['primary']}; }}
        .task-content {{ flex: 1; }}
        .task-title {{ font-size: 16px; font-weight: 700; margin-bottom: 8px; }}
        .task-meta {{ font-size: 14px; color: #999; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Projects Dashboard</h1>
            <button style="padding: 16px 32px; background: {colors['primary']}; color: white; 
                           border: none; border-radius: 12px; font-weight: 700; cursor: pointer;">
                + New Project
            </button>
        </div>
        
        <div class="projects">
            <div class="project-card">
                <div class="project-header">
                    <div class="project-name">Website Redesign</div>
                    <div class="project-status status-active">Active</div>
                </div>
                <div class="project-progress">
                    <div class="progress-label">Progress: 68%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 68%;"></div>
                    </div>
                </div>
                <div class="project-team">
                    <div class="team-avatar"></div>
                    <div class="team-avatar"></div>
                    <div class="team-avatar"></div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-header">
                    <div class="project-name">Mobile App</div>
                    <div class="project-status status-active">Active</div>
                </div>
                <div class="project-progress">
                    <div class="progress-label">Progress: 42%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 42%;"></div>
                    </div>
                </div>
                <div class="project-team">
                    <div class="team-avatar"></div>
                    <div class="team-avatar"></div>
                </div>
            </div>
            
            <div class="project-card">
                <div class="project-header">
                    <div class="project-name">Marketing Campaign</div>
                    <div class="project-status status-pending">Pending</div>
                </div>
                <div class="project-progress">
                    <div class="progress-label">Progress: 15%</div>
                    <div class="progress-bar">
                        <div class="progress-fill" style="width: 15%;"></div>
                    </div>
                </div>
                <div class="project-team">
                    <div class="team-avatar"></div>
                </div>
            </div>
        </div>
        
        <div class="tasks">
            <h2>Today's Tasks</h2>
            <div class="task-item">
                <div class="task-checkbox"></div>
                <div class="task-content">
                    <div class="task-title">Review design mockups</div>
                    <div class="task-meta">Website Redesign • Due today</div>
                </div>
            </div>
            <div class="task-item">
                <div class="task-checkbox"></div>
                <div class="task-content">
                    <div class="task-title">Update project timeline</div>
                    <div class="task-meta">Mobile App • Due in 2 days</div>
                </div>
            </div>
            <div class="task-item">
                <div class="task-checkbox"></div>
                <div class="task-content">
                    <div class="task-title">Client meeting preparation</div>
                    <div class="task-meta">Marketing Campaign • Due tomorrow</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _dashboard_sales_analytics(self, colors: dict) -> str:
        """Sales Analytics Dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sales Analytics</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        .container {{ max-width: 1800px; margin: 0 auto; padding: 40px; }}
        
        .header {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                  color: white; padding: 50px; border-radius: 24px; margin-bottom: 40px; }}
        .header h1 {{ font-size: 48px; font-weight: 900; margin-bottom: 12px; }}
        .header p {{ font-size: 20px; opacity: 0.9; }}
        
        /* KPI Cards */
        .kpi-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 40px; }}
        .kpi-card {{ background: white; padding: 32px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .kpi-label {{ font-size: 14px; color: #999; font-weight: 600; margin-bottom: 8px; }}
        .kpi-value {{ font-size: 42px; font-weight: 900; color: {colors['primary']}; margin-bottom: 12px; }}
        .kpi-change {{ font-size: 14px; font-weight: 700; }}
        .kpi-change.positive {{ color: #10b981; }}
        .kpi-change.negative {{ color: #ef4444; }}
        
        /* Charts */
        .charts {{ display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin-bottom: 40px; }}
        .chart-card {{ background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .chart-card h3 {{ font-size: 24px; font-weight: 900; margin-bottom: 30px; }}
        .chart-bars {{ display: flex; align-items: flex-end; gap: 20px; height: 300px; }}
        .bar {{ flex: 1; background: linear-gradient(180deg, {colors['primary']}, {colors['secondary']}); 
               border-radius: 8px 8px 0 0; }}
        
        /* Top Products */
        .top-products {{ }}
        .product-item {{ display: flex; justify-content: space-between; align-items: center; 
                        padding: 20px; background: #f8f9fa; border-radius: 12px; margin-bottom: 12px; }}
        .product-name {{ font-weight: 700; }}
        .product-sales {{ font-size: 18px; font-weight: 900; color: {colors['primary']}; }}
        
        /* Sales Table */
        .table-card {{ background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .table-card h3 {{ font-size: 24px; font-weight: 900; margin-bottom: 30px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; padding: 16px; background: #f8f9fa; font-weight: 700; }}
        td {{ padding: 16px; border-bottom: 1px solid #f0f0f0; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Sales Analytics</h1>
            <p>Real-time sales performance and insights</p>
        </div>
        
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-label">Total Revenue</div>
                <div class="kpi-value">$847K</div>
                <div class="kpi-change positive">↑ 23.5%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Orders</div>
                <div class="kpi-value">2,847</div>
                <div class="kpi-change positive">↑ 18.2%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Avg Order Value</div>
                <div class="kpi-value">$297</div>
                <div class="kpi-change negative">↓ 3.1%</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-label">Conversion Rate</div>
                <div class="kpi-value">3.8%</div>
                <div class="kpi-change positive">↑ 0.4%</div>
            </div>
        </div>
        
        <div class="charts">
            <div class="chart-card">
                <h3>Monthly Sales Trend</h3>
                <div class="chart-bars">
                    <div class="bar" style="height: 65%;"></div>
                    <div class="bar" style="height: 78%;"></div>
                    <div class="bar" style="height: 82%;"></div>
                    <div class="bar" style="height: 70%;"></div>
                    <div class="bar" style="height: 88%;"></div>
                    <div class="bar" style="height: 95%;"></div>
                    <div class="bar" style="height: 100%;"></div>
                    <div class="bar" style="height: 92%;"></div>
                </div>
            </div>
            <div class="chart-card top-products">
                <h3>Top Products</h3>
                <div class="product-item">
                    <span class="product-name">Premium Package</span>
                    <span class="product-sales">$127K</span>
                </div>
                <div class="product-item">
                    <span class="product-name">Standard Package</span>
                    <span class="product-sales">$98K</span>
                </div>
                <div class="product-item">
                    <span class="product-name">Basic Package</span>
                    <span class="product-sales">$76K</span>
                </div>
                <div class="product-item">
                    <span class="product-name">Enterprise</span>
                    <span class="product-sales">$54K</span>
                </div>
            </div>
        </div>
        
        <div class="table-card">
            <h3>Recent Transactions</h3>
            <table>
                <thead>
                    <tr>
                        <th>Order ID</th>
                        <th>Customer</th>
                        <th>Product</th>
                        <th>Amount</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>#ORD-2847</td>
                        <td>John Smith</td>
                        <td>Premium Package</td>
                        <td>$499</td>
                        <td style="color: #10b981; font-weight: 700;">Completed</td>
                    </tr>
                    <tr>
                        <td>#ORD-2846</td>
                        <td>Sarah Johnson</td>
                        <td>Standard Package</td>
                        <td>$299</td>
                        <td style="color: #10b981; font-weight: 700;">Completed</td>
                    </tr>
                    <tr>
                        <td>#ORD-2845</td>
                        <td>Mike Davis</td>
                        <td>Enterprise</td>
                        <td>$1,299</td>
                        <td style="color: #f59e0b; font-weight: 700;">Pending</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</body>
</html>"""
    
    def _dashboard_user_admin(self, colors: dict) -> str:
        """User Administration Dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>User Admin</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; }}
        
        .admin-layout {{ display: grid; grid-template-columns: 260px 1fr; min-height: 100vh; }}
        
        /* Sidebar */
        .sidebar {{ background: white; border-right: 2px solid #e0e0e0; padding: 40px 0; }}
        .logo {{ padding: 0 30px; font-size: 26px; font-weight: 900; color: {colors['primary']}; margin-bottom: 50px; }}
        .nav-item {{ padding: 16px 30px; cursor: pointer; transition: all 0.3s; font-weight: 600; }}
        .nav-item:hover {{ background: #f8f9fa; }}
        .nav-item.active {{ background: {colors['primary']}; color: white; }}
        
        /* Main Content */
        .main {{ padding: 50px; }}
        .page-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }}
        .page-header h1 {{ font-size: 42px; font-weight: 900; }}
        .add-user-btn {{ padding: 16px 32px; background: {colors['primary']}; color: white; border: none; 
                        border-radius: 12px; font-weight: 700; cursor: pointer; }}
        
        /* Stats Cards */
        .stats {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 40px; }}
        .stat-card {{ background: white; padding: 32px; border-radius: 16px; box-shadow: 0 2px 15px rgba(0,0,0,0.06); }}
        .stat-number {{ font-size: 36px; font-weight: 900; color: {colors['primary']}; margin-bottom: 8px; }}
        .stat-label {{ font-size: 14px; color: #666; font-weight: 600; }}
        
        /* Users Table */
        .users-table {{ background: white; border-radius: 20px; overflow: hidden; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .table-header {{ padding: 24px 32px; background: #f8f9fa; border-bottom: 2px solid #e0e0e0; }}
        .table-header h2 {{ font-size: 22px; font-weight: 900; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; padding: 20px 32px; background: white; font-weight: 700; 
             border-bottom: 2px solid #f0f0f0; }}
        td {{ padding: 20px 32px; border-bottom: 1px solid #f0f0f0; }}
        .user-avatar {{ width: 45px; height: 45px; border-radius: 50%; 
                       background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                       display: inline-block; vertical-align: middle; margin-right: 12px; }}
        .user-name {{ font-weight: 700; font-size: 16px; }}
        .user-role {{ display: inline-block; padding: 6px 14px; border-radius: 20px; font-size: 12px; 
                     font-weight: 700; }}
        .role-admin {{ background: #fef3c7; color: #92400e; }}
        .role-user {{ background: #dbeafe; color: #1e40af; }}
        .role-moderator {{ background: #e0e7ff; color: #4338ca; }}
        .action-btn {{ padding: 8px 16px; border: 2px solid {colors['primary']}; background: white; 
                      color: {colors['primary']}; border-radius: 8px; font-weight: 600; cursor: pointer; 
                      margin-right: 8px; }}
    </style>
</head>
<body>
    <div class="admin-layout">
        <div class="sidebar">
            <div class="logo">Admin</div>
            <div class="nav-item active">Users</div>
            <div class="nav-item">Roles</div>
            <div class="nav-item">Permissions</div>
            <div class="nav-item">Activity Log</div>
            <div class="nav-item">Settings</div>
        </div>
        
        <div class="main">
            <div class="page-header">
                <h1>User Management</h1>
                <button class="add-user-btn">+ Add New User</button>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <div class="stat-number">2,847</div>
                    <div class="stat-label">Total Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">1,234</div>
                    <div class="stat-label">Active Today</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">184</div>
                    <div class="stat-label">New This Week</div>
                </div>
                <div class="stat-card">
                    <div class="stat-number">23</div>
                    <div class="stat-label">Admins</div>
                </div>
            </div>
            
            <div class="users-table">
                <div class="table-header">
                    <h2>All Users</h2>
                </div>
                <table>
                    <thead>
                        <tr>
                            <th>User</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td>
                                <div class="user-avatar"></div>
                                <span class="user-name">John Smith</span>
                            </td>
                            <td>john.smith@company.com</td>
                            <td><span class="user-role role-admin">Admin</span></td>
                            <td style="color: #10b981; font-weight: 700;">Active</td>
                            <td>
                                <button class="action-btn">Edit</button>
                                <button class="action-btn">Delete</button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div class="user-avatar"></div>
                                <span class="user-name">Sarah Johnson</span>
                            </td>
                            <td>sarah.j@company.com</td>
                            <td><span class="user-role role-moderator">Moderator</span></td>
                            <td style="color: #10b981; font-weight: 700;">Active</td>
                            <td>
                                <button class="action-btn">Edit</button>
                                <button class="action-btn">Delete</button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div class="user-avatar"></div>
                                <span class="user-name">Mike Davis</span>
                            </td>
                            <td>mike.davis@company.com</td>
                            <td><span class="user-role role-user">User</span></td>
                            <td style="color: #10b981; font-weight: 700;">Active</td>
                            <td>
                                <button class="action-btn">Edit</button>
                                <button class="action-btn">Delete</button>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <div class="user-avatar"></div>
                                <span class="user-name">Emily Wilson</span>
                            </td>
                            <td>emily.w@company.com</td>
                            <td><span class="user-role role-user">User</span></td>
                            <td style="color: #999;">Inactive</td>
                            <td>
                                <button class="action-btn">Edit</button>
                                <button class="action-btn">Delete</button>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _dashboard_financial_overview(self, colors: dict) -> str:
        """Financial Overview Dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Financial Overview</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
               min-height: 100vh; padding: 60px; }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        
        .dashboard-header {{ color: white; margin-bottom: 50px; }}
        .dashboard-header h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 16px; }}
        .dashboard-header p {{ font-size: 20px; opacity: 0.9; }}
        
        /* Financial Cards */
        .finance-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-bottom: 40px; }}
        .finance-card {{ background: white; padding: 40px; border-radius: 24px; 
                        box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
        .finance-card h3 {{ font-size: 16px; color: #666; margin-bottom: 16px; font-weight: 600; }}
        .finance-amount {{ font-size: 48px; font-weight: 900; margin-bottom: 16px; }}
        .finance-amount.positive {{ color: #10b981; }}
        .finance-amount.negative {{ color: #ef4444; }}
        .finance-amount.neutral {{ color: {colors['primary']}; }}
        .finance-change {{ font-size: 14px; font-weight: 700; }}
        .change-up {{ color: #10b981; }}
        .change-down {{ color: #ef4444; }}
        
        /* Chart Section */
        .chart-section {{ display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin-bottom: 40px; }}
        .chart-box {{ background: white; padding: 40px; border-radius: 24px; 
                     box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
        .chart-box h2 {{ font-size: 28px; font-weight: 900; margin-bottom: 30px; }}
        .line-chart {{ height: 300px; display: flex; align-items: flex-end; gap: 24px; }}
        .line-bar {{ flex: 1; background: linear-gradient(180deg, {colors['accent']}, {colors['primary']}); 
                    border-radius: 8px 8px 0 0; }}
        
        /* Breakdown */
        .breakdown-item {{ display: flex; justify-content: space-between; padding: 20px 0; 
                          border-bottom: 1px solid #f0f0f0; }}
        .breakdown-label {{ font-weight: 700; }}
        .breakdown-value {{ font-size: 18px; font-weight: 900; color: {colors['primary']}; }}
        
        /* Transactions */
        .transactions {{ background: white; padding: 40px; border-radius: 24px; 
                        box-shadow: 0 8px 30px rgba(0,0,0,0.12); }}
        .transactions h2 {{ font-size: 28px; font-weight: 900; margin-bottom: 30px; }}
        .transaction-item {{ display: flex; justify-content: space-between; align-items: center; 
                            padding: 24px; background: #f8f9fa; border-radius: 16px; margin-bottom: 16px; }}
        .transaction-info {{ }}
        .transaction-title {{ font-size: 18px; font-weight: 700; margin-bottom: 6px; }}
        .transaction-date {{ font-size: 14px; color: #999; }}
        .transaction-amount {{ font-size: 24px; font-weight: 900; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="dashboard-header">
            <h1>Financial Overview</h1>
            <p>Track your financial performance in real-time</p>
        </div>
        
        <div class="finance-grid">
            <div class="finance-card">
                <h3>Total Revenue</h3>
                <div class="finance-amount neutral">$1.2M</div>
                <div class="finance-change change-up">↑ 15.3% from last month</div>
            </div>
            <div class="finance-card">
                <h3>Net Profit</h3>
                <div class="finance-amount positive">+$347K</div>
                <div class="finance-change change-up">↑ 8.7% from last month</div>
            </div>
            <div class="finance-card">
                <h3>Total Expenses</h3>
                <div class="finance-amount negative">-$853K</div>
                <div class="finance-change change-down">↑ 12.4% from last month</div>
            </div>
        </div>
        
        <div class="chart-section">
            <div class="chart-box">
                <h2>Revenue Trend (Last 12 Months)</h2>
                <div class="line-chart">
                    <div class="line-bar" style="height: 55%;"></div>
                    <div class="line-bar" style="height: 62%;"></div>
                    <div class="line-bar" style="height: 58%;"></div>
                    <div class="line-bar" style="height: 70%;"></div>
                    <div class="line-bar" style="height: 75%;"></div>
                    <div class="line-bar" style="height: 68%;"></div>
                    <div class="line-bar" style="height: 82%;"></div>
                    <div class="line-bar" style="height: 88%;"></div>
                    <div class="line-bar" style="height: 85%;"></div>
                    <div class="line-bar" style="height: 92%;"></div>
                    <div class="line-bar" style="height: 95%;"></div>
                    <div class="line-bar" style="height: 100%;"></div>
                </div>
            </div>
            <div class="chart-box">
                <h2>Expense Breakdown</h2>
                <div class="breakdown-item">
                    <span class="breakdown-label">Salaries</span>
                    <span class="breakdown-value">$420K</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Marketing</span>
                    <span class="breakdown-value">$180K</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Operations</span>
                    <span class="breakdown-value">$145K</span>
                </div>
                <div class="breakdown-item">
                    <span class="breakdown-label">Technology</span>
                    <span class="breakdown-value">$108K</span>
                </div>
            </div>
        </div>
        
        <div class="transactions">
            <h2>Recent Transactions</h2>
            <div class="transaction-item">
                <div class="transaction-info">
                    <div class="transaction-title">Client Payment - Tech Corp</div>
                    <div class="transaction-date">March 18, 2024</div>
                </div>
                <div class="transaction-amount" style="color: #10b981;">+$45,000</div>
            </div>
            <div class="transaction-item">
                <div class="transaction-info">
                    <div class="transaction-title">Office Rent</div>
                    <div class="transaction-date">March 17, 2024</div>
                </div>
                <div class="transaction-amount" style="color: #ef4444;">-$12,500</div>
            </div>
            <div class="transaction-item">
                <div class="transaction-info">
                    <div class="transaction-title">Consulting Services</div>
                    <div class="transaction-date">March 16, 2024</div>
                </div>
                <div class="transaction-amount" style="color: #10b981;">+$28,000</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _dashboard_social_media_metrics(self, colors: dict) -> str:
        """Social Media Metrics Dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Social Media Metrics</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; padding: 50px; }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        
        .header {{ text-align: center; margin-bottom: 60px; }}
        .header h1 {{ font-size: 56px; font-weight: 900; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                     -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 16px; }}
        .header p {{ font-size: 20px; color: #666; }}
        
        /* Platform Cards */
        .platforms {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; margin-bottom: 40px; }}
        .platform-card {{ background: white; padding: 32px; border-radius: 20px; text-align: center; 
                         box-shadow: 0 4px 20px rgba(0,0,0,0.08); transition: transform 0.3s; }}
        .platform-card:hover {{ transform: translateY(-5px); }}
        .platform-icon {{ width: 70px; height: 70px; margin: 0 auto 20px; border-radius: 50%; 
                         background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .platform-name {{ font-size: 18px; font-weight: 700; margin-bottom: 12px; }}
        .platform-followers {{ font-size: 32px; font-weight: 900; color: {colors['primary']}; margin-bottom: 8px; }}
        .platform-growth {{ font-size: 14px; color: #10b981; font-weight: 700; }}
        
        /* Engagement Stats */
        .engagement {{ display: grid; grid-template-columns: 2fr 1fr; gap: 30px; margin-bottom: 40px; }}
        .engagement-chart {{ background: white; padding: 40px; border-radius: 20px; 
                            box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .engagement-chart h2 {{ font-size: 28px; font-weight: 900; margin-bottom: 30px; }}
        .bars {{ display: flex; align-items: flex-end; gap: 16px; height: 250px; }}
        .bar-group {{ flex: 1; display: flex; flex-direction: column; align-items: center; gap: 8px; }}
        .bar {{ width: 100%; background: linear-gradient(180deg, {colors['accent']}, {colors['primary']}); 
               border-radius: 8px 8px 0 0; }}
        .bar-label {{ font-size: 12px; color: #666; font-weight: 600; margin-top: 8px; }}
        
        /* Top Posts */
        .top-posts {{ background: white; padding: 40px; border-radius: 20px; 
                     box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .top-posts h2 {{ font-size: 28px; font-weight: 900; margin-bottom: 24px; }}
        .post-item {{ padding: 20px; background: #f8f9fa; border-radius: 12px; margin-bottom: 16px; }}
        .post-metric {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; margin-bottom: 6px; }}
        .post-label {{ font-size: 14px; color: #666; }}
        
        /* Recent Activity */
        .recent-activity {{ background: white; padding: 40px; border-radius: 20px; 
                           box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .recent-activity h2 {{ font-size: 28px; font-weight: 900; margin-bottom: 30px; }}
        .activity-item {{ display: flex; gap: 20px; padding: 20px 0; border-bottom: 1px solid #f0f0f0; }}
        .activity-time {{ font-size: 14px; color: #999; font-weight: 600; min-width: 100px; }}
        .activity-text {{ font-size: 16px; }}
        .activity-highlight {{ color: {colors['primary']}; font-weight: 700; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Social Media Dashboard</h1>
            <p>Monitor your social media performance across all platforms</p>
        </div>
        
        <div class="platforms">
            <div class="platform-card">
                <div class="platform-icon"></div>
                <div class="platform-name">Instagram</div>
                <div class="platform-followers">127.5K</div>
                <div class="platform-growth">↑ 12.3% this month</div>
            </div>
            <div class="platform-card">
                <div class="platform-icon"></div>
                <div class="platform-name">Twitter</div>
                <div class="platform-followers">89.2K</div>
                <div class="platform-growth">↑ 8.7% this month</div>
            </div>
            <div class="platform-card">
                <div class="platform-icon"></div>
                <div class="platform-name">Facebook</div>
                <div class="platform-followers">245.8K</div>
                <div class="platform-growth">↑ 5.4% this month</div>
            </div>
            <div class="platform-card">
                <div class="platform-icon"></div>
                <div class="platform-name">LinkedIn</div>
                <div class="platform-followers">56.3K</div>
                <div class="platform-growth">↑ 15.2% this month</div>
            </div>
        </div>
        
        <div class="engagement">
            <div class="engagement-chart">
                <h2>Weekly Engagement</h2>
                <div class="bars">
                    <div class="bar-group">
                        <div class="bar" style="height: 65%;"></div>
                        <div class="bar-label">Mon</div>
                    </div>
                    <div class="bar-group">
                        <div class="bar" style="height: 78%;"></div>
                        <div class="bar-label">Tue</div>
                    </div>
                    <div class="bar-group">
                        <div class="bar" style="height: 85%;"></div>
                        <div class="bar-label">Wed</div>
                    </div>
                    <div class="bar-group">
                        <div class="bar" style="height: 72%;"></div>
                        <div class="bar-label">Thu</div>
                    </div>
                    <div class="bar-group">
                        <div class="bar" style="height: 92%;"></div>
                        <div class="bar-label">Fri</div>
                    </div>
                    <div class="bar-group">
                        <div class="bar" style="height: 100%;"></div>
                        <div class="bar-label">Sat</div>
                    </div>
                    <div class="bar-group">
                        <div class="bar" style="height: 88%;"></div>
                        <div class="bar-label">Sun</div>
                    </div>
                </div>
            </div>
            <div class="top-posts">
                <h2>Top Posts</h2>
                <div class="post-item">
                    <div class="post-metric">28.4K</div>
                    <div class="post-label">Likes • Instagram</div>
                </div>
                <div class="post-item">
                    <div class="post-metric">15.7K</div>
                    <div class="post-label">Retweets • Twitter</div>
                </div>
                <div class="post-item">
                    <div class="post-metric">12.3K</div>
                    <div class="post-label">Shares • Facebook</div>
                </div>
            </div>
        </div>
        
        <div class="recent-activity">
            <h2>Recent Activity</h2>
            <div class="activity-item">
                <div class="activity-time">2 hours ago</div>
                <div class="activity-text">New post gained <span class="activity-highlight">1,247 likes</span> on Instagram</div>
            </div>
            <div class="activity-item">
                <div class="activity-time">5 hours ago</div>
                <div class="activity-text">Reached <span class="activity-highlight">10K followers</span> milestone on Twitter</div>
            </div>
            <div class="activity-item">
                <div class="activity-time">1 day ago</div>
                <div class="activity-text">Video post reached <span class="activity-highlight">50K views</span> on Facebook</div>
            </div>
            <div class="activity-item">
                <div class="activity-time">2 days ago</div>
                <div class="activity-text">Article shared <span class="activity-highlight">892 times</span> on LinkedIn</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _dashboard_inventory_management(self, colors: dict) -> str:
        """Inventory Management Dashboard"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inventory Management</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        
        /* Top Navigation */
        .top-nav {{ background: white; padding: 24px 60px; border-bottom: 2px solid #e0e0e0; 
                   display: flex; justify-content: space-between; align-items: center; }}
        .nav-logo {{ font-size: 28px; font-weight: 900; color: {colors['primary']}; }}
        .nav-actions {{ display: flex; gap: 16px; }}
        .nav-btn {{ padding: 12px 24px; border: 2px solid {colors['primary']}; background: white; 
                   border-radius: 10px; font-weight: 700; cursor: pointer; color: {colors['primary']}; }}
        .nav-btn.primary {{ background: {colors['primary']}; color: white; }}
        
        .container {{ max-width: 1800px; margin: 0 auto; padding: 50px; }}
        
        /* Inventory Stats */
        .inventory-stats {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 24px; margin-bottom: 40px; }}
        .stat-box {{ background: white; padding: 32px; border-radius: 16px; box-shadow: 0 2px 15px rgba(0,0,0,0.06); }}
        .stat-box h3 {{ font-size: 14px; color: #666; margin-bottom: 12px; font-weight: 600; }}
        .stat-box .value {{ font-size: 36px; font-weight: 900; color: {colors['primary']}; }}
        
        /* Inventory Table */
        .inventory-table {{ background: white; border-radius: 20px; overflow: hidden; 
                           box-shadow: 0 4px 20px rgba(0,0,0,0.08); margin-bottom: 40px; }}
        .table-toolbar {{ padding: 24px 32px; background: #f8f9fa; display: flex; 
                         justify-content: space-between; align-items: center; }}
        .table-toolbar h2 {{ font-size: 24px; font-weight: 900; }}
        .search-box {{ padding: 12px 20px; border: 2px solid #e0e0e0; border-radius: 10px; width: 300px; }}
        table {{ width: 100%; border-collapse: collapse; }}
        th {{ text-align: left; padding: 20px 32px; background: white; font-weight: 700; 
             border-bottom: 2px solid #f0f0f0; }}
        td {{ padding: 20px 32px; border-bottom: 1px solid #f0f0f0; }}
        .product-name {{ font-weight: 700; font-size: 16px; }}
        .product-sku {{ font-size: 13px; color: #999; }}
        .stock-badge {{ display: inline-block; padding: 6px 16px; border-radius: 20px; 
                       font-size: 12px; font-weight: 700; }}
        .stock-in {{ background: #d1fae5; color: #065f46; }}
        .stock-low {{ background: #fef3c7; color: #92400e; }}
        .stock-out {{ background: #fee2e2; color: #991b1b; }}
        
        /* Alerts */
        .alerts {{ background: white; padding: 40px; border-radius: 20px; 
                  box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .alerts h2 {{ font-size: 24px; font-weight: 900; margin-bottom: 24px; }}
        .alert-item {{ display: flex; gap: 20px; padding: 20px; background: #fef3c7; 
                      border-left: 4px solid #f59e0b; border-radius: 12px; margin-bottom: 16px; }}
        .alert-icon {{ width: 50px; height: 50px; border-radius: 50%; background: #f59e0b; }}
        .alert-content {{ flex: 1; }}
        .alert-title {{ font-size: 16px; font-weight: 700; margin-bottom: 6px; }}
        .alert-desc {{ font-size: 14px; color: #666; }}
    </style>
</head>
<body>
    <div class="top-nav">
        <div class="nav-logo">Inventory</div>
        <div class="nav-actions">
            <button class="nav-btn">Export Report</button>
            <button class="nav-btn primary">+ Add Product</button>
        </div>
    </div>
    
    <div class="container">
        <div class="inventory-stats">
            <div class="stat-box">
                <h3>Total Products</h3>
                <div class="value">2,847</div>
            </div>
            <div class="stat-box">
                <h3>In Stock</h3>
                <div class="value">2,234</div>
            </div>
            <div class="stat-box">
                <h3>Low Stock</h3>
                <div class="value">456</div>
            </div>
            <div class="stat-box">
                <h3>Out of Stock</h3>
                <div class="value">157</div>
            </div>
            <div class="stat-box">
                <h3>Total Value</h3>
                <div class="value">$1.2M</div>
            </div>
        </div>
        
        <div class="inventory-table">
            <div class="table-toolbar">
                <h2>Products</h2>
                <input type="text" class="search-box" placeholder="Search products...">
            </div>
            <table>
                <thead>
                    <tr>
                        <th>Product</th>
                        <th>Category</th>
                        <th>Stock</th>
                        <th>Status</th>
                        <th>Price</th>
                        <th>Value</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <div class="product-name">Wireless Headphones</div>
                            <div class="product-sku">SKU: WH-2024-001</div>
                        </td>
                        <td>Electronics</td>
                        <td style="font-weight: 700;">247 units</td>
                        <td><span class="stock-badge stock-in">In Stock</span></td>
                        <td>$299</td>
                        <td style="font-weight: 700;">$73,853</td>
                    </tr>
                    <tr>
                        <td>
                            <div class="product-name">Smart Watch Pro</div>
                            <div class="product-sku">SKU: SW-2024-002</div>
                        </td>
                        <td>Wearables</td>
                        <td style="font-weight: 700;">45 units</td>
                        <td><span class="stock-badge stock-low">Low Stock</span></td>
                        <td>$399</td>
                        <td style="font-weight: 700;">$17,955</td>
                    </tr>
                    <tr>
                        <td>
                            <div class="product-name">Laptop Stand</div>
                            <div class="product-sku">SKU: LS-2024-003</div>
                        </td>
                        <td>Accessories</td>
                        <td style="font-weight: 700;">0 units</td>
                        <td><span class="stock-badge stock-out">Out of Stock</span></td>
                        <td>$79</td>
                        <td style="font-weight: 700;">$0</td>
                    </tr>
                    <tr>
                        <td>
                            <div class="product-name">USB-C Cable</div>
                            <div class="product-sku">SKU: UC-2024-004</div>
                        </td>
                        <td>Accessories</td>
                        <td style="font-weight: 700;">1,243 units</td>
                        <td><span class="stock-badge stock-in">In Stock</span></td>
                        <td>$19</td>
                        <td style="font-weight: 700;">$23,617</td>
                    </tr>
                </tbody>
            </table>
        </div>
        
        <div class="alerts">
            <h2>Inventory Alerts</h2>
            <div class="alert-item">
                <div class="alert-icon"></div>
                <div class="alert-content">
                    <div class="alert-title">Low Stock Alert: Smart Watch Pro</div>
                    <div class="alert-desc">Only 45 units remaining. Reorder recommended.</div>
                </div>
            </div>
            <div class="alert-item">
                <div class="alert-icon"></div>
                <div class="alert-content">
                    <div class="alert-title">Out of Stock: Laptop Stand</div>
                    <div class="alert-desc">Product is currently unavailable. Immediate restock needed.</div>
                </div>
            </div>
            <div class="alert-item">
                <div class="alert-icon"></div>
                <div class="alert-content">
                    <div class="alert-title">Low Stock Alert: Wireless Mouse</div>
                    <div class="alert-desc">Stock level below minimum threshold (38 units).</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # ===== E-commerce (5가지 구조) =====
    def generate_ecommerce(self, colors: dict) -> str:
        """E-commerce 디자인 생성"""
        layouts = [
            self._ecommerce_product_grid,
            self._ecommerce_product_detail,
            self._ecommerce_cart,
            self._ecommerce_checkout,
            self._ecommerce_category,
            self._ecommerce_wishlist,
            self._ecommerce_order_tracking,
            self._ecommerce_search_results,
            self._ecommerce_customer_reviews,
        ]
        chosen_method = random.choice(layouts)
        self.current_method_name = chosen_method.__name__
        return chosen_method(colors)
    
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
    
    def _ecommerce_cart(self, colors: dict) -> str:
        """Shopping Cart Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shopping Cart</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #fafafa; padding: 80px 60px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        h1 {{ font-size: 48px; font-weight: 900; margin-bottom: 50px; }}
        .cart-layout {{ display: grid; grid-template-columns: 2fr 1fr; gap: 40px; }}
        .cart-items {{ background: white; padding: 40px; border-radius: 20px; }}
        .cart-item {{ display: grid; grid-template-columns: 120px 1fr auto; gap: 30px; 
                     padding: 30px 0; border-bottom: 2px solid #f0f0f0; }}
        .item-image {{ width: 120px; height: 120px; border-radius: 12px; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .item-info h3 {{ font-size: 20px; margin-bottom: 8px; }}
        .item-price {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; }}
        .cart-summary {{ background: white; padding: 40px; border-radius: 20px; height: fit-content; }}
        .summary-row {{ display: flex; justify-content: space-between; padding: 16px 0; border-bottom: 1px solid #f0f0f0; }}
        .total-row {{ font-size: 24px; font-weight: 900; margin-top: 20px; padding-top: 20px; 
                     border-top: 3px solid #e0e0e0; }}
        .checkout-btn {{ width: 100%; padding: 20px; background: {colors['primary']}; color: white; 
                        border: none; border-radius: 12px; font-size: 18px; font-weight: 700; 
                        margin-top: 30px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Shopping Cart</h1>
        <div class="cart-layout">
            <div class="cart-items">
                <div class="cart-item">
                    <div class="item-image"></div>
                    <div class="item-info">
                        <h3>Premium Headphones</h3>
                        <p style="color: #666;">Wireless, Noise Cancelling</p>
                        <div class="item-price" style="margin-top: 12px;">$299.00</div>
                    </div>
                    <div>Qty: 1</div>
                </div>
                <div class="cart-item">
                    <div class="item-image"></div>
                    <div class="item-info">
                        <h3>Laptop Stand</h3>
                        <p style="color: #666;">Aluminum, Adjustable</p>
                        <div class="item-price" style="margin-top: 12px;">$89.00</div>
                    </div>
                    <div>Qty: 2</div>
                </div>
            </div>
            <div class="cart-summary">
                <h2 style="font-size: 28px; margin-bottom: 30px;">Order Summary</h2>
                <div class="summary-row">
                    <span>Subtotal</span>
                    <span>$477.00</span>
                </div>
                <div class="summary-row">
                    <span>Shipping</span>
                    <span>$15.00</span>
                </div>
                <div class="summary-row">
                    <span>Tax</span>
                    <span>$42.30</span>
                </div>
                <div class="summary-row total-row">
                    <span>Total</span>
                    <span>${{534.30}}</span>
                </div>
                <button class="checkout-btn">Proceed to Checkout</button>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _ecommerce_checkout(self, colors: dict) -> str:
        """Checkout Flow"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Checkout</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        .checkout-layout {{ display: grid; grid-template-columns: 1.5fr 1fr; min-height: 100vh; }}
        .checkout-form {{ padding: 80px 100px; }}
        .checkout-form h1 {{ font-size: 48px; font-weight: 900; margin-bottom: 50px; }}
        .form-section {{ margin-bottom: 50px; }}
        .form-section h2 {{ font-size: 24px; margin-bottom: 24px; }}
        .form-group {{ margin-bottom: 20px; }}
        .form-label {{ font-size: 14px; font-weight: 700; margin-bottom: 8px; display: block; }}
        .form-input {{ width: 100%; padding: 16px; border: 2px solid #e0e0e0; border-radius: 10px; font-size: 16px; }}
        .order-summary {{ background: #f8f9fa; padding: 80px 60px; }}
        .order-summary h2 {{ font-size: 32px; margin-bottom: 40px; }}
        .order-item {{ display: flex; justify-content: space-between; padding: 20px 0; border-bottom: 1px solid #e0e0e0; }}
        .place-order-btn {{ width: 100%; padding: 20px; background: {colors['primary']}; color: white; 
                           border: none; border-radius: 12px; font-size: 18px; font-weight: 700; 
                           margin-top: 40px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="checkout-layout">
        <div class="checkout-form">
            <h1>Checkout</h1>
            <div class="form-section">
                <h2>Shipping Information</h2>
                <div class="form-group">
                    <label class="form-label">Full Name</label>
                    <input class="form-input" placeholder="John Doe">
                </div>
                <div class="form-group">
                    <label class="form-label">Address</label>
                    <input class="form-input" placeholder="123 Main Street">
                </div>
                <div class="form-group">
                    <label class="form-label">City, State ZIP</label>
                    <input class="form-input" placeholder="San Francisco, CA 94102">
                </div>
            </div>
            <div class="form-section">
                <h2>Payment Method</h2>
                <div class="form-group">
                    <label class="form-label">Card Number</label>
                    <input class="form-input" placeholder="1234 5678 9012 3456">
                </div>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 20px;">
                    <div class="form-group">
                        <label class="form-label">Expiry</label>
                        <input class="form-input" placeholder="MM/YY">
                    </div>
                    <div class="form-group">
                        <label class="form-label">CVV</label>
                        <input class="form-input" placeholder="123">
                    </div>
                </div>
            </div>
        </div>
        <div class="order-summary">
            <h2>Order Summary</h2>
            <div class="order-item">
                <span>Premium Headphones</span>
                <span>$299.00</span>
            </div>
            <div class="order-item">
                <span>Laptop Stand (x2)</span>
                <span>$178.00</span>
            </div>
            <div class="order-item" style="font-size: 24px; font-weight: 900; margin-top: 20px; padding-top: 30px; border-top: 3px solid #d0d0d0;">
                <span>Total</span>
                <span style="color: {colors['primary']};">${{534.30}}</span>
            </div>
            <button class="place-order-btn">Place Order</button>
        </div>
    </div>
</body>
</html>"""
    
    def _ecommerce_category(self, colors: dict) -> str:
        """Category Browse Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shop by Category</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; }}
        .hero {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                 color: white; padding: 100px 60px; text-align: center; }}
        .hero h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 20px; }}
        .hero p {{ font-size: 24px; opacity: 0.95; }}
        .filters {{ padding: 40px 60px; background: white; border-bottom: 2px solid #e0e0e0; 
                   display: flex; gap: 20px; }}
        .filter-btn {{ padding: 12px 30px; border: 2px solid #e0e0e0; background: white; 
                      border-radius: 8px; font-weight: 600; cursor: pointer; }}
        .filter-btn.active {{ background: {colors['primary']}; color: white; border-color: {colors['primary']}; }}
        .products {{ padding: 60px; max-width: 1600px; margin: 0 auto; }}
        .product-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 30px; }}
        .product {{ background: white; border-radius: 16px; overflow: hidden; 
                   box-shadow: 0 4px 20px rgba(0,0,0,0.08); transition: transform 0.3s; }}
        .product:hover {{ transform: translateY(-8px); }}
        .product-img {{ width: 100%; aspect-ratio: 1; 
                       background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .product-info {{ padding: 24px; }}
        .product-name {{ font-size: 18px; font-weight: 700; margin-bottom: 8px; }}
        .product-price {{ font-size: 22px; font-weight: 900; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Electronics</h1>
        <p>Discover the latest tech products</p>
    </div>
    <div class="filters">
        <button class="filter-btn active">All</button>
        <button class="filter-btn">Headphones</button>
        <button class="filter-btn">Laptops</button>
        <button class="filter-btn">Accessories</button>
        <button class="filter-btn">Cameras</button>
    </div>
    <div class="products">
        <div class="product-grid">
            <div class="product">
                <div class="product-img"></div>
                <div class="product-info">
                    <div class="product-name">Wireless Headphones</div>
                    <div class="product-price">$299</div>
                </div>
            </div>
            <div class="product">
                <div class="product-img"></div>
                <div class="product-info">
                    <div class="product-name">Laptop Pro</div>
                    <div class="product-price">$1,999</div>
                </div>
            </div>
            <div class="product">
                <div class="product-img"></div>
                <div class="product-info">
                    <div class="product-name">Smart Watch</div>
                    <div class="product-price">$399</div>
                </div>
            </div>
            <div class="product">
                <div class="product-img"></div>
                <div class="product-info">
                    <div class="product-name">Camera Kit</div>
                    <div class="product-price">$1,299</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _ecommerce_wishlist(self, colors: dict) -> str:
        """Wishlist Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Wishlist</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #fafafa; }}
        nav {{ background: white; padding: 24px 60px; border-bottom: 1px solid #e0e0e0; 
               display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 28px; font-weight: 900; color: {colors['primary']}; }}
        .container {{ max-width: 1400px; margin: 60px auto; padding: 0 60px; }}
        .page-title {{ font-size: 48px; font-weight: 900; margin-bottom: 16px; }}
        .page-subtitle {{ font-size: 18px; color: #666; margin-bottom: 50px; }}
        .wishlist-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }}
        .wishlist-item {{ background: white; border-radius: 20px; overflow: hidden; 
                         box-shadow: 0 4px 20px rgba(0,0,0,0.08); position: relative; }}
        .remove-btn {{ position: absolute; top: 20px; right: 20px; width: 40px; height: 40px; 
                      background: white; border-radius: 50%; border: none; cursor: pointer; 
                      box-shadow: 0 2px 10px rgba(0,0,0,0.1); font-size: 20px; }}
        .item-image {{ width: 100%; aspect-ratio: 1; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .item-info {{ padding: 28px; }}
        .item-name {{ font-size: 22px; font-weight: 900; margin-bottom: 12px; }}
        .item-price {{ font-size: 28px; font-weight: 900; color: {colors['primary']}; margin-bottom: 20px; }}
        .add-to-cart-btn {{ width: 100%; padding: 16px; background: {colors['primary']}; color: white; 
                           border: none; border-radius: 12px; font-weight: 700; font-size: 16px; cursor: pointer; }}
        .empty-state {{ text-align: center; padding: 100px 0; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">Shop</div>
        <div style="font-weight: 700;">My Wishlist (6)</div>
    </nav>
    
    <div class="container">
        <h1 class="page-title">My Wishlist</h1>
        <p class="page-subtitle">Your favorite items saved for later</p>
        
        <div class="wishlist-grid">
            <div class="wishlist-item">
                <button class="remove-btn">×</button>
                <div class="item-image"></div>
                <div class="item-info">
                    <div class="item-name">Premium Headphones</div>
                    <div class="item-price">$299</div>
                    <button class="add-to-cart-btn">Add to Cart</button>
                </div>
            </div>
            
            <div class="wishlist-item">
                <button class="remove-btn">×</button>
                <div class="item-image"></div>
                <div class="item-info">
                    <div class="item-name">Smart Watch Ultra</div>
                    <div class="item-price">$499</div>
                    <button class="add-to-cart-btn">Add to Cart</button>
                </div>
            </div>
            
            <div class="wishlist-item">
                <button class="remove-btn">×</button>
                <div class="item-image"></div>
                <div class="item-info">
                    <div class="item-name">Wireless Keyboard</div>
                    <div class="item-price">$159</div>
                    <button class="add-to-cart-btn">Add to Cart</button>
                </div>
            </div>
            
            <div class="wishlist-item">
                <button class="remove-btn">×</button>
                <div class="item-image"></div>
                <div class="item-info">
                    <div class="item-name">4K Monitor</div>
                    <div class="item-price">$799</div>
                    <button class="add-to-cart-btn">Add to Cart</button>
                </div>
            </div>
            
            <div class="wishlist-item">
                <button class="remove-btn">×</button>
                <div class="item-image"></div>
                <div class="item-info">
                    <div class="item-name">Gaming Mouse</div>
                    <div class="item-price">$89</div>
                    <button class="add-to-cart-btn">Add to Cart</button>
                </div>
            </div>
            
            <div class="wishlist-item">
                <button class="remove-btn">×</button>
                <div class="item-image"></div>
                <div class="item-info">
                    <div class="item-name">Laptop Stand</div>
                    <div class="item-price">$79</div>
                    <button class="add-to-cart-btn">Add to Cart</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _ecommerce_order_tracking(self, colors: dict) -> str:
        """Order Tracking Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Order Tracking</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
               min-height: 100vh; padding: 80px 40px; }}
        .container {{ max-width: 900px; margin: 0 auto; }}
        .card {{ background: white; border-radius: 24px; padding: 50px; 
                box-shadow: 0 10px 40px rgba(0,0,0,0.2); }}
        .order-header {{ text-align: center; margin-bottom: 50px; }}
        .order-header h1 {{ font-size: 42px; font-weight: 900; margin-bottom: 12px; }}
        .order-number {{ font-size: 18px; color: #666; margin-bottom: 8px; }}
        .estimated-delivery {{ font-size: 16px; font-weight: 700; color: {colors['primary']}; }}
        
        /* Timeline */
        .timeline {{ position: relative; padding-left: 60px; }}
        .timeline::before {{ content: ''; position: absolute; left: 20px; top: 0; bottom: 0; 
                            width: 4px; background: #e0e0e0; }}
        .timeline-item {{ position: relative; margin-bottom: 50px; }}
        .timeline-item.completed .timeline-dot {{ background: {colors['primary']}; }}
        .timeline-item.active .timeline-dot {{ background: {colors['primary']}; 
                                              box-shadow: 0 0 0 8px rgba(102, 126, 234, 0.2); }}
        .timeline-dot {{ position: absolute; left: -46px; width: 32px; height: 32px; 
                        border-radius: 50%; background: #e0e0e0; border: 4px solid white; 
                        box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .timeline-content {{ }}
        .timeline-title {{ font-size: 20px; font-weight: 900; margin-bottom: 8px; }}
        .timeline-desc {{ font-size: 15px; color: #666; margin-bottom: 6px; }}
        .timeline-time {{ font-size: 13px; color: #999; }}
        
        /* Order Items */
        .order-items {{ margin-top: 50px; padding-top: 40px; border-top: 2px solid #f0f0f0; }}
        .order-items h3 {{ font-size: 24px; font-weight: 900; margin-bottom: 24px; }}
        .item {{ display: flex; gap: 20px; padding: 20px; background: #f8f9fa; border-radius: 12px; margin-bottom: 16px; }}
        .item-image {{ width: 80px; height: 80px; border-radius: 8px; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .item-details {{ flex: 1; }}
        .item-name {{ font-size: 16px; font-weight: 700; margin-bottom: 6px; }}
        .item-qty {{ font-size: 14px; color: #666; }}
        .item-price {{ font-size: 18px; font-weight: 900; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="card">
            <div class="order-header">
                <h1>Track Your Order</h1>
                <p class="order-number">Order #ORD-2847-2024</p>
                <p class="estimated-delivery">Estimated Delivery: March 22, 2024</p>
            </div>
            
            <div class="timeline">
                <div class="timeline-item completed">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-title">Order Placed</div>
                        <div class="timeline-desc">Your order has been confirmed</div>
                        <div class="timeline-time">March 18, 2024 - 10:30 AM</div>
                    </div>
                </div>
                
                <div class="timeline-item completed">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-title">Processing</div>
                        <div class="timeline-desc">Your order is being prepared</div>
                        <div class="timeline-time">March 18, 2024 - 2:15 PM</div>
                    </div>
                </div>
                
                <div class="timeline-item active">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-title">Shipped</div>
                        <div class="timeline-desc">Package is on its way</div>
                        <div class="timeline-time">March 19, 2024 - 9:00 AM</div>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-title">Out for Delivery</div>
                        <div class="timeline-desc">Package is out for delivery</div>
                        <div class="timeline-time">Pending</div>
                    </div>
                </div>
                
                <div class="timeline-item">
                    <div class="timeline-dot"></div>
                    <div class="timeline-content">
                        <div class="timeline-title">Delivered</div>
                        <div class="timeline-desc">Package delivered successfully</div>
                        <div class="timeline-time">Pending</div>
                    </div>
                </div>
            </div>
            
            <div class="order-items">
                <h3>Order Items</h3>
                <div class="item">
                    <div class="item-image"></div>
                    <div class="item-details">
                        <div class="item-name">Premium Wireless Headphones</div>
                        <div class="item-qty">Quantity: 1</div>
                    </div>
                    <div class="item-price">$299</div>
                </div>
                <div class="item">
                    <div class="item-image"></div>
                    <div class="item-details">
                        <div class="item-name">USB-C Cable</div>
                        <div class="item-qty">Quantity: 2</div>
                    </div>
                    <div class="item-price">$38</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _ecommerce_search_results(self, colors: dict) -> str:
        """Search Results Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        
        /* Search Header */
        .search-header {{ background: {colors['primary']}; color: white; padding: 40px 60px; }}
        .search-header h1 {{ font-size: 36px; font-weight: 900; margin-bottom: 24px; }}
        .search-bar {{ display: flex; gap: 12px; }}
        .search-input {{ flex: 1; padding: 16px 24px; border: none; border-radius: 12px; 
                        font-size: 16px; }}
        .search-btn {{ padding: 16px 40px; background: {colors['secondary']}; color: white; 
                      border: none; border-radius: 12px; font-weight: 700; cursor: pointer; }}
        
        .container {{ max-width: 1600px; margin: 0 auto; padding: 60px; }}
        
        /* Filters and Results */
        .layout {{ display: grid; grid-template-columns: 280px 1fr; gap: 40px; }}
        
        /* Filters Sidebar */
        .filters {{ }}
        .filter-section {{ margin-bottom: 40px; }}
        .filter-section h3 {{ font-size: 18px; font-weight: 900; margin-bottom: 16px; }}
        .filter-option {{ display: flex; align-items: center; gap: 12px; padding: 10px 0; }}
        .filter-checkbox {{ width: 20px; height: 20px; border: 2px solid {colors['primary']}; border-radius: 4px; }}
        .filter-label {{ font-size: 15px; }}
        .price-range {{ display: flex; gap: 12px; align-items: center; margin-top: 16px; }}
        .price-input {{ width: 100px; padding: 10px; border: 2px solid #e0e0e0; border-radius: 8px; }}
        
        /* Results */
        .results {{ }}
        .results-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }}
        .results-count {{ font-size: 20px; font-weight: 700; }}
        .sort-select {{ padding: 12px 20px; border: 2px solid #e0e0e0; border-radius: 8px; font-weight: 600; }}
        
        .results-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }}
        .result-card {{ background: white; border: 2px solid #f0f0f0; border-radius: 16px; 
                       overflow: hidden; cursor: pointer; transition: all 0.3s; }}
        .result-card:hover {{ border-color: {colors['primary']}; transform: translateY(-4px); }}
        .result-image {{ width: 100%; aspect-ratio: 1; 
                        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .result-info {{ padding: 24px; }}
        .result-name {{ font-size: 18px; font-weight: 700; margin-bottom: 8px; }}
        .result-rating {{ color: #fbbf24; margin-bottom: 12px; }}
        .result-price {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="search-header">
        <h1>Search Products</h1>
        <div class="search-bar">
            <input type="text" class="search-input" placeholder="What are you looking for?" value="wireless headphones">
            <button class="search-btn">Search</button>
        </div>
    </div>
    
    <div class="container">
        <div class="layout">
            <div class="filters">
                <div class="filter-section">
                    <h3>Category</h3>
                    <div class="filter-option">
                        <div class="filter-checkbox"></div>
                        <span class="filter-label">Electronics</span>
                    </div>
                    <div class="filter-option">
                        <div class="filter-checkbox"></div>
                        <span class="filter-label">Audio</span>
                    </div>
                    <div class="filter-option">
                        <div class="filter-checkbox"></div>
                        <span class="filter-label">Accessories</span>
                    </div>
                </div>
                
                <div class="filter-section">
                    <h3>Price Range</h3>
                    <div class="price-range">
                        <input type="number" class="price-input" placeholder="Min">
                        <span>-</span>
                        <input type="number" class="price-input" placeholder="Max">
                    </div>
                </div>
                
                <div class="filter-section">
                    <h3>Brand</h3>
                    <div class="filter-option">
                        <div class="filter-checkbox"></div>
                        <span class="filter-label">TechBrand</span>
                    </div>
                    <div class="filter-option">
                        <div class="filter-checkbox"></div>
                        <span class="filter-label">AudioPro</span>
                    </div>
                    <div class="filter-option">
                        <div class="filter-checkbox"></div>
                        <span class="filter-label">SoundMax</span>
                    </div>
                </div>
            </div>
            
            <div class="results">
                <div class="results-header">
                    <div class="results-count">247 results for "wireless headphones"</div>
                    <select class="sort-select">
                        <option>Relevance</option>
                        <option>Price: Low to High</option>
                        <option>Price: High to Low</option>
                        <option>Newest</option>
                    </select>
                </div>
                
                <div class="results-grid">
                    <div class="result-card">
                        <div class="result-image"></div>
                        <div class="result-info">
                            <div class="result-name">Premium Wireless Headphones</div>
                            <div class="result-rating">★★★★★ (247)</div>
                            <div class="result-price">$299</div>
                        </div>
                    </div>
                    
                    <div class="result-card">
                        <div class="result-image"></div>
                        <div class="result-info">
                            <div class="result-name">Pro Audio Headset</div>
                            <div class="result-rating">★★★★☆ (189)</div>
                            <div class="result-price">$199</div>
                        </div>
                    </div>
                    
                    <div class="result-card">
                        <div class="result-image"></div>
                        <div class="result-info">
                            <div class="result-name">Studio Monitors</div>
                            <div class="result-rating">★★★★★ (312)</div>
                            <div class="result-price">$399</div>
                        </div>
                    </div>
                    
                    <div class="result-card">
                        <div class="result-image"></div>
                        <div class="result-info">
                            <div class="result-name">Budget Wireless Set</div>
                            <div class="result-rating">★★★☆☆ (94)</div>
                            <div class="result-price">$79</div>
                        </div>
                    </div>
                    
                    <div class="result-card">
                        <div class="result-image"></div>
                        <div class="result-info">
                            <div class="result-name">Gaming Headset Pro</div>
                            <div class="result-rating">★★★★★ (456)</div>
                            <div class="result-price">$249</div>
                        </div>
                    </div>
                    
                    <div class="result-card">
                        <div class="result-image"></div>
                        <div class="result-info">
                            <div class="result-name">Sport Earbuds</div>
                            <div class="result-rating">★★★★☆ (128)</div>
                            <div class="result-price">$129</div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _ecommerce_customer_reviews(self, colors: dict) -> str:
        """Customer Reviews Page"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Customer Reviews</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f8f9fa; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 80px 40px; }}
        
        /* Product Summary */
        .product-summary {{ background: white; padding: 50px; border-radius: 24px; 
                           margin-bottom: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); 
                           display: grid; grid-template-columns: 200px 1fr; gap: 40px; }}
        .product-image {{ width: 200px; height: 200px; border-radius: 16px; 
                         background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .product-info {{ }}
        .product-name {{ font-size: 36px; font-weight: 900; margin-bottom: 16px; }}
        .product-rating {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; margin-bottom: 12px; }}
        .rating-stars {{ font-size: 32px; color: #fbbf24; margin-bottom: 12px; }}
        .rating-count {{ font-size: 18px; color: #666; }}
        
        /* Rating Breakdown */
        .rating-breakdown {{ background: white; padding: 40px; border-radius: 24px; 
                            margin-bottom: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .rating-breakdown h2 {{ font-size: 28px; font-weight: 900; margin-bottom: 30px; }}
        .rating-row {{ display: flex; align-items: center; gap: 16px; margin-bottom: 16px; }}
        .rating-label {{ font-size: 16px; font-weight: 700; width: 60px; }}
        .rating-bar {{ flex: 1; height: 12px; background: #e0e0e0; border-radius: 6px; overflow: hidden; }}
        .rating-fill {{ height: 100%; background: linear-gradient(90deg, {colors['primary']}, {colors['secondary']}); }}
        .rating-value {{ font-size: 16px; font-weight: 700; width: 60px; text-align: right; }}
        
        /* Reviews List */
        .reviews-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 32px; }}
        .reviews-header h2 {{ font-size: 32px; font-weight: 900; }}
        .filter-btn {{ padding: 12px 24px; border: 2px solid {colors['primary']}; background: white; 
                      color: {colors['primary']}; border-radius: 10px; font-weight: 700; cursor: pointer; }}
        
        .review-card {{ background: white; padding: 40px; border-radius: 20px; margin-bottom: 24px; 
                       box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .review-header {{ display: flex; justify-content: space-between; margin-bottom: 20px; }}
        .reviewer-info {{ display: flex; gap: 16px; align-items: center; }}
        .reviewer-avatar {{ width: 50px; height: 50px; border-radius: 50%; 
                           background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .reviewer-name {{ font-size: 18px; font-weight: 900; margin-bottom: 4px; }}
        .review-date {{ font-size: 14px; color: #999; }}
        .review-stars {{ font-size: 20px; color: #fbbf24; }}
        .review-text {{ font-size: 16px; line-height: 1.7; color: #333; margin-bottom: 16px; }}
        .review-helpful {{ font-size: 14px; color: #666; }}
        .helpful-btn {{ margin-left: 12px; padding: 6px 12px; background: #f0f0f0; border: none; 
                       border-radius: 6px; cursor: pointer; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="product-summary">
            <div class="product-image"></div>
            <div class="product-info">
                <h1 class="product-name">Premium Wireless Headphones</h1>
                <div class="product-rating">4.8</div>
                <div class="rating-stars">★★★★★</div>
                <p class="rating-count">Based on 2,847 reviews</p>
            </div>
        </div>
        
        <div class="rating-breakdown">
            <h2>Rating Breakdown</h2>
            <div class="rating-row">
                <div class="rating-label">5 stars</div>
                <div class="rating-bar"><div class="rating-fill" style="width: 78%;"></div></div>
                <div class="rating-value">78%</div>
            </div>
            <div class="rating-row">
                <div class="rating-label">4 stars</div>
                <div class="rating-bar"><div class="rating-fill" style="width: 15%;"></div></div>
                <div class="rating-value">15%</div>
            </div>
            <div class="rating-row">
                <div class="rating-label">3 stars</div>
                <div class="rating-bar"><div class="rating-fill" style="width: 5%;"></div></div>
                <div class="rating-value">5%</div>
            </div>
            <div class="rating-row">
                <div class="rating-label">2 stars</div>
                <div class="rating-bar"><div class="rating-fill" style="width: 1%;"></div></div>
                <div class="rating-value">1%</div>
            </div>
            <div class="rating-row">
                <div class="rating-label">1 star</div>
                <div class="rating-bar"><div class="rating-fill" style="width: 1%;"></div></div>
                <div class="rating-value">1%</div>
            </div>
        </div>
        
        <div class="reviews-header">
            <h2>Customer Reviews</h2>
            <button class="filter-btn">Most Helpful</button>
        </div>
        
        <div class="review-card">
            <div class="review-header">
                <div class="reviewer-info">
                    <div class="reviewer-avatar"></div>
                    <div>
                        <div class="reviewer-name">John Smith</div>
                        <div class="review-date">Verified Purchase • March 15, 2024</div>
                    </div>
                </div>
                <div class="review-stars">★★★★★</div>
            </div>
            <p class="review-text">Absolutely love these headphones! The sound quality is exceptional, and the noise cancellation works perfectly. Comfortable for long listening sessions. Highly recommended!</p>
            <div class="review-helpful">
                Was this helpful?
                <button class="helpful-btn">👍 Yes (234)</button>
                <button class="helpful-btn">👎 No (12)</button>
            </div>
        </div>
        
        <div class="review-card">
            <div class="review-header">
                <div class="reviewer-info">
                    <div class="reviewer-avatar"></div>
                    <div>
                        <div class="reviewer-name">Sarah Johnson</div>
                        <div class="review-date">Verified Purchase • March 12, 2024</div>
                    </div>
                </div>
                <div class="review-stars">★★★★★</div>
            </div>
            <p class="review-text">Best purchase I've made this year. Battery life is amazing - lasts all day. The build quality feels premium and the connection is stable. Worth every penny!</p>
            <div class="review-helpful">
                Was this helpful?
                <button class="helpful-btn">👍 Yes (189)</button>
                <button class="helpful-btn">👎 No (8)</button>
            </div>
        </div>
        
        <div class="review-card">
            <div class="review-header">
                <div class="reviewer-info">
                    <div class="reviewer-avatar"></div>
                    <div>
                        <div class="reviewer-name">Mike Davis</div>
                        <div class="review-date">Verified Purchase • March 10, 2024</div>
                    </div>
                </div>
                <div class="review-stars">★★★★☆</div>
            </div>
            <p class="review-text">Great headphones overall. Sound is crisp and clear. Only minor complaint is they can feel a bit tight after wearing for several hours, but that might just be me.</p>
            <div class="review-helpful">
                Was this helpful?
                <button class="helpful-btn">👍 Yes (147)</button>
                <button class="helpful-btn">👎 No (15)</button>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # ===== Portfolio (5가지 구조) =====
    def generate_portfolio(self, colors: dict) -> str:
        """Portfolio 디자인 생성"""
        layouts = [
            self._portfolio_masonry,
            self._portfolio_minimal,
            self._portfolio_grid,
            self._portfolio_case_study,
            self._portfolio_timeline,
            self._portfolio_photography,
            self._portfolio_developer,
            self._portfolio_designer_resume,
            self._portfolio_video_creator,
            self._portfolio_freelancer,
        ]
        chosen_method = random.choice(layouts)
        self.current_method_name = chosen_method.__name__
        return chosen_method(colors)
    
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
    
    def _portfolio_grid(self, colors: dict) -> str:
        """Standard Grid Portfolio"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Grid</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        .header {{ padding: 40px 60px; border-bottom: 2px solid #f0f0f0; }}
        .header h1 {{ font-size: 32px; font-weight: 900; }}
        .portfolio-grid {{ padding: 60px; max-width: 1600px; margin: 0 auto; 
                          display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }}
        .project-card {{ background: white; border-radius: 16px; overflow: hidden; 
                        box-shadow: 0 4px 30px rgba(0,0,0,0.1); transition: transform 0.3s; }}
        .project-card:hover {{ transform: translateY(-10px); }}
        .project-img {{ width: 100%; aspect-ratio: 4/3; 
                       background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .project-info {{ padding: 30px; }}
        .project-category {{ font-size: 12px; font-weight: 700; text-transform: uppercase; 
                            color: {colors['primary']}; letter-spacing: 1.5px; margin-bottom: 12px; }}
        .project-title {{ font-size: 24px; font-weight: 900; margin-bottom: 12px; }}
        .project-desc {{ color: #666; line-height: 1.6; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>My Work</h1>
    </div>
    <div class="portfolio-grid">
        <div class="project-card">
            <div class="project-img"></div>
            <div class="project-info">
                <div class="project-category">Web Design</div>
                <h3 class="project-title">E-commerce Platform</h3>
                <p class="project-desc">Modern online shopping experience</p>
            </div>
        </div>
        <div class="project-card">
            <div class="project-img"></div>
            <div class="project-info">
                <div class="project-category">Mobile App</div>
                <h3 class="project-title">Fitness Tracker</h3>
                <p class="project-desc">iOS health and wellness app</p>
            </div>
        </div>
        <div class="project-card">
            <div class="project-img"></div>
            <div class="project-info">
                <div class="project-category">Branding</div>
                <h3 class="project-title">Coffee Brand</h3>
                <p class="project-desc">Complete brand identity design</p>
            </div>
        </div>
        <div class="project-card">
            <div class="project-img"></div>
            <div class="project-info">
                <div class="project-category">UI/UX</div>
                <h3 class="project-title">Dashboard Design</h3>
                <p class="project-desc">Analytics platform interface</p>
            </div>
        </div>
        <div class="project-card">
            <div class="project-img"></div>
            <div class="project-info">
                <div class="project-category">Illustration</div>
                <h3 class="project-title">Character Set</h3>
                <p class="project-desc">Custom illustration series</p>
            </div>
        </div>
        <div class="project-card">
            <div class="project-img"></div>
            <div class="project-info">
                <div class="project-category">Web Design</div>
                <h3 class="project-title">Portfolio Website</h3>
                <p class="project-desc">Personal portfolio redesign</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _portfolio_case_study(self, colors: dict) -> str:
        """Detailed Case Study"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Case Study</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        .hero-case {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                     color: white; padding: 120px 80px; text-align: center; }}
        .hero-case h1 {{ font-size: 72px; font-weight: 900; margin-bottom: 24px; }}
        .hero-case .meta {{ font-size: 20px; opacity: 0.9; }}
        .content {{ max-width: 1000px; margin: 0 auto; padding: 80px 40px; }}
        .section {{ margin-bottom: 80px; }}
        .section h2 {{ font-size: 40px; font-weight: 900; margin-bottom: 24px; }}
        .section p {{ font-size: 18px; line-height: 1.8; color: #444; }}
        .image-showcase {{ width: 100%; aspect-ratio: 16/9; border-radius: 20px; 
                          background: linear-gradient(135deg, {colors['secondary']}, {colors['accent']}); 
                          margin: 40px 0; }}
        .stats {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; 
                 background: #f8f9fa; padding: 60px; border-radius: 20px; }}
        .stat h3 {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; margin-bottom: 8px; }}
        .stat p {{ font-size: 18px; color: #666; }}
    </style>
</head>
<body>
    <div class="hero-case">
        <h1>E-commerce Redesign</h1>
        <p class="meta">2024 • Web Design • UX Research</p>
    </div>
    <div class="content">
        <div class="section">
            <h2>Overview</h2>
            <p>A complete redesign of a legacy e-commerce platform, focusing on improving conversion rates and user experience. The project involved extensive user research, prototyping, and iterative testing.</p>
        </div>
        <div class="image-showcase"></div>
        <div class="section">
            <h2>The Challenge</h2>
            <p>The existing platform had a 68% cart abandonment rate and users frequently complained about the checkout process. Our goal was to streamline the experience and increase completed purchases.</p>
        </div>
        <div class="stats">
            <div class="stat">
                <h3>+45%</h3>
                <p>Conversion Rate</p>
            </div>
            <div class="stat">
                <h3>-32%</h3>
                <p>Cart Abandonment</p>
            </div>
            <div class="stat">
                <h3>+2.5M</h3>
                <p>Revenue Increase</p>
            </div>
        </div>
        <div class="section">
            <h2>Solution</h2>
            <p>We implemented a streamlined checkout flow, improved product discovery with advanced filtering, and added personalized recommendations based on user behavior.</p>
        </div>
        <div class="image-showcase"></div>
    </div>
</body>
</html>"""
    
    def _portfolio_timeline(self, colors: dict) -> str:
        """Chronological Portfolio Timeline"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Timeline</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #fafafa; }}
        .header-timeline {{ background: white; padding: 60px; text-align: center; border-bottom: 2px solid #e0e0e0; }}
        .header-timeline h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 16px; }}
        .header-timeline p {{ font-size: 20px; color: #666; }}
        .timeline {{ max-width: 1200px; margin: 80px auto; padding: 0 60px; }}
        .timeline-item {{ display: grid; grid-template-columns: 200px 1fr; gap: 60px; 
                         margin-bottom: 80px; }}
        .timeline-year {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; }}
        .timeline-content {{ background: white; padding: 40px; border-radius: 20px; 
                            box-shadow: 0 4px 30px rgba(0,0,0,0.08); }}
        .timeline-image {{ width: 100%; aspect-ratio: 16/9; border-radius: 12px; 
                          background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                          margin-bottom: 24px; }}
        .timeline-title {{ font-size: 32px; font-weight: 900; margin-bottom: 12px; }}
        .timeline-desc {{ font-size: 18px; line-height: 1.6; color: #666; }}
    </style>
</head>
<body>
    <div class="header-timeline">
        <h1>My Journey</h1>
        <p>A chronological view of my work</p>
    </div>
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-year">2024</div>
            <div class="timeline-content">
                <div class="timeline-image"></div>
                <h3 class="timeline-title">AI Dashboard</h3>
                <p class="timeline-desc">Built an advanced analytics dashboard for machine learning models with real-time monitoring and custom visualizations.</p>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-year">2023</div>
            <div class="timeline-content">
                <div class="timeline-image"></div>
                <h3 class="timeline-title">Mobile Banking App</h3>
                <p class="timeline-desc">Designed and developed a secure mobile banking application with biometric authentication and real-time transactions.</p>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-year">2022</div>
            <div class="timeline-content">
                <div class="timeline-image"></div>
                <h3 class="timeline-title">E-learning Platform</h3>
                <p class="timeline-desc">Created an interactive online learning platform with video courses, quizzes, and student progress tracking.</p>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-year">2021</div>
            <div class="timeline-content">
                <div class="timeline-image"></div>
                <h3 class="timeline-title">Restaurant Website</h3>
                <p class="timeline-desc">Developed a modern restaurant website with online reservations, menu management, and customer reviews.</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _portfolio_photography(self, colors: dict) -> str:
        """Photography Portfolio"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Photography Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: black; color: white; }}
        
        /* Hero */
        .hero {{ height: 100vh; display: flex; align-items: center; justify-content: center; 
                text-align: center; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .hero h1 {{ font-size: 96px; font-weight: 900; margin-bottom: 24px; }}
        .hero p {{ font-size: 28px; opacity: 0.9; }}
        
        /* Gallery */
        .gallery {{ padding: 100px 40px; }}
        .gallery-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 4px; max-width: 1800px; margin: 0 auto; }}
        .photo {{ width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                 cursor: pointer; transition: transform 0.3s; }}
        .photo:hover {{ transform: scale(1.05); }}
        .photo.tall {{ aspect-ratio: 0.7; }}
        .photo.wide {{ aspect-ratio: 1.5; }}
        
        /* About Section */
        .about {{ padding: 120px 60px; text-align: center; background: #111; }}
        .about h2 {{ font-size: 56px; font-weight: 900; margin-bottom: 32px; }}
        .about p {{ font-size: 22px; line-height: 1.6; max-width: 800px; margin: 0 auto; opacity: 0.85; }}
        
        /* Contact */
        .contact {{ padding: 100px 60px; text-align: center; }}
        .contact h2 {{ font-size: 48px; font-weight: 900; margin-bottom: 32px; }}
        .contact-btn {{ padding: 20px 50px; background: white; color: black; border: none; 
                       border-radius: 50px; font-size: 18px; font-weight: 700; cursor: pointer; 
                       margin-top: 24px; }}
    </style>
</head>
<body>
    <div class="hero">
        <div>
            <h1>Sarah Williams</h1>
            <p>Visual Storyteller & Photographer</p>
        </div>
    </div>
    
    <div class="gallery">
        <div class="gallery-grid">
            <div class="photo"></div>
            <div class="photo tall"></div>
            <div class="photo"></div>
            <div class="photo"></div>
            <div class="photo"></div>
            <div class="photo tall"></div>
            <div class="photo wide" style="grid-column: span 2;"></div>
            <div class="photo"></div>
            <div class="photo"></div>
            <div class="photo"></div>
            <div class="photo tall"></div>
        </div>
    </div>
    
    <div class="about">
        <h2>About Me</h2>
        <p>I'm a professional photographer specializing in portrait, landscape, and editorial photography. With over 10 years of experience, I've worked with clients around the world to capture moments that tell compelling stories.</p>
    </div>
    
    <div class="contact">
        <h2>Let's Work Together</h2>
        <p style="font-size: 20px; opacity: 0.8; margin-bottom: 16px;">Available for commissions and collaborations</p>
        <button class="contact-btn">Get In Touch</button>
    </div>
</body>
</html>"""
    
    def _portfolio_developer(self, colors: dict) -> str:
        """Developer Portfolio"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Developer Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Monaco', 'Courier New', monospace; background: #1a1a1a; color: #00ff00; }}
        
        /* Terminal Header */
        .terminal {{ max-width: 1200px; margin: 80px auto; background: #000; border-radius: 12px; 
                    overflow: hidden; box-shadow: 0 10px 50px rgba(0,255,0,0.2); }}
        .terminal-header {{ background: #333; padding: 12px 20px; display: flex; gap: 8px; }}
        .terminal-btn {{ width: 14px; height: 14px; border-radius: 50%; }}
        .btn-red {{ background: #ff5f56; }}
        .btn-yellow {{ background: #ffbd2e; }}
        .btn-green {{ background: #27c93f; }}
        
        .terminal-body {{ padding: 40px; }}
        .prompt {{ color: {colors['primary']}; }}
        .command {{ margin-bottom: 30px; }}
        .output {{ margin-bottom: 40px; line-height: 1.8; }}
        
        /* Projects */
        .project {{ background: rgba(0,255,0,0.05); border-left: 4px solid {colors['primary']}; 
                   padding: 30px; margin-bottom: 30px; border-radius: 8px; }}
        .project-title {{ font-size: 28px; font-weight: 900; color: {colors['primary']}; margin-bottom: 12px; }}
        .project-desc {{ font-size: 16px; line-height: 1.7; margin-bottom: 16px; color: #00ff00; }}
        .project-tech {{ font-size: 14px; color: {colors['accent']}; }}
        
        /* Skills */
        .skills {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin: 40px 0; }}
        .skill {{ background: rgba(0,255,0,0.1); padding: 20px; border-radius: 8px; text-align: center; }}
        .skill-name {{ font-size: 18px; font-weight: 700; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="terminal">
        <div class="terminal-header">
            <div class="terminal-btn btn-red"></div>
            <div class="terminal-btn btn-yellow"></div>
            <div class="terminal-btn btn-green"></div>
        </div>
        <div class="terminal-body">
            <div class="command">
                <span class="prompt">$ </span>whoami
            </div>
            <div class="output">
                Alex Chen - Full Stack Developer<br>
                Specializing in React, Node.js, and Cloud Architecture<br>
                Location: San Francisco, CA
            </div>
            
            <div class="command">
                <span class="prompt">$ </span>ls projects/
            </div>
            <div class="output">
                <div class="project">
                    <div class="project-title">AI Chat Platform</div>
                    <div class="project-desc">Built a real-time chat application with AI-powered responses using GPT-4 API. Supports multiple users, file sharing, and voice messages.</div>
                    <div class="project-tech">Tech: React, Node.js, Socket.io, OpenAI API, MongoDB</div>
                </div>
                
                <div class="project">
                    <div class="project-title">E-commerce Dashboard</div>
                    <div class="project-desc">Created a comprehensive analytics dashboard for e-commerce businesses with real-time data visualization and reporting.</div>
                    <div class="project-tech">Tech: Next.js, TypeScript, PostgreSQL, Chart.js, AWS</div>
                </div>
                
                <div class="project">
                    <div class="project-title">Mobile Fitness App</div>
                    <div class="project-desc">Developed a cross-platform mobile app for workout tracking, nutrition logging, and progress analytics.</div>
                    <div class="project-tech">Tech: React Native, Firebase, Redux, Expo</div>
                </div>
            </div>
            
            <div class="command">
                <span class="prompt">$ </span>cat skills.json
            </div>
            <div class="output">
                <div class="skills">
                    <div class="skill"><div class="skill-name">JavaScript/TypeScript</div></div>
                    <div class="skill"><div class="skill-name">React & Next.js</div></div>
                    <div class="skill"><div class="skill-name">Node.js & Express</div></div>
                    <div class="skill"><div class="skill-name">PostgreSQL & MongoDB</div></div>
                    <div class="skill"><div class="skill-name">AWS & Docker</div></div>
                    <div class="skill"><div class="skill-name">Git & CI/CD</div></div>
                </div>
            </div>
            
            <div class="command">
                <span class="prompt">$ </span>contact --email
            </div>
            <div class="output">
                alex.chen@developer.com<br>
                github.com/alexchen<br>
                linkedin.com/in/alexchen
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _portfolio_designer_resume(self, colors: dict) -> str:
        """Designer Resume Portfolio"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Designer Resume</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        
        /* Layout */
        .resume {{ display: grid; grid-template-columns: 350px 1fr; min-height: 100vh; }}
        
        /* Sidebar */
        .sidebar {{ background: linear-gradient(180deg, {colors['primary']}, {colors['secondary']}); 
                   color: white; padding: 60px 40px; }}
        .profile-pic {{ width: 180px; height: 180px; border-radius: 50%; background: white; 
                       margin: 0 auto 32px; }}
        .name {{ font-size: 36px; font-weight: 900; text-align: center; margin-bottom: 12px; }}
        .title {{ font-size: 18px; text-align: center; opacity: 0.95; margin-bottom: 50px; }}
        
        .section {{ margin-bottom: 50px; }}
        .section h3 {{ font-size: 16px; font-weight: 900; letter-spacing: 2px; margin-bottom: 20px; 
                      opacity: 0.8; }}
        .section p {{ line-height: 1.7; margin-bottom: 12px; opacity: 0.95; }}
        .skill-bar {{ margin-bottom: 20px; }}
        .skill-name {{ font-size: 14px; margin-bottom: 8px; font-weight: 600; }}
        .bar {{ height: 8px; background: rgba(255,255,255,0.3); border-radius: 4px; overflow: hidden; }}
        .bar-fill {{ height: 100%; background: white; }}
        
        /* Main Content */
        .main {{ padding: 80px 60px; }}
        .main h2 {{ font-size: 48px; font-weight: 900; margin-bottom: 50px; color: {colors['primary']}; }}
        
        .experience-item {{ margin-bottom: 50px; padding-bottom: 40px; border-bottom: 2px solid #f0f0f0; }}
        .experience-item:last-child {{ border-bottom: none; }}
        .job-title {{ font-size: 28px; font-weight: 900; margin-bottom: 8px; }}
        .company {{ font-size: 18px; color: {colors['secondary']}; font-weight: 700; margin-bottom: 8px; }}
        .duration {{ font-size: 14px; color: #999; margin-bottom: 20px; }}
        .job-desc {{ font-size: 16px; line-height: 1.8; color: #333; }}
        .job-desc li {{ margin-bottom: 12px; }}
        
        .education-item {{ margin-bottom: 30px; }}
        .degree {{ font-size: 22px; font-weight: 900; margin-bottom: 8px; }}
        .school {{ font-size: 16px; color: #666; }}
    </style>
</head>
<body>
    <div class="resume">
        <div class="sidebar">
            <div class="profile-pic"></div>
            <h1 class="name">Emma Taylor</h1>
            <p class="title">UX/UI Designer</p>
            
            <div class="section">
                <h3>CONTACT</h3>
                <p>emma.taylor@design.com</p>
                <p>+1 (555) 123-4567</p>
                <p>San Francisco, CA</p>
            </div>
            
            <div class="section">
                <h3>SKILLS</h3>
                <div class="skill-bar">
                    <div class="skill-name">UI Design</div>
                    <div class="bar"><div class="bar-fill" style="width: 95%;"></div></div>
                </div>
                <div class="skill-bar">
                    <div class="skill-name">UX Research</div>
                    <div class="bar"><div class="bar-fill" style="width: 90%;"></div></div>
                </div>
                <div class="skill-bar">
                    <div class="skill-name">Figma</div>
                    <div class="bar"><div class="bar-fill" style="width: 95%;"></div></div>
                </div>
                <div class="skill-bar">
                    <div class="skill-name">Prototyping</div>
                    <div class="bar"><div class="bar-fill" style="width: 88%;"></div></div>
                </div>
                <div class="skill-bar">
                    <div class="skill-name">Design Systems</div>
                    <div class="bar"><div class="bar-fill" style="width: 92%;"></div></div>
                </div>
            </div>
            
            <div class="section">
                <h3>LANGUAGES</h3>
                <p>English - Native</p>
                <p>Spanish - Fluent</p>
                <p>French - Intermediate</p>
            </div>
        </div>
        
        <div class="main">
            <h2>Experience</h2>
            
            <div class="experience-item">
                <div class="job-title">Senior UI/UX Designer</div>
                <div class="company">Tech Innovations Inc.</div>
                <div class="duration">2021 - Present</div>
                <ul class="job-desc">
                    <li>Led design for flagship mobile app used by 2M+ users</li>
                    <li>Created and maintained comprehensive design system</li>
                    <li>Conducted user research and usability testing sessions</li>
                    <li>Collaborated with product and engineering teams</li>
                </ul>
            </div>
            
            <div class="experience-item">
                <div class="job-title">UI Designer</div>
                <div class="company">Creative Studio</div>
                <div class="duration">2019 - 2021</div>
                <ul class="job-desc">
                    <li>Designed interfaces for web and mobile applications</li>
                    <li>Created wireframes, mockups, and prototypes</li>
                    <li>Worked with clients to understand requirements</li>
                </ul>
            </div>
            
            <div class="experience-item">
                <div class="job-title">Junior Designer</div>
                <div class="company">Digital Agency</div>
                <div class="duration">2017 - 2019</div>
                <ul class="job-desc">
                    <li>Assisted in designing marketing materials and websites</li>
                    <li>Learned industry best practices and design principles</li>
                </ul>
            </div>
            
            <h2 style="margin-top: 60px;">Education</h2>
            
            <div class="education-item">
                <div class="degree">Bachelor of Fine Arts in Graphic Design</div>
                <div class="school">California College of the Arts • 2013-2017</div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _portfolio_video_creator(self, colors: dict) -> str:
        """Video Creator Portfolio"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Video Creator Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; color: white; }}
        
        /* Navigation */
        nav {{ position: fixed; top: 0; width: 100%; background: rgba(0,0,0,0.95); padding: 24px 60px; 
              z-index: 100; display: flex; justify-content: space-between; align-items: center; 
              backdrop-filter: blur(10px); }}
        .logo {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; }}
        .nav-links {{ display: flex; gap: 32px; }}
        .nav-link {{ color: white; text-decoration: none; font-weight: 600; }}
        
        /* Hero Video */
        .hero-video {{ height: 100vh; display: flex; align-items: center; justify-content: center; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                      position: relative; }}
        .play-icon {{ width: 120px; height: 120px; border-radius: 50%; background: white; 
                     display: flex; align-items: center; justify-content: center; cursor: pointer; 
                     transition: transform 0.3s; }}
        .play-icon:hover {{ transform: scale(1.1); }}
        
        /* Video Grid */
        .videos {{ padding: 100px 60px; }}
        .section-title {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .video-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; max-width: 1600px; margin: 0 auto; }}
        .video-card {{ background: #1a1a1a; border-radius: 20px; overflow: hidden; cursor: pointer; 
                      transition: transform 0.3s; }}
        .video-card:hover {{ transform: translateY(-8px); }}
        .video-thumbnail {{ width: 100%; aspect-ratio: 16/9; 
                           background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                           position: relative; }}
        .video-play {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); 
                      width: 80px; height: 80px; border-radius: 50%; background: rgba(255,255,255,0.9); }}
        .video-info {{ padding: 32px; }}
        .video-title {{ font-size: 24px; font-weight: 900; margin-bottom: 12px; }}
        .video-desc {{ font-size: 16px; color: #999; line-height: 1.6; margin-bottom: 16px; }}
        .video-stats {{ display: flex; gap: 24px; font-size: 14px; color: #666; }}
        
        /* About */
        .about {{ padding: 120px 60px; background: #111; text-align: center; }}
        .about h2 {{ font-size: 56px; font-weight: 900; margin-bottom: 32px; }}
        .about p {{ font-size: 20px; line-height: 1.8; max-width: 800px; margin: 0 auto; color: #ccc; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">VIDEOCREATOR</div>
        <div class="nav-links">
            <a href="#" class="nav-link">Work</a>
            <a href="#" class="nav-link">About</a>
            <a href="#" class="nav-link">Contact</a>
        </div>
    </nav>
    
    <div class="hero-video">
        <div class="play-icon">
            <div style="width: 0; height: 0; border-left: 30px solid black; 
                       border-top: 20px solid transparent; border-bottom: 20px solid transparent; 
                       margin-left: 8px;"></div>
        </div>
    </div>
    
    <div class="videos">
        <h2 class="section-title">Featured Work</h2>
        <div class="video-grid">
            <div class="video-card">
                <div class="video-thumbnail">
                    <div class="video-play"></div>
                </div>
                <div class="video-info">
                    <h3 class="video-title">Brand Commercial - Tech Startup</h3>
                    <p class="video-desc">A dynamic 60-second commercial showcasing innovative technology solutions for modern businesses.</p>
                    <div class="video-stats">
                        <span>2:30</span>
                        <span>•</span>
                        <span>Commercial</span>
                    </div>
                </div>
            </div>
            
            <div class="video-card">
                <div class="video-thumbnail">
                    <div class="video-play"></div>
                </div>
                <div class="video-info">
                    <h3 class="video-title">Documentary - Creative Journey</h3>
                    <p class="video-desc">An inspiring documentary following artists as they create their masterpieces.</p>
                    <div class="video-stats">
                        <span>12:45</span>
                        <span>•</span>
                        <span>Documentary</span>
                    </div>
                </div>
            </div>
            
            <div class="video-card">
                <div class="video-thumbnail">
                    <div class="video-play"></div>
                </div>
                <div class="video-info">
                    <h3 class="video-title">Music Video - Electric Dreams</h3>
                    <p class="video-desc">Vibrant and energetic music video with stunning visual effects and choreography.</p>
                    <div class="video-stats">
                        <span>3:42</span>
                        <span>•</span>
                        <span>Music Video</span>
                    </div>
                </div>
            </div>
            
            <div class="video-card">
                <div class="video-thumbnail">
                    <div class="video-play"></div>
                </div>
                <div class="video-info">
                    <h3 class="video-title">Product Showcase - Luxury Watch</h3>
                    <p class="video-desc">Elegant product video highlighting the craftsmanship and details of premium timepieces.</p>
                    <div class="video-stats">
                        <span>1:15</span>
                        <span>•</span>
                        <span>Product</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="about">
        <h2>About</h2>
        <p>I'm a video creator and cinematographer with a passion for visual storytelling. Specializing in commercials, music videos, and documentaries, I bring ideas to life through compelling visuals and creative direction.</p>
    </div>
</body>
</html>"""
    
    def _portfolio_freelancer(self, colors: dict) -> str:
        """Freelancer Portfolio"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Freelancer Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        
        /* Hero */
        .hero {{ padding: 120px 60px; text-align: center; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                color: white; }}
        .hero h1 {{ font-size: 72px; font-weight: 900; margin-bottom: 24px; }}
        .hero p {{ font-size: 28px; margin-bottom: 40px; opacity: 0.95; }}
        .cta-btn {{ padding: 20px 50px; background: white; color: {colors['primary']}; border: none; 
                   border-radius: 50px; font-size: 18px; font-weight: 900; cursor: pointer; }}
        
        /* Services */
        .services {{ padding: 100px 60px; max-width: 1400px; margin: 0 auto; }}
        .services h2 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .services-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }}
        .service-card {{ text-align: center; padding: 50px 30px; border-radius: 24px; 
                        background: #fafafa; transition: all 0.3s; }}
        .service-card:hover {{ transform: translateY(-10px); box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
        .service-icon {{ width: 100px; height: 100px; margin: 0 auto 30px; border-radius: 50%; 
                        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .service-title {{ font-size: 26px; font-weight: 900; margin-bottom: 16px; }}
        .service-desc {{ font-size: 16px; line-height: 1.7; color: #666; }}
        
        /* Portfolio Samples */
        .portfolio-samples {{ padding: 100px 60px; background: #fafafa; }}
        .portfolio-samples h2 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .samples-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; 
                        max-width: 1400px; margin: 0 auto; }}
        .sample {{ background: white; border-radius: 20px; overflow: hidden; 
                  box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .sample-image {{ width: 100%; aspect-ratio: 16/9; 
                        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .sample-info {{ padding: 40px; }}
        .sample-title {{ font-size: 28px; font-weight: 900; margin-bottom: 12px; }}
        .sample-client {{ font-size: 16px; color: {colors['primary']}; font-weight: 700; margin-bottom: 16px; }}
        .sample-desc {{ font-size: 16px; line-height: 1.7; color: #666; }}
        
        /* Testimonials */
        .testimonials {{ padding: 100px 60px; max-width: 1200px; margin: 0 auto; }}
        .testimonials h2 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .testimonial {{ background: white; padding: 50px; border-radius: 24px; margin-bottom: 32px; 
                       box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .testimonial-text {{ font-size: 20px; line-height: 1.8; margin-bottom: 24px; color: #333; 
                            font-style: italic; }}
        .testimonial-author {{ display: flex; gap: 20px; align-items: center; }}
        .author-avatar {{ width: 60px; height: 60px; border-radius: 50%; 
                         background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .author-name {{ font-size: 18px; font-weight: 900; }}
        .author-title {{ font-size: 14px; color: #999; }}
        
        /* CTA */
        .cta {{ padding: 120px 60px; text-align: center; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
               color: white; }}
        .cta h2 {{ font-size: 56px; font-weight: 900; margin-bottom: 32px; }}
        .cta p {{ font-size: 24px; margin-bottom: 40px; opacity: 0.95; }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Marcus Johnson</h1>
        <p>Full Stack Developer & Designer</p>
        <button class="cta-btn">View My Work</button>
    </div>
    
    <div class="services">
        <h2>What I Do</h2>
        <div class="services-grid">
            <div class="service-card">
                <div class="service-icon"></div>
                <h3 class="service-title">Web Development</h3>
                <p class="service-desc">Creating responsive, fast, and scalable web applications using modern technologies.</p>
            </div>
            <div class="service-card">
                <div class="service-icon"></div>
                <h3 class="service-title">UI/UX Design</h3>
                <p class="service-desc">Designing intuitive and beautiful user interfaces that enhance user experience.</p>
            </div>
            <div class="service-card">
                <div class="service-icon"></div>
                <h3 class="service-title">Branding</h3>
                <p class="service-desc">Developing cohesive brand identities that make lasting impressions.</p>
            </div>
        </div>
    </div>
    
    <div class="portfolio-samples">
        <h2>Recent Projects</h2>
        <div class="samples-grid">
            <div class="sample">
                <div class="sample-image"></div>
                <div class="sample-info">
                    <h3 class="sample-title">E-commerce Platform</h3>
                    <p class="sample-client">Client: Fashion Brand Co.</p>
                    <p class="sample-desc">Developed a complete e-commerce solution with custom CMS, payment integration, and real-time inventory management.</p>
                </div>
            </div>
            <div class="sample">
                <div class="sample-image"></div>
                <div class="sample-info">
                    <h3 class="sample-title">SaaS Dashboard</h3>
                    <p class="sample-client">Client: Tech Startup Inc.</p>
                    <p class="sample-desc">Created an analytics dashboard with data visualization, reporting, and team collaboration features.</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="testimonials">
        <h2>Client Testimonials</h2>
        <div class="testimonial">
            <p class="testimonial-text">"Marcus delivered exceptional work on our e-commerce platform. His attention to detail and technical expertise exceeded our expectations. Highly recommended!"</p>
            <div class="testimonial-author">
                <div class="author-avatar"></div>
                <div>
                    <div class="author-name">Sarah Williams</div>
                    <div class="author-title">CEO, Fashion Brand Co.</div>
                </div>
            </div>
        </div>
        <div class="testimonial">
            <p class="testimonial-text">"Working with Marcus was a pleasure. He understood our vision perfectly and delivered a product that our users love. Great communication throughout the project."</p>
            <div class="testimonial-author">
                <div class="author-avatar"></div>
                <div>
                    <div class="author-name">John Smith</div>
                    <div class="author-title">Founder, Tech Startup Inc.</div>
                </div>
            </div>
        </div>
    </div>
    
    <div class="cta">
        <h2>Let's Work Together</h2>
        <p>Have a project in mind? Let's discuss how I can help.</p>
        <button class="cta-btn">Get In Touch</button>
    </div>
</body>
</html>"""
    
    # ===== Blog (5가지 구조) =====
    def generate_blog(self, colors: dict) -> str:
        """Blog 디자인 생성"""
        layouts = [
            self._blog_grid,
            self._blog_magazine,
            self._blog_list,
            self._blog_featured,
            self._blog_sidebar,
            self._blog_personal,
            self._blog_tech_news,
            self._blog_food_recipe,
            self._blog_travel,
            self._blog_minimal_medium,
        ]
        chosen_method = random.choice(layouts)
        self.current_method_name = chosen_method.__name__
        return chosen_method(colors)
    
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
    
    def _blog_list(self, colors: dict) -> str:
        """List View Blog"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog List</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        .blog-header {{ background: {colors['primary']}; color: white; padding: 80px 60px; text-align: center; }}
        .blog-header h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 20px; }}
        .blog-header p {{ font-size: 20px; opacity: 0.9; }}
        .blog-container {{ max-width: 900px; margin: 80px auto; padding: 0 40px; }}
        .post-list-item {{ display: flex; gap: 40px; padding: 40px 0; border-bottom: 2px solid #f0f0f0; }}
        .post-list-item:last-child {{ border-bottom: none; }}
        .post-list-image {{ width: 200px; height: 200px; flex-shrink: 0; border-radius: 12px; 
                           background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .post-list-content {{ flex: 1; }}
        .post-list-date {{ font-size: 14px; color: #999; margin-bottom: 12px; }}
        .post-list-title {{ font-size: 32px; font-weight: 900; margin-bottom: 16px; }}
        .post-list-excerpt {{ font-size: 16px; line-height: 1.6; color: #666; margin-bottom: 20px; }}
        .read-more {{ color: {colors['primary']}; font-weight: 700; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="blog-header">
        <h1>Stories & Insights</h1>
        <p>Thoughts on design, development, and creativity</p>
    </div>
    <div class="blog-container">
        <div class="post-list-item">
            <div class="post-list-image"></div>
            <div class="post-list-content">
                <div class="post-list-date">March 15, 2024</div>
                <h2 class="post-list-title">The Future of Web Design</h2>
                <p class="post-list-excerpt">Exploring emerging trends and technologies that will shape how we build websites in the coming years.</p>
                <a href="#" class="read-more">Read Article →</a>
            </div>
        </div>
        <div class="post-list-item">
            <div class="post-list-image"></div>
            <div class="post-list-content">
                <div class="post-list-date">March 10, 2024</div>
                <h2 class="post-list-title">Mastering CSS Grid</h2>
                <p class="post-list-excerpt">A comprehensive guide to creating complex layouts with CSS Grid, including practical examples and best practices.</p>
                <a href="#" class="read-more">Read Article →</a>
            </div>
        </div>
        <div class="post-list-item">
            <div class="post-list-image"></div>
            <div class="post-list-content">
                <div class="post-list-date">March 5, 2024</div>
                <h2 class="post-list-title">Building Accessible Websites</h2>
                <p class="post-list-excerpt">Learn how to make your websites accessible to everyone, including users with disabilities.</p>
                <a href="#" class="read-more">Read Article →</a>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _blog_featured(self, colors: dict) -> str:
        """Featured Post Layout"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Featured Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #fafafa; }}
        .featured-hero {{ height: 100vh; display: flex; align-items: center; justify-content: center; 
                         background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                         color: white; text-align: center; padding: 60px; }}
        .featured-hero h1 {{ font-size: 96px; font-weight: 900; margin-bottom: 24px; }}
        .featured-hero .meta {{ font-size: 20px; opacity: 0.9; }}
        .content-section {{ max-width: 800px; margin: 80px auto; padding: 0 40px; }}
        .content-section p {{ font-size: 20px; line-height: 1.8; margin-bottom: 32px; }}
        .more-posts {{ background: white; padding: 80px 60px; }}
        .more-posts h2 {{ text-align: center; font-size: 48px; margin-bottom: 60px; }}
        .more-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; max-width: 1200px; margin: 0 auto; }}
        .more-card {{ background: #fafafa; border-radius: 16px; overflow: hidden; }}
        .more-card-img {{ width: 100%; aspect-ratio: 16/9; 
                         background: linear-gradient(135deg, {colors['secondary']}, {colors['accent']}); }}
        .more-card-content {{ padding: 24px; }}
        .more-card-title {{ font-size: 20px; font-weight: 700; }}
    </style>
</head>
<body>
    <div class="featured-hero">
        <div>
            <h1>The Art of<br>Minimalism</h1>
            <p class="meta">By Sarah Johnson • March 20, 2024 • 8 min read</p>
        </div>
    </div>
    <div class="content-section">
        <p>Minimalism in design isn't just about using less—it's about using exactly what's needed to communicate effectively. Every element serves a purpose, every pixel has meaning.</p>
        <p>In this article, we'll explore the principles of minimalist design, from whitespace to typography, and how to apply them to create elegant, functional interfaces.</p>
        <p>The journey to mastery begins with understanding that simplicity is the ultimate sophistication.</p>
    </div>
    <div class="more-posts">
        <h2>More Stories</h2>
        <div class="more-grid">
            <div class="more-card">
                <div class="more-card-img"></div>
                <div class="more-card-content">
                    <h3 class="more-card-title">Color Theory Basics</h3>
                </div>
            </div>
            <div class="more-card">
                <div class="more-card-img"></div>
                <div class="more-card-content">
                    <h3 class="more-card-title">Typography Guide</h3>
                </div>
            </div>
            <div class="more-card">
                <div class="more-card-img"></div>
                <div class="more-card-content">
                    <h3 class="more-card-title">Design Systems</h3>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _blog_sidebar(self, colors: dict) -> str:
        """Blog with Sidebar"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog with Sidebar</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        .blog-layout {{ display: grid; grid-template-columns: 1fr 350px; gap: 60px; 
                       max-width: 1400px; margin: 0 auto; padding: 80px 60px; }}
        .main-content {{ }}
        .main-content h1 {{ font-size: 56px; font-weight: 900; margin-bottom: 40px; }}
        .post-item-sidebar {{ display: flex; gap: 24px; padding: 32px 0; border-bottom: 1px solid #f0f0f0; }}
        .post-thumb {{ width: 120px; height: 120px; flex-shrink: 0; border-radius: 8px; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .post-item-title {{ font-size: 20px; font-weight: 700; margin-bottom: 8px; }}
        .post-item-date {{ font-size: 14px; color: #999; }}
        .sidebar {{ background: #f8f9fa; padding: 40px; border-radius: 20px; height: fit-content; }}
        .sidebar h3 {{ font-size: 24px; margin-bottom: 24px; }}
        .category-list {{ list-style: none; }}
        .category-list li {{ padding: 12px 0; border-bottom: 1px solid #e0e0e0; }}
        .category-list a {{ text-decoration: none; color: #333; font-weight: 600; }}
        .newsletter {{ background: {colors['primary']}; color: white; padding: 30px; 
                     border-radius: 16px; margin-top: 40px; }}
        .newsletter h3 {{ font-size: 20px; margin-bottom: 16px; }}
        .newsletter input {{ width: 100%; padding: 12px; border: none; border-radius: 8px; margin-top: 12px; }}
    </style>
</head>
<body>
    <div class="blog-layout">
        <div class="main-content">
            <h1>Latest Articles</h1>
            <div class="post-item-sidebar">
                <div class="post-thumb"></div>
                <div>
                    <h3 class="post-item-title">Getting Started with React Hooks</h3>
                    <p class="post-item-date">March 18, 2024</p>
                </div>
            </div>
            <div class="post-item-sidebar">
                <div class="post-thumb"></div>
                <div>
                    <h3 class="post-item-title">Advanced CSS Animations</h3>
                    <p class="post-item-date">March 15, 2024</p>
                </div>
            </div>
            <div class="post-item-sidebar">
                <div class="post-thumb"></div>
                <div>
                    <h3 class="post-item-title">Building Scalable APIs</h3>
                    <p class="post-item-date">March 12, 2024</p>
                </div>
            </div>
            <div class="post-item-sidebar">
                <div class="post-thumb"></div>
                <div>
                    <h3 class="post-item-title">UX Research Methods</h3>
                    <p class="post-item-date">March 10, 2024</p>
                </div>
            </div>
        </div>
        <div class="sidebar">
            <h3>Categories</h3>
            <ul class="category-list">
                <li><a href="#">Web Development</a></li>
                <li><a href="#">UI/UX Design</a></li>
                <li><a href="#">JavaScript</a></li>
                <li><a href="#">CSS Tips</a></li>
                <li><a href="#">Career</a></li>
            </ul>
            <div class="newsletter">
                <h3>Newsletter</h3>
                <p style="font-size: 14px;">Get weekly updates delivered to your inbox</p>
                <input type="email" placeholder="Your email">
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _blog_personal(self, colors: dict) -> str:
        """Personal Blog"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Personal Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; background: #fdfcfb; color: #333; }}
        .container {{ max-width: 800px; margin: 0 auto; padding: 80px 40px; }}
        
        /* Header */
        .blog-header {{ text-align: center; margin-bottom: 80px; padding-bottom: 40px; 
                       border-bottom: 2px solid #e0e0e0; }}
        .blog-title {{ font-size: 56px; font-weight: 900; margin-bottom: 16px; color: {colors['primary']}; }}
        .blog-tagline {{ font-size: 18px; color: #666; font-style: italic; }}
        
        /* Post */
        .post {{ margin-bottom: 80px; }}
        .post-date {{ font-size: 14px; color: #999; margin-bottom: 16px; text-transform: uppercase; 
                     letter-spacing: 2px; }}
        .post-title {{ font-size: 42px; font-weight: 900; margin-bottom: 24px; line-height: 1.2; }}
        .post-excerpt {{ font-size: 20px; line-height: 1.7; color: #666; margin-bottom: 24px; }}
        .read-more {{ font-size: 16px; color: {colors['primary']}; font-weight: 700; 
                     text-decoration: none; }}
        .read-more:hover {{ text-decoration: underline; }}
        
        /* Featured Image */
        .featured-image {{ width: 100%; aspect-ratio: 16/9; border-radius: 16px; margin-bottom: 32px; 
                          background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        
        /* Categories */
        .categories {{ display: flex; gap: 12px; margin-bottom: 24px; flex-wrap: wrap; }}
        .category {{ padding: 6px 16px; background: {colors['primary']}; color: white; 
                    border-radius: 20px; font-size: 13px; font-weight: 700; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="blog-header">
            <h1 class="blog-title">My Journal</h1>
            <p class="blog-tagline">Thoughts, stories, and ideas</p>
        </div>
        
        <article class="post">
            <div class="post-date">March 18, 2024</div>
            <h2 class="post-title">Finding Balance in a Digital World</h2>
            <div class="categories">
                <span class="category">Life</span>
                <span class="category">Technology</span>
            </div>
            <div class="featured-image"></div>
            <p class="post-excerpt">In today's hyperconnected world, finding moments of stillness has become increasingly challenging. This is my journey toward digital minimalism and intentional living...</p>
            <a href="#" class="read-more">Read More →</a>
        </article>
        
        <article class="post">
            <div class="post-date">March 15, 2024</div>
            <h2 class="post-title">The Art of Slow Living</h2>
            <div class="categories">
                <span class="category">Lifestyle</span>
            </div>
            <div class="featured-image"></div>
            <p class="post-excerpt">Learning to appreciate the simple moments and embrace a slower pace of life has transformed my perspective. Here's what I've discovered along the way...</p>
            <a href="#" class="read-more">Read More →</a>
        </article>
        
        <article class="post">
            <div class="post-date">March 12, 2024</div>
            <h2 class="post-title">Creative Morning Routines</h2>
            <div class="categories">
                <span class="category">Productivity</span>
                <span class="category">Creativity</span>
            </div>
            <div class="featured-image"></div>
            <p class="post-excerpt">How I redesigned my mornings to prioritize creativity and set the tone for productive, fulfilling days...</p>
            <a href="#" class="read-more">Read More →</a>
        </article>
    </div>
</body>
</html>"""
    
    def _blog_tech_news(self, colors: dict) -> str:
        """Tech News Blog"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Tech News</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #0a0a0a; color: white; }}
        
        /* Header */
        .header {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                  padding: 60px; text-align: center; }}
        .header h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 16px; }}
        .header p {{ font-size: 20px; opacity: 0.95; }}
        
        /* Breaking News */
        .breaking {{ background: #ff0000; padding: 20px 60px; font-weight: 700; font-size: 14px; 
                    display: flex; gap: 16px; align-items: center; }}
        .breaking-label {{ background: white; color: #ff0000; padding: 6px 12px; border-radius: 4px; }}
        
        .container {{ max-width: 1400px; margin: 0 auto; padding: 60px 40px; }}
        
        /* Featured Story */
        .featured {{ background: #1a1a1a; border-radius: 24px; overflow: hidden; margin-bottom: 60px; 
                    display: grid; grid-template-columns: 1.2fr 1fr; }}
        .featured-image {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                          aspect-ratio: 16/9; }}
        .featured-content {{ padding: 60px; }}
        .featured-tag {{ color: {colors['accent']}; font-size: 14px; font-weight: 700; 
                        margin-bottom: 16px; }}
        .featured-title {{ font-size: 42px; font-weight: 900; margin-bottom: 20px; line-height: 1.2; }}
        .featured-excerpt {{ font-size: 18px; line-height: 1.7; color: #999; margin-bottom: 24px; }}
        .featured-meta {{ font-size: 14px; color: #666; }}
        
        /* News Grid */
        .news-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }}
        .news-card {{ background: #1a1a1a; border-radius: 16px; overflow: hidden; cursor: pointer; 
                     transition: transform 0.3s; }}
        .news-card:hover {{ transform: translateY(-5px); }}
        .news-image {{ width: 100%; aspect-ratio: 16/9; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .news-content {{ padding: 28px; }}
        .news-tag {{ color: {colors['accent']}; font-size: 12px; font-weight: 700; margin-bottom: 12px; }}
        .news-title {{ font-size: 20px; font-weight: 900; margin-bottom: 12px; line-height: 1.3; }}
        .news-excerpt {{ font-size: 14px; color: #999; margin-bottom: 16px; line-height: 1.6; }}
        .news-meta {{ font-size: 12px; color: #666; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>TechDaily</h1>
        <p>Latest technology news and insights</p>
    </div>
    
    <div class="breaking">
        <span class="breaking-label">BREAKING</span>
        <span>Major AI breakthrough announced by leading tech company</span>
    </div>
    
    <div class="container">
        <div class="featured">
            <div class="featured-image"></div>
            <div class="featured-content">
                <div class="featured-tag">ARTIFICIAL INTELLIGENCE</div>
                <h2 class="featured-title">The Future of AI: What's Coming in 2024</h2>
                <p class="featured-excerpt">Experts predict revolutionary advances in artificial intelligence that will transform how we work, communicate, and solve complex problems.</p>
                <div class="featured-meta">By Sarah Chen • 2 hours ago</div>
            </div>
        </div>
        
        <div class="news-grid">
            <div class="news-card">
                <div class="news-image"></div>
                <div class="news-content">
                    <div class="news-tag">SMARTPHONES</div>
                    <h3 class="news-title">New Flagship Phone Breaks Performance Records</h3>
                    <p class="news-excerpt">Latest benchmark tests reveal unprecedented processing power...</p>
                    <div class="news-meta">4 hours ago</div>
                </div>
            </div>
            
            <div class="news-card">
                <div class="news-image"></div>
                <div class="news-content">
                    <div class="news-tag">CYBERSECURITY</div>
                    <h3 class="news-title">Major Security Vulnerability Discovered</h3>
                    <p class="news-excerpt">Researchers find critical flaw affecting millions of devices...</p>
                    <div class="news-meta">6 hours ago</div>
                </div>
            </div>
            
            <div class="news-card">
                <div class="news-image"></div>
                <div class="news-content">
                    <div class="news-tag">STARTUPS</div>
                    <h3 class="news-title">Tech Startup Raises $100M Series B</h3>
                    <p class="news-excerpt">Emerging company valued at $1 billion after latest funding round...</p>
                    <div class="news-meta">8 hours ago</div>
                </div>
            </div>
            
            <div class="news-card">
                <div class="news-image"></div>
                <div class="news-content">
                    <div class="news-tag">CLOUD COMPUTING</div>
                    <h3 class="news-title">Cloud Services See Record Growth</h3>
                    <p class="news-excerpt">Market analysis shows 45% increase in cloud adoption...</p>
                    <div class="news-meta">10 hours ago</div>
                </div>
            </div>
            
            <div class="news-card">
                <div class="news-image"></div>
                <div class="news-content">
                    <div class="news-tag">GAMING</div>
                    <h3 class="news-title">Next-Gen Console Specs Revealed</h3>
                    <p class="news-excerpt">Technical specifications promise 8K gaming at 120fps...</p>
                    <div class="news-meta">12 hours ago</div>
                </div>
            </div>
            
            <div class="news-card">
                <div class="news-image"></div>
                <div class="news-content">
                    <div class="news-tag">ELECTRIC VEHICLES</div>
                    <h3 class="news-title">EV Sales Surpass Traditional Cars</h3>
                    <p class="news-excerpt">Historic milestone as electric vehicles dominate market...</p>
                    <div class="news-meta">1 day ago</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _blog_food_recipe(self, colors: dict) -> str:
        """Food & Recipe Blog"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Food Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        
        /* Hero */
        .hero {{ background: linear-gradient(rgba(0,0,0,0.3), rgba(0,0,0,0.3)), 
                linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                height: 60vh; display: flex; align-items: center; justify-content: center; 
                text-align: center; color: white; }}
        .hero h1 {{ font-size: 72px; font-weight: 900; margin-bottom: 16px; }}
        .hero p {{ font-size: 24px; }}
        
        .container {{ max-width: 1400px; margin: 80px auto; padding: 0 40px; }}
        
        /* Recipe Grid */
        .recipe-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }}
        .recipe-card {{ background: white; border-radius: 20px; overflow: hidden; 
                       box-shadow: 0 4px 20px rgba(0,0,0,0.08); transition: transform 0.3s; }}
        .recipe-card:hover {{ transform: translateY(-8px); }}
        .recipe-image {{ width: 100%; aspect-ratio: 1; 
                        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .recipe-info {{ padding: 32px; }}
        .recipe-category {{ font-size: 12px; color: {colors['primary']}; font-weight: 700; 
                           text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; }}
        .recipe-title {{ font-size: 26px; font-weight: 900; margin-bottom: 16px; }}
        .recipe-desc {{ font-size: 15px; color: #666; line-height: 1.7; margin-bottom: 20px; }}
        .recipe-meta {{ display: flex; gap: 20px; font-size: 14px; color: #999; }}
        .meta-item {{ display: flex; align-items: center; gap: 6px; }}
        
        /* Featured Recipe */
        .featured-recipe {{ margin-bottom: 80px; background: #fafafa; border-radius: 24px; padding: 60px; 
                           display: grid; grid-template-columns: 1fr 1fr; gap: 60px; align-items: center; }}
        .featured-image {{ width: 100%; aspect-ratio: 4/3; border-radius: 20px; 
                          background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .featured-badge {{ display: inline-block; padding: 8px 20px; background: {colors['primary']}; 
                          color: white; border-radius: 20px; font-size: 12px; font-weight: 700; 
                          margin-bottom: 20px; }}
        .featured-title {{ font-size: 48px; font-weight: 900; margin-bottom: 20px; }}
        .featured-desc {{ font-size: 18px; line-height: 1.7; color: #666; margin-bottom: 24px; }}
        .view-recipe-btn {{ padding: 16px 40px; background: {colors['primary']}; color: white; 
                           border: none; border-radius: 12px; font-weight: 700; font-size: 16px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="hero">
        <div>
            <h1>Delicious Recipes</h1>
            <p>Homemade meals that bring joy to your table</p>
        </div>
    </div>
    
    <div class="container">
        <div class="featured-recipe">
            <div class="featured-image"></div>
            <div>
                <span class="featured-badge">FEATURED RECIPE</span>
                <h2 class="featured-title">Classic Italian Carbonara</h2>
                <p class="featured-desc">A traditional Roman pasta dish with crispy pancetta, creamy egg sauce, and perfectly al dente spaghetti. Simple ingredients, incredible flavor.</p>
                <button class="view-recipe-btn">View Full Recipe</button>
            </div>
        </div>
        
        <div class="recipe-grid">
            <div class="recipe-card">
                <div class="recipe-image"></div>
                <div class="recipe-info">
                    <div class="recipe-category">Breakfast</div>
                    <h3 class="recipe-title">Fluffy Pancakes</h3>
                    <p class="recipe-desc">Light and airy pancakes perfect for weekend mornings.</p>
                    <div class="recipe-meta">
                        <span class="meta-item">⏱ 20 min</span>
                        <span class="meta-item">🍴 4 servings</span>
                    </div>
                </div>
            </div>
            
            <div class="recipe-card">
                <div class="recipe-image"></div>
                <div class="recipe-info">
                    <div class="recipe-category">Main Course</div>
                    <h3 class="recipe-title">Grilled Salmon</h3>
                    <p class="recipe-desc">Perfectly seasoned salmon with lemon and herbs.</p>
                    <div class="recipe-meta">
                        <span class="meta-item">⏱ 25 min</span>
                        <span class="meta-item">🍴 2 servings</span>
                    </div>
                </div>
            </div>
            
            <div class="recipe-card">
                <div class="recipe-image"></div>
                <div class="recipe-info">
                    <div class="recipe-category">Dessert</div>
                    <h3 class="recipe-title">Chocolate Cake</h3>
                    <p class="recipe-desc">Rich, moist chocolate cake with ganache frosting.</p>
                    <div class="recipe-meta">
                        <span class="meta-item">⏱ 60 min</span>
                        <span class="meta-item">🍴 8 servings</span>
                    </div>
                </div>
            </div>
            
            <div class="recipe-card">
                <div class="recipe-image"></div>
                <div class="recipe-info">
                    <div class="recipe-category">Salad</div>
                    <h3 class="recipe-title">Caesar Salad</h3>
                    <p class="recipe-desc">Classic Caesar with homemade dressing and croutons.</p>
                    <div class="recipe-meta">
                        <span class="meta-item">⏱ 15 min</span>
                        <span class="meta-item">🍴 4 servings</span>
                    </div>
                </div>
            </div>
            
            <div class="recipe-card">
                <div class="recipe-image"></div>
                <div class="recipe-info">
                    <div class="recipe-category">Appetizer</div>
                    <h3 class="recipe-title">Bruschetta</h3>
                    <p class="recipe-desc">Toasted bread topped with fresh tomatoes and basil.</p>
                    <div class="recipe-meta">
                        <span class="meta-item">⏱ 10 min</span>
                        <span class="meta-item">🍴 6 servings</span>
                    </div>
                </div>
            </div>
            
            <div class="recipe-card">
                <div class="recipe-image"></div>
                <div class="recipe-info">
                    <div class="recipe-category">Soup</div>
                    <h3 class="recipe-title">Tomato Soup</h3>
                    <p class="recipe-desc">Creamy tomato soup perfect for chilly days.</p>
                    <div class="recipe-meta">
                        <span class="meta-item">⏱ 30 min</span>
                        <span class="meta-item">🍴 4 servings</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _blog_travel(self, colors: dict) -> str:
        """Travel Blog"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Travel Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        
        /* Hero */
        .hero {{ height: 80vh; background: linear-gradient(rgba(0,0,0,0.4), rgba(0,0,0,0.4)), 
                linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                display: flex; align-items: center; justify-content: center; text-align: center; color: white; }}
        .hero h1 {{ font-size: 84px; font-weight: 900; margin-bottom: 24px; }}
        .hero p {{ font-size: 28px; opacity: 0.95; }}
        
        /* Destinations */
        .destinations {{ padding: 100px 60px; max-width: 1600px; margin: 0 auto; }}
        .section-title {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .destination-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 40px; }}
        .destination-card {{ position: relative; border-radius: 24px; overflow: hidden; height: 500px; 
                            cursor: pointer; }}
        .destination-image {{ width: 100%; height: 100%; 
                             background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .destination-overlay {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 50px; 
                               background: linear-gradient(transparent, rgba(0,0,0,0.9)); color: white; }}
        .destination-location {{ font-size: 14px; font-weight: 700; letter-spacing: 2px; 
                                text-transform: uppercase; margin-bottom: 12px; opacity: 0.9; }}
        .destination-title {{ font-size: 36px; font-weight: 900; margin-bottom: 12px; }}
        .destination-desc {{ font-size: 16px; opacity: 0.9; }}
        
        /* Stories */
        .stories {{ padding: 100px 60px; background: #fafafa; }}
        .stories-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; 
                        max-width: 1600px; margin: 0 auto; }}
        .story-card {{ background: white; border-radius: 20px; overflow: hidden; 
                      box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .story-image {{ width: 100%; aspect-ratio: 16/9; 
                       background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .story-content {{ padding: 32px; }}
        .story-date {{ font-size: 13px; color: #999; margin-bottom: 12px; }}
        .story-title {{ font-size: 24px; font-weight: 900; margin-bottom: 16px; }}
        .story-excerpt {{ font-size: 15px; line-height: 1.7; color: #666; margin-bottom: 20px; }}
        .read-story {{ color: {colors['primary']}; font-weight: 700; text-decoration: none; }}
    </style>
</head>
<body>
    <div class="hero">
        <div>
            <h1>Wanderlust</h1>
            <p>Exploring the world one adventure at a time</p>
        </div>
    </div>
    
    <div class="destinations">
        <h2 class="section-title">Top Destinations</h2>
        <div class="destination-grid">
            <div class="destination-card">
                <div class="destination-image"></div>
                <div class="destination-overlay">
                    <div class="destination-location">Japan</div>
                    <h3 class="destination-title">Tokyo & Kyoto</h3>
                    <p class="destination-desc">Experience ancient temples and modern technology</p>
                </div>
            </div>
            
            <div class="destination-card">
                <div class="destination-image"></div>
                <div class="destination-overlay">
                    <div class="destination-location">Italy</div>
                    <h3 class="destination-title">Amalfi Coast</h3>
                    <p class="destination-desc">Stunning coastal views and Mediterranean charm</p>
                </div>
            </div>
            
            <div class="destination-card">
                <div class="destination-image"></div>
                <div class="destination-overlay">
                    <div class="destination-location">Iceland</div>
                    <h3 class="destination-title">Reykjavik</h3>
                    <p class="destination-desc">Northern lights and natural wonders</p>
                </div>
            </div>
            
            <div class="destination-card">
                <div class="destination-image"></div>
                <div class="destination-overlay">
                    <div class="destination-location">Peru</div>
                    <h3 class="destination-title">Machu Picchu</h3>
                    <p class="destination-desc">Ancient Incan citadel in the clouds</p>
                </div>
            </div>
        </div>
    </div>
    
    <div class="stories">
        <h2 class="section-title">Travel Stories</h2>
        <div class="stories-grid">
            <div class="story-card">
                <div class="story-image"></div>
                <div class="story-content">
                    <div class="story-date">March 18, 2024</div>
                    <h3 class="story-title">10 Days in Tokyo: A Complete Guide</h3>
                    <p class="story-excerpt">From bustling streets of Shibuya to peaceful temples in Asakusa, discover the best of Japan's capital city...</p>
                    <a href="#" class="read-story">Read More →</a>
                </div>
            </div>
            
            <div class="story-card">
                <div class="story-image"></div>
                <div class="story-content">
                    <div class="story-date">March 15, 2024</div>
                    <h3 class="story-title">Hidden Gems of the Amalfi Coast</h3>
                    <p class="story-excerpt">Beyond the tourist hotspots lie charming villages and secret beaches waiting to be discovered...</p>
                    <a href="#" class="read-story">Read More →</a>
                </div>
            </div>
            
            <div class="story-card">
                <div class="story-image"></div>
                <div class="story-content">
                    <div class="story-date">March 12, 2024</div>
                    <h3 class="story-title">Chasing Northern Lights in Iceland</h3>
                    <p class="story-excerpt">Tips and tricks for photographing the aurora borealis in the land of fire and ice...</p>
                    <a href="#" class="read-story">Read More →</a>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _blog_minimal_medium(self, colors: dict) -> str:
        """Minimal Medium-Style Blog"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimal Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Georgia', serif; background: white; color: #1a1a1a; }}
        
        /* Navigation */
        nav {{ padding: 30px 60px; border-bottom: 1px solid #e0e0e0; display: flex; 
              justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 28px; font-weight: 900; }}
        .subscribe-btn {{ padding: 10px 24px; background: {colors['primary']}; color: white; 
                         border: none; border-radius: 20px; font-weight: 700; cursor: pointer; }}
        
        /* Container */
        .container {{ max-width: 720px; margin: 80px auto; padding: 0 40px; }}
        
        /* Article */
        .article {{ margin-bottom: 80px; padding-bottom: 60px; border-bottom: 1px solid #f0f0f0; }}
        .article-meta {{ display: flex; gap: 16px; align-items: center; margin-bottom: 24px; }}
        .author-avatar {{ width: 48px; height: 48px; border-radius: 50%; 
                         background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .author-info {{ }}
        .author-name {{ font-size: 15px; font-weight: 700; margin-bottom: 4px; }}
        .article-date {{ font-size: 14px; color: #666; }}
        
        .article-title {{ font-size: 48px; font-weight: 900; line-height: 1.2; margin-bottom: 20px; 
                         font-family: 'Inter', sans-serif; }}
        .article-subtitle {{ font-size: 22px; line-height: 1.5; color: #666; margin-bottom: 32px; }}
        .article-image {{ width: 100%; aspect-ratio: 16/9; border-radius: 8px; margin-bottom: 32px; 
                         background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .article-content {{ font-size: 20px; line-height: 1.8; }}
        .article-content p {{ margin-bottom: 24px; }}
        
        /* Read Time */
        .read-time {{ display: inline-block; padding: 6px 12px; background: #f0f0f0; border-radius: 4px; 
                     font-size: 13px; font-weight: 600; margin-bottom: 24px; font-family: 'Inter', sans-serif; }}
        
        /* Claps */
        .article-footer {{ display: flex; gap: 24px; margin-top: 40px; padding-top: 24px; 
                          border-top: 1px solid #f0f0f0; }}
        .clap-btn {{ display: flex; align-items: center; gap: 8px; padding: 10px 20px; 
                    border: 1px solid #e0e0e0; border-radius: 20px; background: white; 
                    font-weight: 600; cursor: pointer; }}
    </style>
</head>
<body>
    <nav>
        <div class="logo">Medium</div>
        <button class="subscribe-btn">Subscribe</button>
    </nav>
    
    <div class="container">
        <article class="article">
            <div class="article-meta">
                <div class="author-avatar"></div>
                <div class="author-info">
                    <div class="author-name">Sarah Johnson</div>
                    <div class="article-date">Mar 18 • 8 min read</div>
                </div>
            </div>
            
            <h1 class="article-title">The Future of Remote Work: Lessons from 2024</h1>
            <p class="article-subtitle">How distributed teams are reshaping the way we think about productivity, collaboration, and work-life balance.</p>
            
            <div class="article-image"></div>
            
            <div class="article-content">
                <p>The landscape of work has fundamentally changed. What started as a temporary response to global circumstances has evolved into a permanent shift in how we approach our professional lives.</p>
                
                <p>Companies that once insisted on office presence are now embracing hybrid models, while others have gone fully remote. This transformation isn't just about where we work—it's about reimagining what work means in the modern era.</p>
                
                <p>Through conversations with leaders across industries, patterns emerge. Successful remote organizations share common traits: intentional communication, trust-based management, and technology that enhances rather than hinders human connection.</p>
            </div>
            
            <div class="article-footer">
                <button class="clap-btn">👏 247</button>
                <button class="clap-btn">💬 12</button>
            </div>
        </article>
        
        <article class="article">
            <div class="article-meta">
                <div class="author-avatar"></div>
                <div class="author-info">
                    <div class="author-name">Michael Chen</div>
                    <div class="article-date">Mar 15 • 6 min read</div>
                </div>
            </div>
            
            <h1 class="article-title">Building Products People Love: A Designer's Perspective</h1>
            <p class="article-subtitle">The intersection of user needs, business goals, and technical constraints.</p>
            
            <div class="article-image"></div>
            
            <div class="article-content">
                <p>Great products don't happen by accident. They emerge from a deep understanding of human behavior, careful attention to detail, and countless iterations.</p>
                
                <p>In my years designing digital experiences, I've learned that the best solutions often come from constraints. When you're forced to simplify, to focus on what truly matters, magic happens.</p>
            </div>
            
            <div class="article-footer">
                <button class="clap-btn">👏 189</button>
                <button class="clap-btn">💬 8</button>
            </div>
        </article>
    </div>
</body>
</html>"""
    
    # ===== Components (5가지 구조) =====
    def generate_components(self, colors: dict) -> str:
        """Components 디자인 생성"""
        layouts = [
            self._components_showcase,
            self._components_library,
            self._components_design_system,
            self._components_pattern_library,
            self._components_interactive_demo,
            self._components_form_elements,
            self._components_navigation_menus,
            self._components_card_layouts,
            self._components_modal_dialogs,
            self._components_pricing_tables,
        ]
        chosen_method = random.choice(layouts)
        self.current_method_name = chosen_method.__name__
        return chosen_method(colors)
    
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

    def _components_design_system(self, colors: dict) -> str:
        """Design System Documentation"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Design System</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; }}
        
        /* Sidebar Navigation */
        .layout {{ display: grid; grid-template-columns: 280px 1fr; min-height: 100vh; }}
        .sidebar {{ background: #1a1a1a; color: white; padding: 40px 0; }}
        .sidebar-brand {{ padding: 0 30px; font-size: 24px; font-weight: 900; margin-bottom: 50px; 
                         color: {colors['primary']}; }}
        .nav-group {{ padding: 0 20px; margin-bottom: 30px; }}
        .nav-group-title {{ font-size: 12px; opacity: 0.5; margin-bottom: 12px; padding: 0 10px; }}
        .nav-item {{ padding: 12px 16px; border-radius: 8px; margin-bottom: 4px; cursor: pointer; }}
        .nav-item:hover {{ background: rgba(255,255,255,0.1); }}
        
        /* Main Content */
        .main {{ padding: 80px 100px; }}
        .page-title {{ font-size: 56px; font-weight: 900; margin-bottom: 16px; }}
        .page-subtitle {{ font-size: 20px; color: #666; margin-bottom: 60px; }}
        
        /* Color Palette */
        .color-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 30px; margin-bottom: 80px; }}
        .color-card {{ aspect-ratio: 1.5; border-radius: 20px; padding: 30px; color: white; 
                      display: flex; flex-direction: column; justify-content: flex-end; }}
        .color-name {{ font-size: 24px; font-weight: 900; margin-bottom: 8px; }}
        .color-hex {{ font-size: 16px; opacity: 0.9; }}
        
        /* Typography */
        .typo-section {{ margin-bottom: 80px; }}
        .typo-section h2 {{ font-size: 36px; font-weight: 900; margin-bottom: 40px; }}
        .typo-sample {{ padding: 40px; background: #f8f9fa; border-radius: 16px; margin-bottom: 20px; }}
        
        /* Spacing System */
        .spacing-grid {{ display: flex; gap: 20px; align-items: flex-end; }}
        .spacing-box {{ background: {colors['primary']}; border-radius: 8px; }}
    </style>
</head>
<body>
    <div class="layout">
        <div class="sidebar">
            <div class="sidebar-brand">Design System</div>
            <div class="nav-group">
                <div class="nav-group-title">FOUNDATIONS</div>
                <div class="nav-item">Colors</div>
                <div class="nav-item">Typography</div>
                <div class="nav-item">Spacing</div>
                <div class="nav-item">Icons</div>
            </div>
            <div class="nav-group">
                <div class="nav-group-title">COMPONENTS</div>
                <div class="nav-item">Buttons</div>
                <div class="nav-item">Forms</div>
                <div class="nav-item">Cards</div>
                <div class="nav-item">Navigation</div>
            </div>
        </div>
        
        <div class="main">
            <h1 class="page-title">Color System</h1>
            <p class="page-subtitle">Our carefully crafted color palette for consistent brand experience</p>
            
            <div class="color-grid">
                <div class="color-card" style="background: {colors['primary']};">
                    <div class="color-name">Primary</div>
                    <div class="color-hex">{colors['primary']}</div>
                </div>
                <div class="color-card" style="background: {colors['secondary']};">
                    <div class="color-name">Secondary</div>
                    <div class="color-hex">{colors['secondary']}</div>
                </div>
                <div class="color-card" style="background: {colors['accent']};">
                    <div class="color-name">Accent</div>
                    <div class="color-hex">{colors['accent']}</div>
                </div>
            </div>
            
            <div class="typo-section">
                <h2>Typography Scale</h2>
                <div class="typo-sample" style="font-size: 48px; font-weight: 900;">Heading 1</div>
                <div class="typo-sample" style="font-size: 36px; font-weight: 800;">Heading 2</div>
                <div class="typo-sample" style="font-size: 24px; font-weight: 700;">Heading 3</div>
                <div class="typo-sample" style="font-size: 18px;">Body Text</div>
            </div>
            
            <div>
                <h2 style="font-size: 36px; font-weight: 900; margin-bottom: 40px;">Spacing Scale</h2>
                <div class="spacing-grid">
                    <div class="spacing-box" style="width: 40px; height: 40px;"></div>
                    <div class="spacing-box" style="width: 60px; height: 60px;"></div>
                    <div class="spacing-box" style="width: 80px; height: 80px;"></div>
                    <div class="spacing-box" style="width: 100px; height: 100px;"></div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _components_pattern_library(self, colors: dict) -> str:
        """Pattern Library with Examples"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pattern Library</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', sans-serif; padding: 80px 60px; background: #fafafa; }}
        
        .container {{ max-width: 1600px; margin: 0 auto; }}
        .header {{ text-align: center; margin-bottom: 80px; }}
        .header h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 20px; }}
        .header p {{ font-size: 22px; color: #666; }}
        
        /* Pattern Grid */
        .pattern-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 50px; }}
        .pattern-card {{ background: white; border-radius: 24px; overflow: hidden; 
                        box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
        .pattern-preview {{ padding: 60px; background: linear-gradient(135deg, {colors['primary']}10, {colors['secondary']}10); 
                           display: flex; align-items: center; justify-content: center; min-height: 300px; }}
        .pattern-info {{ padding: 40px; }}
        .pattern-title {{ font-size: 28px; font-weight: 900; margin-bottom: 16px; }}
        .pattern-desc {{ font-size: 16px; color: #666; line-height: 1.7; margin-bottom: 24px; }}
        .pattern-code {{ background: #1a1a1a; color: #00ff00; padding: 20px; border-radius: 12px; 
                        font-family: 'Courier New', monospace; font-size: 14px; }}
        
        /* Sample Components */
        .sample-btn {{ padding: 16px 40px; background: {colors['primary']}; color: white; border: none; 
                      border-radius: 12px; font-weight: 700; font-size: 16px; }}
        .sample-card {{ background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); }}
        .sample-input {{ width: 100%; padding: 16px; border: 2px solid {colors['primary']}; border-radius: 10px; 
                        font-size: 16px; }}
        .sample-badge {{ padding: 8px 20px; background: {colors['accent']}; color: white; border-radius: 20px; 
                        font-size: 14px; font-weight: 700; display: inline-block; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>UI Pattern Library</h1>
            <p>Reusable components and design patterns</p>
        </div>
        
        <div class="pattern-grid">
            <div class="pattern-card">
                <div class="pattern-preview">
                    <button class="sample-btn">Primary Button</button>
                </div>
                <div class="pattern-info">
                    <h3 class="pattern-title">Button Component</h3>
                    <p class="pattern-desc">Primary action button with hover effects and multiple variants</p>
                    <div class="pattern-code">&lt;button class="btn-primary"&gt;Click Me&lt;/button&gt;</div>
                </div>
            </div>
            
            <div class="pattern-card">
                <div class="pattern-preview">
                    <div class="sample-card" style="width: 300px;">
                        <h4 style="font-size: 20px; margin-bottom: 12px;">Card Title</h4>
                        <p style="color: #666;">Card description text goes here</p>
                    </div>
                </div>
                <div class="pattern-info">
                    <h3 class="pattern-title">Card Component</h3>
                    <p class="pattern-desc">Versatile container for grouping related content</p>
                    <div class="pattern-code">&lt;div class="card"&gt;Content&lt;/div&gt;</div>
                </div>
            </div>
            
            <div class="pattern-card">
                <div class="pattern-preview">
                    <input class="sample-input" placeholder="Enter your email" style="max-width: 400px;">
                </div>
                <div class="pattern-info">
                    <h3 class="pattern-title">Input Field</h3>
                    <p class="pattern-desc">Form input with validation states and focus styling</p>
                    <div class="pattern-code">&lt;input class="input-field" /&gt;</div>
                </div>
            </div>
            
            <div class="pattern-card">
                <div class="pattern-preview">
                    <span class="sample-badge">New Feature</span>
                </div>
                <div class="pattern-info">
                    <h3 class="pattern-title">Badge Component</h3>
                    <p class="pattern-desc">Small status indicators and labels</p>
                    <div class="pattern-code">&lt;span class="badge"&gt;Badge&lt;/span&gt;</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _components_interactive_demo(self, colors: dict) -> str:
        """Interactive Component Playground"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Component Playground</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; }}
        
        /* Top Bar */
        .topbar {{ background: white; padding: 20px 60px; border-bottom: 2px solid #e0e0e0; 
                  display: flex; justify-content: space-between; align-items: center; }}
        .logo {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; }}
        .theme-toggle {{ padding: 10px 24px; border: 2px solid {colors['primary']}; background: white; 
                        border-radius: 8px; font-weight: 700; cursor: pointer; }}
        
        /* Split Layout */
        .split {{ display: grid; grid-template-columns: 1fr 1fr; height: calc(100vh - 80px); }}
        
        /* Left - Component List */
        .component-list {{ background: white; padding: 40px; overflow-y: auto; border-right: 2px solid #e0e0e0; }}
        .component-list h2 {{ font-size: 32px; font-weight: 900; margin-bottom: 30px; }}
        .component-item {{ padding: 20px; margin-bottom: 12px; background: #f8f9fa; border-radius: 12px; 
                          cursor: pointer; transition: all 0.3s; }}
        .component-item:hover {{ background: {colors['primary']}; color: white; transform: translateX(5px); }}
        .component-name {{ font-size: 18px; font-weight: 700; margin-bottom: 6px; }}
        .component-category {{ font-size: 14px; opacity: 0.7; }}
        
        /* Right - Preview Area */
        .preview-area {{ padding: 60px; overflow-y: auto; display: flex; align-items: center; 
                        justify-content: center; }}
        .preview-content {{ text-align: center; }}
        .preview-content h3 {{ font-size: 36px; font-weight: 900; margin-bottom: 40px; }}
        
        /* Sample Components in Preview */
        .demo-buttons {{ display: flex; gap: 16px; flex-wrap: wrap; justify-content: center; margin-bottom: 40px; }}
        .demo-btn {{ padding: 16px 36px; border-radius: 12px; font-weight: 700; border: none; cursor: pointer; }}
        .demo-btn-primary {{ background: {colors['primary']}; color: white; }}
        .demo-btn-secondary {{ background: {colors['secondary']}; color: white; }}
        .demo-btn-outline {{ background: white; border: 3px solid {colors['primary']}; color: {colors['primary']}; }}
        
        .demo-cards {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 20px; max-width: 600px; }}
        .demo-card {{ background: white; padding: 30px; border-radius: 16px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); 
                     text-align: left; }}
        .demo-card h4 {{ font-size: 20px; margin-bottom: 12px; }}
        .demo-card p {{ color: #666; }}
    </style>
</head>
<body>
    <div class="topbar">
        <div class="logo">Component Playground</div>
        <button class="theme-toggle">Toggle Theme</button>
    </div>
    
    <div class="split">
        <div class="component-list">
            <h2>Components</h2>
            <div class="component-item">
                <div class="component-name">Buttons</div>
                <div class="component-category">Actions & Controls</div>
            </div>
            <div class="component-item">
                <div class="component-name">Cards</div>
                <div class="component-category">Containers</div>
            </div>
            <div class="component-item">
                <div class="component-name">Forms</div>
                <div class="component-category">Input Elements</div>
            </div>
            <div class="component-item">
                <div class="component-name">Navigation</div>
                <div class="component-category">Navigation</div>
            </div>
            <div class="component-item">
                <div class="component-name">Modals</div>
                <div class="component-category">Overlays</div>
            </div>
            <div class="component-item">
                <div class="component-name">Tables</div>
                <div class="component-category">Data Display</div>
            </div>
        </div>
        
        <div class="preview-area">
            <div class="preview-content">
                <h3>Button Variations</h3>
                <div class="demo-buttons">
                    <button class="demo-btn demo-btn-primary">Primary</button>
                    <button class="demo-btn demo-btn-secondary">Secondary</button>
                    <button class="demo-btn demo-btn-outline">Outline</button>
                </div>
                
                <h3 style="margin-top: 40px;">Card Examples</h3>
                <div class="demo-cards" style="margin-top: 30px;">
                    <div class="demo-card">
                        <h4>Feature Card</h4>
                        <p>Description text goes here</p>
                    </div>
                    <div class="demo-card">
                        <h4>Info Card</h4>
                        <p>More information here</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _components_form_elements(self, colors: dict) -> str:
        """Form Elements Library"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Elements</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; padding: 80px 40px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        h1 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 60px; 
             background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
             -webkit-background-clip: text; -webkit-text-fill-color: transparent; }}
        
        .form-section {{ background: white; padding: 50px; border-radius: 24px; margin-bottom: 40px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .form-section h2 {{ font-size: 32px; font-weight: 900; margin-bottom: 32px; }}
        
        /* Input Fields */
        .input-group {{ margin-bottom: 24px; }}
        .input-label {{ display: block; font-size: 14px; font-weight: 700; margin-bottom: 8px; }}
        .input-field {{ width: 100%; padding: 16px; border: 2px solid #e0e0e0; border-radius: 12px; 
                       font-size: 16px; transition: border 0.3s; }}
        .input-field:focus {{ outline: none; border-color: {colors['primary']}; }}
        .input-field::placeholder {{ color: #999; }}
        
        /* Textarea */
        textarea.input-field {{ min-height: 120px; resize: vertical; font-family: inherit; }}
        
        /* Select */
        select.input-field {{ cursor: pointer; }}
        
        /* Checkbox & Radio */
        .checkbox-group, .radio-group {{ margin-bottom: 24px; }}
        .checkbox-item, .radio-item {{ display: flex; align-items: center; gap: 12px; margin-bottom: 12px; }}
        input[type="checkbox"], input[type="radio"] {{ width: 20px; height: 20px; cursor: pointer; }}
        
        /* Buttons */
        .button-group {{ display: flex; gap: 16px; flex-wrap: wrap; }}
        .btn {{ padding: 16px 36px; border-radius: 12px; font-weight: 700; font-size: 16px; cursor: pointer; }}
        .btn-primary {{ background: {colors['primary']}; color: white; border: none; }}
        .btn-secondary {{ background: {colors['secondary']}; color: white; border: none; }}
        .btn-outline {{ background: white; color: {colors['primary']}; border: 2px solid {colors['primary']}; }}
        .btn-ghost {{ background: transparent; color: {colors['primary']}; border: none; }}
        
        /* Switch */
        .switch-group {{ margin-bottom: 24px; }}
        .switch {{ position: relative; display: inline-block; width: 60px; height: 34px; }}
        .switch input {{ opacity: 0; width: 0; height: 0; }}
        .slider {{ position: absolute; cursor: pointer; top: 0; left: 0; right: 0; bottom: 0; 
                  background-color: #ccc; border-radius: 34px; transition: .4s; }}
        .slider:before {{ position: absolute; content: ""; height: 26px; width: 26px; left: 4px; 
                        bottom: 4px; background-color: white; border-radius: 50%; transition: .4s; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Form Elements Library</h1>
        
        <div class="form-section">
            <h2>Text Inputs</h2>
            <div class="input-group">
                <label class="input-label">Full Name</label>
                <input type="text" class="input-field" placeholder="Enter your name">
            </div>
            <div class="input-group">
                <label class="input-label">Email Address</label>
                <input type="email" class="input-field" placeholder="your@email.com">
            </div>
            <div class="input-group">
                <label class="input-label">Password</label>
                <input type="password" class="input-field" placeholder="••••••••">
            </div>
        </div>
        
        <div class="form-section">
            <h2>Select & Textarea</h2>
            <div class="input-group">
                <label class="input-label">Country</label>
                <select class="input-field">
                    <option>United States</option>
                    <option>United Kingdom</option>
                    <option>Canada</option>
                    <option>Australia</option>
                </select>
            </div>
            <div class="input-group">
                <label class="input-label">Message</label>
                <textarea class="input-field" placeholder="Enter your message here..."></textarea>
            </div>
        </div>
        
        <div class="form-section">
            <h2>Checkboxes & Radio Buttons</h2>
            <div class="checkbox-group">
                <label class="input-label">Interests (Multiple)</label>
                <div class="checkbox-item">
                    <input type="checkbox" id="web"><label for="web">Web Development</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="design"><label for="design">UI/UX Design</label>
                </div>
                <div class="checkbox-item">
                    <input type="checkbox" id="mobile"><label for="mobile">Mobile Apps</label>
                </div>
            </div>
            
            <div class="radio-group">
                <label class="input-label">Experience Level (Single)</label>
                <div class="radio-item">
                    <input type="radio" name="level" id="beginner"><label for="beginner">Beginner</label>
                </div>
                <div class="radio-item">
                    <input type="radio" name="level" id="intermediate"><label for="intermediate">Intermediate</label>
                </div>
                <div class="radio-item">
                    <input type="radio" name="level" id="advanced"><label for="advanced">Advanced</label>
                </div>
            </div>
        </div>
        
        <div class="form-section">
            <h2>Buttons</h2>
            <div class="button-group">
                <button class="btn btn-primary">Primary Button</button>
                <button class="btn btn-secondary">Secondary Button</button>
                <button class="btn btn-outline">Outline Button</button>
                <button class="btn btn-ghost">Ghost Button</button>
            </div>
        </div>
        
        <div class="form-section">
            <h2>Toggle Switches</h2>
            <div class="switch-group">
                <label class="input-label">Enable Notifications</label>
                <label class="switch">
                    <input type="checkbox">
                    <span class="slider"></span>
                </label>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _components_navigation_menus(self, colors: dict) -> str:
        """Navigation Menus Collection"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation Menus</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; padding: 80px 40px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        h1 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        
        .nav-section {{ background: white; padding: 40px; border-radius: 24px; margin-bottom: 40px; 
                       box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .nav-section h2 {{ font-size: 24px; font-weight: 900; margin-bottom: 24px; }}
        
        /* Horizontal Nav */
        .nav-horizontal {{ background: {colors['primary']}; padding: 20px 40px; border-radius: 16px; 
                          display: flex; justify-content: space-between; align-items: center; }}
        .nav-logo {{ font-size: 24px; font-weight: 900; color: white; }}
        .nav-links {{ display: flex; gap: 32px; }}
        .nav-link {{ color: white; text-decoration: none; font-weight: 600; }}
        
        /* Sidebar Nav */
        .nav-sidebar {{ background: linear-gradient(180deg, {colors['primary']}, {colors['secondary']}); 
                       padding: 40px 30px; border-radius: 16px; color: white; width: 280px; }}
        .sidebar-item {{ padding: 14px 16px; margin-bottom: 8px; border-radius: 10px; cursor: pointer; 
                        transition: background 0.3s; }}
        .sidebar-item:hover {{ background: rgba(255,255,255,0.2); }}
        .sidebar-item.active {{ background: rgba(255,255,255,0.25); font-weight: 700; }}
        
        /* Tab Navigation */
        .nav-tabs {{ display: flex; gap: 8px; background: #f0f0f0; padding: 8px; border-radius: 12px; }}
        .tab {{ flex: 1; padding: 12px 24px; background: transparent; border: none; border-radius: 8px; 
               font-weight: 600; cursor: pointer; transition: background 0.3s; }}
        .tab.active {{ background: white; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }}
        
        /* Breadcrumb */
        .breadcrumb {{ display: flex; gap: 8px; align-items: center; }}
        .breadcrumb-item {{ color: #666; text-decoration: none; }}
        .breadcrumb-item.active {{ color: {colors['primary']}; font-weight: 700; }}
        .breadcrumb-separator {{ color: #ccc; }}
        
        /* Pagination */
        .pagination {{ display: flex; gap: 8px; justify-content: center; }}
        .page-number {{ width: 44px; height: 44px; display: flex; align-items: center; justify-content: center; 
                       border-radius: 8px; border: 2px solid #e0e0e0; cursor: pointer; font-weight: 600; }}
        .page-number.active {{ background: {colors['primary']}; color: white; border-color: {colors['primary']}; }}
        
        /* Dropdown */
        .dropdown {{ position: relative; display: inline-block; }}
        .dropdown-btn {{ padding: 12px 24px; background: {colors['primary']}; color: white; border: none; 
                        border-radius: 10px; font-weight: 700; cursor: pointer; }}
        .dropdown-menu {{ position: absolute; top: 100%; left: 0; margin-top: 8px; background: white; 
                         border-radius: 12px; box-shadow: 0 4px 20px rgba(0,0,0,0.1); min-width: 200px; 
                         padding: 8px; }}
        .dropdown-item {{ padding: 12px 16px; border-radius: 8px; cursor: pointer; }}
        .dropdown-item:hover {{ background: #f5f7fa; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Navigation Components</h1>
        
        <div class="nav-section">
            <h2>Horizontal Navigation</h2>
            <div class="nav-horizontal">
                <div class="nav-logo">Brand</div>
                <div class="nav-links">
                    <a href="#" class="nav-link">Home</a>
                    <a href="#" class="nav-link">Products</a>
                    <a href="#" class="nav-link">About</a>
                    <a href="#" class="nav-link">Contact</a>
                </div>
            </div>
        </div>
        
        <div class="nav-section">
            <h2>Sidebar Navigation</h2>
            <div class="nav-sidebar">
                <div class="sidebar-item active">Dashboard</div>
                <div class="sidebar-item">Analytics</div>
                <div class="sidebar-item">Projects</div>
                <div class="sidebar-item">Team</div>
                <div class="sidebar-item">Settings</div>
            </div>
        </div>
        
        <div class="nav-section">
            <h2>Tab Navigation</h2>
            <div class="nav-tabs">
                <button class="tab active">Overview</button>
                <button class="tab">Details</button>
                <button class="tab">Reviews</button>
                <button class="tab">Specifications</button>
            </div>
        </div>
        
        <div class="nav-section">
            <h2>Breadcrumb Navigation</h2>
            <div class="breadcrumb">
                <a href="#" class="breadcrumb-item">Home</a>
                <span class="breadcrumb-separator">/</span>
                <a href="#" class="breadcrumb-item">Products</a>
                <span class="breadcrumb-separator">/</span>
                <a href="#" class="breadcrumb-item active">Electronics</a>
            </div>
        </div>
        
        <div class="nav-section">
            <h2>Pagination</h2>
            <div class="pagination">
                <div class="page-number">←</div>
                <div class="page-number">1</div>
                <div class="page-number active">2</div>
                <div class="page-number">3</div>
                <div class="page-number">4</div>
                <div class="page-number">5</div>
                <div class="page-number">→</div>
            </div>
        </div>
        
        <div class="nav-section">
            <h2>Dropdown Menu</h2>
            <div class="dropdown">
                <button class="dropdown-btn">Account ▼</button>
                <div class="dropdown-menu">
                    <div class="dropdown-item">Profile</div>
                    <div class="dropdown-item">Settings</div>
                    <div class="dropdown-item">Billing</div>
                    <div class="dropdown-item">Logout</div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _components_card_layouts(self, colors: dict) -> str:
        """Card Layout Collection"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Card Layouts</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; padding: 80px 40px; }}
        .container {{ max-width: 1600px; margin: 0 auto; }}
        
        h1 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        
        .card-section {{ margin-bottom: 80px; }}
        .card-section h2 {{ font-size: 32px; font-weight: 900; margin-bottom: 32px; }}
        
        /* Basic Cards */
        .basic-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }}
        .basic-card {{ background: white; padding: 40px; border-radius: 20px; 
                      box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .basic-card h3 {{ font-size: 24px; font-weight: 900; margin-bottom: 12px; }}
        .basic-card p {{ color: #666; line-height: 1.7; }}
        
        /* Image Cards */
        .image-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }}
        .image-card {{ background: white; border-radius: 16px; overflow: hidden; 
                      box-shadow: 0 4px 20px rgba(0,0,0,0.08); cursor: pointer; transition: transform 0.3s; }}
        .image-card:hover {{ transform: translateY(-5px); }}
        .card-image {{ width: 100%; aspect-ratio: 1; 
                      background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .card-content {{ padding: 24px; }}
        .card-title {{ font-size: 18px; font-weight: 900; margin-bottom: 8px; }}
        .card-desc {{ font-size: 14px; color: #666; }}
        
        /* Feature Cards */
        .feature-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }}
        .feature-card {{ background: white; padding: 50px 40px; border-radius: 24px; text-align: center; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .feature-icon {{ width: 80px; height: 80px; margin: 0 auto 24px; border-radius: 50%; 
                        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .feature-title {{ font-size: 22px; font-weight: 900; margin-bottom: 12px; }}
        .feature-desc {{ font-size: 15px; color: #666; line-height: 1.7; }}
        
        /* Stat Cards */
        .stat-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }}
        .stat-card {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                     color: white; padding: 36px; border-radius: 20px; }}
        .stat-value {{ font-size: 42px; font-weight: 900; margin-bottom: 8px; }}
        .stat-label {{ font-size: 16px; opacity: 0.95; }}
        
        /* Profile Cards */
        .profile-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }}
        .profile-card {{ background: white; padding: 32px; border-radius: 20px; text-align: center; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .profile-avatar {{ width: 100px; height: 100px; margin: 0 auto 20px; border-radius: 50%; 
                          background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .profile-name {{ font-size: 20px; font-weight: 900; margin-bottom: 6px; }}
        .profile-role {{ font-size: 14px; color: #666; margin-bottom: 16px; }}
        .profile-btn {{ padding: 10px 24px; background: {colors['primary']}; color: white; border: none; 
                       border-radius: 8px; font-weight: 700; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Card Components</h1>
        
        <div class="card-section">
            <h2>Basic Cards</h2>
            <div class="basic-grid">
                <div class="basic-card">
                    <h3>Simple Card</h3>
                    <p>A basic card layout with title and description. Perfect for displaying content in a clean, organized way.</p>
                </div>
                <div class="basic-card">
                    <h3>Content Card</h3>
                    <p>Another example of a simple card design with consistent padding and typography.</p>
                </div>
                <div class="basic-card">
                    <h3>Info Card</h3>
                    <p>Cards are versatile components that can be used for various purposes across your application.</p>
                </div>
            </div>
        </div>
        
        <div class="card-section">
            <h2>Image Cards</h2>
            <div class="image-grid">
                <div class="image-card">
                    <div class="card-image"></div>
                    <div class="card-content">
                        <div class="card-title">Product Name</div>
                        <div class="card-desc">$99.00</div>
                    </div>
                </div>
                <div class="image-card">
                    <div class="card-image"></div>
                    <div class="card-content">
                        <div class="card-title">Product Name</div>
                        <div class="card-desc">$129.00</div>
                    </div>
                </div>
                <div class="image-card">
                    <div class="card-image"></div>
                    <div class="card-content">
                        <div class="card-title">Product Name</div>
                        <div class="card-desc">$79.00</div>
                    </div>
                </div>
                <div class="image-card">
                    <div class="card-image"></div>
                    <div class="card-content">
                        <div class="card-title">Product Name</div>
                        <div class="card-desc">$149.00</div>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="card-section">
            <h2>Feature Cards</h2>
            <div class="feature-grid">
                <div class="feature-card">
                    <div class="feature-icon"></div>
                    <h3 class="feature-title">Fast Performance</h3>
                    <p class="feature-desc">Lightning-fast load times and smooth interactions</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon"></div>
                    <h3 class="feature-title">Secure Platform</h3>
                    <p class="feature-desc">Bank-level security to protect your data</p>
                </div>
                <div class="feature-card">
                    <div class="feature-icon"></div>
                    <h3 class="feature-title">24/7 Support</h3>
                    <p class="feature-desc">Always here to help when you need us</p>
                </div>
            </div>
        </div>
        
        <div class="card-section">
            <h2>Stat Cards</h2>
            <div class="stat-grid">
                <div class="stat-card">
                    <div class="stat-value">2.4K</div>
                    <div class="stat-label">Active Users</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">127</div>
                    <div class="stat-label">Projects</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">$47K</div>
                    <div class="stat-label">Revenue</div>
                </div>
                <div class="stat-card">
                    <div class="stat-value">98%</div>
                    <div class="stat-label">Satisfaction</div>
                </div>
            </div>
        </div>
        
        <div class="card-section">
            <h2>Profile Cards</h2>
            <div class="profile-grid">
                <div class="profile-card">
                    <div class="profile-avatar"></div>
                    <div class="profile-name">John Smith</div>
                    <div class="profile-role">Designer</div>
                    <button class="profile-btn">Follow</button>
                </div>
                <div class="profile-card">
                    <div class="profile-avatar"></div>
                    <div class="profile-name">Sarah Johnson</div>
                    <div class="profile-role">Developer</div>
                    <button class="profile-btn">Follow</button>
                </div>
                <div class="profile-card">
                    <div class="profile-avatar"></div>
                    <div class="profile-name">Mike Davis</div>
                    <div class="profile-role">Manager</div>
                    <button class="profile-btn">Follow</button>
                </div>
                <div class="profile-card">
                    <div class="profile-avatar"></div>
                    <div class="profile-name">Emma Wilson</div>
                    <div class="profile-role">Marketing</div>
                    <button class="profile-btn">Follow</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _components_modal_dialogs(self, colors: dict) -> str:
        """Modal Dialog Collection"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modal Dialogs</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; padding: 80px 40px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        
        h1 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        
        .modal-section {{ background: white; padding: 50px; border-radius: 24px; margin-bottom: 40px; 
                         box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .modal-section h2 {{ font-size: 28px; font-weight: 900; margin-bottom: 32px; }}
        
        /* Basic Modal */
        .modal {{ background: white; border-radius: 24px; max-width: 500px; padding: 40px; 
                 box-shadow: 0 10px 50px rgba(0,0,0,0.2); }}
        .modal-header {{ display: flex; justify-content: space-between; align-items: center; 
                        margin-bottom: 24px; }}
        .modal-title {{ font-size: 28px; font-weight: 900; }}
        .modal-close {{ width: 32px; height: 32px; border-radius: 50%; border: none; background: #f0f0f0; 
                       font-size: 20px; cursor: pointer; }}
        .modal-content {{ font-size: 16px; line-height: 1.7; color: #666; margin-bottom: 32px; }}
        .modal-actions {{ display: flex; gap: 12px; justify-content: flex-end; }}
        .modal-btn {{ padding: 14px 28px; border-radius: 10px; font-weight: 700; cursor: pointer; }}
        .modal-btn-primary {{ background: {colors['primary']}; color: white; border: none; }}
        .modal-btn-secondary {{ background: #f0f0f0; color: #333; border: none; }}
        
        /* Confirmation Modal */
        .confirm-modal {{ background: white; border-radius: 24px; max-width: 450px; padding: 50px; 
                         text-align: center; box-shadow: 0 10px 50px rgba(0,0,0,0.2); }}
        .confirm-icon {{ width: 80px; height: 80px; margin: 0 auto 24px; border-radius: 50%; 
                        background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .confirm-title {{ font-size: 32px; font-weight: 900; margin-bottom: 16px; }}
        .confirm-message {{ font-size: 16px; color: #666; line-height: 1.7; margin-bottom: 32px; }}
        
        /* Alert Modal */
        .alert-modal {{ background: white; border-radius: 20px; max-width: 400px; padding: 40px; 
                       border-left: 6px solid {colors['primary']}; box-shadow: 0 10px 50px rgba(0,0,0,0.2); }}
        .alert-title {{ font-size: 24px; font-weight: 900; margin-bottom: 12px; }}
        .alert-message {{ font-size: 15px; color: #666; line-height: 1.7; margin-bottom: 24px; }}
        .alert-btn {{ width: 100%; padding: 14px; background: {colors['primary']}; color: white; 
                     border: none; border-radius: 10px; font-weight: 700; cursor: pointer; }}
        
        /* Form Modal */
        .form-modal {{ background: white; border-radius: 24px; max-width: 550px; padding: 40px; 
                      box-shadow: 0 10px 50px rgba(0,0,0,0.2); }}
        .form-group {{ margin-bottom: 24px; }}
        .form-label {{ display: block; font-size: 14px; font-weight: 700; margin-bottom: 8px; }}
        .form-input {{ width: 100%; padding: 14px; border: 2px solid #e0e0e0; border-radius: 10px; 
                      font-size: 16px; }}
        .form-input:focus {{ outline: none; border-color: {colors['primary']}; }}
        
        .divider {{ height: 40px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Modal Dialogs</h1>
        
        <div class="modal-section">
            <h2>Basic Modal</h2>
            <div class="modal">
                <div class="modal-header">
                    <h3 class="modal-title">Modal Title</h3>
                    <button class="modal-close">×</button>
                </div>
                <div class="modal-content">
                    <p>This is a basic modal dialog. It can be used to display information, collect user input, or confirm actions.</p>
                </div>
                <div class="modal-actions">
                    <button class="modal-btn modal-btn-secondary">Cancel</button>
                    <button class="modal-btn modal-btn-primary">Confirm</button>
                </div>
            </div>
        </div>
        
        <div class="modal-section">
            <h2>Confirmation Modal</h2>
            <div class="confirm-modal">
                <div class="confirm-icon"></div>
                <h3 class="confirm-title">Are you sure?</h3>
                <p class="confirm-message">This action cannot be undone. Do you want to proceed with deleting this item?</p>
                <div class="modal-actions" style="justify-content: center;">
                    <button class="modal-btn modal-btn-secondary">Cancel</button>
                    <button class="modal-btn modal-btn-primary">Delete</button>
                </div>
            </div>
        </div>
        
        <div class="modal-section">
            <h2>Alert Modal</h2>
            <div class="alert-modal">
                <h3 class="alert-title">Success!</h3>
                <p class="alert-message">Your changes have been saved successfully.</p>
                <button class="alert-btn">OK</button>
            </div>
        </div>
        
        <div class="modal-section">
            <h2>Form Modal</h2>
            <div class="form-modal">
                <div class="modal-header">
                    <h3 class="modal-title">Create Account</h3>
                    <button class="modal-close">×</button>
                </div>
                <div class="form-group">
                    <label class="form-label">Full Name</label>
                    <input type="text" class="form-input" placeholder="Enter your name">
                </div>
                <div class="form-group">
                    <label class="form-label">Email Address</label>
                    <input type="email" class="form-input" placeholder="your@email.com">
                </div>
                <div class="form-group">
                    <label class="form-label">Password</label>
                    <input type="password" class="form-input" placeholder="••••••••">
                </div>
                <div class="modal-actions">
                    <button class="modal-btn modal-btn-secondary">Cancel</button>
                    <button class="modal-btn modal-btn-primary">Create Account</button>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    def _components_pricing_tables(self, colors: dict) -> str:
        """Pricing Table Collection"""
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing Tables</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f5f7fa; padding: 80px 40px; }}
        .container {{ max-width: 1400px; margin: 0 auto; }}
        
        h1 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 20px; }}
        .subtitle {{ text-align: center; font-size: 20px; color: #666; margin-bottom: 80px; }}
        
        /* Pricing Grid */
        .pricing-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; margin-bottom: 80px; }}
        .pricing-card {{ background: white; padding: 50px 40px; border-radius: 24px; 
                        box-shadow: 0 4px 20px rgba(0,0,0,0.08); transition: transform 0.3s; }}
        .pricing-card:hover {{ transform: translateY(-8px); }}
        .pricing-card.featured {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                                 color: white; transform: scale(1.05); }}
        
        .plan-badge {{ display: inline-block; padding: 6px 16px; background: {colors['accent']}; 
                      color: white; border-radius: 20px; font-size: 12px; font-weight: 700; 
                      margin-bottom: 16px; }}
        .featured .plan-badge {{ background: rgba(255,255,255,0.3); }}
        
        .plan-name {{ font-size: 32px; font-weight: 900; margin-bottom: 16px; }}
        .plan-price {{ font-size: 56px; font-weight: 900; margin-bottom: 8px; }}
        .plan-price .currency {{ font-size: 28px; }}
        .plan-period {{ font-size: 16px; opacity: 0.8; margin-bottom: 32px; }}
        
        .features {{ list-style: none; margin-bottom: 40px; }}
        .features li {{ padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.1); }}
        .featured .features li {{ border-bottom: 1px solid rgba(255,255,255,0.2); }}
        .features li::before {{ content: "✓"; margin-right: 12px; font-weight: 900; }}
        
        .plan-btn {{ width: 100%; padding: 18px; border-radius: 12px; font-weight: 700; font-size: 16px; 
                    cursor: pointer; transition: all 0.3s; }}
        .plan-btn-default {{ background: {colors['primary']}; color: white; border: none; }}
        .plan-btn-featured {{ background: white; color: {colors['primary']}; border: none; }}
        
        /* Comparison Table */
        .comparison {{ background: white; border-radius: 24px; padding: 50px; 
                      box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .comparison h2 {{ font-size: 36px; font-weight: 900; margin-bottom: 40px; text-align: center; }}
        .comparison-table {{ width: 100%; border-collapse: collapse; }}
        .comparison-table th {{ text-align: left; padding: 20px; background: #f8f9fa; font-weight: 900; 
                               border-bottom: 2px solid #e0e0e0; }}
        .comparison-table td {{ padding: 20px; border-bottom: 1px solid #f0f0f0; }}
        .comparison-table .check {{ color: {colors['primary']}; font-size: 20px; font-weight: 900; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Choose Your Plan</h1>
        <p class="subtitle">Select the perfect plan for your needs</p>
        
        <div class="pricing-grid">
            <div class="pricing-card">
                <span class="plan-badge">STARTER</span>
                <h3 class="plan-name">Basic</h3>
                <div class="plan-price"><span class="currency">$</span>9</div>
                <p class="plan-period">per month</p>
                <ul class="features">
                    <li>Up to 10 projects</li>
                    <li>5GB storage</li>
                    <li>Email support</li>
                    <li>Basic analytics</li>
                </ul>
                <button class="plan-btn plan-btn-default">Get Started</button>
            </div>
            
            <div class="pricing-card featured">
                <span class="plan-badge">MOST POPULAR</span>
                <h3 class="plan-name">Professional</h3>
                <div class="plan-price"><span class="currency">$</span>29</div>
                <p class="plan-period">per month</p>
                <ul class="features">
                    <li>Unlimited projects</li>
                    <li>50GB storage</li>
                    <li>Priority support</li>
                    <li>Advanced analytics</li>
                    <li>Custom integrations</li>
                </ul>
                <button class="plan-btn plan-btn-featured">Get Started</button>
            </div>
            
            <div class="pricing-card">
                <span class="plan-badge">ENTERPRISE</span>
                <h3 class="plan-name">Business</h3>
                <div class="plan-price"><span class="currency">$</span>99</div>
                <p class="plan-period">per month</p>
                <ul class="features">
                    <li>Unlimited everything</li>
                    <li>500GB storage</li>
                    <li>24/7 phone support</li>
                    <li>Advanced analytics</li>
                    <li>Dedicated account manager</li>
                    <li>Custom contracts</li>
                </ul>
                <button class="plan-btn plan-btn-default">Get Started</button>
            </div>
        </div>
        
        <div class="comparison">
            <h2>Feature Comparison</h2>
            <table class="comparison-table">
                <thead>
                    <tr>
                        <th>Feature</th>
                        <th>Basic</th>
                        <th>Professional</th>
                        <th>Business</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>Projects</td>
                        <td>10</td>
                        <td>Unlimited</td>
                        <td>Unlimited</td>
                    </tr>
                    <tr>
                        <td>Storage</td>
                        <td>5GB</td>
                        <td>50GB</td>
                        <td>500GB</td>
                    </tr>
                    <tr>
                        <td>Team Members</td>
                        <td>1</td>
                        <td>5</td>
                        <td>Unlimited</td>
                    </tr>
                    <tr>
                        <td>API Access</td>
                        <td>-</td>
                        <td><span class="check">✓</span></td>
                        <td><span class="check">✓</span></td>
                    </tr>
                    <tr>
                        <td>Custom Branding</td>
                        <td>-</td>
                        <td>-</td>
                        <td><span class="check">✓</span></td>
                    </tr>
                    <tr>
                        <td>Dedicated Support</td>
                        <td>-</td>
                        <td>-</td>
                        <td><span class="check">✓</span></td>
                    </tr>
                </tbody>
            </table>
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
        """Database 저장 (중복 체크)"""
        print(f"💾 Saving: {data['title']}")
        
        # 중복 체크: 같은 title과 category 조합이 이미 존재하는지 확인
        existing = supabase.table('designs')\
            .select('id')\
            .eq('title', data['title'])\
            .eq('category', data['category'])\
            .execute()
        
        if existing.data:
            print(f"⚠️  Warning: Design with title '{data['title']}' and category '{data['category']}' already exists!")
            print(f"   Existing ID: {existing.data[0]['id']}")
            raise Exception(f"Duplicate design: {data['title']} ({data['category']})")
        
        response = supabase.table('designs').insert(data).execute()
        print("✅ Saved to database")
        return response.data[0]
    
    async def create_unique_design(self, category: str, max_attempts: int = 10) -> Dict[str, Any]:
        """고유한 디자인 생성"""
        
        print(f"\n{'='*70}")
        print(f"🎨 Creating {category} design")
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
        
        # 디자인 이름 가져오기
        design_name = self.get_design_name(self.current_method_name)
        
        # 스크린샷
        screenshot = await self.capture_screenshot(html_code)
        
        # 업로드
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{timestamp}_{category.replace(' ', '_').lower()}_{self.design_count}.png"
        image_url = self.upload_to_storage(screenshot, filename)
        
        # DB 저장
        design_data = {
            "title": design_name,
            "description": f"Professional {category.lower()} design with modern layout and features",
            "image_url": image_url,
            "category": category,
            "code": html_code,
            "prompt": f"Enhanced {category} | {design_name}",
        }
        
        result = self.save_to_database(design_data)
        
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
    parser.add_argument('--count', type=int, default=5, help='각 카테고리별 디자인 수')
    parser.add_argument('--category', type=str, help='특정 카테고리만 생성')
    args = parser.parse_args()
    
    generator = EnhancedDesignGenerator()
    
    # 카테고리 선택
    if args.category and args.category in CATEGORIES:
        categories = [args.category]
    else:
        categories = CATEGORIES
    
    print(f"\n🚀 Enhanced Design Generator Starting...")
    print(f"📊 Categories: {', '.join(categories)}")
    print(f"🎯 Target: {args.count} designs per category\n")
    
    # 각 카테고리별로 디자인 생성
    for category in categories:
        print(f"\n{'#'*70}")
        print(f"📁 CATEGORY: {category.upper()}")
        print(f"{'#'*70}\n")
        
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
