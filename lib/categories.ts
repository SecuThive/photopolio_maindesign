export type CategoryDefinition = {
  slug: string;
  label: string;
  description: string;
  keywords: string[];
  matchValues?: string[];
};

const CATEGORY_DEFINITIONS: CategoryDefinition[] = [
  {
    slug: 'landing-page',
    label: 'Landing Page',
    description: 'High-converting hero flows, pricing stacks, and launch-ready landing page templates built for SaaS and product teams.',
    keywords: ['landing page', 'hero layout', 'pricing page'],
  },
  {
    slug: 'dashboard',
    label: 'Dashboard',
    description: 'Data-rich admin panels, telemetry views, and operator dashboards optimized for fast decision making.',
    keywords: ['dashboard ui', 'admin panel', 'data visualization'],
  },
  {
    slug: 'e-commerce',
    label: 'E-commerce',
    description: 'Conversion-focused product grids, PDPs, and cart flows covering modern retail and marketplace scenarios.',
    keywords: ['ecommerce ui', 'shopping cart', 'product page'],
  },
  {
    slug: 'portfolio',
    label: 'Portfolio',
    description: 'Case-study storytelling, studio reels, and creative portfolio layouts designed for agencies and individuals.',
    keywords: ['portfolio website', 'case study', 'creative layout'],
  },
  {
    slug: 'blog',
    label: 'Blog',
    description: 'Editorial templates, knowledge base layouts, and long-form storytelling surfaces with strong typography.',
    keywords: ['blog design', 'editorial ui', 'knowledge base'],
  },
  {
    slug: 'components',
    label: 'Components',
    description: 'Reusable micro-interactions, modals, nav bars, and UI components ready to drop into product flows.',
    keywords: ['ui components', 'modal', 'navigation'],
    matchValues: ['Components', 'Component'],
  },
];

const CATEGORY_LOOKUP = new Map<string, CategoryDefinition>(
  CATEGORY_DEFINITIONS.map((definition) => [definition.slug, definition])
);

export function getCategoryDefinition(slug: string): CategoryDefinition | null {
  return CATEGORY_LOOKUP.get(slug) ?? null;
}

export function categoryToSlug(label: string): string {
  const normalized = label.trim().toLowerCase().replace(/[^a-z0-9]+/g, '-');
  return normalized.replace(/^-+|-+$/g, '') || 'category';
}

export const CATEGORY_SLUGS = CATEGORY_DEFINITIONS.map((definition) => definition.slug);
