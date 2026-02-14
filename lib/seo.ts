import type { Metadata } from 'next';

const RAW_SITE_URL = process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com';
export const SITE_URL = RAW_SITE_URL.replace(/\/$/, '');
export const SITE_NAME = 'UI Syntax';

function ensureLeadingSlash(path: string): string {
  if (!path) {
    return '/';
  }
  return path.startsWith('/') ? path : `/${path}`;
}

export function buildCanonicalUrl(path: string = '/'): string {
  const normalizedPath = ensureLeadingSlash(path);
  return `${SITE_URL}${normalizedPath === '/' ? '' : normalizedPath}`;
}

export function buildPageTitle(title: string): string {
  if (!title) {
    return SITE_NAME;
  }
  return title.includes(SITE_NAME) ? title : `${title} · ${SITE_NAME}`;
}

type CreateMetadataOptions = {
  title: string;
  description: string;
  path?: string;
  openGraphType?: 'website' | 'article';
  image?: string | null;
};

export function createPageMetadata({
  title,
  description,
  path = '/',
  openGraphType = 'website',
  image,
}: CreateMetadataOptions): Metadata {
  const canonical = buildCanonicalUrl(path);
  const fullTitle = buildPageTitle(title);

  const ogImages = image ? [image] : undefined;

  return {
    title: fullTitle,
    description,
    alternates: {
      canonical,
    },
    openGraph: {
      title: fullTitle,
      description,
      url: canonical,
      type: openGraphType,
      images: ogImages,
    },
    twitter: {
      card: 'summary_large_image',
      title: fullTitle,
      description,
      images: ogImages,
    },
  };
}
