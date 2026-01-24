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
import re
import asyncio
import hashlib
import random
import json
from datetime import datetime
from typing import Dict, Any, Set, List, Optional

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

BATCH_FILE_PATH = os.path.join(os.path.dirname(__file__), "latest_batch.json")


class UniversalDesignGenerator:
    """모든 카테고리를 지원하는 디자인 생성기"""
    
    def __init__(self):
        self.used_hashes: Set[str] = set()
        self.design_count = 0
        self.last_layout_type = None  # 마지막 생성 레이아웃 타입 추적
        self.external_designs = self._load_external_designs()
        self.total_existing_designs = 0
        self.existing_slugs: Set[str] = set()
        self._load_existing_structure_hashes()
    
    def _load_existing_structure_hashes(self) -> None:
        """Supabase에 저장된 기존 구조 해시를 불러와 중복 생성을 방지."""
        print("📦 Loading existing structure hashes from Supabase...")
        start = 0
        batch_size = 500
        try:
            while True:
                response = (
                    supabase
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
                    self.used_hashes.add(self.get_structure_hash(html))
                    slug_val = (row.get('slug') or '').strip()
                    if slug_val:
                        self.existing_slugs.add(slug_val)
                self.total_existing_designs += len(rows)
                if len(rows) < batch_size:
                    break
                start += batch_size
            print(f"✅ Loaded {len(self.used_hashes)} existing hash(es)")
        except Exception as exc:
            print(f"⚠️ Failed to load existing hashes: {exc}")
        finally:
            self.design_count = self.total_existing_designs

    def _load_external_designs(self) -> Dict[str, List[Dict[str, Any]]]:
        """advanced_generator.js가 만든 batch를 불러와 카테고리별 큐 형태로 보관."""
        queues: Dict[str, List[Dict[str, Any]]] = {cat: [] for cat in CATEGORIES}
        if not os.path.exists(BATCH_FILE_PATH):
            return queues
        try:
            with open(BATCH_FILE_PATH, 'r', encoding='utf-8') as batch_file:
                data = json.load(batch_file)
                if not isinstance(data, list):
                    return queues
                for item in data:
                    category = item.get('category')
                    if category in queues:
                        queues[category].append(item)
        except Exception as exc:
            print(f"⚠️ Failed to load external design batch: {exc}")
        return queues

    def _persist_external_designs(self) -> None:
        """현재 큐 상태를 latest_batch.json에 다시 저장."""
        flattened: List[Dict[str, Any]] = []
        for bucket in self.external_designs.values():
            flattened.extend(bucket)
        try:
            with open(BATCH_FILE_PATH, 'w', encoding='utf-8') as batch_file:
                json.dump(flattened, batch_file, ensure_ascii=False, indent=2)
        except Exception as exc:
            print(f"⚠️ Failed to persist external design batch: {exc}")

    def _apply_style_variant(self, html: str, style: Dict[str, Any]) -> str:
        """Tailwind 스타일 클래스를 <main> 컨테이너에 주입."""
        if not html or not style:
            return html
        classes = style.get('tailwindClasses') or style.get('classes')
        if not classes:
            return html
        class_blob = ' '.join(sorted(set(classes)))

        def _inject(match: re.Match) -> str:
            existing = match.group(1)
            return f'<main class="{existing} {class_blob}">'  # noqa: E501

        updated, count = re.subn(r'<main\s+class="([^"]+)"', _inject, html, count=1)
        return updated if count else html

    def _pop_external_design(self, category: str) -> Optional[Dict[str, Any]]:
        """카테고리 큐에서 하나 꺼내 스타일 적용 후 반환."""
        bucket = self.external_designs.get(category)
        if not bucket:
            return None
        entry = bucket.pop(0)
        styled_html = self._apply_style_variant(entry.get('html', ''), entry.get('style'))
        entry['html'] = styled_html
        self._persist_external_designs()
        return entry

    def _slugify(self, value: str) -> str:
        slug = re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')
        return slug or 'design'

    def _generate_slug(self, category: str) -> str:
        base_title = f"{category} Design {self.design_count + 1}"
        base_slug = self._slugify(base_title)
        candidate = base_slug
        suffix = 2
        while candidate in self.existing_slugs:
            candidate = f"{base_slug}-{suffix}"
            suffix += 1
        self.existing_slugs.add(candidate)
        return candidate

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
            "landing_bento_grid": [
                "Bento box grid layout with asymmetric tile sizing and modern aesthetics. Featured section spans multiple cells while stats occupy single tiles. Trendy design pattern popular in contemporary web applications.",
                "Japanese-inspired bento grid creating visual hierarchy through size variation. Hero tile dominates with supporting metrics in compact boxes. Clean, organized appearance with strong geometric structure.",
                "Modular bento layout breaking content into digestible grid components. Large featured block paired with smaller info tiles. Modern design language favored by tech companies and startups.",
                "Grid-based bento design using varied cell sizes for emphasis. Primary message takes prominent position while data points fill gaps. Balanced composition creates engaging visual experience.",
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
            "dashboard_analytics": [
                "Dark-themed analytics dashboard with data visualization focus. Chart area dominates viewport with gradient gridlines for depth. Time filter controls enable period comparison for trend analysis.",
                "Analytics-first dashboard design prioritizing data insights over decoration. Dark mode reduces eye strain during extended monitoring sessions. Interactive time selection drives metric recalculation.",
                "Data-focused admin panel with prominent chart visualization. Dark aesthetic creates professional atmosphere for analytics work. Flexible time windows support various reporting periods.",
            ],
            "dashboard_kanban": [
                "Kanban board dashboard with drag-and-drop task management. Column-based workflow visualization with card components for tasks. Perfect for project management and agile team coordination.",
                "Task board layout organizing work across status columns. Card-based tasks display priority, deadline, and assignment info. Ideal for tracking project progress visually.",
                "Agile board dashboard with swimlane task organization. Each column represents workflow stage with draggable cards. Supports sprint planning and backlog management.",
            ],
            "dashboard_table_view": [
                "Data table dashboard with sortable columns and row actions. Clean tabular layout optimized for bulk data management. Features search, filter, and export functionality for records.",
                "Table-driven admin interface for structured data viewing and editing. Sortable headers and inline actions streamline data operations. Built for CRM, inventory, and user management systems.",
                "Spreadsheet-style dashboard presenting data in tabular format. Column sorting and row selection enable efficient data handling. Export and bulk action support enhance productivity.",
            ],
            
            # E-commerce descriptions
            "ecommerce_product_grid": [
                "Clean product grid layout with hover effects and quick-view functionality. Features responsive card design, pricing display, and add-to-cart actions. Perfect for fashion, electronics, and retail storefronts.",
                "Product catalog grid optimized for browsing and discovery. Card hover reveals additional product details and purchase options. Consistent spacing and imagery create professional shopping experience.",
                "Grid-based product display with uniform card structure and interactions. Hover states provide visual feedback and action buttons. Pricing and product names maintain hierarchy for easy scanning.",
                "Responsive product grid adapting columns based on viewport size. Each card features image, title, price, and cart integration. Hover animations enhance interactivity without overwhelming users.",
            ],
            "ecommerce_product_detail": [
                "Product detail page with large image gallery and comprehensive information. Split layout divides imagery from product specs and purchase options. Reviews and ratings build trust before checkout.",
                "Detailed product view optimized for conversion and information discovery. Gallery showcases product from multiple angles and contexts. Specifications, reviews, and related items support purchase decision.",
                "Full product page combining visuals with detailed descriptions. Image gallery occupies primary position while details fill secondary space. Add to cart prominence reduces friction in buying process.",
            ],
            "ecommerce_cart_checkout": [
                "Shopping cart page with item list and order summary. Displays cart contents with quantity controls and removal options. Summary sidebar shows pricing breakdown and checkout CTA.",
                "Cart view optimizing review and modification before purchase. Line items show product details with edit capabilities. Summary panel maintains visibility of total and next steps.",
                "Checkout preparation page listing cart items with full details. Product images, quantities, and subtotals provide complete overview. Persistent summary encourages checkout completion.",
            ],
            "ecommerce_category_page": [
                "Category landing page with hero banner and product filtering. Featured collection highlighted at top with navigation filters below. Product grid displays category items with sort options.",
                "Collection page organizing products by category with visual hierarchy. Hero section establishes category theme and messaging. Filter chips enable refinement of displayed products.",
                "Category browse experience with promotional header and grid layout. Top banner showcases collection benefits and aesthetic. Product cards fill scrollable grid with pagination support.",
            ],
            "ecommerce_hero_sale": [
                "Flash sale landing with countdown timer and promotional messaging. Bold discount display creates urgency for limited-time offers. Countdown clock drives time-sensitive purchasing behavior.",
                "Sale campaign page featuring time-limited promotion and countdown. Large percentage-off messaging commands immediate attention. Timer creates scarcity psychology for conversion boost.",
                "Promotional sale page with expiration countdown and bold offers. Hero treatment of discount percentage builds excitement. Time pressure through countdown encourages faster decisions.",
            ],
            "ecommerce_wishlist": [
                "Wishlist page displaying saved products with quick actions. Heart icons indicate saved status with remove functionality. Enables easy transition from consideration to purchase.",
                "Saved items collection showing user's product interests. Card grid presents wishlisted products with pricing and availability. Quick add-to-cart conversion from saved favorites.",
                "Favorites page organizing products user wants to track. Product cards maintain consistency with main catalog styling. Wishlist enables purchase planning and gift list creation.",
            ],
            "ecommerce_search_results": [
                "Search results page with query display and product matches. Search bar remains visible for query refinement. Grid or list view presents matching products with relevance sorting.",
                "Product search interface showing results for user query. Prominent search input enables quick re-searching. Result count and filtering help narrow large result sets.",
                "E-commerce search page optimized for product discovery. Search term highlighted with matching product count displayed. Sort and filter options refine results efficiently.",
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
            "portfolio_case_study": [
                "In-depth case study layout documenting project from challenge to solution. Hero section introduces project with client and role details. Content sections break down process with supporting imagery.",
                "Project case study page with narrative structure and visual proof. Header establishes context while content reveals methodology. Image grids demonstrate execution and final results.",
                "Detailed portfolio case study walking through complete project lifecycle. Initial problem statement transitions into solution documentation. Mixed media presentation combines text with visuals effectively.",
            ],
            "portfolio_timeline": [
                "Career timeline portfolio showing professional journey chronologically. Vertical timeline with alternating content blocks. Perfect for showcasing career progression and major milestones.",
                "Work history displayed as interactive timeline with project details. Chronological presentation highlights growth and experience range. Visual timeline format makes scanning career path intuitive.",
                "Professional timeline layout documenting work experience over time. Timeline spine connects career milestones with project examples. Clear chronology demonstrates skill development arc.",
            ],
            "portfolio_fullwidth": [
                "Full-width portfolio with immersive project presentations. Edge-to-edge imagery maximizes visual impact per project. Scrolling reveals projects in sequence with breathing room.",
                "Fullscreen portfolio layout giving each project dedicated screen space. Maximum image size creates gallery-like experience. Vertical scrolling transitions between featured works smoothly.",
                "Expansive portfolio design utilizing full viewport for each piece. Large-scale presentation emphasizes quality over quantity. Generous spacing between projects creates premium feel.",
            ],
            "portfolio_split_showcase": [
                "Split-screen portfolio dividing space between project categories. Dual panels enable hovering to explore different work types. Modern interaction pattern creates engaging browsing experience.",
                "Half-and-half portfolio layout separating work into two streams. Each side represents different skill set or service offering. Hover interactions reveal project collections distinctly.",
                "Divided portfolio showcasing multiple disciplines simultaneously. Split layout allows comparison between different work styles. Interactive panels encourage exploration of both portfolios.",
            ],
            "portfolio_gallery_hover": [
                "Hover-reveal portfolio gallery with overlay interactions. Grid layout shows project thumbnails with details on hover. Dark theme creates dramatic showcase for creative work.",
                "Interactive portfolio grid revealing project info through hover states. Overlay animations provide smooth transition to details. Gallery format suitable for photography and visual work.",
                "Portfolio gallery with hover-activated project information. Grid maintains clean appearance until user interaction. Overlay design pattern popular in contemporary portfolios.",
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
            "blog_minimal_typography": [
                "Typography-focused blog with generous whitespace and readability emphasis. Serif fonts and ample line spacing create premium reading experience. Minimal distractions keep attention on content quality.",
                "Text-first blog design celebrating typographic hierarchy and spacing. Large headlines command attention while body text ensures comfort. Perfect for long-form content and thought leadership.",
                "Minimalist blog prioritizing reading experience over visual decoration. Careful font selection and spacing optimize content consumption. Subtle accents maintain interest without distraction.",
            ],
            "blog_featured_hero": [
                "Hero-driven blog highlighting featured article with full-screen treatment. Primary post receives maximum visibility and engagement opportunity. Gradient backgrounds create visual depth and emphasis.",
                "Featured post layout with dramatic hero presentation. Full-viewport article preview creates immediate impact. Background effects draw readers into featured content.",
                "Blog design emphasizing one key article through hero sizing. Featured post dominates screen with compelling imagery and headline. Supporting articles follow in standard grid format.",
            ],
            "blog_sidebar_list": [
                "Traditional blog layout with main content column and sidebar widgets. Article list occupies primary space while sidebar shows popular posts. Classic structure familiar to readers from established blogs.",
                "Two-column blog separating article feed from supplementary content. Main posts display with full previews and metadata. Sidebar maintains persistent navigation and recommendations.",
                "Sidebar blog layout balancing content with discovery features. Post list shows recent articles with excerpts and images. Fixed sidebar aids navigation and highlights key content.",
            ],
            "blog_masonry_cards": [
                "Masonry blog grid with varied card heights creating organic flow. Pinterest-style layout prevents monotonous post arrangement. Mixed content lengths fit naturally without forced sizing.",
                "Waterfall blog layout using masonry algorithm for dynamic arrangement. Varying card sizes accommodate different post preview lengths. Visually interesting alternative to uniform grids.",
                "Asymmetric blog grid breaking free from rigid structure. Masonry positioning creates natural, magazine-like appearance. Card heights adjust to content without awkward cropping.",
            ],
            "blog_timeline_feed": [
                "Timeline-style blog presenting posts in chronological feed format. Cards stack vertically with timestamps and category tags. Social media-inspired layout familiar to modern users.",
                "Chronological blog feed with card-based post presentation. Timeline structure emphasizes recency and publication order. Tags and metadata aid content filtering and discovery.",
                "Feed-based blog layout mimicking social platform aesthetics. Posts display in reverse chronological order with full previews. Modern design pattern resonating with younger audiences.",
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
            "components_forms": [
                "Form component library showcasing input fields, textareas, and validation states. Includes labels, placeholder text, and focus states. Essential for creating consistent form experiences across applications.",
                "Input component collection demonstrating various form field types. Shows proper labeling, spacing, and interaction patterns. Critical for standardizing data collection interfaces.",
                "Form elements showcase with different input variations and states. Displays text fields, select menus, and submission buttons. Foundational components for any application's forms.",
            ],
            "components_navigation": [
                "Navigation component library featuring headers, tabs, and breadcrumbs. Shows different navigation patterns and hierarchy levels. Essential for maintaining consistent site navigation structure.",
                "Nav component collection demonstrating various navigation types. Includes horizontal menus, tab interfaces, and breadcrumb trails. Critical for cohesive navigation experience.",
                "Navigation elements showcase with multiple pattern variations. Displays top bars, tabbed interfaces, and location breadcrumbs. Fundamental components for site structure.",
            ],
            "components_modals": [
                "Modal and dialog component library with various styles and purposes. Includes confirmation dialogs, info modals, and alert patterns. Essential for creating consistent overlay interactions.",
                "Overlay component collection showing different modal types. Demonstrates success states, warnings, and informational dialogs. Critical for standardized user feedback patterns.",
                "Dialog component showcase featuring various modal contexts. Displays confirmation prompts, notifications, and action dialogs. Core components for interrupting user flow intentionally.",
            ],
            "components_pricing": [
                "Pricing table component library with tier comparisons and CTAs. Shows different pricing plans with feature lists and highlight states. Essential for SaaS and subscription-based products.",
                "Pricing component collection demonstrating various tier structures. Includes feature comparisons, pricing periods, and purchase actions. Critical for converting visitors to customers.",
                "Price comparison components showcasing plan differentiation. Displays multiple tiers with features, prices, and signup buttons. Fundamental for subscription product marketing.",
            ],
            "components_testimonials": [
                "Testimonial component library featuring customer quotes and reviews. Includes avatar images, names, titles, and rating displays. Essential for building social proof and credibility.",
                "Review component collection showing various testimonial formats. Demonstrates customer feedback with attribution and context. Critical for establishing trust with potential users.",
                "Social proof components showcasing customer testimonials. Displays quotes, reviewer details, and company affiliations. Core components for conversion-focused pages.",
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
            ("landing_bento_grid", self._landing_bento_grid),
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

    def _landing_bento_grid(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Bento Grid Landing</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; padding: 60px; background: #fafafa; }}
        .bento-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; max-width: 1600px; margin: 0 auto; }}
        .bento-item {{ background: white; border-radius: 24px; padding: 40px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .bento-item.large {{ grid-column: span 2; grid-row: span 2; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); color: white; }}
        .bento-item h2 {{ font-size: 36px; font-weight: 900; margin-bottom: 16px; }}
        .bento-item p {{ font-size: 18px; line-height: 1.6; opacity: 0.9; }}
    </style>
</head>
<body>
    <div class="bento-grid">
        <div class="bento-item large">
            <h2>Transform Your Business</h2>
            <p>Next-generation platform for modern teams. Scale faster, work smarter.</p>
        </div>
        <div class="bento-item"><h2>500K+</h2><p>Active Users</p></div>
        <div class="bento-item"><h2>99.9%</h2><p>Uptime</p></div>
        <div class="bento-item"><h2>24/7</h2><p>Support</p></div>
        <div class="bento-item"><h2>$2B+</h2><p>Processed</p></div>
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
            ("dashboard_analytics", self._dashboard_analytics),
            ("dashboard_kanban", self._dashboard_kanban),
            ("dashboard_table_view", self._dashboard_table_view),
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

    def _dashboard_analytics(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Analytics Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #0f1117; color: white; padding: 40px; }}
        .header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 40px; }}
        .header h1 {{ font-size: 48px; font-weight: 900; }}
        .time-filter {{ display: flex; gap: 12px; }}
        .time-btn {{ padding: 12px 24px; background: #1a1d29; border: 1px solid #2a2e3a; border-radius: 8px; color: white; cursor: pointer; }}
        .time-btn.active {{ background: {colors['primary']}; border-color: {colors['primary']}; }}
        .chart-area {{ background: #1a1d29; padding: 40px; border-radius: 20px; min-height: 400px; margin-bottom: 30px;
                      background-image: linear-gradient(0deg, {colors['primary']}20 1px, transparent 1px); 
                      background-size: 100% 50px; }}
        .stats-row {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; }}
        .stat-box {{ background: #1a1d29; padding: 30px; border-radius: 16px; border: 1px solid #2a2e3a; }}
        .stat-box h3 {{ font-size: 14px; color: #9ca3af; margin-bottom: 12px; }}
        .stat-box .number {{ font-size: 36px; font-weight: 900; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Analytics</h1>
        <div class="time-filter">
            <button class="time-btn">Day</button>
            <button class="time-btn active">Week</button>
            <button class="time-btn">Month</button>
            <button class="time-btn">Year</button>
        </div>
    </div>
    <div class="chart-area"></div>
    <div class="stats-row">
        <div class="stat-box">
            <h3>Unique Visitors</h3>
            <div class="number">24.5K</div>
        </div>
        <div class="stat-box">
            <h3>Page Views</h3>
            <div class="number">89.2K</div>
        </div>
        <div class="stat-box">
            <h3>Avg. Session</h3>
            <div class="number">3m 42s</div>
        </div>
        <div class="stat-box">
            <h3>Bounce Rate</h3>
            <div class="number">32.8%</div>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_kanban(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kanban Board</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; background: #f9fafb; padding: 40px; }}
        .board {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 24px; }}
        .column {{ background: #e5e7eb; padding: 20px; border-radius: 12px; }}
        .column-header {{ font-size: 16px; font-weight: 700; margin-bottom: 16px; display: flex; 
                         justify-content: space-between; align-items: center; }}
        .count {{ background: white; padding: 4px 12px; border-radius: 8px; font-size: 14px; }}
        .task-card {{ background: white; padding: 20px; border-radius: 10px; margin-bottom: 12px;
                     box-shadow: 0 1px 3px rgba(0,0,0,0.1); cursor: pointer; }}
        .task-card h4 {{ font-size: 15px; font-weight: 600; margin-bottom: 8px; }}
        .task-meta {{ display: flex; gap: 12px; font-size: 13px; color: #6b7280; }}
        .priority {{ padding: 4px 8px; background: {colors['primary']}20; color: {colors['primary']};
                    border-radius: 4px; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="board">
        <div class="column">
            <div class="column-header">To Do <span class="count">5</span></div>
            <div class="task-card">
                <h4>Design new homepage</h4>
                <div class="task-meta"><span class="priority">High</span> <span>Due: Today</span></div>
            </div>
            <div class="task-card">
                <h4>Update documentation</h4>
                <div class="task-meta"><span class="priority">Medium</span> <span>Due: Tomorrow</span></div>
            </div>
        </div>
        <div class="column">
            <div class="column-header">In Progress <span class="count">3</span></div>
            <div class="task-card">
                <h4>Implement authentication</h4>
                <div class="task-meta"><span class="priority">High</span> <span>Due: Wed</span></div>
            </div>
        </div>
        <div class="column">
            <div class="column-header">Review <span class="count">2</span></div>
            <div class="task-card">
                <h4>Code review for PR #123</h4>
                <div class="task-meta"><span class="priority">Medium</span></div>
            </div>
        </div>
        <div class="column">
            <div class="column-header">Done <span class="count">8</span></div>
            <div class="task-card">
                <h4>Setup CI/CD pipeline</h4>
                <div class="task-meta"><span>Completed</span></div>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _dashboard_table_view(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Data Table Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: white; padding: 40px; }}
        .header {{ display: flex; justify-content: space-between; margin-bottom: 30px; }}
        .header h1 {{ font-size: 36px; font-weight: 900; }}
        .actions {{ display: flex; gap: 12px; }}
        .btn {{ padding: 12px 24px; background: {colors['primary']}; color: white; border: none;
               border-radius: 8px; font-weight: 600; cursor: pointer; }}
        .btn-outline {{ background: white; color: {colors['primary']}; border: 2px solid {colors['primary']}; }}
        table {{ width: 100%; border-collapse: collapse; }}
        thead {{ background: #f9fafb; }}
        th {{ padding: 16px; text-align: left; font-weight: 700; color: #374151; font-size: 14px; }}
        td {{ padding: 16px; border-bottom: 1px solid #e5e7eb; }}
        .status {{ padding: 4px 12px; border-radius: 12px; font-size: 13px; font-weight: 600; }}
        .status.active {{ background: #d1fae5; color: #065f46; }}
        .status.pending {{ background: #fef3c7; color: #92400e; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>User Management</h1>
        <div class="actions">
            <button class="btn btn-outline">Export</button>
            <button class="btn">Add User</button>
        </div>
    </div>
    <table>
        <thead>
            <tr>
                <th>Name</th>
                <th>Email</th>
                <th>Role</th>
                <th>Status</th>
                <th>Joined</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>John Doe</td>
                <td>john@example.com</td>
                <td>Admin</td>
                <td><span class="status active">Active</span></td>
                <td>Jan 15, 2024</td>
            </tr>
            <tr>
                <td>Jane Smith</td>
                <td>jane@example.com</td>
                <td>Editor</td>
                <td><span class="status active">Active</span></td>
                <td>Jan 12, 2024</td>
            </tr>
            <tr>
                <td>Bob Johnson</td>
                <td>bob@example.com</td>
                <td>Viewer</td>
                <td><span class="status pending">Pending</span></td>
                <td>Jan 18, 2024</td>
            </tr>
        </tbody>
    </table>
</body>
</html>"""
    
    # ===== E-commerce =====
    def generate_ecommerce(self, colors: dict) -> str:
        layouts = [
            ("ecommerce_product_grid", self._ecommerce_product_grid),
            ("ecommerce_product_detail", self._ecommerce_product_detail),
            ("ecommerce_cart_checkout", self._ecommerce_cart_checkout),
            ("ecommerce_category_page", self._ecommerce_category_page),
            ("ecommerce_hero_sale", self._ecommerce_hero_sale),
            ("ecommerce_wishlist", self._ecommerce_wishlist),
            ("ecommerce_search_results", self._ecommerce_search_results),
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

    def _ecommerce_cart_checkout(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shopping Cart</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; background: #f9fafb; padding: 60px 40px; }}
        .cart-container {{ max-width: 1200px; margin: 0 auto; display: grid; grid-template-columns: 2fr 1fr; gap: 40px; }}
        .cart-items {{ background: white; padding: 40px; border-radius: 16px; }}
        .cart-item {{ display: flex; gap: 24px; padding: 24px 0; border-bottom: 1px solid #e5e7eb; }}
        .item-image {{ width: 120px; height: 120px; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); border-radius: 12px; }}
        .item-info {{ flex: 1; }}
        .item-price {{ font-size: 24px; font-weight: 900; color: {colors['primary']}; }}
        .summary {{ background: white; padding: 40px; border-radius: 16px; height: fit-content; }}
        .summary h2 {{ font-size: 28px; margin-bottom: 24px; }}
        .summary-row {{ display: flex; justify-content: space-between; padding: 12px 0; }}
        .checkout-btn {{ width: 100%; padding: 18px; background: {colors['primary']}; color: white; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; margin-top: 20px; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="cart-container">
        <div class="cart-items">
            <h1 style="font-size: 36px; margin-bottom: 32px;">Shopping Cart (3)</h1>
            <div class="cart-item">
                <div class="item-image"></div>
                <div class="item-info">
                    <h3 style="font-size: 20px;">Premium Product</h3>
                    <p style="color: #666; margin: 8px 0;">Color: Blue, Size: M</p>
                    <div class="item-price">$99.00</div>
                </div>
            </div>
            <div class="cart-item">
                <div class="item-image"></div>
                <div class="item-info">
                    <h3 style="font-size: 20px;">Deluxe Item</h3>
                    <p style="color: #666; margin: 8px 0;">Color: Black, Size: L</p>
                    <div class="item-price">$149.00</div>
                </div>
            </div>
        </div>
        <div class="summary">
            <h2>Order Summary</h2>
            <div class="summary-row"><span>Subtotal</span><span>$248.00</span></div>
            <div class="summary-row"><span>Shipping</span><span>$10.00</span></div>
            <div class="summary-row" style="font-size: 24px; font-weight: 900; border-top: 2px solid #e5e7eb; margin-top: 16px; padding-top: 20px;"><span>Total</span><span>${{258.00}}</span></div>
            <button class="checkout-btn">Proceed to Checkout</button>
        </div>
    </div>
</body>
</html>"""

    def _ecommerce_category_page(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Shop by Category</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; }}
        .hero {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); padding: 120px 60px; text-align: center; color: white; }}
        .hero h1 {{ font-size: 64px; font-weight: 900; margin-bottom: 16px; }}
        .filters {{ padding: 40px 60px; background: #f9fafb; display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; }}
        .filter-btn {{ padding: 12px 32px; background: white; border: 2px solid #e5e7eb; border-radius: 24px; cursor: pointer; font-weight: 600; }}
        .filter-btn.active {{ background: {colors['primary']}; color: white; border-color: {colors['primary']}; }}
        .products {{ padding: 60px; display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }}
        .product {{ background: white; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
        .product-img {{ width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}40, {colors['secondary']}40); }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Women's Collection</h1>
        <p style="font-size: 20px;">Discover the latest trends</p>
    </div>
    <div class="filters">
        <button class="filter-btn active">All</button>
        <button class="filter-btn">New Arrivals</button>
        <button class="filter-btn">Best Sellers</button>
        <button class="filter-btn">Sale</button>
    </div>
    <div class="products">
        <div class="product">
            <div class="product-img"></div>
            <div style="padding: 24px;">
                <h3 style="font-size: 18px; margin-bottom: 8px;">Stylish Item</h3>
                <p style="font-size: 20px; font-weight: 900; color: {colors['primary']};">$89.00</p>
            </div>
        </div>
        <div class="product">
            <div class="product-img"></div>
            <div style="padding: 24px;">
                <h3 style="font-size: 18px; margin-bottom: 8px;">Trendy Product</h3>
                <p style="font-size: 20px; font-weight: 900; color: {colors['primary']};">$119.00</p>
            </div>
        </div>
        <div class="product">
            <div class="product-img"></div>
            <div style="padding: 24px;">
                <h3 style="font-size: 18px; margin-bottom: 8px;">Classic Design</h3>
                <p style="font-size: 20px; font-weight: 900; color: {colors['primary']};">$99.00</p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _ecommerce_hero_sale(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Flash Sale</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; }}
        .sale-hero {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); min-height: 600px; 
                     display: flex; align-items: center; justify-content: center; color: white; text-align: center; padding: 60px; }}
        .sale-hero h1 {{ font-size: 96px; font-weight: 900; margin-bottom: 24px; }}
        .countdown {{ display: flex; gap: 32px; justify-content: center; margin: 40px 0; }}
        .time-box {{ background: rgba(255,255,255,0.2); backdrop-filter: blur(10px); padding: 24px 32px; border-radius: 16px; }}
        .time-number {{ font-size: 56px; font-weight: 900; }}
        .time-label {{ font-size: 14px; margin-top: 8px; opacity: 0.9; }}
        .cta {{ padding: 24px 64px; background: white; color: {colors['primary']}; border: none; border-radius: 16px; font-size: 24px; font-weight: 900; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="sale-hero">
        <div>
            <h1>50% OFF</h1>
            <p style="font-size: 28px; margin-bottom: 40px;">Flash Sale - Limited Time Only!</p>
            <div class="countdown">
                <div class="time-box"><div class="time-number">12</div><div class="time-label">HOURS</div></div>
                <div class="time-box"><div class="time-number">34</div><div class="time-label">MINUTES</div></div>
                <div class="time-box"><div class="time-number">56</div><div class="time-label">SECONDS</div></div>
            </div>
            <button class="cta">Shop Now</button>
        </div>
    </div>
</body>
</html>"""

    def _ecommerce_wishlist(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Wishlist</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 80px 60px; }}
        .wishlist-header {{ text-align: center; margin-bottom: 60px; }}
        .wishlist-header h1 {{ font-size: 56px; font-weight: 900; color: {colors['primary']}; margin-bottom: 16px; }}
        .wishlist-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 32px; max-width: 1600px; margin: 0 auto; }}
        .wishlist-item {{ position: relative; border-radius: 16px; overflow: hidden; box-shadow: 0 4px 16px rgba(0,0,0,0.1); }}
        .wishlist-img {{ width: 100%; aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .heart {{ position: absolute; top: 16px; right: 16px; background: white; width: 48px; height: 48px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; }}
    </style>
</head>
<body>
    <div class="wishlist-header">
        <h1>My Wishlist</h1>
        <p style="font-size: 18px; color: #666;">8 items saved</p>
    </div>
    <div class="wishlist-grid">
        <div class="wishlist-item">
            <div class="wishlist-img"></div>
            <div class="heart">❤️</div>
            <div style="padding: 20px; background: white;">
                <h3>Favorite Item</h3>
                <p style="font-weight: 900; font-size: 20px; color: {colors['primary']}; margin-top: 8px;">$129.00</p>
            </div>
        </div>
        <div class="wishlist-item">
            <div class="wishlist-img"></div>
            <div class="heart">❤️</div>
            <div style="padding: 20px; background: white;">
                <h3>Saved Product</h3>
                <p style="font-weight: 900; font-size: 20px; color: {colors['primary']}; margin-top: 8px;">$99.00</p>
            </div>
        </div>
        <div class="wishlist-item">
            <div class="wishlist-img"></div>
            <div class="heart">❤️</div>
            <div style="padding: 20px; background: white;">
                <h3>Dream Item</h3>
                <p style="font-weight: 900; font-size: 20px; color: {colors['primary']}; margin-top: 8px;">$159.00</p>
            </div>
        </div>
        <div class="wishlist-item">
            <div class="wishlist-img"></div>
            <div class="heart">❤️</div>
            <div style="padding: 20px; background: white;">
                <h3>Must Have</h3>
                <p style="font-weight: 900; font-size: 20px; color: {colors['primary']}; margin-top: 8px;">$89.00</p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _ecommerce_search_results(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Search Results</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; padding: 40px 60px; }}
        .search-bar {{ max-width: 800px; margin: 0 auto 60px; }}
        .search-input {{ width: 100%; padding: 24px; border: 2px solid {colors['primary']}; border-radius: 16px; font-size: 20px; }}
        .results-header {{ margin-bottom: 40px; }}
        .results-header h2 {{ font-size: 32px; margin-bottom: 8px; }}
        .results-header p {{ color: #666; }}
        .results-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; }}
        .result-item {{ display: flex; gap: 24px; background: white; padding: 24px; border-radius: 16px; border: 1px solid #e5e7eb; }}
        .result-img {{ width: 120px; height: 120px; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); border-radius: 12px; flex-shrink: 0; }}
    </style>
</head>
<body>
    <div class="search-bar">
        <input class="search-input" placeholder="Search products..." value="premium">
    </div>
    <div class="results-header">
        <h2>Search Results</h2>
        <p>Found 24 products matching "premium"</p>
    </div>
    <div class="results-grid">
        <div class="result-item">
            <div class="result-img"></div>
            <div>
                <h3 style="font-size: 18px; margin-bottom: 8px;">Premium Product</h3>
                <p style="color: #666; margin-bottom: 12px;">High-quality item</p>
                <p style="font-weight: 900; font-size: 20px; color: {colors['primary']};">$139.00</p>
            </div>
        </div>
        <div class="result-item">
            <div class="result-img"></div>
            <div>
                <h3 style="font-size: 18px; margin-bottom: 8px;">Premium Select</h3>
                <p style="color: #666; margin-bottom: 12px;">Best choice</p>
                <p style="font-weight: 900; font-size: 20px; color: {colors['primary']};">$189.00</p>
            </div>
        </div>
        <div class="result-item">
            <div class="result-img"></div>
            <div>
                <h3 style="font-size: 18px; margin-bottom: 8px;">Premium Edition</h3>
                <p style="color: #666; margin-bottom: 12px;">Limited stock</p>
                <p style="font-weight: 900; font-size: 20px; color: {colors['primary']};">$249.00</p>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # ===== Portfolio =====
    def generate_portfolio(self, colors: dict) -> str:
        layouts = [
            ("portfolio_grid_masonry", self._portfolio_masonry),
            ("portfolio_minimal_about", self._portfolio_minimal),
            ("portfolio_case_study", self._portfolio_case_study),
            ("portfolio_timeline", self._portfolio_timeline),
            ("portfolio_fullwidth", self._portfolio_fullwidth),
            ("portfolio_split_showcase", self._portfolio_split_showcase),
            ("portfolio_gallery_hover", self._portfolio_gallery_hover),
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

    def _portfolio_case_study(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Case Study</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; }}
        .hero {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); padding: 120px 60px; color: white; text-align: center; }}
        .hero h1 {{ font-size: 72px; font-weight: 900; margin-bottom: 24px; }}
        .hero .meta {{ font-size: 18px; opacity: 0.9; }}
        .content {{ max-width: 1200px; margin: 80px auto; padding: 0 60px; }}
        .content h2 {{ font-size: 48px; font-weight: 900; margin-bottom: 24px; }}
        .content p {{ font-size: 20px; line-height: 1.8; color: #666; margin-bottom: 40px; }}
        .image-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 32px; margin: 60px 0; }}
        .case-image {{ aspect-ratio: 16/9; background: {colors['primary']}20; border-radius: 16px; }}
    </style>
</head>
<body>
    <div class="hero">
        <h1>Brand Redesign Project</h1>
        <div class="meta">Client: Tech Startup • Year: 2024 • Role: Lead Designer</div>
    </div>
    <div class="content">
        <h2>Challenge</h2>
        <p>The client needed a complete brand overhaul to appeal to enterprise customers while maintaining their startup roots.</p>
        <div class="image-grid">
            <div class="case-image"></div>
            <div class="case-image"></div>
        </div>
        <h2>Solution</h2>
        <p>We developed a sophisticated visual identity that bridges professionalism with innovation.</p>
    </div>
</body>
</html>"""

    def _portfolio_timeline(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Work Timeline</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; padding: 80px 40px; background: #f9fafb; }}
        .timeline {{ max-width: 1000px; margin: 0 auto; position: relative; }}
        .timeline::before {{ content: ''; position: absolute; left: 50%; top: 0; bottom: 0; width: 4px; background: {colors['primary']}; }}
        .timeline-item {{ display: flex; margin-bottom: 80px; }}
        .timeline-item:nth-child(odd) {{ flex-direction: row; }}
        .timeline-item:nth-child(even) {{ flex-direction: row-reverse; }}
        .timeline-content {{ flex: 1; background: white; padding: 40px; border-radius: 16px; margin: 0 40px; box-shadow: 0 4px 16px rgba(0,0,0,0.1); }}
        .timeline-year {{ font-size: 48px; font-weight: 900; color: {colors['primary']}; margin-bottom: 16px; }}
        .timeline-content h3 {{ font-size: 28px; margin-bottom: 12px; }}
    </style>
</head>
<body>
    <div class="timeline">
        <div class="timeline-item">
            <div class="timeline-content">
                <div class="timeline-year">2024</div>
                <h3>Senior Designer at Tech Co</h3>
                <p style="color: #666;">Leading design for enterprise products</p>
            </div>
        </div>
        <div class="timeline-item">
            <div class="timeline-content">
                <div class="timeline-year">2022</div>
                <h3>Freelance Designer</h3>
                <p style="color: #666;">Working with startups worldwide</p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _portfolio_fullwidth(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Portfolio Fullwidth</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Poppins', sans-serif; }}
        .project-full {{ min-height: 100vh; padding: 100px 60px; }}
        .project-full:nth-child(odd) {{ background: {colors['primary']}; color: white; }}
        .project-full:nth-child(even) {{ background: white; }}
        .project-container {{ max-width: 1400px; margin: 0 auto; }}
        .project-container h1 {{ font-size: 96px; font-weight: 900; margin-bottom: 32px; }}
        .project-container p {{ font-size: 24px; opacity: 0.9; max-width: 600px; margin-bottom: 48px; }}
        .project-image {{ width: 100%; aspect-ratio: 16/9; background: rgba(0,0,0,0.1); border-radius: 24px; }}
    </style>
</head>
<body>
    <section class="project-full">
        <div class="project-container">
            <h1>Digital Experience</h1>
            <p>Immersive web application for modern enterprises. Designed for scale.</p>
            <div class="project-image"></div>
        </div>
    </section>
    <section class="project-full">
        <div class="project-container">
            <h1>Mobile Innovation</h1>
            <p>Award-winning app that transformed the industry standard.</p>
            <div class="project-image"></div>
        </div>
    </section>
</body>
</html>"""

    def _portfolio_split_showcase(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Split Portfolio</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; }}
        .split {{ display: grid; grid-template-columns: repeat(2, 1fr); height: 100vh; }}
        .split-item {{ position: relative; overflow: hidden; cursor: pointer; }}
        .split-bg {{ width: 100%; height: 100%; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); transition: transform 0.4s; }}
        .split-item:hover .split-bg {{ transform: scale(1.05); }}
        .split-content {{ position: absolute; bottom: 60px; left: 60px; color: white; }}
        .split-content h2 {{ font-size: 56px; font-weight: 900; margin-bottom: 16px; }}
        .split-content p {{ font-size: 20px; opacity: 0.95; }}
    </style>
</head>
<body>
    <div class="split">
        <div class="split-item">
            <div class="split-bg"></div>
            <div class="split-content">
                <h2>Web Design</h2>
                <p>12 Projects</p>
            </div>
        </div>
        <div class="split-item">
            <div class="split-bg" style="background: linear-gradient(135deg, {colors['secondary']}, {colors['accent']});"></div>
            <div class="split-content">
                <h2>Branding</h2>
                <p>8 Projects</p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _portfolio_gallery_hover(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hover Gallery</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; padding: 60px; background: #000; color: white; }}
        .gallery {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; }}
        .gallery-item {{ aspect-ratio: 1; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                        border-radius: 20px; position: relative; overflow: hidden; cursor: pointer; }}
        .overlay {{ position: absolute; inset: 0; background: rgba(0,0,0,0.8); display: flex; align-items: center; 
                    justify-content: center; opacity: 0; transition: opacity 0.3s; }}
        .gallery-item:hover .overlay {{ opacity: 1; }}
        .overlay-content {{ text-align: center; }}
        .overlay-content h3 {{ font-size: 32px; font-weight: 900; margin-bottom: 8px; }}
    </style>
</head>
<body>
    <h1 style="font-size: 72px; margin-bottom: 60px; text-align: center;">Selected Works</h1>
    <div class="gallery">
        <div class="gallery-item">
            <div class="overlay">
                <div class="overlay-content">
                    <h3>Project Alpha</h3>
                    <p>Web Design</p>
                </div>
            </div>
        </div>
        <div class="gallery-item">
            <div class="overlay">
                <div class="overlay-content">
                    <h3>Project Beta</h3>
                    <p>Branding</p>
                </div>
            </div>
        </div>
        <div class="gallery-item">
            <div class="overlay">
                <div class="overlay-content">
                    <h3>Project Gamma</h3>
                    <p>App Design</p>
                </div>
            </div>
        </div>
    </div>
</body>
</html>"""
    
    # ===== Blog =====
    def generate_blog(self, colors: dict) -> str:
        layouts = [
            ("blog_magazine_grid", self._blog_grid),
            ("blog_card_modern", self._blog_magazine),
            ("blog_minimal_typography", self._blog_minimal_typography),
            ("blog_featured_hero", self._blog_featured_hero),
            ("blog_sidebar_list", self._blog_sidebar_list),
            ("blog_masonry_cards", self._blog_masonry_cards),
            ("blog_timeline_feed", self._blog_timeline_feed),
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

    def _blog_minimal_typography(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Minimal Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Merriweather', serif; max-width: 800px; margin: 0 auto; padding: 120px 40px; }}
        article {{ margin-bottom: 120px; }}
        .date {{ font-size: 14px; color: {colors['primary']}; text-transform: uppercase; letter-spacing: 2px; margin-bottom: 16px; }}
        h1 {{ font-size: 64px; font-weight: 900; line-height: 1.1; margin-bottom: 32px; }}
        .excerpt {{ font-size: 24px; line-height: 1.6; color: #666; margin-bottom: 32px; }}
        .read-more {{ color: {colors['primary']}; font-weight: 700; font-size: 18px; text-decoration: none; }}
    </style>
</head>
<body>
    <article>
        <div class="date">January 15, 2024</div>
        <h1>The Art of Minimalism</h1>
        <div class="excerpt">Exploring how less really can be more in modern design and the principles that guide minimalist thinking.</div>
        <a href="#" class="read-more">Read Article →</a>
    </article>
    <article>
        <div class="date">January 12, 2024</div>
        <h1>Building Better Interfaces</h1>
        <div class="excerpt">A comprehensive guide to creating user experiences that truly resonate with your audience.</div>
        <a href="#" class="read-more">Read Article →</a>
    </article>
</body>
</html>"""

    def _blog_featured_hero(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Featured Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; }}
        .featured {{ min-height: 100vh; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); 
                    display: flex; align-items: center; justify-content: center; padding: 60px; color: white; }}
        .featured-content {{ max-width: 900px; text-align: center; }}
        .category {{ font-size: 16px; text-transform: uppercase; letter-spacing: 3px; margin-bottom: 24px; opacity: 0.9; }}
        .featured-content h1 {{ font-size: 88px; font-weight: 900; line-height: 1.1; margin-bottom: 32px; }}
        .featured-content p {{ font-size: 24px; line-height: 1.6; opacity: 0.95; margin-bottom: 48px; }}
        .read-btn {{ padding: 20px 60px; background: white; color: {colors['primary']}; border: none; border-radius: 12px; font-size: 20px; font-weight: 700; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="featured">
        <div class="featured-content">
            <div class="category">Design Trends</div>
            <h1>The Future is Now</h1>
            <p>Discover the emerging trends shaping the digital landscape and how you can stay ahead of the curve.</p>
            <button class="read-btn">Read Full Story</button>
        </div>
    </div>
</body>
</html>"""

    def _blog_sidebar_list(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Blog with Sidebar</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; padding: 60px; background: #f9fafb; }}
        .layout {{ display: grid; grid-template-columns: 2fr 1fr; gap: 60px; max-width: 1400px; margin: 0 auto; }}
        .article {{ background: white; padding: 40px; border-radius: 16px; margin-bottom: 32px; }}
        .article h2 {{ font-size: 36px; margin-bottom: 16px; }}
        .article .meta {{ font-size: 14px; color: #666; margin-bottom: 20px; }}
        .article p {{ font-size: 18px; color: #444; line-height: 1.7; }}
        .sidebar {{ position: sticky; top: 60px; }}
        .sidebar-widget {{ background: white; padding: 32px; border-radius: 16px; margin-bottom: 24px; }}
        .sidebar-widget h3 {{ font-size: 20px; margin-bottom: 20px; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="layout">
        <main>
            <article class="article">
                <h2>Recent Tech Developments</h2>
                <div class="meta">Posted on Jan 15 • 5 min read</div>
                <p>Stay updated with the latest technology news and breakthroughs that are changing the world.</p>
            </article>
            <article class="article">
                <h2>Design Thinking Workshop</h2>
                <div class="meta">Posted on Jan 12 • 8 min read</div>
                <p>Learn how to apply design thinking principles to solve complex business problems.</p>
            </article>
        </main>
        <aside class="sidebar">
            <div class="sidebar-widget">
                <h3>Popular Posts</h3>
                <div style="padding: 12px 0; border-bottom: 1px solid #e5e7eb;">Getting Started Guide</div>
                <div style="padding: 12px 0; border-bottom: 1px solid #e5e7eb;">Best Practices</div>
                <div style="padding: 12px 0;">Expert Tips</div>
            </div>
        </aside>
    </div>
</body>
</html>"""

    def _blog_masonry_cards(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Masonry Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 60px 40px; }}
        .masonry-grid {{ column-count: 3; column-gap: 32px; max-width: 1600px; margin: 0 auto; }}
        .blog-card {{ break-inside: avoid; background: white; border-radius: 16px; overflow: hidden; 
                     box-shadow: 0 4px 16px rgba(0,0,0,0.1); margin-bottom: 32px; }}
        .card-image {{ width: 100%; aspect-ratio: 16/9; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); }}
        .card-content {{ padding: 32px; }}
        .card-content h3 {{ font-size: 24px; margin-bottom: 12px; }}
        .card-content p {{ color: #666; line-height: 1.6; }}
    </style>
</head>
<body>
    <h1 style="font-size: 64px; text-align: center; margin-bottom: 80px;">Latest Articles</h1>
    <div class="masonry-grid">
        <div class="blog-card">
            <div class="card-image"></div>
            <div class="card-content">
                <h3>Design Systems 101</h3>
                <p>Building scalable design systems for modern applications.</p>
            </div>
        </div>
        <div class="blog-card">
            <div class="card-content">
                <h3>Quick Tips</h3>
                <p>Short and actionable advice for designers.</p>
            </div>
        </div>
        <div class="blog-card">
            <div class="card-image"></div>
            <div class="card-content">
                <h3>Case Study: Redesign</h3>
                <p>How we transformed a legacy system into a modern platform.</p>
            </div>
        </div>
    </div>
</body>
</html>"""

    def _blog_timeline_feed(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Timeline Blog</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Helvetica Neue', sans-serif; padding: 80px 40px; background: #fafafa; }}
        .timeline {{ max-width: 900px; margin: 0 auto; }}
        .post {{ background: white; padding: 48px; border-radius: 20px; margin-bottom: 40px; 
                box-shadow: 0 4px 20px rgba(0,0,0,0.08); border-left: 6px solid {colors['primary']}; }}
        .post-date {{ font-size: 14px; color: {colors['primary']}; font-weight: 700; margin-bottom: 16px; }}
        .post h2 {{ font-size: 40px; font-weight: 900; margin-bottom: 20px; }}
        .post p {{ font-size: 18px; color: #555; line-height: 1.7; margin-bottom: 24px; }}
        .tags {{ display: flex; gap: 12px; }}
        .tag {{ padding: 8px 16px; background: {colors['primary']}20; color: {colors['primary']}; 
               border-radius: 20px; font-size: 14px; font-weight: 600; }}
    </style>
</head>
<body>
    <div class="timeline">
        <article class="post">
            <div class="post-date">2 hours ago</div>
            <h2>Breaking News in Tech</h2>
            <p>Major announcement that will reshape the industry as we know it.</p>
            <div class="tags">
                <span class="tag">Technology</span>
                <span class="tag">Innovation</span>
            </div>
        </article>
        <article class="post">
            <div class="post-date">Yesterday</div>
            <h2>Design Workflow Tips</h2>
            <p>Streamline your creative process with these proven techniques.</p>
            <div class="tags">
                <span class="tag">Design</span>
                <span class="tag">Productivity</span>
            </div>
        </article>
    </div>
</body>
</html>"""
    
    # ===== Components =====
    def generate_components(self, colors: dict) -> str:
        layouts = [
            ("components_buttons", self._components_showcase),
            ("components_cards", self._components_library),
            ("components_forms", self._components_forms),
            ("components_navigation", self._components_navigation),
            ("components_modals", self._components_modals),
            ("components_pricing_tables", self._components_pricing),
            ("components_testimonials", self._components_testimonials),
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

    def _components_forms(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Form Components</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 80px 60px; background: #f9fafb; }}
        .form-container {{ max-width: 600px; margin: 0 auto; background: white; padding: 60px; border-radius: 24px; box-shadow: 0 10px 40px rgba(0,0,0,0.1); }}
        .form-container h2 {{ font-size: 36px; margin-bottom: 40px; color: {colors['primary']}; }}
        .form-group {{ margin-bottom: 24px; }}
        .form-group label {{ display: block; font-weight: 600; margin-bottom: 8px; color: #333; }}
        .form-group input, .form-group textarea {{ width: 100%; padding: 16px; border: 2px solid #e5e7eb; border-radius: 12px; font-size: 16px; }}
        .form-group input:focus, .form-group textarea:focus {{ outline: none; border-color: {colors['primary']}; }}
        .submit-btn {{ width: 100%; padding: 18px; background: {colors['primary']}; color: white; border: none; border-radius: 12px; font-size: 18px; font-weight: 700; cursor: pointer; }}
    </style>
</head>
<body>
    <div class="form-container">
        <h2>Contact Us</h2>
        <form>
            <div class="form-group">
                <label>Full Name</label>
                <input type="text" placeholder="John Doe">
            </div>
            <div class="form-group">
                <label>Email Address</label>
                <input type="email" placeholder="john@example.com">
            </div>
            <div class="form-group">
                <label>Message</label>
                <textarea rows="5" placeholder="Your message here..."></textarea>
            </div>
            <button class="submit-btn">Send Message</button>
        </form>
    </div>
</body>
</html>"""

    def _components_navigation(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Navigation Components</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; }}
        .nav {{ background: {colors['primary']}; padding: 20px 60px; display: flex; justify-content: space-between; align-items: center; }}
        .nav-brand {{ font-size: 28px; font-weight: 900; color: white; }}
        .nav-links {{ display: flex; gap: 40px; }}
        .nav-links a {{ color: white; text-decoration: none; font-weight: 600; font-size: 16px; }}
        .tabs {{ background: #f9fafb; padding: 40px 60px; }}
        .tab-list {{ display: flex; gap: 0; border-bottom: 2px solid #e5e7eb; }}
        .tab {{ padding: 16px 32px; background: none; border: none; font-size: 16px; font-weight: 600; color: #666; cursor: pointer; border-bottom: 3px solid transparent; }}
        .tab.active {{ color: {colors['primary']}; border-bottom-color: {colors['primary']}; }}
        .breadcrumb {{ padding: 40px 60px; display: flex; gap: 12px; font-size: 14px; }}
        .breadcrumb a {{ color: {colors['primary']}; text-decoration: none; }}
    </style>
</head>
<body>
    <nav class="nav">
        <div class="nav-brand">Brand</div>
        <div class="nav-links">
            <a href="#">Home</a>
            <a href="#">Products</a>
            <a href="#">About</a>
            <a href="#">Contact</a>
        </div>
    </nav>
    <div class="tabs">
        <div class="tab-list">
            <button class="tab active">Overview</button>
            <button class="tab">Features</button>
            <button class="tab">Pricing</button>
            <button class="tab">Support</button>
        </div>
    </div>
    <div class="breadcrumb">
        <a href="#">Home</a> / <a href="#">Products</a> / <span>Item</span>
    </div>
</body>
</html>"""

    def _components_modals(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Modal Components</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 60px; background: #f3f4f6; display: flex; align-items: center; justify-content: center; min-height: 100vh; }}
        .modal {{ background: white; padding: 48px; border-radius: 24px; box-shadow: 0 20px 60px rgba(0,0,0,0.2); max-width: 500px; }}
        .modal-header {{ text-align: center; margin-bottom: 32px; }}
        .modal-icon {{ width: 80px; height: 80px; background: {colors['primary']}20; border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; font-size: 40px; }}
        .modal-header h3 {{ font-size: 32px; font-weight: 900; margin-bottom: 12px; }}
        .modal-header p {{ color: #666; font-size: 16px; }}
        .modal-actions {{ display: flex; gap: 16px; margin-top: 32px; }}
        .btn {{ flex: 1; padding: 16px; border: none; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; }}
        .btn-primary {{ background: {colors['primary']}; color: white; }}
        .btn-secondary {{ background: #e5e7eb; color: #333; }}
    </style>
</head>
<body>
    <div class="modal">
        <div class="modal-header">
            <div class="modal-icon">✓</div>
            <h3>Success!</h3>
            <p>Your action has been completed successfully.</p>
        </div>
        <div class="modal-actions">
            <button class="btn btn-secondary">Cancel</button>
            <button class="btn btn-primary">Continue</button>
        </div>
    </div>
</body>
</html>"""

    def _components_pricing(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pricing Tables</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'SF Pro Display', sans-serif; padding: 80px 40px; background: #fafafa; }}
        .pricing-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 32px; max-width: 1400px; margin: 0 auto; }}
        .pricing-card {{ background: white; padding: 48px; border-radius: 24px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); text-align: center; }}
        .pricing-card.featured {{ background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); color: white; transform: scale(1.05); }}
        .plan-name {{ font-size: 24px; font-weight: 700; margin-bottom: 16px; }}
        .price {{ font-size: 64px; font-weight: 900; margin-bottom: 8px; }}
        .price-period {{ font-size: 16px; opacity: 0.8; margin-bottom: 32px; }}
        .features {{ list-style: none; margin-bottom: 40px; }}
        .features li {{ padding: 12px 0; border-bottom: 1px solid rgba(0,0,0,0.1); }}
        .cta-btn {{ width: 100%; padding: 16px; background: {colors['primary']}; color: white; border: none; border-radius: 12px; font-size: 16px; font-weight: 700; cursor: pointer; }}
        .featured .cta-btn {{ background: white; color: {colors['primary']}; }}
    </style>
</head>
<body>
    <div class="pricing-grid">
        <div class="pricing-card">
            <div class="plan-name">Starter</div>
            <div class="price">$29</div>
            <div class="price-period">per month</div>
            <ul class="features">
                <li>10 Projects</li>
                <li>5GB Storage</li>
                <li>Email Support</li>
            </ul>
            <button class="cta-btn">Get Started</button>
        </div>
        <div class="pricing-card featured">
            <div class="plan-name">Professional</div>
            <div class="price">$99</div>
            <div class="price-period">per month</div>
            <ul class="features">
                <li>Unlimited Projects</li>
                <li>100GB Storage</li>
                <li>Priority Support</li>
            </ul>
            <button class="cta-btn">Get Started</button>
        </div>
        <div class="pricing-card">
            <div class="plan-name">Enterprise</div>
            <div class="price">$299</div>
            <div class="price-period">per month</div>
            <ul class="features">
                <li>Everything</li>
                <li>Unlimited Storage</li>
                <li>24/7 Support</li>
            </ul>
            <button class="cta-btn">Contact Sales</button>
        </div>
    </div>
</body>
</html>"""

    def _components_testimonials(self, colors: dict) -> str:
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Testimonials</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Inter', sans-serif; padding: 100px 60px; background: linear-gradient(135deg, {colors['primary']}10, {colors['secondary']}10); }}
        .testimonials {{ max-width: 1400px; margin: 0 auto; }}
        .testimonials h2 {{ font-size: 56px; font-weight: 900; text-align: center; margin-bottom: 80px; }}
        .testimonial-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 40px; }}
        .testimonial {{ background: white; padding: 40px; border-radius: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.08); }}
        .testimonial-quote {{ font-size: 20px; line-height: 1.6; color: #333; margin-bottom: 24px; }}
        .testimonial-author {{ display: flex; align-items: center; gap: 16px; }}
        .author-avatar {{ width: 56px; height: 56px; background: linear-gradient(135deg, {colors['primary']}, {colors['secondary']}); border-radius: 50%; }}
        .author-info h4 {{ font-size: 16px; font-weight: 700; margin-bottom: 4px; }}
        .author-info p {{ font-size: 14px; color: #666; }}
    </style>
</head>
<body>
    <div class="testimonials">
        <h2>What People Say</h2>
        <div class="testimonial-grid">
            <div class="testimonial">
                <div class="testimonial-quote">"This product completely transformed how our team works. Highly recommended!"</div>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div class="author-info">
                        <h4>Sarah Johnson</h4>
                        <p>CEO, Tech Startup</p>
                    </div>
                </div>
            </div>
            <div class="testimonial">
                <div class="testimonial-quote">"Best investment we've made this year. The ROI speaks for itself."</div>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div class="author-info">
                        <h4>Michael Chen</h4>
                        <p>CTO, SaaS Company</p>
                    </div>
                </div>
            </div>
            <div class="testimonial">
                <div class="testimonial-quote">"Intuitive, powerful, and elegant. Everything we needed in one place."</div>
                <div class="testimonial-author">
                    <div class="author-avatar"></div>
                    <div class="author-info">
                        <h4>Emily Rodriguez</h4>
                        <p>Designer, Agency</p>
                    </div>
                </div>
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
        
        external_entry = self._pop_external_design(category)
        html_code = None
        external_description = None
        prompt_context = None

        if external_entry:
            html_code = external_entry.get('html', '')
            external_description = external_entry.get('description')
            prompt_context = external_entry
            print("🧩 Using pre-generated structure/style combo from advanced generator")
            if not html_code.strip():
                print("⚠️ External combo had empty HTML. Falling back to built-in generator.")
                html_code = None
                external_description = None
                prompt_context = None

        if html_code is None:
            # 고유한 구조 생성
            for attempt in range(max_attempts):
                print(f"🔄 Attempt {attempt + 1}/{max_attempts}")
                html_code = self.generate_design(category)
                
                if self.is_unique_structure(html_code):
                    print("✅ Unique structure generated")
                    break
            else:
                raise Exception("Failed to generate unique structure")
        else:
            # 외부 구조는 충돌 검사를 통과했다고 가정하고 해시만 등록
            self.used_hashes.add(self.get_structure_hash(html_code))
        
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
        
        # 레이아웃 타입에 따른 고유한 설명 생성 (외부 조합 우선)
        layout_hint = self.last_layout_type or "external_layout"
        unique_description = external_description or self.get_description_by_layout(category, layout_hint)
        
        # DB 저장
        slug_value = self._generate_slug(category)
        if prompt_context:
            style_label = prompt_context.get('style', {}).get('label')
            prompt_meta = f"External combo {prompt_context.get('id')} | Style: {style_label}"
        else:
            prompt_meta = f"Structure #{self.design_count} | Hash: {self.get_structure_hash(html_code)[:12]} | Layout: {self.last_layout_type}"

        design_data = {
            "title": f"{category} Design #{self.design_count + 1}",
            "description": unique_description,
            "image_url": image_url,
            "category": category,
            "code": html_code,
            "slug": slug_value,
            "prompt": prompt_meta,
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
    parser.add_argument('--total', type=int, help='Total number of designs to create across all categories')
    parser.add_argument('--category', type=str, help='Specific category')
    args = parser.parse_args()
    
    generator = UniversalDesignGenerator()
    
    # 카테고리 선택
    if args.category and args.category in CATEGORIES:
        categories = [args.category]
    else:
        categories = CATEGORIES

    async def wait_between_runs(current: int, target: int) -> None:
        if current < target:
            print("⏳ Waiting...\n")
            await asyncio.sleep(2)

    # 전체 생성 개수 우선
    if args.total and args.total > 0:
        total_target = args.total
        produced = 0
        while produced < total_target:
            category = categories[produced % len(categories)]
            try:
                await generator.create_unique_design(category)
                produced += 1
                await wait_between_runs(produced, total_target)
            except Exception as e:
                print(f"\n❌ Error: {e}\n")
                continue
    else:
        # 각 카테고리별로 디자인 생성
        for category in categories:
            for i in range(args.count):
                try:
                    await generator.create_unique_design(category)
                    await wait_between_runs(i + 1, args.count)
                except Exception as e:
                    print(f"\n❌ Error: {e}\n")
                    continue
    
    print(f"\n{'='*70}")
    print(f"🎉 Completed! Total: {generator.design_count} designs")
    print(f"{'='*70}\n")


if __name__ == "__main__":
    asyncio.run(main())
