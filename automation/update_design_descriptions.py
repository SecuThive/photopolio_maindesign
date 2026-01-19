"""
기존 데이터베이스의 디자인 설명을 고유한 설명으로 업데이트하는 스크립트

각 디자인의 코드를 분석하여 적절한 레이아웃 타입을 감지하고,
해당 레이아웃에 맞는 고유한 설명으로 업데이트합니다.
"""

import os
import re
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    raise ValueError("Missing required environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# 레이아웃 타입별 설명 (design_generator_final.py와 동일)
LAYOUT_DESCRIPTIONS = {
    # Landing Page descriptions
    "landing_hero_centered": "Bold hero-centered landing page with gradient backgrounds and powerful CTAs. Features centered typography, dual-action buttons, and feature grid showcasing key benefits. Perfect for SaaS products and digital services launching to market.",
    "landing_split_screen": "Modern split-screen layout dividing content and conversion form. Left side highlights social proof with user metrics and compelling copy. Right side contains streamlined signup form for maximum lead generation.",
    "landing_fullscreen_video": "Immersive fullscreen video-style landing with fixed navigation overlay. Emphasizes storytelling through minimal text and strong visual hierarchy. Includes scroll-to-explore interaction for modern digital experiences.",
    "landing_asymmetric": "Asymmetric grid layout with 2:1 content ratio and sticky sidebar. Main content features gradient text effects and large typography. Sidebar cards highlight different customer segments for targeted messaging.",
    "landing_minimal": "Ultra-minimal design focusing on typography and whitespace. Single centered message with large heading and simple grid showcasing numbered features. Ideal for design-forward brands emphasizing clarity and focus.",
    "landing_mobile_first": "Mobile app landing page with app store buttons and phone mockup. Features download CTAs, app icon, and feature list optimized for mobile conversion. Includes star ratings and social proof for app credibility.",
    
    # Dashboard descriptions
    "dashboard_sidebar": "Classic sidebar navigation dashboard with organized menu structure. Left sidebar contains categorized navigation links with icons. Main content area displays charts, tables, and real-time data widgets.",
    "dashboard_top_nav": "Modern top navigation dashboard with horizontal menu and workspace switcher. Features KPI cards in grid layout with charts and trend indicators. Optimized for data-driven decision making and analytics.",
    "dashboard_cards": "Card-based dashboard layout with modular information architecture. Each card represents distinct data category with visual hierarchy. Perfect for customizable admin panels and multi-tenant applications.",
    
    # E-commerce descriptions
    "ecommerce_product_grid": "Clean product grid layout with hover effects and quick-view functionality. Features responsive card design, pricing display, and add-to-cart actions. Perfect for fashion, electronics, and retail storefronts.",
    "ecommerce_product_detail": "Comprehensive product detail page with image gallery and purchase options. Includes product specifications, size selectors, and customer reviews section. Designed for high-conversion e-commerce experiences.",
    
    # Portfolio descriptions
    "portfolio_masonry": "Masonry grid portfolio with varying image heights creating dynamic visual rhythm. Hover effects reveal project titles and descriptions. Perfect for photographers, designers, and creative professionals.",
    "portfolio_minimal": "Minimal portfolio combining about section with curated project selection. Clean typography, generous spacing, and focus on personal branding. Great for individual creatives building their personal brand.",
    
    # Blog descriptions
    "blog_grid": "Magazine-style blog grid with editorial layout and visual hierarchy. Featured posts receive larger placement while recent articles fill grid. Perfect for news sites, lifestyle blogs, and digital publications.",
    "blog_magazine": "Modern card-based blog with consistent spacing and hover animations. Each post card includes thumbnail, title, excerpt, and metadata. Great for tech blogs, business publications, and multi-author platforms.",
    
    # Components descriptions
    "components_showcase": "Button component library showcasing various styles, sizes, and states. Includes primary, secondary, outline, and icon button variations. Essential UI kit for design systems and component libraries.",
    "components_library": "Comprehensive component library featuring cards, buttons, and UI elements. Demonstrates different component variations and use cases in organized sections. Critical for building consistent design systems.",
}


def detect_layout_type(code: str, category: str) -> str:
    """
    HTML 코드를 분석하여 레이아웃 타입을 감지합니다.
    """
    code_lower = code.lower()
    
    if category == "Landing Page":
        if "split" in code_lower or "grid-template-columns: 1fr 1fr" in code_lower:
            return "landing_split_screen"
        elif "fullscreen" in code_lower or "position: fixed" in code_lower and "nav" in code_lower:
            return "landing_fullscreen_video"
        elif "asymmetric" in code_lower or "grid-template-columns: 2fr 1fr" in code_lower:
            return "landing_asymmetric"
        elif "phone-mockup" in code_lower or "app store" in code_lower or "google play" in code_lower:
            return "landing_mobile_first"
        elif "simplicity" in code_lower or ".card" in code_lower and "aspect-ratio: 1" in code_lower:
            return "landing_minimal"
        else:
            return "landing_hero_centered"
    
    elif category == "Dashboard":
        if "sidebar" in code_lower and "grid-template-columns: 280px" in code_lower:
            return "dashboard_sidebar"
        elif ".card-grid" in code_lower or "display: grid" in code_lower and "card" in code_lower:
            return "dashboard_cards"
        else:
            return "dashboard_top_nav"
    
    elif category == "E-commerce":
        if "product-detail" in code_lower or ".product-gallery" in code_lower:
            return "ecommerce_product_detail"
        else:
            return "ecommerce_product_grid"
    
    elif category == "Portfolio":
        if "masonry" in code_lower or "columns:" in code_lower:
            return "portfolio_masonry"
        else:
            return "portfolio_minimal"
    
    elif category == "Blog":
        if "magazine" in code_lower or "featured-post" in code_lower:
            return "blog_magazine"
        else:
            return "blog_grid"
    
    elif category == "Components":
        if "component library" in code_lower or "section" in code_lower:
            return "components_library"
        else:
            return "components_showcase"
    
    # 기본값
    return "unknown"


def update_descriptions():
    """
    모든 디자인의 설명을 업데이트합니다.
    """
    print("📊 Fetching all designs from database...")
    
    # 모든 디자인 가져오기
    response = supabase.table('designs').select('*').execute()
    designs = response.data
    
    print(f"✅ Found {len(designs)} designs\n")
    
    updated_count = 0
    skipped_count = 0
    
    for design in designs:
        design_id = design['id']
        category = design['category']
        code = design.get('code', '')
        current_description = design.get('description', '')
        
        # 이미 고유한 설명이 있는지 확인 (중복 설명 감지)
        # "Unique", "Professional"로 시작하거나 너무 짧은 설명은 업데이트 대상
        needs_update = (
            not current_description or 
            current_description.startswith("Unique") or
            current_description.startswith("Professional") or
            len(current_description) < 100 or  # 3줄 설명은 최소 100자 이상
            "with multiple color themes" in current_description or
            "with modern layout and features" in current_description
        )
        
        if not needs_update:
            print(f"⏭️  Skipping design {design_id} - already has detailed description")
            skipped_count += 1
            continue
        
        # 코드가 없으면 스킵
        if not code:
            print(f"⚠️  Skipping design {design_id} - no code available")
            skipped_count += 1
            continue
        
        # 레이아웃 타입 감지
        layout_type = detect_layout_type(code, category)
        
        # 설명 가져오기
        new_description = LAYOUT_DESCRIPTIONS.get(
            layout_type,
            f"Modern {category.lower()} design with clean aesthetics and professional layout. Features responsive structure with attention to typography and visual hierarchy. Built with contemporary UI patterns for optimal user experience."
        )
        
        # 데이터베이스 업데이트
        try:
            supabase.table('designs').update({
                'description': new_description
            }).eq('id', design_id).execute()
            
            print(f"✅ Updated design {design_id} ({category}) - Layout: {layout_type}")
            print(f"   Description: {new_description[:80]}...")
            print()
            updated_count += 1
            
        except Exception as e:
            print(f"❌ Error updating design {design_id}: {e}")
            print()
    
    print("\n" + "="*70)
    print(f"🎉 Update complete!")
    print(f"   Updated: {updated_count} designs")
    print(f"   Skipped: {skipped_count} designs")
    print("="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🔄 Design Description Updater")
    print("="*70 + "\n")
    
    update_descriptions()
