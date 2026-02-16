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
  filterTags?: string[]; // Tags to filter designs more precisely within category
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
    filterTags: ['saas', 'landing', 'b2b', 'conversion'],
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
    filterTags: ['dashboard', 'minimal', 'clean', 'analytics'],
    metaDescription:
      'Minimalist dashboard collection featuring signal-first cards, density controls, and dark mode token guidance.',
  },
  {
    slug: 'high-conversion-hero-sections',
    title: 'High-Conversion Hero Sections',
    heroEyebrow: 'Collection 03',
    heroHeading: 'Hero layouts that clarify value in one scroll',
    heroSummary:
      'Hero-first layouts with outcome-driven headlines, proof placement, and CTA ladders tuned for SaaS conversion velocity.',
    description: [
      'Hero sections are the decision moment. This collection prioritizes layouts that explain the product, prove credibility, and present a single primary action before the user scrolls.',
      'Each layout is scored for message clarity, proof density, and CTA hierarchy so teams can swap in new copy without breaking conversion intent.',
    ],
    highlightPoints: [
      'Role-based headlines anchored to one measurable outcome.',
      'Trust signals placed adjacent to CTA buttons, not below the fold.',
      'Two-step CTA ladder that preserves evaluation options.',
    ],
    bestPractices: [
      {
        title: 'Outcome headline',
        description:
          'Lead with a role + result statement and keep the verb concrete. Avoid “all-in-one platform” language.',
      },
      {
        title: 'Immediate proof',
        description:
          'Pair the headline with a metric badge, testimonial, or customer count in the same visual block.',
      },
      {
        title: 'CTA hierarchy',
        description:
          'Use a primary CTA plus a secondary evaluation CTA (Docs, Pricing) to avoid intent conflict.',
      },
      {
        title: 'Hero performance',
        description:
          'Keep hero imagery at 1200px WebP and reserve the same height for LCP stability.',
      },
    ],
    checklist: [
      'Headline under 12 words with one KPI.',
      'Proof element within the first scroll.',
      'Primary CTA paired with risk-reversal microcopy.',
      'Secondary CTA remains visible but de-emphasized.',
      'Hero visual size locked to prevent CLS.',
    ],
    faqs: [
      {
        question: 'What makes a hero high-conversion?',
        answer:
          'It explains the outcome, proves credibility, and offers a clear next action without extra scrolling.',
      },
      {
        question: 'Should I always add two CTAs?',
        answer:
          'Yes, a primary action plus a secondary evaluation path improves intent clarity for most B2B funnels.',
      },
      {
        question: 'How do I keep the hero fast?',
        answer:
          'Optimize the hero image, preload fonts, and avoid heavy overlays that delay LCP.',
      },
    ],
    pillar: {
      title: 'SaaS Landing Page UX Strategy',
      href: '/playbooks/saas-landing-page-ux',
      summary: 'The playbook that standardizes hero messaging, proof placement, and CTA sequencing.',
    },
    supabaseCategory: 'Landing Page',
    filterTags: ['hero', 'above-fold', 'conversion', 'landing'],
    metaDescription:
      'High-conversion hero section collection with outcome headlines, proof placement, and CTA ladder examples.',
  },
  {
    slug: 'saas-pricing-pages',
    title: 'SaaS Pricing Pages',
    heroEyebrow: 'Collection 04',
    heroHeading: 'Pricing layouts that reduce evaluation friction',
    heroSummary:
      'Pricing page systems that combine plan clarity, tier storytelling, and enterprise guardrails for modern SaaS teams.',
    description: [
      'Pricing pages should clarify who each plan is for, not just list features. This collection favors layouts that pair plan tiers with use-case narratives and clear enterprise paths.',
      'Each design also highlights performance and trust cues so pricing feels stable, transparent, and actionable.',
    ],
    highlightPoints: [
      'Plan tiers grouped by team size, usage, or maturity stage.',
      'Enterprise pathways surfaced without derailing self-serve flow.',
      'Risk-reversal and compliance notes positioned near pricing CTA.',
    ],
    bestPractices: [
      {
        title: 'Tier narrative',
        description:
          'Describe each tier with a team archetype and outcome statement rather than a feature checklist only.',
      },
      {
        title: 'Feature density',
        description:
          'Keep feature tables short and group details under expandable sections to preserve scan speed.',
      },
      {
        title: 'Enterprise lane',
        description:
          'Provide a clear enterprise CTA with security and SLA notes to prevent sales detours.',
      },
      {
        title: 'Trust anchors',
        description:
          'Place compliance badges and refund policies adjacent to pricing blocks, not in the footer.',
      },
    ],
    checklist: [
      'Each tier has a team-size or usage label.',
      'Primary pricing CTA includes risk-reversal microcopy.',
      'Enterprise CTA includes SLA or security note.',
      'Feature grid limited to 8–12 key items.',
      'Pricing toggle (monthly/annual) shows savings.',
    ],
    faqs: [
      {
        question: 'How many plans should a SaaS pricing page show?',
        answer: 'Three plans is a reliable default; add enterprise as a separate path when needed.',
      },
      {
        question: 'Should pricing show annual savings?',
        answer: 'Yes, explicit savings improve conversion and reduce pricing ambiguity.',
      },
      {
        question: 'Where should security info live?',
        answer: 'Place it beside pricing so buyers see it during evaluation, not after the fold.',
      },
    ],
    pillar: {
      title: 'SaaS Landing Page UX Strategy',
      href: '/playbooks/saas-landing-page-ux',
      summary: 'Guidance on CTA ladders, proof placement, and pricing narrative clarity.',
    },
    supabaseCategory: 'Landing Page',
    filterTags: ['pricing', 'saas', 'conversion', 'tiers'],
    metaDescription:
      'SaaS pricing page collection featuring tier storytelling, enterprise pathways, and transparent CTA layouts.',
  },
  {
    slug: 'onboarding-activation-flows',
    title: 'Onboarding & Activation Flows',
    heroEyebrow: 'Collection 05',
    heroHeading: 'First-session flows that lead to activation',
    heroSummary:
      'Activation-focused onboarding patterns that guide users to value moments quickly without overloading them.',
    description: [
      'Onboarding is a commitment device. This collection surfaces flows that reduce friction while still capturing key setup data.',
      'Layouts highlight progress signals, milestone messaging, and supportive microcopy that keeps users moving.',
    ],
    highlightPoints: [
      'Progress cues that reinforce completion momentum.',
      'Step-by-step capture that avoids long multi-field forms.',
      'Clear success state that signals value delivered.',
    ],
    bestPractices: [
      {
        title: 'Progressive disclosure',
        description:
          'Collect only the minimum data needed for the first value moment; postpone non-critical fields.',
      },
      {
        title: 'Milestone messaging',
        description:
          'Celebrate completion of key steps and preview the next value state to keep momentum.',
      },
      {
        title: 'Contextual help',
        description:
          'Use inline hints and short tooltips rather than modal interruptions.',
      },
      {
        title: 'Activation proof',
        description:
          'Show a “you’re live” confirmation with the exact outcome achieved.',
      },
    ],
    checklist: [
      'First step requires fewer than three fields.',
      'Each step explains why the data is needed.',
      'Success screen summarizes the outcome.',
      'Optional setup steps are skippable.',
      'Progress indicator shows remaining steps.',
    ],
    faqs: [
      {
        question: 'What is the best onboarding length?',
        answer: 'Keep it to 3–5 steps unless compliance requires more.',
      },
      {
        question: 'Should onboarding allow skipping?',
        answer: 'Yes, optional steps should be skippable to preserve momentum.',
      },
      {
        question: 'How do I signal activation?',
        answer: 'Use a clear success screen that states the value delivered.',
      },
    ],
    pillar: {
      title: 'UX Psychology in Modern Interfaces',
      href: '/playbooks/ux-psychology',
      summary: 'Behavioral patterns that reduce hesitation and increase activation.',
    },
    supabaseCategory: 'Components',
    filterTags: ['onboarding', 'activation', 'signup', 'flow'],
    metaDescription:
      'Onboarding and activation flow collection covering progress cues, step-by-step forms, and success states.',
  },
  {
    slug: 'product-tour-pages',
    title: 'Product Tour Pages',
    heroEyebrow: 'Collection 06',
    heroHeading: 'Guided product tours that explain value fast',
    heroSummary:
      'Narrative product tour layouts designed to help evaluators understand features without heavy friction.',
    description: [
      'Product tours should feel like a guided walkthrough, not a feature dump. This collection emphasizes story-driven sections and clear evaluation CTAs.',
      'Each layout shows how to blend visuals, proof, and short copy blocks so teams can reduce sales cycles.',
    ],
    highlightPoints: [
      'Narrative sections anchored by outcomes, not features.',
      'Visuals aligned to the exact workflow described in copy.',
      'Proof blocks positioned after each major benefit.',
    ],
    bestPractices: [
      {
        title: 'Outcome sequencing',
        description:
          'Organize the tour by user journey phases (setup, execute, analyze) rather than product modules.',
      },
      {
        title: 'Visual alignment',
        description:
          'Ensure screenshots match the exact text beside them to prevent cognitive dissonance.',
      },
      {
        title: 'Tour CTA',
        description:
          'Include a CTA after each major outcome so evaluators can act without scrolling back.',
      },
      {
        title: 'Proof placement',
        description:
          'Insert testimonials or metrics after each feature cluster to keep trust flowing.',
      },
    ],
    checklist: [
      'Each section maps to a user job or workflow.',
      'Visuals match copy, no mismatched UI states.',
      'CTA repeats every 2–3 sections.',
      'Proof included at least twice per page.',
      'Navigation anchor links for quick scanning.',
    ],
    faqs: [
      {
        question: 'How long should a product tour be?',
        answer: '6–8 sections is a practical ceiling before attention drops.',
      },
      {
        question: 'Are product tours better than demos?',
        answer: 'They complement demos by shortening the evaluation step and clarifying outcomes.',
      },
      {
        question: 'Where should CTAs live?',
        answer: 'Place a CTA after each key outcome so users can act immediately.',
      },
    ],
    pillar: {
      title: 'SaaS Landing Page UX Strategy',
      href: '/playbooks/saas-landing-page-ux',
      summary: 'Guidance on narrative sequencing and CTA ladders for SaaS evaluation pages.',
    },
    supabaseCategory: 'Landing Page',
    filterTags: ['product-tour', 'onboarding', 'walkthrough'],
    metaDescription:
      'Product tour page collection with narrative sections, aligned visuals, and repeated evaluation CTAs.',
  },
  {
    slug: 'developer-docs-layouts',
    title: 'Developer Docs Layouts',
    heroEyebrow: 'Collection 07',
    heroHeading: 'Documentation layouts engineered for scanning',
    heroSummary:
      'Documentation patterns that balance quick starts, reference depth, and copy-paste blocks for developer audiences.',
    description: [
      'Developer documentation must be skimmable, searchable, and easy to copy. This collection focuses on layouts that surface quick start guides, endpoints, and examples without overwhelming readers.',
      'Each layout includes visual hierarchy patterns that reduce time-to-first-success for APIs or SDKs.',
    ],
    highlightPoints: [
      'Quick-start modules above deep reference sections.',
      'Code block presentation optimized for copy/paste.',
      'Sidebar navigation that keeps context and versioning clear.',
    ],
    bestPractices: [
      {
        title: 'Quick start first',
        description:
          'Place a minimal setup path at the top so developers can reach a success state fast.',
      },
      {
        title: 'Contextual examples',
        description:
          'Attach examples to every endpoint or component so readers don’t switch tabs.',
      },
      {
        title: 'Navigation clarity',
        description:
          'Use persistent side navigation with clear version labels and sticky headings.',
      },
      {
        title: 'Copy ergonomics',
        description:
          'Provide one-click copy and keep code blocks short to reduce errors.',
      },
    ],
    checklist: [
      'Quick start within the first screen.',
      'Every endpoint has a code sample.',
      'Code blocks include language labels.',
      'Navigation highlights current section.',
      'Search input visible on every page.',
    ],
    faqs: [
      {
        question: 'How long should quick start guides be?',
        answer: 'Aim for 5–8 steps so developers reach success quickly.',
      },
      {
        question: 'Should docs include screenshots?',
        answer: 'Yes, but keep them secondary to text and code blocks.',
      },
      {
        question: 'What matters most for docs CTR?',
        answer: 'Clear “Quick Start” language and explicit outcome statements in metadata.',
      },
    ],
    pillar: {
      title: 'UI Optimization for Core Web Vitals',
      href: '/playbooks/ui-core-web-vitals',
      summary: 'Performance guardrails that keep documentation fast and stable.',
    },
    supabaseCategory: 'Blog',
    filterTags: ['docs', 'documentation', 'developer', 'technical'],
    metaDescription:
      'Developer documentation layout collection with quick starts, code samples, and scannable side navigation.',
  },
  {
    slug: 'fintech-trust-screens',
    title: 'Fintech Trust Screens',
    heroEyebrow: 'Collection 08',
    heroHeading: 'Trust-forward fintech UI patterns',
    heroSummary:
      'Fintech landing and onboarding screens designed to reduce risk perception and improve credibility fast.',
    description: [
      'Fintech interfaces must reduce perceived risk within seconds. This collection emphasizes trust language, compliance signals, and secure CTA placement.',
      'Each layout includes proof elements, security markers, and copy patterns that reassure cautious buyers.',
    ],
    highlightPoints: [
      'Security badges integrated into primary CTA sections.',
      'Regulatory or compliance cues near pricing or signup.',
      'Risk-reversal language on key conversion steps.',
    ],
    bestPractices: [
      {
        title: 'Trust positioning',
        description:
          'State regulatory compliance or bank partners in the first scroll.',
      },
      {
        title: 'Secure CTA framing',
        description:
          'Add microcopy that clarifies verification, approval time, or security posture.',
      },
      {
        title: 'Proof density',
        description:
          'Use verified metrics and testimonials with real titles or firms.',
      },
      {
        title: 'Risk reduction',
        description:
          'Explain data handling and privacy in plain language, not legalese.',
      },
    ],
    checklist: [
      'Compliance badge or partner logo above the fold.',
      'Security statement near CTA.',
      'Metric or testimonial tied to trust.',
      'Clear timeline for approval or onboarding.',
      'Privacy language in human-readable copy.',
    ],
    faqs: [
      {
        question: 'What’s the fastest way to build trust?',
        answer: 'Place compliance and partner signals beside the hero CTA and headline.',
      },
      {
        question: 'Should fintech CTAs be softer?',
        answer: 'Yes, use “Start secure signup” or “Verify account” over aggressive copy.',
      },
      {
        question: 'How much proof is enough?',
        answer: 'At least one metric and one testimonial above the fold.',
      },
    ],
    pillar: {
      title: 'UX Psychology in Modern Interfaces',
      href: '/playbooks/ux-psychology',
      summary: 'Behavioral patterns that reinforce trust and reduce hesitation.',
    },
    supabaseCategory: 'Landing Page',
    filterTags: ['fintech', 'trust', 'security', 'landing'],
    metaDescription:
      'Fintech trust screen collection featuring compliance cues, security microcopy, and risk-reversal CTAs.',
  },
  {
    slug: 'ecommerce-product-detail-pages',
    title: 'E-commerce Product Detail Pages',
    heroEyebrow: 'Collection 09',
    heroHeading: 'PDP layouts optimized for conversion',
    heroSummary:
      'Product detail page patterns that surface price anchors, proof, and delivery promises without clutter.',
    description: [
      'PDPs are decision briefs. This collection curates layouts that lead with price clarity, shipping promises, and proof elements to keep buyers moving.',
      'Each design balances media density with readability so users can scan product details without fatigue.',
    ],
    highlightPoints: [
      'Price anchors and delivery promises above the CTA.',
      'Social proof blocks aligned with product benefits.',
      'Guarantee and return policies near the buy button.',
    ],
    bestPractices: [
      {
        title: 'Decision stack',
        description:
          'Order the layout as price → proof → CTA → details to maintain momentum.',
      },
      {
        title: 'Media rhythm',
        description:
          'Mix 1:1 and 4:5 images to show scale and context.',
      },
      {
        title: 'Shipping clarity',
        description:
          'Surface shipping ETA and returns policy above the fold.',
      },
      {
        title: 'Trust markers',
        description:
          'Place warranty badges and review counts near the CTA.',
      },
    ],
    checklist: [
      'Price and CTA visible without scroll.',
      'Shipping ETA and returns near CTA.',
      'At least one proof block above the fold.',
      'Gallery supports zoom or alternate views.',
      'Guarantee language in plain text.',
    ],
    faqs: [
      {
        question: 'What is the most important PDP section?',
        answer: 'The price + proof + CTA cluster above the fold.',
      },
      {
        question: 'Do I need long product descriptions?',
        answer: 'Keep descriptions concise and lead with benefits first.',
      },
      {
        question: 'Where should reviews live?',
        answer: 'At least one review summary should be above the fold.',
      },
    ],
    pillar: {
      title: 'E-Commerce UI Conversion Patterns',
      href: '/playbooks/ecommerce-conversion-patterns',
      summary: 'Conversion principles for PDPs, carts, and checkout flows.',
    },
    supabaseCategory: 'E-commerce',
    filterTags: ['ecommerce', 'product', 'pdp'],
    metaDescription:
      'E-commerce PDP collection with price anchors, proof placement, and delivery promise layouts.',
  },
  {
    slug: 'checkout-cart-flows',
    title: 'Checkout & Cart Flows',
    heroEyebrow: 'Collection 10',
    heroHeading: 'Checkout layouts that reduce abandonment',
    heroSummary:
      'Cart and checkout patterns focused on transparency, trust, and frictionless payment flow.',
    description: [
      'Checkout is a form compression problem. This collection highlights flows that keep costs transparent while reducing required fields.',
      'Each layout uses trust signals and sticky order summaries so buyers stay confident to the final step.',
    ],
    highlightPoints: [
      'Cost breakdown and delivery window visible immediately.',
      'Short form fields with autofill support.',
      'Trust badges placed next to payment actions.',
    ],
    bestPractices: [
      {
        title: 'Cost clarity',
        description:
          'Show subtotal, shipping, and tax within the first screen.',
      },
      {
        title: 'Form compression',
        description:
          'Keep total fields under twelve and use address autocomplete.',
      },
      {
        title: 'Sticky summary',
        description:
          'Provide a mobile sticky order summary for confidence.',
      },
      {
        title: 'Payment trust',
        description:
          'Place payment logos and security badges adjacent to the submit action.',
      },
    ],
    checklist: [
      'All costs visible before checkout.',
      'Address autocomplete enabled.',
      'Order summary sticky on mobile.',
      'No forced account creation.',
      'Trust badges near CTA.',
    ],
    faqs: [
      {
        question: 'How do I reduce checkout abandonment?',
        answer: 'Make costs transparent and reduce fields to the minimum required.',
      },
      {
        question: 'Should I require account creation?',
        answer: 'No, offer guest checkout to preserve momentum.',
      },
      {
        question: 'Where should trust badges appear?',
        answer: 'Right next to the pay or place order button.',
      },
    ],
    pillar: {
      title: 'E-Commerce UI Conversion Patterns',
      href: '/playbooks/ecommerce-conversion-patterns',
      summary: 'Checkout compression and trust patterns for conversion.',
    },
    supabaseCategory: 'E-commerce',
    filterTags: ['ecommerce', 'checkout', 'cart', 'conversion'],
    metaDescription:
      'Checkout and cart flow collection with transparent cost breakdowns, short forms, and trust badges.',
  },
  {
    slug: 'subscription-management-ui',
    title: 'Subscription Management UI',
    heroEyebrow: 'Collection 11',
    heroHeading: 'Account and billing experiences that retain users',
    heroSummary:
      'Subscription management screens that clarify plans, invoices, and downgrade paths without frustration.',
    description: [
      'Billing screens are a trust moment. This collection highlights layouts that explain plan changes, renewal dates, and invoices with transparency.',
      'Each design keeps actions clear while reducing churn-driving confusion.',
    ],
    highlightPoints: [
      'Plan change UX with clear outcomes and pricing impact.',
      'Invoice history with quick download access.',
      'Cancellation flows that preserve user control.',
    ],
    bestPractices: [
      {
        title: 'Clarity of impact',
        description:
          'Show exactly how plan changes affect billing before confirmation.',
      },
      {
        title: 'Accessible history',
        description:
          'Invoices should be visible with a single click and include billing period context.',
      },
      {
        title: 'Cancellation transparency',
        description:
          'Offer clear outcomes and allow users to retain data where possible.',
      },
      {
        title: 'Trust copy',
        description:
          'Use human-language labels for renewal dates and policy terms.',
      },
    ],
    checklist: [
      'Plan change shows new total before confirm.',
      'Invoice list available in one click.',
      'Cancellation shows immediate impact.',
      'Renewal date visible on every plan.',
      'Support contact in billing view.',
    ],
    faqs: [
      {
        question: 'What reduces churn in billing screens?',
        answer: 'Clear change summaries and transparent renewal info.',
      },
      {
        question: 'Should cancellation be one click?',
        answer: 'It should be simple and transparent, with a short confirmation step.',
      },
      {
        question: 'Where should invoices live?',
        answer: 'In the primary billing view with download access.',
      },
    ],
    pillar: {
      title: 'UX Psychology in Modern Interfaces',
      href: '/playbooks/ux-psychology',
      summary: 'Behavioral guardrails that keep user trust intact.',
    },
    supabaseCategory: 'Dashboard',
    filterTags: ['dashboard', 'subscription', 'billing', 'settings'],
    metaDescription:
      'Subscription management UI collection featuring billing clarity, plan change flows, and invoice access.',
  },
  {
    slug: 'analytics-kpi-dashboards',
    title: 'Analytics & KPI Dashboards',
    heroEyebrow: 'Collection 12',
    heroHeading: 'KPI dashboards built for fast decisions',
    heroSummary:
      'Analytics layouts that surface key metrics, trends, and anomalies without noise.',
    description: [
      'KPI dashboards are decision engines. This collection prioritizes metric-first layouts that keep scan paths consistent.',
      'Designs include trend context and alert surfaces to reduce time-to-action.',
    ],
    highlightPoints: [
      'KPI cards anchored with deltas and trend tags.',
      'Trends visualized near metrics, not in separate tabs.',
      'Anomaly callouts for rapid triage.',
    ],
    bestPractices: [
      {
        title: 'Scan path',
        description:
          'Keep KPI cards in the first row, followed by trends and tables.',
      },
      {
        title: 'Delta clarity',
        description:
          'Always pair KPIs with a comparison period label.',
      },
      {
        title: 'Anomaly surfacing',
        description:
          'Highlight unusual changes with small, non-intrusive callouts.',
      },
      {
        title: 'Density balance',
        description:
          'Use compact toggles for power users without sacrificing default clarity.',
      },
    ],
    checklist: [
      'KPI row limited to three or four cards.',
      'Trend comparisons labeled clearly.',
      'Alerts appear near the metric they affect.',
      'Table headers sticky for scan speed.',
      'Dark mode contrast meets 4.5:1.',
    ],
    faqs: [
      {
        question: 'How many KPIs should be in the first row?',
        answer: 'Three or four is enough for decision speed.',
      },
      {
        question: 'Where do anomalies go?',
        answer: 'Place them next to affected KPIs for immediate context.',
      },
      {
        question: 'Do dashboards need density toggles?',
        answer: 'Yes, for power users who require more data per view.',
      },
    ],
    pillar: {
      title: 'Dashboard UX Design Principles',
      href: '/playbooks/dashboard-ux-principles',
      summary: 'Hierarchy and density guardrails for analytics UIs.',
    },
    supabaseCategory: 'Dashboard',
    filterTags: ['dashboard', 'analytics', 'kpi', 'metrics'],
    metaDescription:
      'Analytics dashboard collection with KPI scan paths, trend context, and anomaly callouts.',
  },
  {
    slug: 'admin-operations-tables',
    title: 'Admin & Operations Tables',
    heroEyebrow: 'Collection 13',
    heroHeading: 'Operational tables that stay readable at scale',
    heroSummary:
      'Admin layouts with dense tables, bulk actions, and contextual filters built for operations teams.',
    description: [
      'Operations dashboards need high data density without sacrificing readability. This collection highlights table-first layouts with clear filtering and bulk actions.',
      'Designs favor consistent row height, inline actions, and quick export controls.',
    ],
    highlightPoints: [
      'Sticky headers and filter bars for fast navigation.',
      'Bulk actions grouped and visible without hover.',
      'Inline status tags to reduce column density.',
    ],
    bestPractices: [
      {
        title: 'Table hierarchy',
        description:
          'Use leftmost columns for primary identifiers, keep actions on the right.',
      },
      {
        title: 'Filter clarity',
        description:
          'Expose default filters and save states to reduce repeat setup.',
      },
      {
        title: 'Bulk actions',
        description:
          'Surface bulk actions immediately after row selection.',
      },
      {
        title: 'Density control',
        description:
          'Provide compact mode toggles for power users.',
      },
    ],
    checklist: [
      'Sticky table header enabled.',
      'Row actions visible without hover.',
      'Bulk action bar appears on selection.',
      'Filters saved or remembered.',
      'Row height consistent across the table.',
    ],
    faqs: [
      {
        question: 'What keeps admin tables readable?',
        answer: 'Consistent row height, clear status tags, and minimal column clutter.',
      },
      {
        question: 'Do bulk actions need confirmation?',
        answer: 'Yes, especially for destructive operations.',
      },
      {
        question: 'How do I handle dense filters?',
        answer: 'Use a persistent filter bar with saved presets.',
      },
    ],
    pillar: {
      title: 'Dashboard UX Design Principles',
      href: '/playbooks/dashboard-ux-principles',
      summary: 'Density and hierarchy standards for operational UI.',
    },
    supabaseCategory: 'Dashboard',
    filterTags: ['dashboard', 'admin', 'table', 'operations'],
    metaDescription:
      'Admin operations table collection featuring sticky headers, bulk actions, and dense filtering systems.',
  },
  {
    slug: 'portfolio-case-studies',
    title: 'Portfolio Case Studies',
    heroEyebrow: 'Collection 14',
    heroHeading: 'Case study layouts that tell a clear story',
    heroSummary:
      'Portfolio case studies structured around problem, process, and outcome so visitors understand impact fast.',
    description: [
      'Case studies should communicate outcomes with clarity. This collection focuses on story-driven layouts that blend visuals with concise summaries.',
      'Designs highlight metrics, artifacts, and workflow summaries to reduce cognitive load.',
    ],
    highlightPoints: [
      'Story flow anchored to problem → process → outcome.',
      'Metrics showcased alongside visuals for proof.',
      'Timeline and role clarity for credibility.',
    ],
    bestPractices: [
      {
        title: 'Outcome framing',
        description:
          'Start with the business outcome and reference it throughout the story.',
      },
      {
        title: 'Artifact balance',
        description:
          'Mix high-fidelity visuals with short process summaries.',
      },
      {
        title: 'Role clarity',
        description:
          'Define your role and team size in the intro to build trust.',
      },
      {
        title: 'Metric proof',
        description:
          'Use at least one quantified result in the hero or summary.',
      },
    ],
    checklist: [
      'Outcome stated within the first paragraph.',
      'Process steps listed in sequence.',
      'Metrics placed near the hero visuals.',
      'Role and tools listed succinctly.',
      'CTA to contact or hire visible.',
    ],
    faqs: [
      {
        question: 'How long should a case study be?',
        answer: 'Keep it concise: one scroll for summary, one scroll for process.',
      },
      {
        question: 'What matters most for portfolios?',
        answer: 'Outcome clarity and proof of impact.',
      },
      {
        question: 'Should I include metrics?',
        answer: 'Yes, even directional metrics increase credibility.',
      },
    ],
    pillar: {
      title: 'UX Psychology in Modern Interfaces',
      href: '/playbooks/ux-psychology',
      summary: 'Narrative and trust patterns that shape perception.',
    },
    supabaseCategory: 'Portfolio',
    filterTags: ['portfolio', 'case-study', 'showcase'],
    metaDescription:
      'Portfolio case study collection with story-driven layouts, metric proof, and clear role framing.',
  },
  {
    slug: 'agency-landing-pages',
    title: 'Agency Landing Pages',
    heroEyebrow: 'Collection 15',
    heroHeading: 'Agency pages that win high-intent leads',
    heroSummary:
      'Agency landing patterns that emphasize credibility, case studies, and a clear booking path.',
    description: [
      'Agency websites must earn trust quickly. This collection highlights layouts that foreground outcomes, past work, and simple lead capture.',
      'Each design reduces friction with clear CTA positioning and strong social proof.',
    ],
    highlightPoints: [
      'Case studies placed near the hero CTA.',
      'Service scope written in outcome language.',
      'Lead capture forms kept short and focused.',
    ],
    bestPractices: [
      {
        title: 'Credibility stack',
        description:
          'Show logos, testimonials, and metrics within the first scroll.',
      },
      {
        title: 'Service framing',
        description:
          'List services by outcome, not deliverables alone.',
      },
      {
        title: 'CTA focus',
        description:
          'Use one booking CTA and a secondary case study link.',
      },
      {
        title: 'Lead capture',
        description:
          'Keep forms short and explain the next step.',
      },
    ],
    checklist: [
      'Hero includes a primary booking CTA.',
      'At least two case studies above the fold.',
      'Service list tied to outcomes.',
      'Lead form under five fields.',
      'Response timeline clarified.',
    ],
    faqs: [
      {
        question: 'What drives agency CTR?',
        answer: 'Clear outcomes and proof near the hero CTA.',
      },
      {
        question: 'How many services should be listed?',
        answer: 'Three to five core services is a strong default.',
      },
      {
        question: 'Should agencies show pricing?',
        answer: 'If possible, add a starting range to pre-qualify leads.',
      },
    ],
    pillar: {
      title: 'SaaS Landing Page UX Strategy',
      href: '/playbooks/saas-landing-page-ux',
      summary: 'Messaging and proof patterns that increase conversion.',
    },
    supabaseCategory: 'Landing Page',
    filterTags: ['landing', 'agency', 'services', 'b2b'],
    metaDescription:
      'Agency landing page collection with proof-heavy heroes, short lead forms, and outcome-based service framing.',
  },
  {
    slug: 'community-event-pages',
    title: 'Community & Event Pages',
    heroEyebrow: 'Collection 16',
    heroHeading: 'Event layouts that drive registration',
    heroSummary:
      'Community and event landing pages focused on speaker proof, agenda clarity, and rapid registration.',
    description: [
      'Event pages must translate excitement into registration. This collection emphasizes clear agendas, speaker proof, and short sign-up paths.',
      'Layouts include social proof and key logistics above the fold to reduce uncertainty.',
    ],
    highlightPoints: [
      'Agenda highlights positioned above the registration CTA.',
      'Speaker proof integrated into hero sections.',
      'Location and time clarity in the first scroll.',
    ],
    bestPractices: [
      {
        title: 'Agenda clarity',
        description:
          'Show 3–5 key sessions early to establish value.',
      },
      {
        title: 'Speaker credibility',
        description:
          'Include speaker titles or company logos near their names.',
      },
      {
        title: 'CTA focus',
        description:
          'Primary CTA should be registration, with a secondary “View agenda” link.',
      },
      {
        title: 'Logistics transparency',
        description:
          'Time zone, location, and format (virtual/in-person) should be explicit.',
      },
    ],
    checklist: [
      'Registration CTA above the fold.',
      'Agenda summary visible immediately.',
      'Speaker list includes credentials.',
      'Location/time stated clearly.',
      'Social proof or attendee count displayed.',
    ],
    faqs: [
      {
        question: 'What raises event registration?',
        answer: 'Clear agenda highlights and speaker credibility near the CTA.',
      },
      {
        question: 'Should event pages include pricing?',
        answer: 'Yes, keep pricing visible next to registration.',
      },
      {
        question: 'How do I reduce no-shows?',
        answer: 'Send confirmation details and remind attendees of key sessions.',
      },
    ],
    pillar: {
      title: 'UX Psychology in Modern Interfaces',
      href: '/playbooks/ux-psychology',
      summary: 'Behavioral triggers that move users to register.',
    },
    supabaseCategory: 'Landing Page',
    filterTags: ['landing', 'event', 'community', 'registration'],
    metaDescription:
      'Community and event page collection with agenda clarity, speaker proof, and registration CTAs.',
  },
  {
    slug: 'waitlist-early-access',
    title: 'Waitlist & Early Access Pages',
    heroEyebrow: 'Collection 17',
    heroHeading: 'Waitlist layouts that maximize signups',
    heroSummary:
      'Early access landing pages that balance exclusivity, value clarity, and short signup forms.',
    description: [
      'Waitlist pages must create urgency without dark patterns. This collection showcases layouts that highlight exclusivity while staying transparent.',
      'Each design uses simple forms, proof of demand, and clear benefit statements.',
    ],
    highlightPoints: [
      'Short signup forms that minimize friction.',
      'Social proof or waitlist counters for credibility.',
      'Value statement tied to a specific user problem.',
    ],
    bestPractices: [
      {
        title: 'Form simplicity',
        description:
          'Only request one required field to maximize signup conversion.',
      },
      {
        title: 'Demand proof',
        description:
          'Show current waitlist count or partner logos to signal traction.',
      },
      {
        title: 'Benefit clarity',
        description:
          'Explain what users gain by joining and when access begins.',
      },
      {
        title: 'Expectation setting',
        description:
          'Describe how invites are sent and how long the wait might be.',
      },
    ],
    checklist: [
      'Signup form under two fields.',
      'Waitlist value statement above the CTA.',
      'Proof of demand visible near the form.',
      'Expectation setting for invites.',
      'Privacy assurance under the form.',
    ],
    faqs: [
      {
        question: 'What increases waitlist conversion?',
        answer: 'Short forms, clear value, and proof of demand.',
      },
      {
        question: 'Should I show a waitlist count?',
        answer: 'Yes, counts or partner logos help establish credibility.',
      },
      {
        question: 'How do I reduce drop-off?',
        answer: 'Explain what happens after signup and how invites are sent.',
      },
    ],
    pillar: {
      title: 'UX Psychology in Modern Interfaces',
      href: '/playbooks/ux-psychology',
      summary: 'Behavioral triggers that encourage signups without manipulation.',
    },
    supabaseCategory: 'Landing Page',
    filterTags: ['landing', 'waitlist', 'signup', 'launch'],
    metaDescription:
      'Waitlist and early access page collection with short forms, demand proof, and clear value statements.',
  },
  {
    slug: 'knowledge-base-help-centers',
    title: 'Knowledge Base & Help Centers',
    heroEyebrow: 'Collection 18',
    heroHeading: 'Support layouts designed for fast resolution',
    heroSummary:
      'Help center layouts that surface top questions, guides, and search tools without friction.',
    description: [
      'Support content should be searchable and skimmable. This collection showcases layouts that emphasize top tasks, search-first navigation, and easy category scanning.',
      'Designs focus on reducing time-to-answer while keeping documentation accessible.',
    ],
    highlightPoints: [
      'Search-first layout with suggested results.',
      'Top tasks and FAQs visible in the hero section.',
      'Category tiles optimized for quick scanning.',
    ],
    bestPractices: [
      {
        title: 'Search prominence',
        description:
          'Place a large search input in the hero to signal self-serve support.',
      },
      {
        title: 'Task grouping',
        description:
          'Group articles by user goals instead of internal teams.',
      },
      {
        title: 'Breadcrumb guidance',
        description:
          'Use breadcrumbs to reduce user disorientation.',
      },
      {
        title: 'Support escalation',
        description:
          'Offer a clear contact CTA for unresolved issues.',
      },
    ],
    checklist: [
      'Hero includes a search field.',
      'Top 5 tasks highlighted.',
      'Category tiles short and descriptive.',
      'Breadcrumbs visible on article pages.',
      'Contact CTA available for escalation.',
    ],
    faqs: [
      {
        question: 'What improves help center CTR?',
        answer: 'Search-first layouts with clear top tasks and task labels.',
      },
      {
        question: 'Should help centers include chat widgets?',
        answer: 'Yes, but keep them secondary to search and self-serve content.',
      },
      {
        question: 'How do I reduce support tickets?',
        answer: 'Surface the top 5 tasks and keep the search visible.',
      },
    ],
    pillar: {
      title: 'UI Optimization for Core Web Vitals',
      href: '/playbooks/ui-core-web-vitals',
      summary: 'Performance and stability guidance for content-heavy support hubs.',
    },
    supabaseCategory: 'Blog',
    filterTags: ['blog', 'help', 'documentation', 'support'],
    metaDescription:
      'Help center and knowledge base collection with search-first layouts, top tasks, and clear category tiles.',
  },
  {
    slug: 'design-system-libraries',
    title: 'Design System Libraries',
    heroEyebrow: 'Collection 19',
    heroHeading: 'Component libraries and token docs',
    heroSummary:
      'Design system pages that document tokens, components, and usage guidelines with clarity.',
    description: [
      'Design systems succeed when documentation is consistent. This collection highlights layouts that map tokens, components, and usage guidelines in a scannable way.',
      'Each design emphasizes clear navigation, visual examples, and copy-ready guidelines.',
    ],
    highlightPoints: [
      'Component pages with usage guidance and variants.',
      'Token documentation with clear naming rules.',
      'Navigation that scales with hundreds of components.',
    ],
    bestPractices: [
      {
        title: 'Usage clarity',
        description:
          'Document when to use each component and include “avoid” notes.',
      },
      {
        title: 'Token taxonomy',
        description:
          'Group tokens by category and provide usage examples.',
      },
      {
        title: 'Variant coverage',
        description:
          'Show interactive examples for states and sizes.',
      },
      {
        title: 'Navigation scale',
        description:
          'Use clear side navigation with search for fast access.',
      },
    ],
    checklist: [
      'Component pages show usage and variants.',
      'Token docs include naming rules.',
      'Search visible across the system.',
      'Interactive examples available for key components.',
      'Version history accessible.',
    ],
    faqs: [
      {
        question: 'What makes design system docs effective?',
        answer: 'Clear usage guidance and consistent token naming.',
      },
      {
        question: 'How should components be organized?',
        answer: 'Group by function (inputs, navigation, feedback) to reduce scanning time.',
      },
      {
        question: 'Do design systems need search?',
        answer: 'Yes, search dramatically speeds up component discovery.',
      },
    ],
    pillar: {
      title: 'UI Optimization for Core Web Vitals',
      href: '/playbooks/ui-core-web-vitals',
      summary: 'Performance-friendly component documentation patterns.',
    },
    supabaseCategory: 'Components',
    filterTags: ['component', 'design-system', 'library', 'documentation'],
    metaDescription:
      'Design system library collection with token documentation, component usage guidance, and scalable navigation.',
  },
  {
    slug: 'app-shell-layouts',
    title: 'SaaS App Shell Layouts',
    heroEyebrow: 'Collection 20',
    heroHeading: 'Application shells built for daily use',
    heroSummary:
      'Shell layouts that define navigation, workspace hierarchy, and layout density for SaaS apps.',
    description: [
      'App shells determine how users navigate the product every day. This collection focuses on stable navigation, workspace selectors, and consistent content rails.',
      'Designs favor predictable patterns that reduce cognitive load across complex applications.',
    ],
    highlightPoints: [
      'Navigation patterns that scale to multi-module apps.',
      'Workspace selectors that reduce context switching.',
      'Consistent content rails for predictable scanning.',
    ],
    bestPractices: [
      {
        title: 'Navigation hierarchy',
        description:
          'Use primary nav for top-level modules and secondary nav for task-specific pages.',
      },
      {
        title: 'Workspace clarity',
        description:
          'Expose workspace or account switching with clear labels and status.',
      },
      {
        title: 'Density consistency',
        description:
          'Keep padding and typography consistent across modules to reduce fatigue.',
      },
      {
        title: 'Sticky utility',
        description:
          'Keep search and global actions accessible via sticky header or command palette.',
      },
    ],
    checklist: [
      'Primary nav visible on all screens.',
      'Workspace switcher includes active status.',
      'Content width capped for readability.',
      'Global search easily accessible.',
      'Contextual actions aligned to page header.',
    ],
    faqs: [
      {
        question: 'What makes a strong app shell?',
        answer: 'Stable navigation, predictable content rails, and clear workspace context.',
      },
      {
        question: 'Should app shells support density toggles?',
        answer: 'Yes, especially for power users who spend hours inside the UI.',
      },
      {
        question: 'How do I avoid navigation sprawl?',
        answer: 'Use a primary/secondary hierarchy and limit top-level modules.',
      },
    ],
    pillar: {
      title: 'Dashboard UX Design Principles',
      href: '/playbooks/dashboard-ux-principles',
      summary: 'Hierarchy and density patterns for application shells.',
    },
    supabaseCategory: 'Dashboard',
    filterTags: ['dashboard', 'layout', 'navigation', 'shell'],
    metaDescription:
      'SaaS app shell collection featuring navigation hierarchies, workspace selectors, and stable layouts.',
  },
];

export function getCollectionConfig(slug: string) {
  return collectionConfigs.find((config) => config.slug === slug);
}
