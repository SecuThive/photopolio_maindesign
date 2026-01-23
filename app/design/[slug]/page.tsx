import { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import ShareLinkButton from '@/components/ShareLinkButton';
import DesignPreview from '@/components/DesignPreview';
import CodeBlock from '@/components/CodeBlock';
import { supabaseServer } from '@/lib/supabase/server';
import { extractDesignIdFromSlug, withDesignSlug, withDesignSlugs } from '@/lib/slug';
import { Design, DesignWithSlug } from '@/types/database';

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://www.ui-syntax.com').replace(/\/$/, '');

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

  if (!design) {
    return {
      title: 'Design not found · UI Syntax',
      description: 'The requested design could not be located.',
      robots: { index: false, follow: false },
    };
  }

  const description = design.description || 'AI-generated design inspiration from UI Syntax.';
  const canonical = `${SITE_URL}/design/${design.slug}`;

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

export default async function DesignDetailPage({ params }: PageProps) {
  const design = await fetchDesignBySlug(params.slug);

  if (!design) {
    notFound();
  }

  const currentDesign = design;
  const relatedDesigns = await fetchRelatedDesigns(currentDesign);
  const sidebarSuggestions = relatedDesigns.slice(0, 3);
  const shareUrl = `${SITE_URL}/design/${currentDesign.slug}`;

  return (
    <div className="min-h-screen bg-luxury-white">
      <Header selectedCategory={currentDesign.category} />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-12">
        <div className="space-y-4 text-center md:text-left">
          <div className="flex justify-center md:justify-start">
            <Link
              href="/"
              className="inline-flex items-center gap-3 rounded-full border border-gray-200 bg-white/80 px-5 py-2 text-[11px] font-semibold uppercase tracking-[0.35em] text-gray-600 shadow-sm transition-all hover:border-black hover:text-black hover:shadow"
            >
              <span className="flex h-6 w-6 items-center justify-center rounded-full border border-gray-300 bg-gray-50 text-[0.65rem] tracking-[0.1em] text-gray-600">
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
              </span>
              <span className="tracking-[0.5em]">Home</span>
            </Link>
          </div>
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Featured Design</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 tracking-tight">{currentDesign.title}</h1>
          <p className="text-sm uppercase tracking-[0.35em] text-gray-400">{formatDate(currentDesign.created_at)}</p>
          <div className="flex flex-wrap items-center justify-center md:justify-start gap-4 text-sm text-gray-500">
            {currentDesign.category && (
              <span className="px-4 py-1 bg-black text-white text-xs uppercase tracking-widest">{currentDesign.category}</span>
            )}
            <ShareLinkButton
              url={shareUrl}
              shareData={{ title: currentDesign.title || 'UI Syntax Design', text: currentDesign.description || undefined }}
              className="rounded-full border border-gray-300 px-4 py-2 text-xs tracking-widest uppercase text-gray-600 hover:text-black hover:border-black transition-colors"
              defaultLabel="Share"
              successLabel="Shared successfully"
              copiedLabel="Link copied"
            />
          </div>
        </div>

        <div className="grid gap-10 lg:grid-cols-[minmax(0,2fr)_minmax(0,1fr)]">
          <div className="space-y-8">
            <DesignPreview 
              imageUrl={currentDesign.image_url}
              title={currentDesign.title}
              colors={currentDesign.colors || undefined}
            />

            {currentDesign.description && (
              <section className="bg-white border border-gray-200 p-8 shadow-sm">
                <h2 className="text-xs uppercase tracking-[0.3em] text-gray-400 mb-4">Overview</h2>
                <p className="text-lg text-gray-700 leading-relaxed">{currentDesign.description}</p>
              </section>
            )}

            {currentDesign.code && (
              <CodeBlock code={currentDesign.code} />
            )}
          </div>

          <aside className="space-y-8 w-full overflow-hidden">
            <div className="bg-white border border-gray-100 p-6 space-y-4">
              <h3 className="text-xs uppercase tracking-[0.3em] text-gray-400">Details</h3>
              <dl className="space-y-3 text-sm text-gray-600">
                <div className="flex justify-between border-b border-gray-100 pb-3">
                  <dt className="font-light">Category</dt>
                  <dd className="font-medium">{currentDesign.category || 'Uncategorized'}</dd>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-3">
                  <dt className="font-light">Created</dt>
                  <dd className="font-medium">{formatDate(currentDesign.created_at)}</dd>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-3">
                  <dt className="font-light">Updated</dt>
                  <dd className="font-medium">{formatDate(currentDesign.updated_at)}</dd>
                </div>
                <div className="flex justify-between border-b border-gray-100 pb-3">
                  <dt className="font-light">Likes</dt>
                  <dd className="font-medium">{currentDesign.likes ?? 0}</dd>
                </div>
                <div className="flex justify-between">
                  <dt className="font-light">Design ID</dt>
                  <dd className="font-mono text-xs text-gray-500">{currentDesign.id}</dd>
                </div>
              </dl>
            </div>

            {currentDesign.prompt && (
              <div className="bg-gray-50 border border-gray-200 p-6">
                <h3 className="text-xs uppercase tracking-[0.3em] text-gray-400 mb-3">AI Prompt</h3>
                <p className="text-sm text-gray-600 font-mono leading-relaxed whitespace-pre-wrap">{currentDesign.prompt}</p>
              </div>
            )}

            {sidebarSuggestions.length > 0 && (
              <div className="bg-white border border-gray-100 p-6">
                <h3 className="text-xs uppercase tracking-[0.3em] text-gray-400 mb-4">Browse next</h3>
                <ul className="space-y-3">
                  {sidebarSuggestions.map((item) => (
                    <li key={item.id}>
                      <Link
                        href={`/design/${item.slug}`}
                        className="group flex items-start gap-3 rounded-lg border border-gray-100 p-3 hover:border-black hover:bg-gray-50 transition-colors"
                      >
                        <div className="relative h-12 w-16 overflow-hidden rounded bg-gray-100">
                          <Image
                            src={item.image_url}
                            alt={item.title}
                            fill
                            className="object-cover"
                            sizes="64px"
                          />
                        </div>
                        <div className="flex-1">
                          <p className="text-sm font-medium text-gray-900 line-clamp-1 group-hover:text-black">{item.title}</p>
                          <p className="text-xs text-gray-500 line-clamp-1">{item.category || 'General'}</p>
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
              className="block text-center w-full px-8 py-4 bg-black text-white text-xs uppercase tracking-[0.3em] hover:bg-gray-900 transition-colors"
            >
              View Original
            </a>
          </aside>
        </div>

        {relatedDesigns.length > 0 && (
          <section className="mt-16 space-y-6 border-t border-gray-200 pt-12">
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
            <div className="flex gap-6 overflow-x-auto pb-4 snap-x snap-mandatory">
              {relatedDesigns.map((item) => (
                <Link
                  key={item.id}
                  href={`/design/${item.slug}`}
                  className="group w-72 flex-shrink-0 snap-start"
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
