export const THIN_BLOG_POST_SLUGS = [
  'community-welcome-post',
  'showcase-your-latest-build',
  'how-to-ask-better-questions',
] as const;

const thinBlogSlugSet = new Set<string>(THIN_BLOG_POST_SLUGS);

export function isThinBlogSlug(slug: string): boolean {
  return thinBlogSlugSet.has(slug);
}
