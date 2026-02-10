import { Metadata } from 'next';
import { notFound, permanentRedirect } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ShareLinkButton from '@/components/ShareLinkButton';
import DesignDetailCustomizer from '@/components/DesignDetailCustomizer';
import ViewCountBadge from '@/components/ViewCountBadge';
import { supabaseServer } from '@/lib/supabase/server';
import { extractDesignIdFromSlug, withDesignSlug, withDesignSlugs } from '@/lib/slug';
import { Design, DesignWithSlug } from '@/types/database';
import { buildReactComponentFromHtml } from '@/lib/codeTransform';

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');

export const revalidate = 0;

type PageProps = {
  params: { slug: string };
};

async function fetchDesignBySlug(slug: string): Promise<DesignWithSlug | null> {
  let resolved: Design | null = null;

  const { data: slugMatch, error: slugError } = await supabaseServer
    .from('designs')
    .select('*')
    .eq('slug', slug)
    .maybeSingle<Design>();

  if (slugMatch) {
    resolved = slugMatch;
  } else if (slugError && !slugError.message?.includes('column "slug" does not exist')) {
    console.error('Failed to query slug column', slugError);
  }

  if (!resolved) {
    const designId = extractDesignIdFromSlug(slug);
    if (!designId) {
      return null;
    }

    const { data, error } = await supabaseServer
      .from('designs')
      .select('*')
      .eq('id', designId)
      .single<Design>();

    if (error || !data) {
      return null;
    }

    resolved = data;
  }

  return withDesignSlug(resolved);
}

async function fetchRelatedDesigns(design: DesignWithSlug): Promise<DesignWithSlug[]> {
  let query = supabaseServer
    .from('designs')
    .select('*')
    .eq('status', 'published')
    .neq('id', design.id)
    .order('created_at', { ascending: false })
    .limit(8);

  if (design.category) {
    query = query.eq('category', design.category);
  }

  const { data, error } = await query;

  if (error || !data) {
    return [];
  }

  return withDesignSlugs(data);
}

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  const design = await fetchDesignBySlug(params.slug);

  if (design?.status === 'archived') {
    permanentRedirect('/');
  }

  if (!design) {
    return {
      title: 'Design not found · UI Syntax',
      description: 'The requested design could not be located.',
      robots: { index: false, follow: false },
    };
  }

  const description = design.description || 'AI-generated design inspiration from UI Syntax.';
  const canonical = `${SITE_URL}/design/${design.slug}`;

  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'CreativeWork',
    name: design.title || 'UI Design',
    description: description,
    image: design.image_url,
    author: {
      '@type': 'Organization',
      name: 'UI Syntax',
      url: 'https://ui-syntax.com'
    },
    datePublished: design.created_at,
    dateModified: design.updated_at,
    inLanguage: 'en-US',
    thumbnailUrl: design.image_url,
    ...(design.category && {
      genre: design.category,
      keywords: design.category
    })
  };

  return {
    title: `${design.title} · UI Syntax`,
    description,
    alternates: { canonical },
    openGraph: {
      title: design.title || 'UI Syntax Design',
      description,
      url: canonical,
      type: 'article',
      images: design.image_url
        ? [
            {
              url: design.image_url,
              alt: design.title || 'Design preview',
            },
          ]
        : undefined,
    },
    twitter: {
      card: 'summary_large_image',
      title: design.title || 'UI Syntax Design',
      description,
      images: design.image_url ? [design.image_url] : undefined,
    },
    other: {
      'script:ld+json': JSON.stringify(jsonLd)
    }
  };
}

function formatDate(dateString: string) {
  const date = new Date(dateString);
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
  });
}

type DescriptionBlock = {
  title?: string;
  body: string;
};

function parseDescriptionBlocks(description?: string | null): DescriptionBlock[] {
  if (!description) {
    return [];
  }

  const normalized = description.replace(/\r\n/g, '\n').trim();
  if (!normalized) {
    return [];
  }

  const rawBlocks = normalized.split(/\n{2,}/).map((block) => block.trim()).filter(Boolean);
  const structured = rawBlocks.map((block) => {
    const headingMatch = block.match(/^([A-Za-z0-9][A-Za-z0-9\s&()\/-]{3,60}):\s*([\s\S]+)$/);
    if (headingMatch) {
      return {
        title: headingMatch[1].trim(),
        body: headingMatch[2].trim(),
      } as DescriptionBlock;
    }
    return { body: block };
  });

  if (structured.length === 1) {
    const sentences = structured[0].body
      .split(/(?<=[.!?])\s+(?=[A-Z0-9])/)
      .map((sentence) => sentence.trim())
      .filter(Boolean);

    if (sentences.length > 2) {
      const chunked: DescriptionBlock[] = [];
      for (let i = 0; i < sentences.length; i += 2) {
        chunked.push({ body: sentences.slice(i, i + 2).join(' ') });
      }
      return chunked;
    }
  }

  return structured;
}

