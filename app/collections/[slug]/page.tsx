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
import { collectionSeoContent } from '@/lib/collectionSeoContent';

export const revalidate = 0;

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');


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

  // Build design query with tag-based filtering for better collection accuracy
  let designQuery = supabaseServer
    .from('designs')
    .select('*')
    .eq('status', 'published')
    .eq('category', config.supabaseCategory)
    .order('created_at', { ascending: false })
    .limit(12);

  // If collection has specific filter tags, use them for more precise matching
  if (config.filterTags && config.filterTags.length > 0) {
    designQuery = designQuery.overlaps('tags', config.filterTags);
  }

  const { data: designs } = await designQuery;

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
          <div className="rounded-3xl border-2 border-dashed border-gray-300 bg-gray-50/50 p-12 text-center space-y-4">
            <div className="text-4xl mb-2">🎨</div>
            <h3 className="text-xl font-semibold text-gray-900">Curating designs for this collection</h3>
            <p className="text-gray-600 max-w-md mx-auto">
              We&apos;re carefully selecting the best {config.title.toLowerCase()} designs. Check back soon or explore related collections below.
            </p>
            {siblingCollections.length > 0 && (
              <div className="mt-6 inline-flex flex-wrap gap-2 justify-center">
                {siblingCollections.slice(0, 3).map((sibling) => (
                  <Link
                    key={sibling.slug}
                    href={`/collections/${sibling.slug}`}
                    className="inline-flex items-center px-4 py-2 rounded-full border border-gray-300 bg-white text-sm font-medium text-gray-700 hover:border-gray-900 hover:bg-gray-50 transition-colors"
                  >
                    {sibling.title}
                  </Link>
                ))}
              </div>
            )}
            {pillarTopic && (
              <Link
                href={`/playbooks/${pillarTopic.slug}`}
                className="mt-4 inline-flex items-center px-5 py-2.5 rounded-full bg-gray-900 text-sm font-semibold text-white hover:bg-gray-800 transition-colors"
              >
                Read {config.pillar.title} →
              </Link>
            )}
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
