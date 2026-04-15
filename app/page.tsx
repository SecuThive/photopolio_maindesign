import type { Metadata } from 'next';
import Link from 'next/link';
import { supabaseServer } from '@/lib/supabase/server';
import DesignGallery from '@/components/DesignGallery';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import EzoicPlacements from '@/components/EzoicPlacements';
import CategoryFilterBar from '@/components/CategoryFilterBar';
import GrowthSection from '@/components/GrowthSection';
import { getPlacementIds } from '@/lib/ezoic';
import { withDesignSlugs } from '@/lib/slug';
import { createPageMetadata, SITE_URL } from '@/lib/seo';
import { buildWebSiteSearchSchema, buildOrganizationSchema } from '@/lib/richSnippets';
import { getRecentChangelog } from '@/lib/changelog';
import { getPublishedDesignCount, getPublishedDesignLabel } from '@/lib/siteStats';

export const revalidate = 0;

export async function generateMetadata(): Promise<Metadata> {
  const totalDesigns = await getPublishedDesignCount();
  const title = totalDesigns > 0
    ? `${totalDesigns.toLocaleString('en-US')} Production-Ready AI Web Designs — Free HTML & React Code`
    : 'Free AI Web Designs with Copy-Paste Code';

  const description = totalDesigns > 0
    ? `Browse ${totalDesigns.toLocaleString('en-US')} AI-generated web designs with copy-paste HTML and React code. SaaS landing pages, dashboards, and e-commerce templates — all free.`
    : 'Download free, production-ready AI web designs with copy-paste HTML & React code. Save hours on every project with our curated gallery. 100% free commercial use.';

  return createPageMetadata({
    title,
    description,
    path: '/',
  });
}

