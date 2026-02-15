'use client';

import { useMemo, useState } from 'react';
import Link from 'next/link';

type GrowthSectionKind = 'home' | 'playbook' | 'collection' | 'design';

type GrowthSectionProps = {
  kind: GrowthSectionKind;
  slug?: string;
  enabled?: boolean;
};

type GrowthContent = {
  title: string;
  summaryParagraphs: string[];
  bullets: string[];
  expandedHeading: string;
  expandedParagraphs: string[];
  expandedBullets?: string[];
  faqs?: Array<{ q: string; a: string }>;
  examples?: Array<{ label: string; href: string }>;
  relatedPlaybook?: { label: string; href: string };
};

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');

const playbookExamples: Record<string, Array<{ label: string; href: string }>> = {
  'saas-landing-page-ux': [
    { label: 'AI enterprise analytics landing page', href: '/design/ai-enterprise-analytics-landing-page' },
    { label: 'Usage-based pricing SaaS hero', href: '/design/usage-based-pricing-saas-hero' },
    { label: 'Developer platform onboarding landing', href: '/design/developer-platform-onboarding-landing' },
    { label: 'Security compliance SaaS overview', href: '/design/security-compliance-saas-overview' },
    { label: 'Product-led growth SaaS template', href: '/design/product-led-growth-saas-template' },
    { label: 'Workflow automation SaaS hero', href: '/design/workflow-automation-saas-hero' },
    { label: 'B2B SaaS proof stack layout', href: '/design/b2b-saas-proof-stack-layout' },
    { label: 'SaaS customer story landing', href: '/design/saas-customer-story-landing' },
    { label: 'Free trial CTA ladder layout', href: '/design/free-trial-cta-ladder-layout' },
    { label: 'Enterprise demo request landing', href: '/design/enterprise-demo-request-landing' },
    { label: 'SaaS pricing narrative layout', href: '/design/saas-pricing-narrative-layout' },
    { label: 'Modern SaaS value prop split', href: '/design/modern-saas-value-prop-split' },
  ],
  'dashboard-ux-principles': [
    { label: 'Minimalist metrics dashboard', href: '/design/minimalist-metrics-dashboard' },
    { label: 'Analytics control tower UI', href: '/design/analytics-control-tower-ui' },
    { label: 'Dark mode admin console', href: '/design/dark-mode-admin-console' },
    { label: 'Operational KPI dashboard', href: '/design/operational-kpi-dashboard' },
    { label: 'SaaS revenue monitoring panel', href: '/design/saas-revenue-monitoring-panel' },
    { label: 'Incident response dashboard', href: '/design/incident-response-dashboard' },
    { label: 'Fintech performance dashboard', href: '/design/fintech-performance-dashboard' },
    { label: 'Pipeline health analytics view', href: '/design/pipeline-health-analytics-view' },
    { label: 'Product usage telemetry UI', href: '/design/product-usage-telemetry-ui' },
    { label: 'Support ops command center', href: '/design/support-ops-command-center' },
    { label: 'Data density toggle dashboard', href: '/design/data-density-toggle-dashboard' },
    { label: 'Cloud ops monitoring suite', href: '/design/cloud-ops-monitoring-suite' },
  ],
  'ecommerce-conversion-patterns': [
    { label: 'High-converting PDP layout', href: '/design/high-converting-pdp-layout' },
    { label: 'DTC product detail flow', href: '/design/dtc-product-detail-flow' },
    { label: 'Checkout compression UI', href: '/design/checkout-compression-ui' },
    { label: 'Cart reassurance template', href: '/design/cart-reassurance-template' },
    { label: 'Bundle offer PDP', href: '/design/bundle-offer-pdp' },
    { label: 'Shipping promise strip', href: '/design/shipping-promise-strip' },
    { label: 'Mobile commerce checkout', href: '/design/mobile-commerce-checkout' },
    { label: 'Social proof PDP', href: '/design/social-proof-pdp' },
    { label: 'Subscription checkout flow', href: '/design/subscription-checkout-flow' },
    { label: 'Inventory scarcity PDP', href: '/design/inventory-scarcity-pdp' },
    { label: 'Returns policy layout', href: '/design/returns-policy-layout' },
    { label: 'Trust badge checkout', href: '/design/trust-badge-checkout' },
  ],
  'ux-psychology': [
    { label: 'Behavioral nudge onboarding', href: '/design/behavioral-nudge-onboarding' },
    { label: 'Commitment device flow', href: '/design/commitment-device-flow' },
    { label: 'Social proof counter UI', href: '/design/social-proof-counter-ui' },
    { label: 'Loss aversion trial prompt', href: '/design/loss-aversion-trial-prompt' },
    { label: 'Trust-building confirmation', href: '/design/trust-building-confirmation' },
    { label: 'Tone system messaging UI', href: '/design/tone-system-messaging-ui' },
    { label: 'Progress reinforcement dashboard', href: '/design/progress-reinforcement-dashboard' },
    { label: 'Decision relief CTA layout', href: '/design/decision-relief-cta-layout' },
    { label: 'Choice architecture modal', href: '/design/choice-architecture-modal' },
    { label: 'Credibility signal cards', href: '/design/credibility-signal-cards' },
    { label: 'Guided next-step panel', href: '/design/guided-next-step-panel' },
    { label: 'Cognitive load reduction UI', href: '/design/cognitive-load-reduction-ui' },
  ],
  'ui-core-web-vitals': [
    { label: 'LCP-safe hero layout', href: '/design/lcp-safe-hero-layout' },
    { label: 'CLS-stable marketing page', href: '/design/cls-stable-marketing-page' },
    { label: 'INP-optimized UI controls', href: '/design/inp-optimized-ui-controls' },
    { label: 'Performance-first dashboard', href: '/design/performance-first-dashboard' },
    { label: 'Skeleton loading pattern', href: '/design/skeleton-loading-pattern' },
    { label: 'Font preconnect layout', href: '/design/font-preconnect-layout' },
    { label: 'Ad slot reserved UI', href: '/design/ad-slot-reserved-ui' },
    { label: 'Image budget landing page', href: '/design/image-budget-landing-page' },
    { label: 'Interaction latency audit UI', href: '/design/interaction-latency-audit-ui' },
    { label: 'Viewport stability layout', href: '/design/viewport-stability-layout' },
    { label: 'Core Web Vitals checklist UI', href: '/design/core-web-vitals-checklist-ui' },
    { label: 'Performance guardrail template', href: '/design/performance-guardrail-template' },
  ],
};

