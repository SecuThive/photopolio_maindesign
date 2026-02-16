import { SITE_URL, SITE_NAME } from './seo';

/**
 * FAQ Schema for Rich Snippets
 * Displays FAQ accordion in Google search results - increases CTR by 30-35%
 */
export function buildFAQSchema(faqs: { question: string; answer: string }[]) {
  return {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
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

/**
 * HowTo Schema for step-by-step guides
 * Shows visual steps in search results - great for code tutorials
 */
export function buildHowToSchema(params: {
  name: string;
  description: string;
  totalTime?: string; // ISO 8601 duration format (e.g., "PT10M" for 10 minutes)
  steps: Array<{
    name: string;
    text: string;
    image?: string;
    url?: string;
  }>;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'HowTo',
    name: params.name,
    description: params.description,
    totalTime: params.totalTime,
    step: params.steps.map((step, index) => ({
      '@type': 'HowToStep',
      position: index + 1,
      name: step.name,
      text: step.text,
      image: step.image,
      url: step.url,
    })),
  };
}

/**
 * AggregateRating Schema for product/service ratings
 * Shows star ratings in search results - increases CTR by 20-25%
 */
export function buildAggregateRatingSchema(params: {
  itemName: string;
  ratingValue: number; // Average rating (e.g., 4.8)
  ratingCount: number; // Total number of ratings
  bestRating?: number; // Default 5
  worstRating?: number; // Default 1
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Product',
    name: params.itemName,
    aggregateRating: {
      '@type': 'AggregateRating',
      ratingValue: params.ratingValue,
      ratingCount: params.ratingCount,
      bestRating: params.bestRating || 5,
      worstRating: params.worstRating || 1,
    },
  };
}

/**
 * WebSite SearchAction Schema
 * Enables site search box in Google results
 */
export function buildWebSiteSearchSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    url: SITE_URL,
    name: SITE_NAME,
    potentialAction: {
      '@type': 'SearchAction',
      target: {
        '@type': 'EntryPoint',
        urlTemplate: `${SITE_URL}/?search={search_term_string}`,
      },
      'query-input': 'required name=search_term_string',
    },
  };
}

/**
 * Organization Schema with SameAs (social profiles)
 * Builds brand authority in knowledge panel
 */
export function buildOrganizationSchema(params: {
  name: string;
  url: string;
  logo: string;
  description: string;
  email?: string;
  socialProfiles?: string[];
  foundingDate?: string;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: params.name,
    url: params.url,
    logo: params.logo,
    description: params.description,
    email: params.email,
    sameAs: params.socialProfiles || [],
    foundingDate: params.foundingDate,
  };
}

/**
 * Breadcrumb Schema
 * Shows breadcrumb trail in search results
 */
export function buildBreadcrumbSchema(items: Array<{ name: string; url: string }>) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, index) => ({
      '@type': 'ListItem',
      position: index + 1,
      name: item.name,
      item: item.url,
    })),
  };
}

/**
 * VideoObject Schema
 * For video tutorials showing design usage
 */
export function buildVideoSchema(params: {
  name: string;
  description: string;
  thumbnailUrl: string;
  uploadDate: string; // ISO 8601 format
  duration?: string; // ISO 8601 duration (e.g., "PT5M30S" for 5:30)
  contentUrl?: string;
  embedUrl?: string;
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'VideoObject',
    name: params.name,
    description: params.description,
    thumbnailUrl: params.thumbnailUrl,
    uploadDate: params.uploadDate,
    duration: params.duration,
    contentUrl: params.contentUrl,
    embedUrl: params.embedUrl,
  };
}

/**
 * SoftwareApplication Schema
 * For tools like Code Match
 */
export function buildSoftwareApplicationSchema(params: {
  name: string;
  description: string;
  url: string;
  applicationCategory: string; // e.g., "DeveloperApplication"
  operatingSystem?: string; // e.g., "Web Browser"
  offers?: {
    price: string; // "0" for free
    priceCurrency: string; // "USD"
  };
}) {
  return {
    '@context': 'https://schema.org',
    '@type': 'SoftwareApplication',
    name: params.name,
    description: params.description,
    url: params.url,
    applicationCategory: params.applicationCategory,
    operatingSystem: params.operatingSystem || 'Web Browser',
    offers: params.offers
      ? {
          '@type': 'Offer',
          price: params.offers.price,
          priceCurrency: params.offers.priceCurrency,
        }
      : undefined,
  };
}
