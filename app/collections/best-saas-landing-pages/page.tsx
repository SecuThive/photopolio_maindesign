import { Metadata } from 'next';
import Link from 'next/link';
import DesignCard from '@/components/DesignCard';
import { supabaseServer } from '@/lib/supabase/server';
import { withDesignSlugs } from '@/lib/slug';

export const metadata: Metadata = {
  title: "Best SaaS Landing Pages - Curated AI Design Collection",
  description: "Explore our handpicked collection of the best SaaS landing page designs. These AI-generated layouts showcase modern conversion patterns, compelling hero sections, and trust-building elements used by successful B2B companies.",
  alternates: {
    canonical: 'https://ui-syntax.com/collections/best-saas-landing-pages',
  },
  openGraph: {
    title: "Best SaaS Landing Pages - UI Syntax",
    description: "Curated collection of top SaaS landing page designs with proven conversion patterns.",
    url: 'https://ui-syntax.com/collections/best-saas-landing-pages',
  },
};

export const dynamic = 'force-dynamic';
export const revalidate = 0;

export default async function BestSaaSLandingPagesPage() {
  // Fetch landing page designs
  const { data: designs } = await supabaseServer
    .from('designs')
    .select('*')
    .eq('category', 'Landing Page')
    .eq('status', 'published')
    .order('created_at', { ascending: false })
    .limit(12);

  const designsWithSlugs = designs ? withDesignSlugs(designs) : [];

  return (
    <section className="space-y-16">
      {/* Hero Section */}
      <div className="space-y-6">
        <nav className="text-sm text-gray-500">
          <Link href="/" className="hover:text-gray-900">Home</Link>
          <span className="mx-2">/</span>
          <Link href="/collections" className="hover:text-gray-900">Collections</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900">Best SaaS Landing Pages</span>
        </nav>

        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900">
            Best SaaS Landing Pages
          </h1>

          <div className="prose prose-lg max-w-none text-gray-700">
            <p className="text-xl leading-relaxed mb-6">
              These AI-generated SaaS landing pages represent the gold standard for B2B software companies 
              looking to convert enterprise buyers. Each design has been curated based on proven conversion 
              principles used by unicorn startups and established platforms.
            </p>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              What Makes a Great SaaS Landing Page?
            </h2>
            
            <p>
              After analyzing hundreds of successful SaaS companies from Stripe to Notion, we&rsquo;ve identified 
              the key elements that make landing pages convert:
            </p>

            <ul className="space-y-3 my-6">
              <li>
                <strong>Clear Value Proposition:</strong> Within 3 seconds, visitors should understand what 
                you do and why it matters. The best SaaS landing pages use concise headlines paired with 
                benefit-driven subheadings.
              </li>
              <li>
                <strong>Social Proof Above the Fold:</strong> Enterprise buyers need validation. Logo bars 
                from recognizable customers, G2 ratings, or quantified results (&ldquo;Join 10,000+ teams&rdquo;) build 
                immediate credibility.
              </li>
              <li>
                <strong>Product Visualization:</strong> Screenshots, demo videos, or interactive product 
                tours help technical decision-makers understand your interface before booking a demo.
              </li>
              <li>
                <strong>Feature-Benefit Mapping:</strong> Don&rsquo;t just list features&mdash;connect each capability 
                to a business outcome. &ldquo;Real-time collaboration&rdquo; becomes &ldquo;Ship products 3x faster with your 
                distributed team.&rdquo;
              </li>
              <li>
                <strong>Strategic CTAs:</strong> Primary CTA should offer low friction (free trial, demo, 
                sandbox access). Secondary CTAs can drive to pricing, case studies, or documentation.
              </li>
            </ul>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              Design Patterns in This Collection
            </h2>

            <p>
              Our curated SaaS landing pages showcase modern design trends from Silicon Valley&rsquo;s top 
              product teams:
            </p>

            <ul className="space-y-3 my-6">
              <li>
                <strong>Minimalist Hero Sections:</strong> Clean layouts with generous whitespace that put 
                focus on messaging rather than decorative elements.
              </li>
              <li>
                <strong>Bento Grid Layouts:</strong> Popularized by Apple and Linear, these modular grids 
                elegantly display multiple features without overwhelming the viewer.
              </li>
              <li>
                <strong>Gradient Accents:</strong> Subtle gradients and glass morphism effects add depth 
                while maintaining professional aesthetics.
              </li>
              <li>
                <strong>Dark Mode Options:</strong> Developer-focused SaaS tools often include dark themes 
                that reduce eye strain and signal technical sophistication.
              </li>
            </ul>

            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">
              Who Should Use These Designs?
            </h2>

            <p>
              These landing page concepts are ideal for:
            </p>

            <ul className="space-y-2 my-4">
              <li>• <strong>B2B SaaS Founders</strong> launching new products or pivoting positioning</li>
              <li>• <strong>Product Marketers</strong> running A/B tests on messaging and layout</li>
              <li>• <strong>Design Teams</strong> exploring modern UI patterns for enterprise software</li>
              <li>• <strong>Agencies</strong> pitching concepts to SaaS clients</li>
            </ul>

            <p className="mt-8">
              Each design in this collection balances conversion optimization with brand expression. 
              Use them as inspiration for your next landing page redesign, or as reference points when 
              briefing designers and developers on what &ldquo;modern SaaS design&rdquo; looks like in 2026.
            </p>
          </div>
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
      <div className="pt-16 border-t border-gray-200">
        <h2 className="text-2xl font-semibold text-gray-900 mb-6">Explore More Collections</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <Link
            href="/collections/minimalist-dashboards"
            className="group p-6 border border-gray-200 rounded-lg hover:border-gray-400 transition-colors"
          >
            <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600">
              Minimalist Dashboards
            </h3>
            <p className="text-gray-600">
              Clean, data-focused dashboard designs that prioritize usability over decoration.
            </p>
          </Link>
          <Link
            href="/"
            className="group p-6 border border-gray-200 rounded-lg hover:border-gray-400 transition-colors"
          >
            <h3 className="text-xl font-semibold text-gray-900 mb-2 group-hover:text-blue-600">
              All Designs
            </h3>
            <p className="text-gray-600">
              Browse our complete gallery of AI-generated web designs across all categories.
            </p>
          </Link>
        </div>
      </div>
    </section>
  );
}