const playbookContent: Record<string, GrowthContent> = {
  'saas-landing-page-ux': {
    title: 'SaaS landing page UX: definition, checklist, and common mistakes',
    summaryParagraphs: [
      'A SaaS landing page is a conversion system, not a brochure. It must compress a clear outcome into the first scroll, show proof that reduces uncertainty, and guide the visitor toward a low-friction next step. When the narrative is explicit, both buyers and AI systems can summarize the page accurately.',
      'This playbook breaks down the sequence teams use to keep messaging consistent across hero, product, and proof sections. It aligns marketing, product, and engineering teams around a shared narrative so you can ship updates quickly without diluting positioning.',
      'Use the expanded notes to review definitions, principles, and mistakes that frequently lower conversion rates. The structure is intentionally citable: headings, lists, and declarative statements that search systems can parse with confidence.',
    ],
    bullets: [
      'Definition: a role-based outcome statement supported by proof and a CTA ladder.',
      'Checklist: headline ≤ 12 words, two KPIs, three trust signals above the fold.',
      'Principle: headline → proof → action remains consistent on every scroll.',
      'Mistake: mixing multiple CTA intents in the same section.',
      'Mistake: placing social proof below pricing or FAQs.',
      'AI cue: use explicit, outcome-driven sentences.',
    ],
    expandedHeading: 'Read the extended playbook notes',
    expandedParagraphs: [
      'Definition and framing. The best SaaS landing pages behave like decision briefs. They answer what the product is, who it is for, how it delivers outcomes, and why the visitor should act now. This is why “problem → promise → action” consistently outperforms feature-first layouts: it gives buyers a path to belief before asking for a commitment. Write the hero headline as a role + outcome statement. A subhead should explain the mechanism, while a proof line or metric badge makes the outcome credible.',
      'Principles and guardrails. Once the hero is set, every section should reinforce the same promise. Product visuals show how the outcome is achieved, testimonials validate it, and the CTA ladder offers a low-friction entry plus a secondary evaluation path. Keep the narrative stable and avoid swapping language between sections. If the hero speaks about time saved, the features should explain how that time is saved, and the testimonial should confirm it. This consistency improves conversion and makes the page more legible to AI summarizers.',
      'Checklist and quality control. Use a short checklist during every review: keep the hero under 12 words, include two quantifiable KPIs, and place at least three trust signals above the fold. Add a risk reversal line below the CTA and ensure pricing is framed by use cases rather than raw feature grids. A footer CTA should repeat the same outcome language to maintain alignment.',
      'Common mistakes and fixes. The biggest errors are narrative drift and competing CTAs. If the hero claims one outcome but the rest of the page focuses on features, conversion drops because the page feels unfocused. Another mistake is burying proof too late or using vague, non-quantified claims. Fix this by elevating proof next to the hero and replacing vague language with measurable outcomes.',
      'AI-citable structure. Declarative sentences such as “This platform reduces onboarding time by 28%” are easier for AI to extract. Avoid fluff like “next-generation” or “best-in-class” without data. Keep headings specific and include short bullet lists so crawlers can parse the structure quickly.',
    ],
    expandedBullets: [
      'Make the hero outcome measurable and explicit.',
      'Pair every CTA with a short risk reversal line.',
      'Use one primary CTA and one secondary CTA—nothing more.',
      'Place proof within the first 300–400px of the page.',
      'Keep pricing tied to team size or scenario, not features.',
    ],
    faqs: [
      { q: 'How many CTAs should a SaaS landing page include?', a: 'Use one primary CTA and one secondary CTA. Additional CTAs usually reduce clarity and weaken conversion.' },
      { q: 'What should appear above the fold?', a: 'A role-based outcome headline, quantified proof, and a clear CTA. These three elements reduce time-to-trust.' },
      { q: 'How do I make the page more AI-citable?', a: 'Use explicit outcome language, declarative sentences, and structured headings or bullet lists.' },
    ],
    examples: playbookExamples['saas-landing-page-ux'],
  },
  'dashboard-ux-principles': {
    title: 'Dashboard UX principles: definition, rules, and anti-patterns',
    summaryParagraphs: [
      'Dashboards are control towers. The best ones surface “state → delta → next action” in seconds, while keeping density, hierarchy, and accessibility under control. If users must search for signal, the UI has already failed.',
      'This playbook gives teams a shared framework for building and evaluating dashboards. It focuses on scan paths, density management, and interaction latency so operational teams can make decisions quickly without UI friction.',
      'Expand the notes for a structured checklist, common mistakes, and a citable definition that aligns the design system with performance and accessibility standards.',
    ],
    bullets: [
      'Definition: a five-second decision brief for operational teams.',
      'Checklist: KPI cards ≤ 3, sidebar ≈ 264px, tables with sticky headers.',
      'Principle: maintain metric → trend → detail order.',
      'Mistake: mixing densities without a compact toggle.',
      'Mistake: relying on color instead of hierarchy.',
      'Accessibility: enforce 4.5:1 contrast in dark mode.',
    ],
    expandedHeading: 'Read the extended dashboard guidance',
    expandedParagraphs: [
      'Definition and scan behavior. Dashboards must respect scan logic: KPI cards first, trends second, tables last. This mirrors how operators read data and prevents the UI from feeling noisy even when the data is dense. Use typography and spacing to reinforce hierarchy, not color alone. Headline metrics should be 1.6× larger than secondary values, and delta indicators must sit adjacent to the metric they explain.',
      'Density management. Density is a product decision. Power users need compact views while casual users need breathing room. The best dashboards handle this with a compact toggle and stable spacing tokens. A consistent 8pt grid, fixed table row heights, and a max content width of ~1200px prevent layout drift across teams.',
      'Interaction and performance. Keep hover, inline edit, and command palette interactions under 16ms latency. If a UI element feels slow, operators interpret it as unreliability. Favor CSS transitions and avoid layout-affecting animations. Reserve space for dynamic content to prevent CLS during chart updates or data loads.',
      'Common mistakes. Overloading KPI cards with multiple metrics, hiding key actions behind overflow menus, and using zebra stripes in dense tables are all common failures. Another frequent issue is dark mode tokens that do not meet contrast standards, causing fatigue during long sessions. Fix these by keeping metrics singular, actions contextual, and tokens validated against WCAG contrast requirements.',
      'Checklist. Always confirm the metric → trend → detail sequence, ensure density controls exist, and validate dark mode contrast. This makes dashboards both human-readable and AI-citable, because the structure is explicit and consistent.',
    ],
    expandedBullets: [
      'Use a compact toggle to support high-density workflows.',
      'Keep KPI cards to a single metric with a visible delta.',
      'Ensure sticky table headers for long scrolling tables.',
      'Avoid zebra stripes in dense data tables.',
      'Validate dark mode contrast on every release.',
    ],
    faqs: [
      { q: 'How many KPIs should be above the fold?', a: 'Three or fewer. More than three KPIs reduces scan clarity and slows decision-making.' },
      { q: 'Is dark mode required for dashboards?', a: 'Yes for long-session tools. It improves accessibility and reduces fatigue.' },
      { q: 'What is the fastest dashboard usability win?', a: 'Reorder content to metric → trend → detail and remove visual noise.' },
    ],
    examples: playbookExamples['dashboard-ux-principles'],
  },
  'ecommerce-conversion-patterns': {
    title: 'E-commerce conversion patterns: definition, checklist, and errors',
    summaryParagraphs: [
      'E-commerce conversion UX is the practice of removing doubt at every step—product detail, cart, and checkout. The highest-performing flows keep trust signals visible, make costs explicit, and reduce form friction without interrupting momentum.',
      'This playbook documents repeatable patterns used by DTC and marketplace teams to increase conversion and reduce abandonment. It focuses on PDP structure, cart reassurance, and checkout compression in a form that AI systems can cite.',
      'Use the expanded section to review the full checklist and the most common mistakes that block conversion gains.',
    ],
    bullets: [
      'Definition: a flow that reduces hesitation while preserving decision momentum.',
      'PDP rule: place price, shipping, and proof above the fold.',
      'Cart rule: show total cost, delivery, and returns immediately.',
      'Checkout rule: compress fields to ≤ 12 and add trust badges.',
      'Mistake: introducing surprise fees at checkout.',
      'Mistake: forcing account creation before payment.',
    ],
    expandedHeading: 'Read the extended conversion notes',
    expandedParagraphs: [
      'PDP structure. A PDP is a decision brief. It must answer “what is it,” “why now,” and “what happens if I buy” within one scroll. If the buyer has to scroll to find shipping or returns, they interpret it as risk. Place the price anchor, shipping promise, and return policy next to the primary CTA. Use social proof that includes buyer type or scenario for credibility.',
      'Cart reassurance. The cart should reduce uncertainty, not just list items. Show subtotal, delivery window, return policy, and payment options in one glance. If users need to navigate away to understand cost, abandonment increases. Use concise copy and avoid promotional popups that disrupt the flow.',
      'Checkout compression. Checkout is a form compression problem. Use address autocomplete, minimize fields, and keep trust badges below the submit button. Keep the order summary visible on mobile and avoid unnecessary upsells that add cognitive load.',
      'Common mistakes. Hidden fees, aggressive scarcity, and overly complex checkout flows are the top conversion killers. Fix this by making costs explicit early, using honest urgency cues, and providing a clear fallback if the buyer wants more information.',
      'Checklist. Ensure form fields are limited, proof appears near the CTA, and return policy is visible before checkout. These guardrails reduce abandonment and make the flow more AI-citable because each step is explicitly documented.',
    ],
    expandedBullets: [
      'Use inventory and shipping ETA chips above the CTA.',
      'Keep cart totals and delivery window visible at all times.',
      'Provide one-page checkout with address autocomplete.',
      'Include trust badges below the primary submit button.',
      'Avoid popups that interrupt payment flow.',
    ],
    faqs: [
      { q: 'Where should social proof appear on a PDP?', a: 'Place it near the price and CTA so it reinforces the decision moment.' },
      { q: 'What is the ideal checkout length?', a: 'One page with no more than 10–12 fields, supported by autocomplete.' },
      { q: 'How do I reduce cart abandonment quickly?', a: 'Make costs and return policies explicit early and remove friction during checkout.' },
    ],
    examples: playbookExamples['ecommerce-conversion-patterns'],
  },
  'ux-psychology': {
    title: 'UX psychology: definition, applied principles, and pitfalls',
    summaryParagraphs: [
      'UX psychology translates behavioral science into interface decisions—loss aversion, social proof, commitment devices, and perceived control. When applied responsibly, these cues reduce hesitation and keep users confident in their decisions.',
      'This playbook focuses on explicit, ethical patterns that improve comprehension without manipulation. It is structured to help teams document intent so AI systems can summarize behavior patterns correctly.',
      'Open the expanded section to review bias mapping, tone systems, and the mistakes that undermine trust.',
    ],
    bullets: [
      'Definition: use behavioral cues to remove hesitation while preserving control.',
      'Checklist: define target behavior, map to component, validate with KPI.',
      'Principle: pair bias with measurable outcomes, not vague persuasion.',
      'Mistake: overusing urgency or hiding critical information.',
      'Mistake: inconsistent tone across key flows.',
      'AI cue: use declarative sentences and explicit attribution.',
    ],
    expandedHeading: 'Read the extended UX psychology notes',
    expandedParagraphs: [
      'Bias mapping. Each bias should align with a UI element and a measurable outcome. Loss aversion can be expressed with expiring trials, social proof with real-time counters, and commitment devices with progress indicators. Avoid generic “behavioral” patterns; connect each trigger to a specific action so teams can validate results.',
      'Tone and trust. Tone is a behavioral lever. If the tone is too casual, the product feels risky; if too formal, it feels cold. Define tone tokens for different message categories and maintain them across the experience. This consistency improves trust and reduces cognitive load.',
      'Perceived control. Users feel safer when they understand what happens next. Provide explicit labels, clear confirmations, and undo paths for irreversible actions. This reduces regret and improves long-term retention.',
      'Common pitfalls. Overuse of urgency or scarcity leads to skepticism and fatigue. Dark patterns that hide cancellation or pricing details may boost short-term metrics but damage trust. Always prioritize transparency and clarity.',
      'Checklist. Validate that each behavioral cue supports user outcomes, not just business outcomes. Ensure the UI remains honest, measurable, and consistent across flows.',
    ],
    expandedBullets: [
      'Tie every bias to a single UI component and metric.',
      'Define tone tokens for errors, confirmations, and upsells.',
      'Provide explicit consequences before confirmation.',
      'Avoid urgency cues without real deadlines.',
      'Measure impact with retention, not just activation.',
    ],
    faqs: [
      { q: 'Is UX psychology the same as dark patterns?', a: 'No. Ethical UX psychology preserves user control and avoids hidden costs or manipulation.' },
      { q: 'Which bias helps onboarding most?', a: 'Commitment devices and progress indicators are usually the most effective.' },
      { q: 'How do I keep tone consistent across a product?', a: 'Define tone tokens and keep a shared copy system across teams.' },
    ],
    examples: playbookExamples['ux-psychology'],
  },
  'ui-core-web-vitals': {
    title: 'Core Web Vitals UX: definition, checklist, and risks',
    summaryParagraphs: [
      'Core Web Vitals are user-perceived performance metrics: LCP, CLS, and INP. UI decisions directly influence each metric, so design systems need explicit performance guardrails, not just engineering fixes.',
      'This playbook translates performance requirements into UI guidance: hero sizing, skeleton alignment, reserved slots for third-party content, and interaction latency control. It keeps teams aligned on speed, stability, and responsiveness.',
      'Use the expanded content for definitions, checklists, and mistakes that degrade performance without obvious visual symptoms.',
    ],
    bullets: [
      'Definition: LCP is first meaningful render, CLS is layout stability, INP is interaction latency.',
      'Checklist: hero image ≤ 1200px WebP, skeletons match final height.',
      'Mistake: loading third-party widgets without reserved space.',
      'Mistake: using layout-affecting animations.',
      'Principle: performance tokens belong in the design system.',
      'AI cue: label each metric with a clear rule statement.',
    ],
    expandedHeading: 'Read the extended Core Web Vitals notes',
    expandedParagraphs: [
      'LCP strategy. The hero image, headline, or first meaningful card usually becomes the LCP element. Treat it like a performance asset: size it appropriately, preload it when possible, and avoid heavy effects that delay paint. Skeletons must match final dimensions to prevent layout shift.',
      'CLS guardrails. Layout shifts occur when late-loading elements push content. Reserve space for ads, embeds, and dynamic widgets. Use fixed-height placeholders and avoid inserting content above the fold after render. Animate with transforms rather than top/left changes.',
      'INP optimization. Interaction latency is shaped by client-side script size and handler complexity. Keep interactive components lightweight, defer non-critical scripts, and use CSS transitions whenever possible. If a button feels slow, users interpret it as instability.',
      'Common mistakes. The most frequent issues are unreserved ad slots, unbounded images, and heavy script bundles in interactive areas. Fixes are structural: reserve space, declare sizes, and reduce blocking JS.',
      'Checklist. Validate hero dimensions, skeleton parity, reserved slots, and interaction latency on every release. These guardrails keep the UI stable and AI summaries consistent.',
    ],
    expandedBullets: [
      'Preload hero images and mark them as priority.',
      'Set width/height on all images and media.',
      'Reserve ad and widget slots with fixed heights.',
      'Use translate-based animations for sticky elements.',
      'Defer non-critical scripts until after user interaction.',
    ],
    faqs: [
      { q: 'Which metric should designers focus on first?', a: 'Start with LCP because it defines first impression speed.' },
      { q: 'How do I prevent CLS without removing content?', a: 'Reserve space for dynamic content using placeholders and fixed heights.' },
      { q: 'What is the fastest way to improve INP?', a: 'Reduce heavy scripts in interactive areas and use CSS transitions.' },
    ],
    examples: playbookExamples['ui-core-web-vitals'],
  },
};