export default async function HomePage({
  searchParams,
}: {
  searchParams: { category?: string };
}) {
  const publishedDesignCount = await getPublishedDesignCount();
  const publishedDesignLabel = getPublishedDesignLabel(publishedDesignCount);
  const category = searchParams?.category;
  const placementIds = getPlacementIds();
  const componentCategoryValues = ['Component', 'Components', 'component', 'components'];
  const recentChangelog = getRecentChangelog(3);

  let query = supabaseServer
    .from('designs')
    .select('*')
    .eq('status', 'published')
    .order('created_at', { ascending: false })
    .range(0, 11);

  if (category) {
    if (componentCategoryValues.includes(category)) {
      query = query.in('category', componentCategoryValues);
    } else {
      query = query.eq('category', category);
    }
  } else {
    query = query.not('category', 'in', '("Component","Components","component","components")');
  }

  const { data: initialDesigns } = await query;
  const designsWithSlugs = initialDesigns ? withDesignSlugs(initialDesigns) : [];

  const websiteSchema = buildWebSiteSearchSchema();
  const organizationSchema = buildOrganizationSchema({
    name: 'UI Syntax',
    url: SITE_URL,
    logo: `${SITE_URL}/icon.png`,
    description: `${publishedDesignLabel} with free copy-paste HTML and React code when available.`,
    email: 'thive8564@gmail.com',
    socialProfiles: [],
  });

  return (
    <div className="min-h-screen bg-white">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(websiteSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(organizationSchema) }}
      />

      <Header />

      <main>
        {/* Hero — compact, scannable, gallery-first */}
        <section className="border-b border-gray-100 bg-gradient-to-b from-gray-50 to-white">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12 md:py-16">
            <div className="max-w-3xl">
              {publishedDesignCount > 0 && (
                <p className="inline-flex items-center gap-2 rounded-full bg-gray-900 px-3 py-1 text-xs font-medium text-white mb-6">
                  <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-400 animate-pulse" />
                  {publishedDesignCount.toLocaleString('en-US')} designs and growing
                </p>
              )}
              <h1 className="text-3xl sm:text-4xl md:text-5xl font-bold text-gray-900 tracking-tight leading-[1.15]">
                Ship faster with
                <br className="hidden sm:inline" />
                <span className="text-gray-400"> production-ready</span> UI designs
              </h1>
              <p className="mt-4 text-lg text-gray-500 max-w-2xl leading-relaxed">
                Browse AI-generated landing pages, dashboards, and components.
                Copy the HTML or React code and start building in minutes.
              </p>
              <div className="mt-6 flex flex-wrap items-center gap-3">
                {["SaaS", "Dashboard", "E-commerce", "Portfolio", "Blog"].map((tag) => (
                  <span
                    key={tag}
                    className="rounded-full border border-gray-200 bg-white px-3 py-1 text-sm text-gray-600"
                  >
                    {tag}
                  </span>
                ))}
              </div>
            </div>
          </div>
        </section>

        {/* Category Filter + Gallery */}
        <CategoryFilterBar selectedCategory={category || null} className="mb-0" />

        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <DesignGallery initialDesigns={designsWithSlugs} initialCategory={category || null} />
        </div>

        {placementIds.length > 0 && (
          <EzoicPlacements placementIds={placementIds} wrapperClassName="my-16 space-y-12" />
        )}

        {/* Playbooks + Collections — below the gallery */}
        <section className="border-t border-gray-100 bg-gray-50/50">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16 md:py-20">
            <div className="grid gap-16 lg:grid-cols-2">
              {/* Playbooks */}
              <div>
                <div className="flex items-center justify-between mb-6">
                  <h2 className="text-xl font-semibold text-gray-900">Playbooks</h2>
                  <Link href="/playbooks" className="text-sm text-gray-500 hover:text-gray-900 transition-colors">
                    View all
                  </Link>
                </div>
                <div className="space-y-3">
                  {[
                    {
                      title: 'SaaS Landing Page UX',
                      href: '/playbooks/saas-landing-page-ux',
                      description: 'Value props, social proof, and CTA patterns for B2B SaaS.',
                    },
                    {
                      title: 'Dashboard UX Principles',
                      href: '/playbooks/dashboard-ux-principles',
                      description: 'Density, hierarchy, and dark mode for analytics products.',
                    },
                    {
                      title: 'E-Commerce Conversion',
                      href: '/playbooks/ecommerce-conversion-patterns',
                      description: 'PDP to checkout flows with trust and urgency patterns.',
                    },
                    {
                      title: 'UX Psychology',
                      href: '/playbooks/ux-psychology',
                      description: 'Behavioral triggers that guide attention and decisions.',
                    },
                  ].map((playbook) => (
                    <Link
                      key={playbook.href}
                      href={playbook.href}
                      className="group flex items-start gap-4 rounded-xl border border-gray-200 bg-white p-4 transition-all hover:border-gray-300 hover:shadow-sm"
                    >
                      <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gray-100 text-gray-500 group-hover:bg-gray-900 group-hover:text-white transition-colors">
                        <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                          <path d="M4 19.5v-15A2.5 2.5 0 0 1 6.5 2H20v20H6.5a2.5 2.5 0 0 1 0-5H20" />
                        </svg>
                      </div>
                      <div className="min-w-0">
                        <h3 className="text-sm font-medium text-gray-900 group-hover:text-gray-700">{playbook.title}</h3>
                        <p className="mt-0.5 text-sm text-gray-500 line-clamp-1">{playbook.description}</p>
                      </div>
                    </Link>
                  ))}
                </div>
              </div>

              {/* Collections + Changelog */}
              <div className="space-y-10">
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-semibold text-gray-900">Collections</h2>
                    <Link href="/collections" className="text-sm text-gray-500 hover:text-gray-900 transition-colors">
                      View all
                    </Link>
                  </div>
                  <div className="space-y-3">
                    {[
                      {
                        title: 'Best SaaS Landing Pages',
                        href: '/collections/best-saas-landing-pages',
                        description: 'Conversion-grade hero, pricing, and proof layouts.',
                      },
                      {
                        title: 'Minimalist Dashboards',
                        href: '/collections/minimalist-dashboards',
                        description: 'Signal-first dashboards balancing density and clarity.',
                      },
                    ].map((collection) => (
                      <Link
                        key={collection.href}
                        href={collection.href}
                        className="group flex items-start gap-4 rounded-xl border border-gray-200 bg-white p-4 transition-all hover:border-gray-300 hover:shadow-sm"
                      >
                        <div className="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-gray-100 text-gray-500 group-hover:bg-gray-900 group-hover:text-white transition-colors">
                          <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                            <rect width="7" height="7" x="3" y="3" rx="1" />
                            <rect width="7" height="7" x="14" y="3" rx="1" />
                            <rect width="7" height="7" x="14" y="14" rx="1" />
                            <rect width="7" height="7" x="3" y="14" rx="1" />
                          </svg>
                        </div>
                        <div className="min-w-0">
                          <h3 className="text-sm font-medium text-gray-900 group-hover:text-gray-700">{collection.title}</h3>
                          <p className="mt-0.5 text-sm text-gray-500 line-clamp-1">{collection.description}</p>
                        </div>
                      </Link>
                    ))}
                  </div>
                </div>

                {/* Recent Updates */}
                <div>
                  <div className="flex items-center justify-between mb-6">
                    <h2 className="text-xl font-semibold text-gray-900">Recent Updates</h2>
                    <Link href="/changelog" className="text-sm text-gray-500 hover:text-gray-900 transition-colors">
                      Changelog
                    </Link>
                  </div>
                  <div className="space-y-3">
                    {recentChangelog.map((item) => (
                      <article key={`${item.date}-${item.title}`} className="rounded-xl border border-gray-200 bg-white p-4">
                        <div className="flex items-center gap-2 mb-2">
                          <time className="text-xs text-gray-400">{item.date}</time>
                          <span className="rounded-full bg-gray-100 px-2 py-0.5 text-[10px] font-medium text-gray-600">
                            {item.type}
                          </span>
                        </div>
                        <h3 className="text-sm font-medium text-gray-900">{item.title}</h3>
                        <p className="mt-1 text-sm text-gray-500 line-clamp-2">{item.summary}</p>
                      </article>
                    ))}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </section>

        <GrowthSection kind="home" enabled={process.env.ENABLE_GROWTH_SECTIONS === 'true'} />
      </main>

      <Footer />
    </div>
  );
}
