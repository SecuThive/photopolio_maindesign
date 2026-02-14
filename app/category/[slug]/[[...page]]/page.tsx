import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { supabaseServer } from '@/lib/supabase/server';
import { withDesignSlugs } from '@/lib/slug';
import type { Design, DesignWithSlug } from '@/types/database';
import { CATEGORY_SLUGS, getCategoryDefinition } from '@/lib/categories';

const PAGE_SIZE = 12;
const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');

export const revalidate = 0;

type PageParams = {
  slug: string;
  page?: string[];
};

type CategoryPageProps = {
  params: PageParams;
};

function parsePageSegment(segment?: string[]): number {
  if (!segment || segment.length === 0) {
    return 1;
  }

  if (segment.length === 2 && segment[0] === 'page') {
    const parsed = Number(segment[1]);
    if (Number.isInteger(parsed) && parsed >= 1) {
      return parsed;
    }
  }

  notFound();
}

async function fetchCategoryDesigns(slug: string, pageNumber: number) {
  const definition = getCategoryDefinition(slug);
  if (!definition) {
    notFound();
  }

  const from = (pageNumber - 1) * PAGE_SIZE;
  const to = from + PAGE_SIZE - 1;
  const categories = definition.matchValues ?? [definition.label];

  const { data, error, count } = await supabaseServer
    .from('designs')
    .select('*', { count: 'exact' })
    .eq('status', 'published')
    .in('category', categories)
    .order('created_at', { ascending: false })
    .range(from, to);

  if (error) {
    console.error('Failed to fetch category designs', error);
    notFound();
  }

  const total = count ?? 0;
  const designs = data ? (withDesignSlugs(data as Design[]) as DesignWithSlug[]) : [];

  return {
    definition,
    designs,
    total,
    from,
  };
}

async function fetchCategoryCount(slug: string): Promise<number> {
  const definition = getCategoryDefinition(slug);
  if (!definition) {
    return 0;
  }

  const categories = definition.matchValues ?? [definition.label];

  const { count, error } = await supabaseServer
    .from('designs')
    .select('id', { count: 'exact', head: true })
    .eq('status', 'published')
    .in('category', categories);

  if (error) {
    console.error('Failed to fetch category count', error);
    return 0;
  }

  return count ?? 0;
}

function buildCanonicalPath(slug: string, pageNumber: number): string {
  return pageNumber > 1 ? `/category/${slug}/page/${pageNumber}` : `/category/${slug}`;
}

export async function generateMetadata({ params }: CategoryPageProps): Promise<Metadata> {
  if (!CATEGORY_SLUGS.includes(params.slug)) {
    return {
      title: 'Category not found · UI Syntax',
      robots: { index: false, follow: false },
    };
  }

  const pageNumber = parsePageSegment(params.page);
  const definition = getCategoryDefinition(params.slug);

  if (!definition) {
    return {
      title: 'Category not found · UI Syntax',
      robots: { index: false, follow: false },
    };
  }

  const totalCount = await fetchCategoryCount(params.slug);
  const totalPages = Math.max(1, Math.ceil(totalCount / PAGE_SIZE));
  if (pageNumber > totalPages) {
    return {
      title: 'Page not found · UI Syntax',
      robots: { index: false, follow: false },
    };
  }

  const baseTitle = `${definition.label} UI Design Inspiration`;
  const pageQualifier = pageNumber > 1 ? ` · Page ${pageNumber}` : '';
  const title = `${baseTitle}${pageQualifier} · UI Syntax`;
  const description = pageNumber > 1
    ? `${definition.description} Browse page ${pageNumber} of the ${definition.label.toLowerCase()} gallery curated by UI Syntax.`
    : definition.description;

  const canonicalPath = buildCanonicalPath(definition.slug, pageNumber);
  const canonicalUrl = `${SITE_URL}${canonicalPath}`;

  const metadata: Metadata = {
    title,
    description,
    alternates: {
      canonical: canonicalUrl,
    },
    openGraph: {
      title,
      description,
      url: canonicalUrl,
      type: 'website',
    },
    twitter: {
      card: 'summary_large_image',
      title,
      description,
    },
  };

  const paginationLinks: Record<string, string> = {};

  if (pageNumber > 1) {
    paginationLinks['link:prev'] = `${SITE_URL}${buildCanonicalPath(definition.slug, pageNumber - 1)}`;
  }

  if (pageNumber < totalPages) {
    paginationLinks['link:next'] = `${SITE_URL}${buildCanonicalPath(definition.slug, pageNumber + 1)}`;
  }

  if (Object.keys(paginationLinks).length > 0) {
    metadata.other = paginationLinks;
  }

  return metadata;
}