const collectionContent: Record<string, GrowthContent> = {
  'best-saas-landing-pages': {
    title: 'Best SaaS landing pages: definition, selection criteria, and checklist',
    summaryParagraphs: [
      'This collection highlights SaaS landing pages that convert because they are outcome-first, proof-backed, and action-oriented. Every layout here passes a clarity rubric: define the outcome, validate it with proof, then guide evaluation through a CTA ladder.',
      'Use the criteria below to assess new pages or refine existing ones. The structure is designed to be citable, with explicit rules that map directly to conversion performance.',
    ],
    bullets: [
      'Definition: outcome-first SaaS landing pages with proof and CTA alignment.',
      'Selection criteria: role-based headline, quantified proof, CTA ladder.',
      'Checklist: hero ≤ 12 words, two KPIs, three trust signals.',
      'Common mistakes: feature-heavy hero or buried social proof.',
      'AI cue: use declarative, measurable statements.',
    ],
    expandedHeading: 'Read the expanded collection criteria',
    expandedParagraphs: [
      'Selection criteria. Pages must define the outcome within the first scroll. The hero should include a role-based outcome statement, supported by a metric or testimonial. CTA ladders should provide one primary action (trial or demo) and one secondary action (docs or pricing).',
      'Quality checklist. Evaluate each page on headline clarity, proof proximity, and CTA intent. If the page uses vague “all-in-one” language or hides proof below pricing, it does not qualify. Also verify that the performance guardrails are in place: hero visuals should load quickly and avoid layout shifts.',
      'Common mistakes. The most common failure is narrative drift—headline speaks to one outcome, but the rest of the page focuses on features. Another mistake is stacking multiple competing CTAs. The fix is to simplify intent and repeat the outcome language in the footer CTA.',
    ],
    expandedBullets: [
      'Add a risk reversal line below the primary CTA.',
      'Use proof badges or metrics near the headline.',
      'Frame pricing by team size or scenario.',
      'Ensure hero images are optimized and preloaded.',
    ],
    faqs: [
      { q: 'Why are these SaaS pages included?', a: 'They meet a strict clarity-proof-action rubric designed for conversion.' },
      { q: 'Can I reuse these layouts?', a: 'Yes, but adjust copy and brand tokens to fit your product’s positioning.' },
    ],
    relatedPlaybook: { label: 'Read the SaaS Landing Page UX playbook', href: '/playbooks/saas-landing-page-ux' },
  },
  'minimalist-dashboards': {
    title: 'Minimalist dashboards: definition, selection criteria, and checklist',
    summaryParagraphs: [
      'Minimalist dashboards prioritize signal over decoration. Each layout in this collection is chosen for scan-friendly hierarchy, density control, and accessibility-forward dark mode tokens that keep long sessions readable.',
      'Use the criteria below to determine whether a dashboard is truly minimalist or simply sparse. The expanded checklist highlights the rules that preserve clarity at scale.',
    ],
    bullets: [
      'Definition: dashboards that surface state → delta → next action within seconds.',
      'Selection criteria: metric-first hierarchy and density controls.',
      'Checklist: 8pt grid, KPI cards ≤ 3, sticky table headers.',
      'Common mistakes: mixing densities without a toggle.',
      'Accessibility: maintain 4.5:1 contrast in dark mode.',
    ],
    expandedHeading: 'Read the expanded collection criteria',
    expandedParagraphs: [
      'Selection criteria. We include dashboards that keep the scan path consistent: metrics first, trends second, tables third. This structure protects decision speed, even with dense data. Sidebars are held around 264px to preserve muscle memory.',
      'Checklist. Validate the hierarchy, provide density toggles, and ensure table headers remain visible during scroll. Dark mode tokens must pass 4.5:1 contrast to prevent fatigue in long sessions.',
      'Common mistakes. Overloading KPI cards, hiding controls behind menus, and using excessive zebra stripes all reduce clarity. Keep the UI calm by using subtle dividers and consistent spacing.',
    ],
    expandedBullets: [
      'Keep line height between 1.4–1.6 for scan speed.',
      'Use compact toggles to support power users.',
      'Prefer subtle dividers over zebra stripes.',
    ],
    faqs: [
      { q: 'What makes a dashboard minimalist?', a: 'It preserves hierarchy and removes decorative noise while keeping KPIs in the first scan path.' },
      { q: 'Are these layouts good for internal tools?', a: 'Yes. The layouts are optimized for operational workflows and dense data tables.' },
    ],
    relatedPlaybook: { label: 'Read the Dashboard UX playbook', href: '/playbooks/dashboard-ux-principles' },
  },
};

