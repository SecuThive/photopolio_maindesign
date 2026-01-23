import { Design, DesignWithSlug } from '@/types/database';

const MAX_SLUG_LENGTH = 80;
const DEFAULT_SLUG = 'design';
const UUID_REGEX = /[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export function createDesignSlug(title: string | null | undefined, id: string): string {
  const normalizedTitle = (title || DEFAULT_SLUG)
    .toLowerCase()
    .replace(/&/g, ' and ')
    .replace(/[^a-z0-9\s-]/g, '')
    .replace(/\s+/g, '-')
    .replace(/-+/g, '-')
    .replace(/^-|-$/g, '')
    .slice(0, MAX_SLUG_LENGTH)
    .replace(/-+$/g, '') || DEFAULT_SLUG;

  return `${normalizedTitle}-${id}`;
}

export function extractDesignIdFromSlug(slug: string): string | null {
  const parts = slug.split('-');
  const candidate = parts.slice(-5).join('-');
  if (UUID_REGEX.test(candidate)) {
    return candidate.toLowerCase();
  }

  const fallback = parts[parts.length - 1];
  return UUID_REGEX.test(fallback) ? fallback.toLowerCase() : null;
}

export function withDesignSlug(design: Design): DesignWithSlug {
  return {
    ...design,
    slug: createDesignSlug(design.title, design.id),
  };
}

export function withDesignSlugs(designs: Design[]): DesignWithSlug[] {
  return designs.map(withDesignSlug);
}
