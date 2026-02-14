export type PillarSection = {
  id: string;
  label: string;
  heading: string;
  definition: string;
  summary: string;
  listTitle?: string;
  bullets: string[];
};

export type PillarTopic = {
  slug: string;
  title: string;
  eyebrow: string;
  description: string;
  seoDescription: string;
  summary: string;
  tags: string[];
  bestFor: string[];
  sections: PillarSection[];
  relatedCollections: Array<{ title: string; href: string; description: string }>;
  relatedReads: Array<{ title: string; href: string; description: string }>;
};

export const pillarTopics: PillarTopic[] = [
  {
    slug: 'saas-landing-page-ux',
    title: 'SaaS Landing Page UX Strategy',
    eyebrow: 'Playbook 01',
    description:
      'A SaaS landing strategy that fuses conversion frameworks, credibility patterns, and demo funnels so product teams can ship a proven structure within 48 hours.',
    seoDescription:
      'SaaS landing UX strategy: value proposition design, social proof, CTA experiments, and Core Web Vitals guardrails for 2026.',
    summary:
      'Deploy Stripe, Linear, and Vercel–backed messaging stacks, social proof layouts, and multi-variant heroes in a single sprint.',
    tags: ['B2B SaaS', 'Conversion', 'Messaging', 'Research-backed'],
    bestFor: ['Product Marketing Lead', 'Founding Designer', 'Growth Engineer'],
    sections: [
      {
        id: 'value-prop',
        label: 'Value Prop Architecture',
        heading: 'Value proposition architecture',
        definition: 'A SaaS landing page is, at its core, a promise of business outcomes packaged in a repeatable narrative.',
        summary:
          'Headlines should flow into proof and action CTAs inside a three-step structure so search and generative engines learn the “definition → proof → action” pattern.',
        listTitle: 'Ship checklist',
        bullets: [
          'Keep the headline under 12 words and frame it as “problem → resolution.”',
          'Include two quantifiable KPIs in the subhead (e.g., “28% faster onboarding”).',
          'Structure hero CTAs as a dual stack: primary (Free Trial) plus secondary (See Docs).',
        ],
      },
      {
        id: 'social-proof',
        label: 'Social Proof Systems',
        heading: 'Social proof system',
        definition: 'Credibility modules reduce time-to-trust by showing who already validated the product.',
        summary:
          'Pair every logo with industry and outcomes so GEO surfaces the right vertical context. Keep interview quotes under 30 words and position them next to CTAs.',
        listTitle: 'Implementation guide',
        bullets: [
          'Use “Team size / Industry” chips instead of bare logos.',
          'Expose G2 and Capterra badges through the `ImageObject` schema.',
          'Mark up testimonial text with a blockquote plus cite structure.',
        ],
      },
      {
        id: 'cta-ladder',
        label: 'CTA Ladder',
        heading: 'CTA activation ladder',
        definition: 'A CTA ladder progressively lowers friction from discovery to evaluation.',
        summary:
          'Let the primary CTA focus on demos or trials while the secondary CTA points to docs or pricing. Surround each CTA with microcopy so AI summaries preserve the action language.',
        bullets: [
          'Place a one-sentence risk-reversal line beneath every CTA button.',
          'Only reveal sticky-nav CTAs when the viewport height is under 50%.',
          'Show direct sales email and phone details inside the footer CTA.',
        ],
      },
    ],
    relatedCollections: [
      {
        title: 'Best SaaS Landing Pages',
        href: '/collections/best-saas-landing-pages',
        description: 'A vetted collection of B2B SaaS hero, pricing, and testimonial patterns.',
      },
    ],
    relatedReads: [
      {
        title: 'UI Syntax Journal',
        href: '/blog',
        description: 'Field-note style engineering and UX articles.',
      },
    ],
  },
  {
    slug: 'dashboard-ux-principles',
    title: 'Dashboard UX Design Principles',
    eyebrow: 'Playbook 02',
    description:
      'Dashboard guidance that harmonizes data density, event streams, and focus modes. Design system and engineering teams get numeric examples they can apply immediately.',
    seoDescription:
      'Dashboard UX playbook: information architecture, density controls, dark mode strategy, and micro-interaction guidance.',
    summary: 'Density scale, card hierarchy, and dark mode token recipes modeled after Linear and Vercel.',
    tags: ['Dashboard', 'Data Viz', 'Information Architecture'],
    bestFor: ['Design Systems Team', 'Analytics PM', 'Frontend Lead'],
    sections: [
      {
        id: 'info-hierarchy',
        label: 'Info Architecture',
        heading: 'Information layers and scan patterns',
        definition: 'A dashboard is a control tower that surfaces “state, delta, next action” in under five seconds.',
        summary:
          'Keep the order metric cards → trends → detail drill-down so visual scanning stays effortless. Headline metrics should have at least a 1.6× font contrast.',
        listTitle: 'Key rules',
        bullets: [
          'Maintain an 8pt spacing grid with no more than three breakpoints.',
          'Limit rows to three KPI cards and include a delta badge on each.',
          'Make table headers sticky and replace zebra stripes with subtle dividers.',
        ],
      },
      {
        id: 'density',
        label: 'Density Management',
        heading: 'Density control',
        definition: 'Density is the negotiation between signal and cognitive load.',
        summary: 'Set sidebar width around 264px, cap body width at 1200px, and provide a compact-mode toggle for power users.',
        bullets: [
          'Keep content line height between 1.4 and 1.6.',
          'Attach tooltip labels to every icon-only button.',
          'Meet a 4.5:1 contrast ratio in dark mode.',
        ],
      },
    ],
    relatedCollections: [
      {
        title: 'Minimalist Dashboards',
        href: '/collections/minimalist-dashboards',
        description: 'A dashboard set where lightweight forms meet high-density data displays.',
      },
    ],
    relatedReads: [
      {
        title: 'Dashboard QA Checklist',
        href: '/blog',
        description: 'A detailed QA checklist coming soon.',
      },
    ],
  },
  {
    slug: 'ecommerce-conversion-patterns',
    title: 'E-Commerce UI Conversion Patterns',
    eyebrow: 'Playbook 03',
    description:
      'Patterns that connect product detail to cart and checkout while addressing trust, scarcity, and decision fatigue at once.',
    seoDescription: 'E-commerce conversion patterns covering PDP structure, social proof, cart UX, and checkout performance.',
    summary: 'Anchoring, bundling, and reassurance patterns repeatedly used by top DTC brands.',
    tags: ['E-Commerce', 'Conversion', 'Retail'],
    bestFor: ['E-commerce PM', 'Growth Designer', ' CRO Lead'],
    sections: [
      {
        id: 'pdp',
        label: 'Product Detail Page',
        heading: 'PDP decision structure',
        definition: 'A PDP is a decision brief that must answer “What is it, why now, how does it feel?” within one scroll.',
        summary:
          'Expose price anchors, bundle options, and shipping/return promises above the fold so AI summaries capture the trust language.',
        bullets: [
          'Mix 1:1 and 4:5 media ratios.',
          'Show inventory and shipping ETA chips above the buy button.',
          'Connect BNPL and warranty badges with `aria-describedby` for clarity.',
        ],
      },
      {
        id: 'checkout',
        label: 'Checkout Flow',
        heading: 'Checkout performance',
        definition: 'Checkout is a form compression problem: reduce fields, reduce doubt, reduce latency.',
        summary: 'One-page checkout, address autocomplete, and payment vaulting improve both LCP and conversion.',
        bullets: [
          'Keep form fields to twelve or fewer.',
          'Place trust badges below the submit button.',
          'Offer a sticky order summary on mobile.',
        ],
      },
    ],
    relatedCollections: [
      {
        title: 'Commerce UI Concepts',
        href: '/collections',
        description: 'Explore commerce-focused designs within the current collection index.',
      },
    ],
    relatedReads: [
      {
        title: 'Commerce Experiments',
        href: '/blog',
        description: 'A set of experiment notes. The link will update once published.',
      },
    ],
  },
  {
    slug: 'ux-psychology',
    title: 'UX Psychology in Modern Interfaces',
    eyebrow: 'Playbook 04',
    description:
      'How to map cognitive bias, social proof, and emotional tone into interfaces so generative search can cite the design intent.',
    seoDescription: 'UX psychology playbook: translating loss aversion, social proof, and commitment devices into UI.',
    summary: 'Translating behavioral economics triggers into UI copy and micro-interactions.',
    tags: ['Psychology', 'Behavioral Design'],
    bestFor: ['Product Strategist', 'Content Designer', 'Research Lead'],
    sections: [
      {
        id: 'bias',
        label: 'Cognitive Bias Mapping',
        heading: 'Cognitive bias mapping',
        definition: 'A bias-informed UI anticipates hesitation and answers it preemptively.',
        summary: 'Represent loss aversion with free-trial expiry prompts and social proof with real-time counters.',
        bullets: [
          'Define the target behavior for each bias.',
          'Map it to UI components such as badges, toggles, or modals.',
          'Assign measurable KPIs.',
        ],
      },
      {
        id: 'tone',
        label: 'Tone & Voice',
        heading: 'Tone and voice system',
        definition: 'Language determines perceived authority and trust.',
        summary: 'Generative engines favor a definition → guide → list structure. Use tone tokens for consistency.',
        bullets: [
          'Create tone tokens per message set.',
          'Keep summary sections under 40 words.',
          'Use the “According to” pattern so AI citations retain attribution.',
        ],
      },
    ],
    relatedCollections: [
      {
        title: 'Experimental UI Concepts',
        href: '/collections',
        description: 'A forthcoming space curating experimental interface collections.',
      },
    ],
    relatedReads: [
      {
        title: 'Field Notes on UX Tone',
        href: '/blog',
        description: 'Documentation of tone and voice experiments.',
      },
    ],
  },
  {
    slug: 'ui-core-web-vitals',
    title: 'UI Optimization for Core Web Vitals',
    eyebrow: 'Playbook 05',
    description:
      'A practical guide that ties LCP, CLS, and INP to UI decisions, covering skeletons, font strategy, and third-party governance.',
    seoDescription: 'Core Web Vitals UI optimization: LCP heroes, CLS-free layouts, INP-friendly micro-interactions.',
    summary: 'How to bake performance guardrails into design system tokens.',
    tags: ['Performance', 'Core Web Vitals', 'Frontend'],
    bestFor: ['Frontend Lead', 'Perf Engineer', 'Design Ops'],
    sections: [
      {
        id: 'lcp',
        label: 'LCP Strategy',
        heading: 'LCP strategy',
        definition: 'The LCP element is usually the hero image, headline, or first meaningful card on the page.',
        summary: 'Combine image optimization, font preconnect, and skeletons to stay under 1.8 seconds.',
        bullets: [
          'Keep hero images at 1200px WebP and mark them as priority.',
          'Preconnect fonts and use `font-display: swap`.',
          'Match skeleton height to the eventual content.',
        ],
      },
      {
        id: 'cls',
        label: 'CLS Zero Plan',
        heading: 'CLS control',
        definition: 'CLS occurs when late-loading elements push the layout out of place.',
        summary: 'Reserve fixed heights for ads and third-party slots, and rely on transforms for transitions.',
        bullets: [
          'Set width and height on all images.',
          'Reserve placeholder divs for dynamic components.',
          'Use translate for sticky-header transitions.',
        ],
      },
    ],
    relatedCollections: [
      {
        title: 'Performance-first Layouts',
        href: '/collections',
        description: 'We will feature a set of performance-friendly layouts here soon.',
      },
    ],
    relatedReads: [
      {
        title: 'Core Web Vitals Monitor',
        href: '/blog',
        description: 'Stories highlighting CLS, LCP, and INP improvements are on the way.',
      },
    ],
  },
];

export function getPillarTopic(slug: string): PillarTopic | undefined {
  return pillarTopics.find((topic) => topic.slug === slug);
}