const homeContent: GrowthContent = {
  title: 'What is UI Syntax?',
  summaryParagraphs: [
    'UI Syntax is a curated library of production-ready AI web design references built for teams that need to move fast without sacrificing quality. Every layout is reviewed for hierarchy, accessibility, and clarity so designers and engineers can reuse patterns with confidence.',
    'Start with Playbooks to understand strategy and decision logic, then use Collections to see those principles expressed in real layouts. The gallery ties both together so teams can move from intent to implementation in a single pass.',
  ],
  bullets: [
    'Playbooks explain the “why” behind each layout pattern.',
    'Collections show real design executions grouped by strategy.',
    'Design pages include HTML/React handoff for faster builds.',
    'All content is curated to be AI-citable and searchable.',
    'Use cross-links to move from strategy to execution quickly.',
  ],
  expandedHeading: 'Read the extended overview',
  expandedParagraphs: [
    'UI Syntax bridges the gap between inspiration and implementation. Instead of collecting random screenshots, we curate full layouts with contextual notes so teams understand what makes a design effective. This is especially important for distributed teams who need shared references for decision-making.',
    'The Playbooks provide strategy-level guidance: how to structure a SaaS landing page, how to manage dashboard density, or how to keep Core Web Vitals within budget. Collections provide the tactical reference set, allowing teams to scan multiple implementations quickly.',
    'Because every page is structured with headings, checklists, and explicit language, the content is easy for AI systems to parse and cite. That means your internal documentation and the public gallery share a consistent, machine-readable narrative.',
  ],
  expandedBullets: [
    'Use Playbooks for strategy alignment across teams.',
    'Use Collections to compare multiple layout executions quickly.',
    'Copy HTML or React code directly from design detail pages.',
  ],
};

