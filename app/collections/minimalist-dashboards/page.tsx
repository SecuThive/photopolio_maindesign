import { Metadata } from 'next';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import DesignCard from '@/components/DesignCard';
import { supabaseServer } from '@/lib/supabase/server';
import { withDesignSlugs } from '@/lib/slug';

export const metadata: Metadata = {
  title: "Minimalist Dashboards - Clean UI Design Collection",
  description: "Discover minimalist dashboard designs that prioritize clarity and usability. These AI-generated admin panels and analytics interfaces showcase how leading SaaS products reduce cognitive load while maximizing data visibility.",
  alternates: {
    canonical: 'https://www.ui-syntax.com/collections/minimalist-dashboards',
  },
  openGraph: {
    title: "Minimalist Dashboards - UI Syntax",
    description: "Curated collection of clean, minimal dashboard designs for modern web applications.",
    url: 'https://www.ui-syntax.com/collections/minimalist-dashboards',
  },
};

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function MinimalistDashboardsPage() {
  // Fetch dashboard designs
  const { data: designs } = await supabaseServer
    .from('designs')
    .select('*')
    .eq('category', 'Dashboard')
    .order('created_at', { ascending: false })
    .limit(12);

  const designsWithSlugs = designs ? withDesignSlugs(designs) : [];

  return (
    <div className="min-h-screen bg-white">
      <Header selectedCategory={null} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {/* Hero Section */}
        <div className="mb-16">
          <nav className="text-sm text-gray-500 mb-4">
            <Link href="/" className="hover:text-gray-900">Home</Link>
            <span className="mx-2">/</span>
            <Link href="/collections" className="hover:text-gray-900">Collections</Link>
            <span className="mx-2">/</span>
            <span className="text-gray-900">Minimalist Dashboards</span>
          </nav>

          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Minimalist Dashboards
          </h1>
          
          <div className="prose prose-lg max-w-none text-gray-700">
            <p className="text-xl leading-relaxed mb-6">
              In the age of information overload, minimalist dashboards represent a design philosophy where 
              every pixel serves a purpose. This curated collection showcases AI-generated admin interfaces 
              that follow the principles used by industry leaders like Linear, Stripe, and Vercel.
            </p>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              The Philosophy Behind Minimalist Dashboards
            </h2>
            
            <p>
              Minimalism in dashboard design isn&rsquo;t about removing features&mdash;it&rsquo;s about ruthless prioritization. 
              When users log into a SaaS platform, they&rsquo;re there to accomplish specific tasks: analyze metrics, 
              manage resources, or configure settings. Great dashboards eliminate friction in these workflows.
            </p>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              Key Design Principles
            </h2>

            <ul className="space-y-3 my-6">
              <li>
                <strong>Progressive Disclosure:</strong> Show essential information by default, with drill-down 
                capabilities for power users. Don&rsquo;t dump 20 metrics on the screen when most users only track 3.
              </li>
              <li>
                <strong>Consistent Spacing Systems:</strong> Modern dashboards use 4px or 8px base spacing units. 
                This creates visual rhythm and makes interfaces feel more organized even with complex data.
              </li>
              <li>
                <strong>Hierarchy Through Typography:</strong> Instead of relying on colors and borders, 
                minimalist designs use font weight and size to establish information hierarchy. A well-chosen 
                type scale (like 12px, 14px, 16px, 20px, 24px) can do more than decorative elements.
              </li>
              <li>
                <strong>Purposeful White Space:</strong> Empty space isn&rsquo;t wasted space&mdash;it gives users room to 
                breathe and helps them focus on what matters. Cramming more widgets into a dashboard usually 
                decreases usability.
              </li>
              <li>
                <strong>Subtle Interactivity:</strong> Hover states, smooth transitions, and micro-interactions 
                should feel natural rather than flashy. The interface should respond immediately to user input 
                without drawing attention to itself.
              </li>
            </ul>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              Color & Contrast Strategy
            </h2>

            <p>
              The dashboards in this collection typically use:
            </p>

            <ul className="space-y-3 my-6">
              <li>
                <strong>Neutral Base Palette:</strong> Grays ranging from #F9FAFB (background) to #111827 
                (primary text) create a calm foundation that doesn&rsquo;t compete with data visualizations.
              </li>
              <li>
                <strong>Semantic Color System:</strong> Color is reserved for meaning&mdash;green for success, 
                red for errors, blue for links and primary actions. This reduces cognitive load because 
                users intuitively understand color coding.
              </li>
              <li>
                <strong>High Contrast Ratios:</strong> WCAG AA compliance (4.5:1 for body text) isn&rsquo;t just 
                about accessibility&mdash;it makes dashboards easier to read during long work sessions.
              </li>
            </ul>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              Layout Patterns You&rsquo;ll See
            </h2>

            <p>
              These designs demonstrate proven layout structures:
            </p>

            <ul className="space-y-2 my-4">
              <li>• <strong>Sidebar Navigation:</strong> Persistent left nav (240-280px wide) for primary 
              sections with collapsible states for focus mode</li>
              <li>• <strong>Metric Cards:</strong> Small, scannable cards displaying KPIs with comparison 
              indicators (↑7.2% vs last week)</li>
              <li>• <strong>Data Tables:</strong> Clean tables with row hover states, sortable columns, 
              and inline actions without clutter</li>
              <li>• <strong>Empty States:</strong> Thoughtfully designed blank slates that guide users 
              toward their first action rather than showing cryptic &ldquo;No data&rdquo; messages</li>
            </ul>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              Technical Implementation Notes
            </h2>

            <p>
              While these are design concepts, they&rsquo;re informed by modern frontend best practices:
            </p>

            <ul className="space-y-2 my-4">
              <li>• Designed with CSS Grid and Flexbox in mind for responsive layouts</li>
              <li>• Component-based architecture (easily translatable to React, Vue, or Svelte)</li>
              <li>• Performance-conscious—minimal use of shadows, gradients, and heavy effects</li>
              <li>• Dark mode ready with proper semantic color tokens</li>
            </ul>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              Who This Collection Is For
            </h2>

            <p>
              These minimalist dashboard designs are perfect for:
            </p>

            <ul className="space-y-2 my-4">
              <li>• <strong>Product Designers</strong> building internal tools or SaaS admin panels</li>
              <li>• <strong>Engineering Teams</strong> who need reference designs for developer-focused platforms</li>
              <li>• <strong>Founders</strong> validating that their MVP dashboard feels modern without over-designing</li>
              <li>• <strong>Design System Teams</strong> establishing patterns for data-heavy applications</li>
            </ul>

            <p className="mt-8">
              Unlike flashy marketing sites that can lean into experimental design, dashboards are tools 
              that users spend hours in daily. The minimalist approach ensures your interface becomes 
              invisible—in the best way possible—letting users focus on their actual work rather than 
              navigating ornate UI elements.
            </p>
          </div>
        </div>

        {/* Design Grid */}
        {designsWithSlugs.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {designsWithSlugs.map((design) => (
              <DesignCard 
                key={design.id} 
                design={design} 
                likes={0} 
                liked={false} 
                onToggleLike={() => {}} 
              />
            ))}
          </div>
        ) : (
          <div className="text-center py-16">
            <p className="text-gray-500 text-lg">No designs found in this collection yet.</p>
            <Link href="/" className="text-blue-600 hover:text-blue-800 mt-4 inline-block">
              Browse all designs
            </Link>
          </div>
        )}

        {/* Related Collections CTA */}
        <div className="mt-24 pt-16 border-t border-gray-200">
          <h2 className="text-2xl font-semibold text-gray-900 mb-6">Explore More Collections</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Link href="/collections/best-saas-landing-pages" 
                  className="group p-6 border border-gray-200 rounded-lg hover:border-gray-400 transition-colors">
              <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600">
                Best SaaS Landing Pages
              </h3>
              <p className="text-gray-600">
                High-converting landing page designs for B2B software companies and startups.
              </p>
            </Link>
            <Link href="/" 
                  className="group p-6 border border-gray-200 rounded-lg hover:border-gray-400 transition-colors">
              <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600">
                All Designs
              </h3>
              <p className="text-gray-600">
                Browse our complete gallery of AI-generated web designs across all categories.
              </p>
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
