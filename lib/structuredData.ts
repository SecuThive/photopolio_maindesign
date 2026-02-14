import { SITE_URL, SITE_NAME } from './seo';

export type BlogListItem = {
  slug: string;
  title: string;
  excerpt?: string | null;
  cover_image_url?: string | null;
  published_at?: string | null;
  updated_at?: string | null;
};

export type BlogPostForSchema = BlogListItem & {
  content?: string;
  category?: string | null;
  tags?: string[] | null;
  author?: string | null;
  author_role?: string | null;
};

export function buildBlogItemListSchema(posts: BlogListItem[]) {
  if (!posts.length) {
    return null;
  }

  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: `${SITE_NAME} Blog`,
    itemListElement: posts.map((post, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      url: `${SITE_URL}/blog/${post.slug}`,
      name: post.title,
      description: post.excerpt ?? undefined,
      image: post.cover_image_url ?? undefined,
      datePublished: post.published_at ?? undefined,
      dateModified: post.updated_at ?? post.published_at ?? undefined,
    })),
  };
}

export function buildBlogPostingSchema(post: BlogPostForSchema) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BlogPosting',
    headline: post.title,
    description: post.excerpt ?? undefined,
    image: post.cover_image_url ? [post.cover_image_url] : undefined,
    datePublished: post.published_at ?? undefined,
    dateModified: post.updated_at ?? post.published_at ?? undefined,
    author: {
      '@type': 'Person',
      name: post.author || 'UI Syntax Studio',
      jobTitle: post.author_role || undefined,
    },
    publisher: {
      '@type': 'Organization',
      name: SITE_NAME,
      logo: {
        '@type': 'ImageObject',
        url: `${SITE_URL}/icon.png`,
      },
    },
    mainEntityOfPage: `${SITE_URL}/blog/${post.slug}`,
    articleSection: post.category ?? undefined,
    keywords: post.tags?.join(', ') || undefined,
  };
}

type DesignSchemaInput = {
  title: string;
  description: string | null;
  imageUrl: string;
  slug: string;
  category?: string | null;
  createdAt: string;
  updatedAt: string;
  strategyNotes?: string | null;
  usageNotes?: string | null;
  collectionUrl?: string | null;
  pillarUrl?: string | null;
};

export function buildDesignCreativeWorkSchema(design: DesignSchemaInput) {
  const canonical = `${SITE_URL}/design/${design.slug}`;
  const keywords = [design.category, design.strategyNotes, design.usageNotes]
    .filter(Boolean)
    .map((value) => value?.replace(/\n/g, ' ').trim())
    .filter(Boolean);
  const hierarchy = [design.collectionUrl, design.pillarUrl].filter(Boolean) as string[];

  return {
    '@context': 'https://schema.org',
    '@type': 'CreativeWork',
    name: design.title,
    description: design.description ?? undefined,
    url: canonical,
    image: design.imageUrl,
    datePublished: design.createdAt,
    dateModified: design.updatedAt,
    inLanguage: 'en-US',
    genre: design.category ?? undefined,
    keywords: keywords.length ? keywords.join(', ') : undefined,
    isPartOf: hierarchy.length ? hierarchy : undefined,
    author: {
      '@type': 'Organization',
      name: SITE_NAME,
      url: SITE_URL,
    },
  };
}

type CollectionItem = {
  slug: string;
  title: string;
  description?: string | null;
};

export function buildCollectionItemListSchema(collectionTitle: string, slug: string, items: CollectionItem[]) {
  if (!items.length) {
    return null;
  }

  return {
    '@context': 'https://schema.org',
    '@type': 'ItemList',
    name: `${collectionTitle} · UI Syntax`,
    url: `${SITE_URL}/collections/${slug}`,
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      url: `${SITE_URL}/design/${item.slug}`,
      name: item.title,
      description: item.description ?? undefined,
    })),
  };
}

export function buildFaqSchema(title: string, faqs: Array<{ question: string; answer: string }>) {
  if (!faqs.length) {
    return null;
  }

  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    name: `${title} FAQ`,
    mainEntity: faqs.map((faq) => ({
      '@type': 'Question',
      name: faq.question,
      acceptedAnswer: {
        '@type': 'Answer',
        text: faq.answer,
      },
    })),
  };
}
