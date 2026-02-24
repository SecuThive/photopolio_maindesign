import { NextResponse } from 'next/server';
import { supabaseServer } from '@/lib/supabase/server';
import { createDesignSlug } from '@/lib/slug';
import { pillarTopics } from '@/lib/pillars';
import { isThinBlogSlug } from '@/lib/noindexList';
import type { Database } from '@/types/database';

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');
const ENABLE_GROWTH_SAFE_SEO_FIXES = process.env.ENABLE_GROWTH_SAFE_SEO_FIXES === 'true';
const STATIC_PATHS = ['/', '/blog', '/about', '/faq', '/contact', '/privacy-policy', '/terms', '/playbooks', '/collections', '/code-match'];
const COLLECTION_SLUGS = ['best-saas-landing-pages', 'minimalist-dashboards'];
type DesignSitemapRow = Pick<Database['public']['Tables']['designs']['Row'], 'id' | 'title' | 'slug' | 'updated_at'>;
type BlogSitemapRow = Pick<Database['public']['Tables']['posts']['Row'], 'slug' | 'published_at'>;

function xmlEscape(value: string): string {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&apos;');
}

function toAbsolute(path: string): string {
  if (path === '/') {
    return SITE_URL;
  }
  return `${SITE_URL}${path.startsWith('/') ? path : `/${path}`}`;
}

function buildUrlEntry(url: string, lastModified?: string): string {
  const safeUrl = xmlEscape(url);
  const safeLastmod = lastModified ? `<lastmod>${xmlEscape(lastModified)}</lastmod>` : '';
  return `<url><loc>${safeUrl}</loc>${safeLastmod}</url>`;
}

function buildSitemapXml(entries: string[]): string {
  return `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${entries.join('\n')}\n</urlset>`;
}

export async function GET() {
  try {
    const [designRes, postRes] = await Promise.all([
      supabaseServer
        .from('designs')
        .select('id, title, slug, updated_at')
        .eq('status', 'published')
        .order('updated_at', { ascending: false }),
      supabaseServer
        .from('posts')
        .select('slug, published_at')
        .eq('status', 'published')
        .order('published_at', { ascending: false }),
    ]);

    const nowIso = new Date().toISOString();
    const staticEntries = STATIC_PATHS.map((path) => buildUrlEntry(toAbsolute(path), nowIso));
    const collectionEntries = COLLECTION_SLUGS.map((slug) => buildUrlEntry(toAbsolute(`/collections/${slug}`), nowIso));
    const playbookEntries = pillarTopics.map((topic) => buildUrlEntry(toAbsolute(`/playbooks/${topic.slug}`), nowIso));

    const designRows = (designRes.data ?? []) as DesignSitemapRow[];
    const postRows = (postRes.data ?? []) as BlogSitemapRow[];

    const designEntries = designRows.map((design) =>
      buildUrlEntry(
        toAbsolute(`/design/${design.slug || createDesignSlug(design.title, design.id)}`),
        design.updated_at ? new Date(design.updated_at).toISOString() : nowIso
      )
    );

    const blogEntries = postRows
      .filter((post) => (ENABLE_GROWTH_SAFE_SEO_FIXES ? !isThinBlogSlug(post.slug) : true))
      .map((post) =>
        buildUrlEntry(
          toAbsolute(`/blog/${post.slug}`),
          post.published_at ? new Date(post.published_at).toISOString() : nowIso
        )
      );

    const xml = buildSitemapXml([
      ...staticEntries,
      ...collectionEntries,
      ...playbookEntries,
      ...blogEntries,
      ...designEntries,
    ]);

    return new NextResponse(xml, {
      status: 200,
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=0, must-revalidate',
      },
    });
  } catch (error) {
    console.error('sitemap.xml route error', error);
    const fallback = buildSitemapXml([buildUrlEntry(SITE_URL, new Date().toISOString())]);
    return new NextResponse(fallback, {
      status: 200,
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=0, must-revalidate',
      },
    });
  }
}