function formatDate(dateString: string) {
  return new Date(dateString).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

function buildExcerpt(description: string | null) {
  if (!description) {
    return null;
  }
  const trimmed = description.trim();
  if (!trimmed) {
    return null;
  }
  const sentences = trimmed
    .split(/(?<=[.!?])\s+/)
    .map((sentence) => sentence.trim())
    .filter(Boolean);
  const snippet = sentences.slice(0, 2).join(' ') || trimmed;
  return snippet.length > 200 ? `${snippet.slice(0, 200)}…` : snippet;
}

export default async function CategoryHubPage({ params }: CategoryPageProps) {
  const pageNumber = parsePageSegment(params.page);
  const { definition, designs, total, from } = await fetchCategoryDesigns(params.slug, pageNumber);
  const totalPages = Math.max(1, Math.ceil(total / PAGE_SIZE));

  if (pageNumber > totalPages) {
    notFound();
  }

  const firstItem = total === 0 ? 0 : from + 1;
  const lastItem = from + designs.length;
  const previousHref = pageNumber > 1 ? buildCanonicalPath(definition.slug, pageNumber - 1) : null;
  const nextHref = pageNumber < totalPages ? buildCanonicalPath(definition.slug, pageNumber + 1) : null;

  const otherCategories = CATEGORY_SLUGS.filter((slug) => slug !== definition.slug);

  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-12 space-y-12">
        <section className="space-y-4">
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Category Hub</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 tracking-tight">
            {definition.label} inspiration
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl">
            {definition.description}
          </p>
          <div className="flex flex-wrap items-center gap-2 text-sm text-gray-500">
            <span className="font-semibold text-gray-900">{total} designs</span>
            <span className="text-gray-400">·</span>
            <span>
              Showing {firstItem}-{lastItem} ({PAGE_SIZE} per page)
            </span>
          </div>
        </section>

        {designs.length === 0 ? (
          <div className="rounded-3xl border border-dashed border-gray-300 bg-white/80 p-10 text-center">
            <p className="text-sm uppercase tracking-[0.3em] text-gray-500">No uploads yet</p>
            <p className="mt-3 text-lg text-gray-600">
              This category is warming up. Fresh designs will land here soon—check back shortly.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-8">
            {designs.map((design) => {
              const excerpt = buildExcerpt(design.description ?? null);
              return (
                <article
                  key={design.id}
                  className="flex flex-col overflow-hidden rounded-[32px] border border-gray-200 bg-white/95 shadow-[0_14px_45px_rgba(15,23,42,0.08)]"
                >
                  <Link href={`/design/${design.slug}`} className="relative block h-56 w-full overflow-hidden bg-gray-100">
                    <Image
                      src={design.image_url}
                      alt={design.title}
                      fill
                      sizes="(max-width: 1024px) 100vw, 33vw"
                      className="object-cover object-top transition-transform duration-500 ease-out hover:scale-105"
                    />
                  </Link>
                  <div className="flex flex-1 flex-col gap-4 p-6">
                    <div className="flex items-center gap-2 text-xs uppercase tracking-[0.3em] text-gray-400">
                      <span>{definition.label}</span>
                      <span className="h-1 w-1 rounded-full bg-gray-300" aria-hidden />
                      <time className="tracking-wide text-[11px]" dateTime={design.created_at}>
                        {formatDate(design.created_at)}
                      </time>
                    </div>
                    <h2 className="text-2xl font-semibold text-gray-900">
                      <Link href={`/design/${design.slug}`} className="hover:text-gray-600">
                        {design.title}
                      </Link>
                    </h2>
                    {excerpt && <p className="text-sm text-gray-600 leading-relaxed line-clamp-3">{excerpt}</p>}
                    <div className="mt-auto">
                      <Link
                        href={`/design/${design.slug}`}
                        className="inline-flex items-center gap-2 text-xs font-semibold uppercase tracking-[0.35em] text-gray-900"
                      >
                        View detail
                        <span aria-hidden className="text-base">
                          →
                        </span>
                      </Link>
                    </div>
                  </div>
                </article>
              );
            })}
          </div>
        )}

        <nav className="flex flex-col items-center gap-4 rounded-2xl border border-gray-200 bg-white/90 p-6 text-sm text-gray-600">
          <div className="flex items-center gap-3">
            <span className="font-semibold text-gray-900">Page {pageNumber}</span>
            <span className="text-gray-400">of</span>
            <span className="font-semibold text-gray-900">{totalPages}</span>
          </div>
          <div className="flex flex-wrap items-center justify-center gap-3">
            <Link
              href={previousHref ?? '#'}
              aria-disabled={!previousHref}
              className={`inline-flex items-center gap-2 rounded-full border px-4 py-2 uppercase tracking-[0.35em] ${
                previousHref
                  ? 'border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white'
                  : 'border-gray-200 text-gray-300 cursor-not-allowed'
              }`}
            >
              ← Prev
            </Link>
            <Link
              href={nextHref ?? '#'}
              aria-disabled={!nextHref}
              className={`inline-flex items-center gap-2 rounded-full border px-4 py-2 uppercase tracking-[0.35em] ${
                nextHref
                  ? 'border-gray-900 text-gray-900 hover:bg-gray-900 hover:text-white'
                  : 'border-gray-200 text-gray-300 cursor-not-allowed'
              }`}
            >
              Next →
            </Link>
          </div>
        </nav>

        <section className="rounded-3xl border border-gray-200 bg-white/90 p-6">
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Explore more</p>
          <div className="mt-4 flex flex-wrap gap-3">
            {otherCategories.map((slug) => (
              <Link
                key={slug}
                href={`/category/${slug}`}
                className="rounded-full border border-gray-200 px-4 py-2 text-sm font-medium text-gray-600 hover:border-gray-900 hover:text-gray-900"
              >
                {getCategoryDefinition(slug)?.label ?? slug}
              </Link>
            ))}
          </div>
        </section>
      </main>
      <Footer />
    </div>
  );
}