function getHeroDescription(blocks: DescriptionBlock[], fallback?: string | null): string | null {
  const base = blocks[0]?.body || fallback || '';
  if (!base) {
    return null;
  }
  return base.length > 220 ? `${base.substring(0, 220).trim()}…` : base;
}

export default async function DesignDetailPage({ params }: PageProps) {
  const design = await fetchDesignBySlug(params.slug);

  if (!design) {
    notFound();
  }

  if (design.status === 'archived') {
    permanentRedirect('/');
  }

  const currentDesign = design;
  const relatedDesigns = await fetchRelatedDesigns(currentDesign);
  const sidebarSuggestions = relatedDesigns.slice(0, 3);
  const shareUrl = `${SITE_URL}/design/${currentDesign.slug}`;
  const initialViewCount = currentDesign.views ?? 0;
  const descriptionBlocks = parseDescriptionBlocks(currentDesign.description);
  const heroDescription = getHeroDescription(descriptionBlocks, currentDesign.description);
  const reactCode = buildReactComponentFromHtml(currentDesign.code);

  return (
    <div className="min-h-screen bg-luxury-white overflow-x-hidden w-full">
      <Header />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10 sm:py-12 space-y-8 sm:space-y-10 w-full overflow-hidden">
        {/* Hero Section with Background */}
        <div className="relative w-full bg-gradient-to-br from-gray-50 via-white to-gray-50 border border-gray-200 rounded-3xl p-6 sm:p-8 md:p-12 shadow-sm overflow-hidden">
          {/* Decorative Elements */}
          <div className="absolute top-0 right-0 w-64 h-64 bg-gradient-to-br from-blue-50/30 to-purple-50/30 rounded-full blur-3xl -z-10"></div>
          <div className="absolute bottom-0 left-0 w-48 h-48 bg-gradient-to-tr from-pink-50/30 to-yellow-50/30 rounded-full blur-3xl -z-10"></div>
          
          <div className="relative space-y-5 sm:space-y-6">
            {/* Breadcrumb */}
            <div className="flex justify-center md:justify-start">
              <Link
                href="/"
                className="inline-flex items-center gap-2 rounded-full border border-gray-200 bg-white/90 backdrop-blur-sm px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.3em] text-gray-600 shadow-sm transition-all hover:border-black hover:text-black hover:shadow-md hover:scale-105"
              >
                <svg
                  aria-hidden="true"
                  viewBox="0 0 20 20"
                  fill="none"
                  xmlns="http://www.w3.org/2000/svg"
                  className="h-3 w-3"
                >
                  <path
                    d="M11.5 5.5 7 10l4.5 4.5"
                    stroke="currentColor"
                    strokeWidth="1.5"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                  />
                </svg>
                <span className="tracking-[0.4em]">Home</span>
              </Link>
            </div>

            {/* Title Section */}
            <div className="text-center md:text-left space-y-3 sm:space-y-4">
              <div className="flex flex-wrap items-center justify-center md:justify-start gap-3">
                <span className="inline-flex items-center px-3 py-1 bg-gradient-to-r from-blue-500 to-purple-500 text-white text-[9px] font-bold uppercase tracking-[0.25em] rounded-full shadow-sm">
                  ⭐ Featured
                </span>
                {currentDesign.category && (
                  <span className="px-3 py-1 bg-black text-white text-[9px] font-bold uppercase tracking-[0.25em] rounded-full">
                    {currentDesign.category}
                  </span>
                )}
              </div>

              <h1 className="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-bold text-gray-900 tracking-tight leading-tight">
                {currentDesign.title}
              </h1>

              {heroDescription && (
                <p className="text-sm sm:text-base md:text-lg text-gray-600 leading-relaxed max-w-3xl mx-auto md:mx-0">
                  {heroDescription}
                </p>
              )}

              {/* Meta Info */}
              <div className="flex flex-wrap items-center justify-center md:justify-start gap-4 sm:gap-6 pt-2">
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
                  </svg>
                  <span className="tracking-wider">{formatDate(currentDesign.created_at)}</span>
                </div>
                <div className="flex items-center gap-2 text-sm text-gray-500">
                  <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
                  </svg>
                  <span className="font-semibold">{currentDesign.likes ?? 0}</span>
                  <span className="tracking-wider">Likes</span>
                </div>
                <ShareLinkButton
                  url={shareUrl}
                  shareData={{ title: currentDesign.title || 'UI Syntax Design', text: currentDesign.description || undefined }}
                  className="inline-flex items-center gap-2 rounded-full border border-gray-300 bg-white/90 backdrop-blur-sm px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.3em] text-gray-600 hover:text-black hover:border-black hover:bg-white transition-all hover:scale-105 shadow-sm"
                  defaultLabel="Share"
                  successLabel="Shared ✓"
                  copiedLabel="Copied ✓"
                />
              </div>
            </div>
          </div>
        </div>

        <div className="grid gap-8 lg:gap-10 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)] w-full overflow-hidden">
          <div className="space-y-6 sm:space-y-8 min-w-0 max-w-full overflow-hidden">
            {descriptionBlocks.length > 0 && (
              <section className="bg-white border border-gray-200 p-6 sm:p-8 shadow-sm rounded-2xl space-y-5 sm:space-y-6 max-w-full overflow-hidden">
                <div className="space-y-1">
                  <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Design Narrative</p>
                  <h2 className="text-2xl font-semibold text-gray-900">Full Context</h2>
                </div>
                <div className="space-y-5 sm:space-y-6">
                  {descriptionBlocks.map((block, index) => (
                    <div key={`${block.title ?? 'block'}-${index}`} className="space-y-2">
                      {block.title && (
                        <p className="text-xs font-semibold uppercase tracking-[0.3em] text-gray-500">
                          {block.title}
                        </p>
                      )}
                      <p className="text-base sm:text-lg text-gray-700 leading-relaxed whitespace-pre-line">
                        {block.body}
                      </p>
                    </div>
                  ))}
                </div>
              </section>
            )}

            <DesignDetailCustomizer
              title={currentDesign.title}
              imageUrl={currentDesign.image_url}
              htmlCode={currentDesign.code}
              reactCode={reactCode}
              colors={currentDesign.colors || undefined}
            />
          </div>

          <aside className="space-y-6 sm:space-y-8 w-full min-w-0 max-w-full overflow-hidden">
            {/* Quick Info Card */}
            <div className="bg-gradient-to-br from-gray-50 to-white border border-gray-200 rounded-2xl p-6 space-y-4 shadow-sm">
              <h3 className="text-xs uppercase tracking-[0.3em] text-gray-400 flex items-center gap-2">
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
                Quick Info
              </h3>
              <dl className="space-y-3 text-sm">
                <div className="flex justify-between items-center py-2">
                  <dt className="text-gray-500 flex items-center gap-2">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
                    </svg>
                    Design ID
                  </dt>
                  <dd className="font-mono text-xs text-gray-700 bg-gray-100 px-2 py-1 rounded">{currentDesign.id.substring(0, 8)}...</dd>
                </div>
                <div className="flex justify-between items-center py-2 border-t border-gray-100">
                  <dt className="text-gray-500 flex items-center gap-2">
                    <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 10l4.553-1.138a1 1 0 01.894 1.737l-3.362 3.028a1 1 0 00-.314.95l.977 4.48a1 1 0 01-1.494 1.06L12 17.882l-4.254 2.236a1 1 0 01-1.494-1.06l.977-4.48a1 1 0 00-.314-.95l-3.362-3.028a1 1 0 01.894-1.737L9 10l1.618-4.664a1 1 0 011.764 0L15 10z" />
                    </svg>
                    Views
                  </dt>
                  <dd className="font-semibold text-gray-900">
                    <ViewCountBadge designId={currentDesign.id} initialViews={initialViewCount} />
                  </dd>
                </div>
                {currentDesign.updated_at !== currentDesign.created_at && (
                  <div className="flex justify-between items-center py-2 border-t border-gray-100">
                    <dt className="text-gray-500 flex items-center gap-2">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                      </svg>
                      Last Updated
                    </dt>
                    <dd className="font-medium text-gray-700">{formatDate(currentDesign.updated_at)}</dd>
                  </div>
                )}
                {currentDesign.code && (
                  <div className="flex justify-between items-center py-2 border-t border-gray-100">
                    <dt className="text-gray-500 flex items-center gap-2">
                      <svg className="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                      </svg>
                      Source Code
                    </dt>
                    <dd className="font-medium text-green-600">Available ✓</dd>
                  </div>
                )}
              </dl>
            </div>

            {currentDesign.prompt && (
              <div className="bg-gradient-to-br from-purple-50 to-pink-50 border border-purple-200 rounded-2xl p-6 shadow-sm">
                <h3 className="text-xs uppercase tracking-[0.3em] text-purple-900 mb-3 flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
                  </svg>
                  AI Prompt
                </h3>
                <p className="text-sm text-purple-900 leading-relaxed">{currentDesign.prompt}</p>
              </div>
            )}

            {sidebarSuggestions.length > 0 && (
              <div className="bg-white border border-gray-100 rounded-2xl p-6 shadow-sm">
                <h3 className="text-xs uppercase tracking-[0.3em] text-gray-400 mb-4 flex items-center gap-2">
                  <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 9l3 3m0 0l-3 3m3-3H8m13 0a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  Browse Next
                </h3>
                <ul className="space-y-3">
                  {sidebarSuggestions.map((item) => (
                    <li key={item.id}>
                      <Link
                        href={`/design/${item.slug}`}
                        className="group flex items-start gap-3 rounded-xl border border-gray-100 p-3 hover:border-black hover:bg-gray-50 transition-all hover:shadow-md"
                      >
                        <div className="relative h-14 w-20 overflow-hidden rounded-lg bg-gray-100 flex-shrink-0">
                          <Image
                            src={item.image_url}
                            alt={item.title}
                            fill
                            className="object-cover"
                            sizes="80px"
                          />
                        </div>
                        <div className="flex-1 min-w-0">
                          <p className="text-sm font-semibold text-gray-900 line-clamp-1 group-hover:text-black">{item.title}</p>
                          <p className="text-xs text-gray-500 mt-1">{item.category || 'General'}</p>
                        </div>
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            <a
              href={currentDesign.image_url}
              target="_blank"
              rel="noopener noreferrer"
              className="flex items-center justify-center gap-2 w-full px-6 py-4 bg-gradient-to-r from-gray-900 to-black text-white text-xs font-bold uppercase tracking-[0.3em] rounded-xl hover:from-black hover:to-gray-900 transition-all shadow-lg hover:shadow-xl hover:scale-105"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
              </svg>
              View Original
            </a>
          </aside>
        </div>

        {relatedDesigns.length > 0 && (
          <section className="mt-12 sm:mt-16 space-y-6 border-t border-gray-200 pt-8 sm:pt-12 overflow-x-hidden">
            <div className="flex flex-wrap items-center justify-between gap-4">
              <div>
                <p className="text-xs uppercase tracking-[0.35em] text-gray-400">Gallery slider</p>
                <h2 className="text-2xl font-semibold text-gray-900 tracking-tight">
                  More {currentDesign.category || 'UI Syntax'} concepts
                </h2>
              </div>
              <Link
                href="/"
                className="text-xs uppercase tracking-[0.3em] text-gray-600 hover:text-black transition-colors"
              >
                Back to gallery
              </Link>
            </div>
            <div className="flex gap-4 sm:gap-6 overflow-x-auto pb-4 sm:pb-6 snap-x snap-mandatory">
              {relatedDesigns.map((item) => (
                <Link
                  key={item.id}
                  href={`/design/${item.slug}`}
                  className="group w-64 sm:w-72 flex-shrink-0 snap-start"
                >
                  <div className="relative aspect-[4/3] overflow-hidden rounded-2xl border border-gray-200 bg-gray-50">
                    <Image
                      src={item.image_url}
                      alt={item.title}
                      fill
                      className="object-cover object-top transition-transform duration-500 group-hover:scale-105"
                      sizes="(max-width: 768px) 80vw, 18rem"
                    />
                  </div>
                  <div className="mt-3 space-y-1">
                    <p className="text-sm font-semibold text-gray-900 line-clamp-1">{item.title}</p>
                    <p className="text-xs text-gray-500 line-clamp-2">{item.description || 'AI design inspiration'}</p>
                  </div>
                </Link>
              ))}
            </div>
          </section>
        )}
      </main>
      <Footer />
    </div>
  );
}
