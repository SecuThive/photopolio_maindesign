import type { Metadata } from 'next';
import Link from 'next/link';
import { createPageMetadata } from '@/lib/seo';
import { collectionConfigs } from '@/lib/collections';

export const metadata: Metadata = createPageMetadata({
  title: '20+ Free Design Collections - SaaS, Dashboards & E-commerce Templates',
  description: 'Browse 20+ curated design collections with 700+ free templates. Find SaaS landing pages, minimalist dashboards, pricing tables, hero sections, and more. All with copy-paste code.',
  path: '/collections',
});

export default function CollectionsIndexPage() {
  return (
    <div className="space-y-10">
      <header className="space-y-4">
        <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Collections</p>
        <h1 className="text-4xl font-semibold text-gray-900">Strategic Design Collections</h1>
        <p className="text-lg text-gray-600">
          A design hub organized by strategy and industry. Every collection links back to a pillar playbook for deeper context.
        </p>
      </header>
      <div className="grid gap-6 md:grid-cols-2">
        {collectionConfigs.map((collection) => (
          <Link
            key={collection.slug}
            href={`/collections/${collection.slug}`}
            className="rounded-3xl border border-gray-200 bg-white/90 p-6 shadow-sm transition hover:-translate-y-1 hover:border-gray-900"
          >
            <h2 className="text-2xl font-semibold text-gray-900">{collection.title}</h2>
            <p className="mt-3 text-sm text-gray-600">{collection.heroSummary}</p>
          </Link>
        ))}
      </div>
    </div>
  );
}