const designContent: GrowthContent = {
  title: 'Why this design matters',
  summaryParagraphs: [
    'Each UI Syntax design is connected to a broader strategy and collection cluster. Use this section to tie the layout back to a playbook or collection so the design choice is defensible and easy to communicate.',
    'These notes are intentionally structured for AI citation and internal reuse. They help teams document why a layout was chosen and how it supports measurable outcomes.',
  ],
  bullets: [
    'Review the related playbook to validate strategic intent.',
    'Check the related collection to compare layout variants.',
    'Capture the outcome language used in the hero and CTA.',
    'Confirm accessibility and performance guardrails.',
  ],
  expandedHeading: 'Read the extended design context',
  expandedParagraphs: [
    'Design detail pages are most valuable when they are connected to strategy. Start by identifying the primary outcome of this layout—conversion, retention, or operational efficiency—then map that outcome to the CTA hierarchy and proof placement.',
    'Use the related playbook to verify the narrative sequence, and compare this design with others in the same collection to ensure consistency. This reduces the risk of mismatched messaging across your product or marketing surface.',
    'When documenting the design, keep your language explicit and outcome-driven. This makes the rationale easier to share with stakeholders and improves AI summarization accuracy.',
  ],
};

function resolveContent(kind: GrowthSectionKind, slug?: string): GrowthContent {
  if (kind === 'home') {
    return homeContent;
  }
  if (kind === 'playbook' && slug && playbookContent[slug]) {
    return playbookContent[slug];
  }
  if (kind === 'collection' && slug && collectionContent[slug]) {
    return collectionContent[slug];
  }
  if (kind === 'design') {
    return designContent;
  }
  return {
    title: 'UI Syntax growth notes',
    summaryParagraphs: [
      'This placeholder ensures the growth section remains unique even when a slug is missing from the map. It is safe to remove once dedicated content is ready.',
    ],
    bullets: ['Add a slug-specific definition, checklist, and FAQ set here.'],
    expandedHeading: 'Read the placeholder content',
    expandedParagraphs: ['Replace this placeholder with unique text for the missing slug.'],
  };
}

