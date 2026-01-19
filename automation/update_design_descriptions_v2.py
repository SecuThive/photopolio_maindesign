"""
기존 데이터베이스의 디자인 설명을 고유한 설명으로 업데이트하는 스크립트 v2

각 디자인의 코드를 분석하여 적절한 레이아웃 타입을 감지하고,
해당 레이아웃에 맞는 여러 설명 변형 중 랜덤하게 선택하여 고유성을 보장합니다.
"""

import os
import re
import random
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    raise ValueError("Missing required environment variables")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)


# 레이아웃 타입별 설명 변형 (각 타입별 3-5개 변형)
LAYOUT_DESCRIPTIONS = {
    # Landing Page descriptions
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
    
    # Dashboard descriptions
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
    "ecommerce_product_detail": [
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


def detect_layout_type(code: str, category: str) -> str:
    """HTML 코드를 분석하여 레이아웃 타입을 감지합니다."""
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
    
    return "unknown"


def update_descriptions():
    """모든 디자인의 설명을 업데이트합니다 (각 디자인마다 랜덤 변형 선택)."""
    print("📊 Fetching all designs from database...")
    
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
        
        # 이미 고유한 설명이 있는지 확인
        needs_update = (
            not current_description or 
            current_description.startswith("Unique") or
            current_description.startswith("Professional") or
            len(current_description) < 100 or
            "with multiple color themes" in current_description or
            "with modern layout and features" in current_description or
            current_description.startswith("Bold hero-centered") or  # 중복 방지 - 기존 설명도 재생성
            current_description.startswith("Modern split-screen") or
            current_description.startswith("Masonry grid") or
            current_description.startswith("Magazine-style") or
            current_description.startswith("Card-based dashboard")
        )
        
        if not needs_update:
            print(f"⏭️  Skipping design {design_id} - already has unique description")
            skipped_count += 1
            continue
        
        if not code:
            print(f"⚠️  Skipping design {design_id} - no code available")
            skipped_count += 1
            continue
        
        # 레이아웃 타입 감지
        layout_type = detect_layout_type(code, category)
        
        # 설명 변형 가져오기 (랜덤 선택)
        variations = LAYOUT_DESCRIPTIONS.get(layout_type, [
            f"Modern {category.lower()} design with clean aesthetics and professional layout. Features responsive structure with attention to typography and visual hierarchy. Built with contemporary UI patterns for optimal user experience."
        ])
        
        new_description = random.choice(variations)
        
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
    print("🔄 Design Description Updater v2 (Unique Variations)")
    print("="*70 + "\n")
    
    update_descriptions()
