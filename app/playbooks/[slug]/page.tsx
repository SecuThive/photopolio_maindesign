import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import DesignCard from '@/components/DesignCard';
import { pillarTopics, getPillarTopic } from '@/lib/pillars';
import { createPageMetadata } from '@/lib/seo';
import { PillarHero } from '@/components/content/PillarHero';
import { PillarSectionBlock } from '@/components/content/PillarSection';
import { PillarTableOfContents } from '@/components/content/PillarToc';
import { getPillarCluster, getSupabaseCategoriesForPillar } from '@/lib/content/linkMatrix';
import { supabaseServer } from '@/lib/supabase/server';
import { withDesignSlugs } from '@/lib/slug';
import type { DesignWithSlug } from '@/types/database';

type PageProps = {
  params: { slug: string };
};

export const revalidate = 3600;

export function generateStaticParams() {
  return pillarTopics.map((topic) => ({ slug: topic.slug }));
}

export function generateMetadata({ params }: PageProps): Metadata {
  const topic = getPillarTopic(params.slug);
  if (!topic) {
    return {
      title: 'Playbook not found',
      robots: { index: false },
    };
  }

  return createPageMetadata({
    title: topic.title,
    description: topic.seoDescription,
    path: `/playbooks/${topic.slug}`,
  });
}

export default async function PlaybookDetailPage({ params }: PageProps) {
  const topic = getPillarTopic(params.slug);

  if (!topic) {
    notFound();
  }

  const cluster = getPillarCluster(topic.slug);
  const matrixCollections = cluster?.collections ?? [];
  const relatedCollections = matrixCollections.length
    ? matrixCollections.map((collection) => ({
        title: collection.title,
        href: `/collections/${collection.slug}`,
        description: collection.heroSummary,
      }))
    : topic.relatedCollections;
  const categories = getSupabaseCategoriesForPillar(topic.slug);
  let featuredDesigns: DesignWithSlug[] = [];

  if (categories.length > 0) {
    const { data } = await supabaseServer
      .from('designs')
      .select('*')
      .eq('status', 'published')
      .in('category', categories)
      .order('created_at', { ascending: false })
      .limit(6);

    featuredDesigns = withDesignSlugs(data ?? []) as DesignWithSlug[];
  }

  return (
    <section className="space-y-12">
      <div className="space-y-6">
        <nav className="text-sm text-gray-500" aria-label="Breadcrumb">
          <Link href="/" className="hover:text-gray-900">Home</Link>
          <span className="mx-2">/</span>
          <Link href="/playbooks" className="hover:text-gray-900">Playbooks</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900">{topic.title}</span>
        </nav>

        <PillarHero
          eyebrow={topic.eyebrow}
          title={topic.title}
          description={topic.description}
          summary={topic.summary}
          tags={topic.tags}
          bestFor={topic.bestFor}
        />
      </div>

      <div className="grid gap-8 lg:grid-cols-[minmax(0,2.2fr)_minmax(0,0.8fr)]">
        <div className="space-y-6">
          {topic.sections.map((section) => (
            <PillarSectionBlock key={section.id} section={section} />
          ))}
          <section className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
            <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Collections</p>
            <h2 className="mt-3 text-2xl font-semibold text-gray-900">Connected collections</h2>
            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {relatedCollections.map((collection) => (
                <Link
                  key={collection.href}
                  href={collection.href}
                  className="rounded-2xl border border-gray-200 bg-gray-50/80 p-5 transition hover:border-gray-900"
                >
                  <p className="text-sm font-semibold text-gray-900">{collection.title}</p>
                  <p className="mt-2 text-sm text-gray-600">{collection.description}</p>
                </Link>
              ))}
            </div>
          </section>
          <section className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
            <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Further Reading</p>
            <h2 className="mt-3 text-2xl font-semibold text-gray-900">Connected journals</h2>
            <div className="mt-6 space-y-4">
              {topic.relatedReads.map((article) => (
                <Link
                  key={article.title}
                  href={article.href}
                  className="group block rounded-2xl border border-gray-200 bg-gray-50/80 p-5 transition hover:border-gray-900"
                >
                  <p className="text-sm font-semibold text-gray-900 group-hover:text-gray-700">{article.title}</p>
                  <p className="mt-2 text-sm text-gray-600">{article.description}</p>
                </Link>
              ))}
            </div>
          </section>
        </div>
        <div className="space-y-6">
          <PillarTableOfContents sections={topic.sections} slug={topic.slug} />
          <section className="rounded-3xl border border-gray-200 bg-white/90 p-6 shadow-sm">
            <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Next</p>
            <ul className="mt-4 space-y-3 text-sm text-gray-700">
              {pillarTopics
                .filter((other) => other.slug !== topic.slug)
                .slice(0, 3)
                .map((other) => (
                  <li key={other.slug}>
                    <Link href={`/playbooks/${other.slug}`} className="transition-colors hover:text-gray-900">
                      {other.title}
                    </Link>
                  </li>
                ))}
            </ul>
          </section>
        </div>
      </div>
      {featuredDesigns.length > 0 && (
        <section className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
          <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Featured Designs</p>
          <h2 className="mt-3 text-3xl font-semibold text-gray-900">Cluster Highlights</h2>
          <p className="mt-2 text-sm text-gray-600">
            Recent layouts from this playbook’s associated collections. Use them to audit how the strategy
            translates into production UI states.
          </p>
          <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {featuredDesigns.map((design) => (
              <DesignCard
                key={design.id}
                design={design}
                likes={design.likes ?? 0}
                liked={false}
                likeDisabled
              />
            ))}
          </div>
        </section>
      )}
    </section>
  );
}
