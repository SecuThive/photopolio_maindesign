export type CollectionFAQ = {
  question: string;
  answer: string;
};

export type CollectionConfig = {
  slug: string;
  title: string;
  heroEyebrow: string;
  heroHeading: string;
  heroSummary: string;
  description: string[];
  highlightPoints: string[];
  bestPractices: Array<{ title: string; description: string }>;
  checklist: string[];
  faqs: CollectionFAQ[];
  pillar: { title: string; href: string; summary: string };
  supabaseCategory: string;
  metaDescription: string;
};

export const collectionConfigs: CollectionConfig[] = [
  {
    slug: 'best-saas-landing-pages',
    title: 'Best SaaS Landing Pages',
    heroEyebrow: 'Collection 01',
    heroHeading: 'Conversion-grade SaaS landing patterns',
    heroSummary:
      'A reference set built so B2B SaaS teams can tighten value props, social proof, and CTA funnels within a single sprint.',
    description: [
      'A SaaS landing page must deliver “problem → promise → action” within five seconds. This collection reverse-engineers the messaging spine that high-growth teams such as Stripe, Linear, and Vercel rely on so you can rebuild hero, pricing, and testimonial blocks with confidence.',
      'Each design considers value proposition architecture, demo booking flow, and onboarding friction at the same time. Every layout has been tested against Core Web Vitals so you understand performance thresholds alongside the copy tone.',
    ],
    highlightPoints: [
      'Hero and social proof modules share the same scroll depth to earn trust immediately.',
      'CTA ladders move visitors from Free Trial → Docs → Pricing without friction.',
      'Tone guide satisfies both developer-friendly copy and enterprise buyer expectations.',
    ],
    bestPractices: [
      {
        title: 'Value Prop Stack',
        description:
          'Combine a role-based headline with a measurable outcome, and use the subhead to describe how you achieve it. Example: “Platform teams launch secure APIs 40% faster.”',
      },
      {
        title: 'Social Proof Orbit',
        description:
          'List segments and results next to each logo so generative search engines understand the context. Surface G2 and Capterra badges with the `ImageObject` schema.',
      },
      {
        title: 'CTA Ladder',
        description:
          'Separate the primary CTA (Free Trial) from the secondary CTA (See Docs) and add a risk-reversal sentence beneath each button to nudge action.',
      },
      {
        title: 'Pricing Narrative',
        description:
          'Explain pricing tiers through team size or usage scenarios instead of feature grids, and include a response-time SLA inside the Contact Sales block.',
      },
    ],
    checklist: [
      'Keep the hero headline under 12 words and include one KPI.',
      'Place at least three trust signals (logo, metric, quote) above the fold.',
      'Add a one-sentence risk-reversal line next to every CTA button.',
      'Use a 1200px WebP product visual with a skeleton placeholder to keep LCP under two seconds.',
      'Expose a demo booking calendar or sales email inside the footer CTA.',
    ],
    faqs: [
      {
        question: 'Who should use this collection?',
        answer:
          'It was designed for B2B SaaS PMs, founding designers, and growth engineers who need a shared messaging frame. Pre–Series A teams can clone it immediately because hero copy and CTA microcopy are included.',
      },
      {
        question: 'What visual style does it follow?',
        answer:
          'It borrows from U.S. SaaS brands that favor neutral palettes, glassmorphism, and bento grid patterns. Each design ships with typography and spacing scales so you can lift only what you need.',
      },
      {
        question: 'Does it account for SEO and Core Web Vitals?',
        answer:
          'Yes. Every section opens with a declarative sentence, and we include image optimization plus font preconnect guidance so LCP and CLS stay within budget.',
      },
      {
        question: 'Can I ship these designs to production?',
        answer:
          'They include HTML/React code so you can port them to production. Update brand tokens and copy before launch.',
      },
    ],
    pillar: {
      title: 'SaaS Landing Page UX Strategy',
      href: '/playbooks/saas-landing-page-ux',
      summary: 'A playbook that unifies value props, social proof, and the CTA ladder in one place.',
    },
    supabaseCategory: 'Landing Page',
    metaDescription:
      'A best-of SaaS landing page collection covering value props, social proof, CTA strategy, and Core Web Vitals guardrails.',
  },
  {
    slug: 'minimalist-dashboards',
    title: 'Minimalist Dashboards',
    heroEyebrow: 'Collection 02',
    heroHeading: 'Signal-first dashboard systems',
    heroSummary:
      'Dashboard references that balance data density, dark mode, and micro-interactions for internal tools and customer-facing admin UIs alike.',
    description: [
      'A dashboard must act like a control tower that surfaces “current state → delta → next action” at a glance. This collection recreates the cards, tables, and subpanels proven inside dense interfaces such as Linear, Vercel, and GitHub Copilot.',
      'Each design bakes in an 8pt spacing grid, semantic color tokens, and dark mode contrast ratios so you can drop it into any Figma file or codebase and keep the same fidelity.',
    ],
    highlightPoints: [
      'Information hierarchy follows metric → trend → table to standardize scan patterns.',
      'Power-user staples such as density toggles, focus mode, and contextual toolbars are ready-made.',
      'Dark mode contrast and accessibility guidance reduce fatigue during long sessions.',
    ],
    bestPractices: [
      {
        title: 'Information Hierarchy',
        description:
          'Show three KPI cards or fewer above the fold and include a delta badge on each so trends are obvious immediately.',
      },
      {
        title: 'Density Controls',
        description:
          'Pair a compact-mode toggle with zebra-less tables to reduce perceived complexity while keeping the data volume.',
      },
      {
        title: 'Dark Mode Tokens',
        description:
          'Hold a neutral contrast ratio of at least 4.5:1 and manage accent colors through semantic tokens.',
      },
      {
        title: 'Micro Interactions',
        description:
          'Keep row hover, inline edits, and command palette interactions under 16 ms of latency to stabilize INP.',
      },
    ],
    checklist: [
      'Stick to an 8pt spacing grid and limit breakpoints to three or fewer.',
      'Fix sidebar width near 264px to preserve muscle memory.',
      'Make table headers sticky and use subtle dividers instead of zebra stripes.',
      'Meet a 4.5:1 contrast ratio in dark mode and document semantic tokens.',
      'Measure micro-interaction latency with Web Vitals and keep it under 16 ms.',
    ],
    faqs: [
      {
        question: 'Who is this layout for?',
        answer:
          'Product analytics PMs, design system teams, and DevOps tool builders can apply it to internal or external dashboards immediately.',
      },
      {
        question: 'Is it compatible with data viz libraries?',
        answer:
          'Cards and tables are sized to align with Chart.js, Recharts, and D3 wrappers commonly used in React or Vue.',
      },
      {
        question: 'How do you maintain accessibility?',
        answer:
          'Every state change pairs color, icon, and text, and focus rings stay visible so keyboard users never lose context.',
      },
      {
        question: 'Does it include performance guidance?',
        answer:
          'Yes. Inline notes cover lazy loading, skeletons, and data virtualization so Core Web Vitals stay healthy.',
      },
    ],
    pillar: {
      title: 'Dashboard UX Design Principles',
      href: '/playbooks/dashboard-ux-principles',
      summary: 'A playbook covering information hierarchy, density controls, and dark mode tokens in one system.',
    },
    supabaseCategory: 'Dashboard',
    metaDescription:
      'Minimalist dashboard collection featuring signal-first cards, density controls, and dark mode token guidance.',
  },
];

export function getCollectionConfig(slug: string) {
  return collectionConfigs.find((config) => config.slug === slug);
}