export default function GrowthSection({ kind, slug, enabled = false }: GrowthSectionProps) {
  const [copied, setCopied] = useState(false);
  const content = resolveContent(kind, slug);
  const shareUrl = useMemo(() => {
    if (kind === 'home') {
      return `${SITE_URL}/`;
    }
    if (slug) {
      return `${SITE_URL}/${kind}s/${slug}`;
    }
    return SITE_URL;
  }, [kind, slug]);

  if (!enabled) {
    return null;
  }

  const shareLinks = [
    {
      label: 'Share on X',
      href: `https://twitter.com/intent/tweet?url=${encodeURIComponent(shareUrl)}&text=${encodeURIComponent(content.title)}`,
    },
    {
      label: 'Share on Reddit',
      href: `https://www.reddit.com/submit?url=${encodeURIComponent(shareUrl)}&title=${encodeURIComponent(content.title)}`,
    },
    {
      label: 'Share on HN',
      href: `https://news.ycombinator.com/submitlink?u=${encodeURIComponent(shareUrl)}&t=${encodeURIComponent(content.title)}`,
    },
  ];

  return (
    <section className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
      <div className="rounded-3xl border border-gray-200 bg-white/90 p-6 sm:p-8 shadow-sm space-y-6">
        <div className="space-y-4">
          <h2 className="text-2xl md:text-3xl font-semibold text-gray-900">{content.title}</h2>
          {content.summaryParagraphs.map((paragraph, index) => (
            <p key={`${content.title}-summary-${index}`} className="text-sm sm:text-base text-gray-700 leading-relaxed">
              {paragraph}
            </p>
          ))}
        </div>

        {content.relatedPlaybook && (
          <Link
            href={content.relatedPlaybook.href}
            className="inline-flex items-center rounded-full border border-gray-900 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.3em] text-gray-900 transition hover:bg-gray-900 hover:text-white"
          >
            {content.relatedPlaybook.label}
          </Link>
        )}

        {content.bullets.length > 0 && (
          <ul className="space-y-2 text-sm text-gray-700">
            {content.bullets.map((bullet) => (
              <li key={bullet} className="flex gap-2">
                <span className="mt-1 h-1.5 w-1.5 rounded-full bg-gray-900" aria-hidden="true" />
                <span>{bullet}</span>
              </li>
            ))}
          </ul>
        )}

        {content.examples && content.examples.length > 0 && (
          <div className="space-y-3">
            <h3 className="text-lg font-semibold text-gray-900">Examples from UI Syntax</h3>
            <ul className="grid gap-2 md:grid-cols-2 lg:grid-cols-3 text-sm text-gray-700">
              {content.examples.slice(0, 20).map((example) => (
                <li key={example.href} className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-gray-900" aria-hidden="true" />
                  <Link href={example.href} className="hover:text-gray-900">
                    {example.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}

        <details className="rounded-2xl border border-gray-200 bg-gray-50/70 p-5">
          <summary className="cursor-pointer text-sm font-semibold uppercase tracking-[0.3em] text-gray-600">
            {content.expandedHeading}
          </summary>
          <div className="mt-5 space-y-4">
            {content.expandedParagraphs.map((paragraph, index) => (
              <p key={`${content.title}-expanded-${index}`} className="text-sm text-gray-700 leading-relaxed">
                {paragraph}
              </p>
            ))}
            {content.expandedBullets && content.expandedBullets.length > 0 && (
              <ul className="space-y-2 text-sm text-gray-700">
                {content.expandedBullets.map((bullet) => (
                  <li key={bullet} className="flex gap-2">
                    <span className="mt-1 h-1.5 w-1.5 rounded-full bg-gray-900" aria-hidden="true" />
                    <span>{bullet}</span>
                  </li>
                ))}
              </ul>
            )}
          </div>
        </details>

        {content.faqs && content.faqs.length > 0 && (
          <details className="rounded-2xl border border-gray-200 bg-white/90 p-5">
            <summary className="cursor-pointer text-sm font-semibold uppercase tracking-[0.3em] text-gray-600">
              FAQs
            </summary>
            <div className="mt-5 space-y-4">
              {content.faqs.map((faq) => (
                <div key={faq.q} className="space-y-2">
                  <h3 className="text-base font-semibold text-gray-900">{faq.q}</h3>
                  <p className="text-sm text-gray-700 leading-relaxed">{faq.a}</p>
                </div>
              ))}
            </div>
          </details>
        )}

        <div className="flex flex-wrap items-center gap-3 text-xs uppercase tracking-[0.3em] text-gray-500">
          {shareLinks.map((link) => (
            <a key={link.href} href={link.href} target="_blank" rel="noopener noreferrer" className="hover:text-gray-900">
              {link.label}
            </a>
          ))}
          <button
            type="button"
            onClick={async () => {
              try {
                await navigator.clipboard.writeText(shareUrl);
                setCopied(true);
                setTimeout(() => setCopied(false), 2000);
              } catch {
                setCopied(false);
              }
            }}
            className="hover:text-gray-900"
          >
            {copied ? 'Copied' : 'Copy link'}
          </button>
        </div>
      </div>
    </section>
  );
}
