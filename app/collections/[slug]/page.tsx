import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import DesignCard from '@/components/DesignCard';
import { supabaseServer } from '@/lib/supabase/server';
import { withDesignSlugs } from '@/lib/slug';
import type { DesignWithSlug } from '@/types/database';
import { collectionConfigs, getCollectionConfig } from '@/lib/collections';
import { createPageMetadata } from '@/lib/seo';
import { buildCollectionItemListSchema, buildFaqSchema } from '@/lib/structuredData';
import { getCollectionCluster } from '@/lib/content/linkMatrix';
import SeoGEOContent from '@/components/SeoGEOContent';
import GrowthSection from '@/components/GrowthSection';

export const revalidate = 0;

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');

const collectionSeoContent: Record<
  string,
  {
    title: string;
    summaryParagraphs: string[];
    bullets: string[];
    expandedSections: Array<{ heading: string; paragraphs: string[]; bullets?: string[] }>;
    faqs: Array<{ q: string; a: string }>;
  }
> = {
  'best-saas-landing-pages': {
    title: 'Best SaaS landing pages: definition, selection criteria, and checklist',
    summaryParagraphs: [
      'This collection curates SaaS landing pages that convert because they follow a consistent narrative: define the outcome, prove credibility, and guide evaluation. Each layout is selected for clarity, proof density, and a CTA ladder that leads to trial or demo without friction.',
      'Use this section to understand why each design made the cut, how to assess new candidates, and which checklist items matter most for conversion and SEO. The expanded content is structured for AI citation and internal design reviews.',
    ],
    bullets: [
      'Definition: outcome-first SaaS landing patterns that compress value into the first scroll.',
      'Selection criteria: explicit role-based headline, proof density, and clear CTA ladder.',
      'Checklist: hero under 12 words, two KPIs, three trust signals, and risk reversal.',
      'Common mistakes: feature-heavy heroes or buried social proof.',
      'SEO/GEO tip: declarative sentences improve summarization accuracy.',
    ],
    expandedSections: [
      {
        heading: 'Selection criteria and scoring rules',
        paragraphs: [
          'Every landing page in this collection is evaluated against a simple rubric: clarity, proof, and action. Clarity means the product’s outcome and persona are obvious in the first five seconds. Proof means metrics, logos, or testimonials are positioned close to the headline. Action means the CTA ladder is visible without forcing the user to scroll.',
          'If a page relies on generic “all-in-one platform” language or hides proof behind multiple sections, it does not qualify. Likewise, pages with conflicting CTAs are excluded because they weaken intent and reduce conversion performance.',
        ],
        bullets: [
          'Headline states role + outcome; subhead explains mechanism.',
          'Proof block appears above the fold or within first scroll.',
          'CTA ladder includes a primary and secondary path.',
        ],
      },
      {
        heading: 'Checklist for evaluating new pages',
        paragraphs: [
          'Use this checklist when reviewing new SaaS landing pages. It keeps the evaluation objective and speeds up iteration across marketing and product teams. The goal is to maintain narrative integrity while allowing visual variation.',
        ],
        bullets: [
          'Hero headline ≤ 12 words, with KPI or quantified claim.',
          'Risk-reversal line beneath primary CTA.',
          'Pricing narrative ties tiers to team size or scenario.',
          'Performance guardrails: LCP under 2s and CLS near 0.',
        ],
      },
    ],
    faqs: [
      {
        q: 'Why are these SaaS pages included?',
        a: 'They meet a strict clarity-proof-action rubric and demonstrate conversion-first storytelling.',
      },
      {
        q: 'Can I use these layouts directly?',
        a: 'Yes, but adjust brand tokens and copy to match your product’s audience and positioning.',
      },
      {
        q: 'What is the quickest win on a SaaS landing page?',
        a: 'Add quantified proof next to the hero headline and tighten the CTA ladder to one primary and one secondary action.',
      },
    ],
  },
  'minimalist-dashboards': {
    title: 'Minimalist dashboards: definition, selection criteria, and checklist',
    summaryParagraphs: [
      'This collection highlights dashboard layouts that prioritize signal over decoration. Each design is chosen for scan-friendly hierarchy, balanced density, and accessibility-forward dark mode tokens.',
      'Use the criteria below to evaluate whether a dashboard layout is truly minimalist or simply sparse. The expanded section includes checklist items and common mistakes that make dashboards slower to read or harder to trust.',
    ],
    bullets: [
      'Definition: dashboards that surface state → delta → next action within seconds.',
      'Selection criteria: metric-first hierarchy, density controls, and clear data tables.',
      'Checklist: 8pt grid, three KPI cards max, sticky table headers.',
      'Common mistakes: mixing densities and hiding controls.',
      'Accessibility: maintain 4.5:1 contrast in dark mode.',
    ],
    expandedSections: [
      {
        heading: 'Selection criteria and data hierarchy',
        paragraphs: [
          'We include dashboards that keep the scan path consistent: metrics first, trends second, tables third. This structure keeps decision-making fast even as data volume grows. Visual systems that bury KPIs below tables or place charts before summary cards are excluded.',
          'The best minimalist dashboards also support density controls. A compact toggle preserves high-density workflows without sacrificing clarity for casual users.',
        ],
        bullets: [
          'KPI cards in a single row, with deltas adjacent to values.',
          'Tables use subtle dividers instead of zebra stripes.',
          'Sidebars stay near 264px to maintain muscle memory.',
        ],
      },
      {
        heading: 'Checklist for evaluating new layouts',
        paragraphs: [
          'Minimalist dashboards should feel fast and calm without sacrificing information. Use this checklist to keep evaluations consistent across design reviews and engineering handoffs.',
        ],
        bullets: [
          'Content line height between 1.4 and 1.6 for scan speed.',
          'Dark mode tokens validated at 4.5:1 contrast ratio.',
          'Hover and inline edit interactions under 16ms latency.',
        ],
      },
    ],
    faqs: [
      {
        q: 'What makes a dashboard “minimalist”?',
        a: 'It preserves information hierarchy and removes decorative noise while keeping key metrics in the first scan path.',
      },
      {
        q: 'Do these layouts work for internal tools?',
        a: 'Yes. The layouts are optimized for operational workflows and dense data tables.',
      },
      {
        q: 'How do I keep density high without clutter?',
        a: 'Use an 8pt grid, compact toggles, and consistent table row heights to preserve clarity.',
      },
    ],
  },
};

type PageProps = {
  params: { slug: string };
};

export function generateStaticParams() {
  return collectionConfigs.map((config) => ({ slug: config.slug }));
}

export function generateMetadata({ params }: PageProps): Metadata {
  const config = getCollectionConfig(params.slug);
  if (!config) {
    return {
      title: 'Collection not found',
      robots: { index: false },
    };
  }

  return createPageMetadata({
    title: config.title,
    description: config.metaDescription,
    path: `/collections/${config.slug}`,
  });
}

export default async function CollectionDetailPage({ params }: PageProps) {
  const config = getCollectionConfig(params.slug);
  if (!config) {
    notFound();
  }

  const cluster = getCollectionCluster(config.slug);
  const siblingCollections = cluster?.siblings ?? [];
  const pillarTopic = cluster?.pillar ?? null;
  const pillarHref = pillarTopic ? `/playbooks/${pillarTopic.slug}` : config.pillar.href;

  const { data: designs } = await supabaseServer
    .from('designs')
    .select('*')
    .eq('status', 'published')
    .eq('category', config.supabaseCategory)
    .order('created_at', { ascending: false })
    .limit(12);

  const designsWithSlugs = (withDesignSlugs(designs ?? []) as DesignWithSlug[]) ?? [];
  const schemaDesigns = designsWithSlugs.filter((design) => Boolean(design.slug));

  const itemListSchema = buildCollectionItemListSchema(
    config.title,
    config.slug,
    schemaDesigns.map((design) => ({
      slug: design.slug as string,
      title: design.title,
      description: design.description,
    }))
  );
  const faqSchema = buildFaqSchema(config.title, config.faqs);
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: SITE_URL,
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Collections',
        item: `${SITE_URL}/collections`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: config.title,
        item: `${SITE_URL}/collections/${config.slug}`,
      },
    ],
  };
  const schemaNodes = [itemListSchema, faqSchema, breadcrumbSchema].filter(Boolean);

  const seoContent = collectionSeoContent[config.slug] ?? {
    title: `${config.title}: definition and checklist`,
    summaryParagraphs: [
      `${config.title} is curated to reinforce the core strategy behind this collection. This placeholder copy is unique so the page remains AI-citable even before custom text is written.`,
      'Expand the section to review selection criteria and a short checklist you can reuse during design reviews.',
    ],
    bullets: [
      'Definition: a curated set aligned with the related playbook.',
      'Selection criteria: consistent narrative and proof placement.',
      'Checklist: clear CTA ladder, trust signals, and performance guardrails.',
      'Mistakes: inconsistent hierarchy or ambiguous outcomes.',
      'AI citation tip: keep sentences declarative and explicit.',
    ],
    expandedSections: [
      {
        heading: 'Expanded guidance',
        paragraphs: [
          'This placeholder explains the intent of the collection and ensures the page includes descriptive, crawlable text. Replace it with collection-specific guidance when ready.',
        ],
      },
    ],
    faqs: [
      {
        q: 'How should I use this collection?',
        a: 'Use it as a reference set during strategy or layout reviews, then map each pattern to your product’s goals.',
      },
      {
        q: 'Is the content ready for AI citation?',
        a: 'Yes. The section uses structured headings, bullets, and explicit definitions for clarity.',
      },
    ],
  };

  return (
    <div className="space-y-12">
      {schemaNodes.length > 0 && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{
            __html: JSON.stringify(schemaNodes.length === 1 ? schemaNodes[0] : schemaNodes),
          }}
        />
      )}

      <nav className="text-sm text-gray-500" aria-label="Breadcrumb">
        <ol className="flex flex-wrap items-center gap-2">
          <li>
            <Link href="/" className="hover:text-gray-900">
              Home
            </Link>
          </li>
          <li aria-hidden>/</li>
          <li>
            <Link href="/collections" className="hover:text-gray-900">
              Collections
            </Link>
          </li>
          <li aria-hidden>/</li>
          <li className="text-gray-900">{config.title}</li>
        </ol>
      </nav>

      <header className="space-y-6">
        <div className="flex items-center gap-3 text-[11px] uppercase tracking-[0.3em] text-gray-500">
          <span className="rounded-full border border-gray-200 bg-white/80 px-4 py-1 font-semibold text-gray-700">
            {config.heroEyebrow}
          </span>
          <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
          <span>Collection</span>
        </div>
        <div className="space-y-4">
          <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 leading-tight">
            {config.heroHeading}
          </h1>
          <p className="text-lg text-gray-600 leading-relaxed max-w-3xl">{config.heroSummary}</p>
        </div>
        <div className="grid gap-4 md:grid-cols-2">
          {config.description.map((paragraph) => (
            <p key={paragraph} className="text-base text-gray-700 leading-relaxed">
              {paragraph}
            </p>
          ))}
        </div>
        <ul className="mt-4 space-y-3 rounded-3xl border border-gray-200 bg-white/90 p-6 shadow-sm text-sm text-gray-700">
          {config.highlightPoints.map((point) => (
            <li key={point} className="flex gap-3">
              <span className="mt-1 h-2 w-2 rounded-full bg-gray-900" aria-hidden />
              <span>{point}</span>
            </li>
          ))}
        </ul>
      </header>

      <GrowthSection kind="collection" slug={params.slug} enabled={process.env.ENABLE_GROWTH_SECTIONS === 'true'} />

      <section className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm space-y-6">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.35em] text-gray-400">Read the related playbook</p>
            <p className="mt-2 text-sm text-gray-600">Dive deeper into the strategy behind this collection.</p>
          </div>
          <Link
            href={pillarHref}
            className="inline-flex items-center rounded-full border border-gray-900 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.3em] text-gray-900 transition hover:bg-gray-900 hover:text-white"
          >
            {config.pillar.title}
          </Link>
        </div>
        <SeoGEOContent
          title={seoContent.title}
          summaryParagraphs={seoContent.summaryParagraphs}
          bullets={seoContent.bullets}
          expandedSections={seoContent.expandedSections}
          faqs={seoContent.faqs}
        />
      </section>

      <section className="space-y-6">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Best Practices</p>
          <h2 className="mt-2 text-3xl font-semibold text-gray-900">Rules for applying these patterns</h2>
        </div>
        <div className="grid gap-5 md:grid-cols-2">
          {config.bestPractices.map((practice) => (
            <div key={practice.title} className="rounded-3xl border border-gray-200 bg-white/90 p-6 shadow-sm">
              <h3 className="text-lg font-semibold text-gray-900">{practice.title}</h3>
              <p className="mt-3 text-sm text-gray-700 leading-relaxed">{practice.description}</p>
            </div>
          ))}
        </div>
      </section>

      <section className="space-y-4 rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
        <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Implementation Checklist</p>
        <h2 className="text-3xl font-semibold text-gray-900">Pre-launch checklist</h2>
        <ol className="mt-4 space-y-3 text-gray-800">
          {config.checklist.map((item, index) => (
            <li key={item} className="flex gap-4">
              <span className="text-sm font-semibold text-gray-500">{String(index + 1).padStart(2, '0')}</span>
              <span className="text-base leading-relaxed">{item}</span>
            </li>
          ))}
        </ol>
      </section>

      <section className="space-y-4">
        <div className="flex items-center justify-between gap-4">
          <div>
            <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Design Library</p>
            <h2 className="text-3xl font-semibold text-gray-900">Representative designs</h2>
          </div>
          <Link
            href={pillarHref}
            className="text-sm font-semibold uppercase tracking-[0.3em] text-gray-700 hover:text-gray-900"
          >
            {config.pillar.title} ↗
          </Link>
        </div>
        {designsWithSlugs.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {designsWithSlugs.map((design) => (
              <DesignCard
                key={design.id}
                design={design}
                likes={design.likes ?? 0}
                liked={false}
              />
            ))}
          </div>
        ) : (
          <div className="rounded-3xl border border-gray-200 bg-white/80 p-10 text-center text-gray-600">
            No published designs yet. Fresh layouts are arriving soon.
          </div>
        )}
      </section>

      {(pillarTopic || siblingCollections.length > 0) && (
        <section className="space-y-4 rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
          <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Cluster Routing</p>
          <h2 className="text-3xl font-semibold text-gray-900">Keep the strategy → collection → design flow</h2>
          <div className="grid gap-4 md:grid-cols-2">
            {pillarTopic && (
              <Link
                href={`/playbooks/${pillarTopic.slug}`}
                className="rounded-2xl border border-gray-200 bg-gray-50/80 p-5 transition hover:border-gray-900"
              >
                <p className="text-[11px] uppercase tracking-[0.3em] text-gray-500">Playbook</p>
                <p className="mt-2 text-lg font-semibold text-gray-900">{pillarTopic.title}</p>
                <p className="mt-2 text-sm text-gray-600 leading-relaxed">{pillarTopic.summary}</p>
              </Link>
            )}
            {siblingCollections.map((sibling) => (
              <Link
                key={sibling.slug}
                href={`/collections/${sibling.slug}`}
                className="rounded-2xl border border-gray-200 bg-gray-50/80 p-5 transition hover:border-gray-900"
              >
                <p className="text-[11px] uppercase tracking-[0.3em] text-gray-500">Adjacent Collection</p>
                <p className="mt-2 text-lg font-semibold text-gray-900">{sibling.title}</p>
                <p className="mt-2 text-sm text-gray-600 leading-relaxed">{sibling.heroSummary}</p>
              </Link>
            ))}
          </div>
        </section>
      )}

      <section className="space-y-5 rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
        <p className="text-xs uppercase tracking-[0.3em] text-gray-500">FAQ</p>
        <h2 className="text-3xl font-semibold text-gray-900">Frequently asked questions</h2>
        <div className="space-y-4">
          {config.faqs.map((faq) => (
            <details key={faq.question} className="rounded-2xl border border-gray-200 bg-gray-50/80 p-4">
              <summary className="cursor-pointer text-sm font-semibold text-gray-900">
                {faq.question}
              </summary>
              <p className="mt-3 text-sm text-gray-700 leading-relaxed">{faq.answer}</p>
            </details>
          ))}
        </div>
      </section>

      <section className="rounded-3xl border border-dashed border-gray-300 bg-white/70 p-8 text-center">
        <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Pillar Playbook</p>
        <h2 className="mt-3 text-2xl font-semibold text-gray-900">{config.pillar.title}</h2>
        <p className="mt-4 text-base text-gray-700">{config.pillar.summary}</p>
        <Link
          href={pillarHref}
          className="mt-6 inline-flex items-center justify-center rounded-full bg-gray-900 px-6 py-3 text-sm font-semibold uppercase tracking-[0.3em] text-white"
        >
          Read the playbook
        </Link>
      </section>
    </div>
  );
}
