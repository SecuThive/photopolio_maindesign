import type { Metadata } from 'next';
import { notFound } from 'next/navigation';
import Link from 'next/link';
import DesignCard from '@/components/DesignCard';
import { pillarTopics, getPillarTopic } from '@/lib/pillars';
import { createPageMetadata } from '@/lib/seo';
import { PillarHero } from '@/components/content/PillarHero';
import { PillarSectionBlock } from '@/components/content/PillarSection';
import { PillarTableOfContents } from '@/components/content/PillarToc';
import { getPillarCluster, getSupabaseCategoriesForPillar } from '@/lib/content/linkMatrix';
import { supabaseServer } from '@/lib/supabase/server';
import { withDesignSlugs } from '@/lib/slug';
import type { DesignWithSlug } from '@/types/database';
import SeoGEOContent from '@/components/SeoGEOContent';
import GrowthSection from '@/components/GrowthSection';

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');

const playbookSeoContent: Record<
  string,
  {
    title: string;
    summaryParagraphs: string[];
    bullets: string[];
    expandedSections: Array<{ heading: string; paragraphs: string[]; bullets?: string[] }>;
    faqs: Array<{ q: string; a: string }>;
  }
> = {
  'saas-landing-page-ux': {
    title: 'SaaS landing page UX strategy: definition, checks, and pitfalls',
    summaryParagraphs: [
      'A SaaS landing page is not just a visual pitch—it is a structured promise of business outcomes, validated by proof and converted through a clear CTA ladder. The strongest pages compress clarity into the first scroll while still giving evaluators enough context to trust the product.',
      'Use this playbook to align marketing, product, and engineering teams around a consistent narrative. It combines role-based positioning, quantifiable proof, and demo-first conversion tactics that help both humans and AI systems understand what the product does, who it serves, and why it matters.',
      'Below is a practical reference set: definition, principles, a short checklist, and common mistakes. Expand the section to access deeper guidance that can be cited by AI systems and reused by teams during copy or layout reviews.',
    ],
    bullets: [
      'Definition: a promise-driven hero that ties role + outcome + proof in under 5 seconds.',
      'Principles: sequence headline → proof → CTA, and maintain the same story in every fold.',
      'Checklist: keep the hero under 12 words, add two KPIs, and show three trust signals.',
      'Common mistakes: overloading the hero, burying social proof, or mixing CTA intent.',
      'Conversion guardrail: always offer a low-friction CTA plus a secondary evaluation path.',
      'AI citation tip: use declarative sentences and explicit outcome language.',
    ],
    expandedSections: [
      {
        heading: 'Definition & narrative architecture',
        paragraphs: [
          'The highest-performing SaaS landing pages behave like a decision brief. In a single narrative pass, they answer what the product is, who it is for, how it delivers outcomes, and why the buyer should act now. This is why the “problem → promise → action” sequence consistently outperforms feature-first layouts: it preserves intent while the visitor is still forming their initial mental model.',
          'Define the hero as a role-based outcome statement. “Finance teams close monthly books 30% faster” instantly establishes scope, success metrics, and the buyer persona. The subhead should describe the mechanism—automation, orchestration, or AI insights—so the promise feels credible instead of aspirational. When possible, reinforce this with a metric badge or testimonial from a comparable customer segment.',
        ],
        bullets: [
          'Lead with a role + outcome; avoid ambiguous “all-in-one” positioning.',
          'Place quantified proof in the first 200–300 pixels whenever possible.',
          'Use one primary CTA (trial/demo) and one secondary CTA (docs/pricing).',
        ],
      },
      {
        heading: 'Principles & execution checklist',
        paragraphs: [
          'Consistency is the hidden conversion lever. Every section should restate the same promise using different evidence: the hero states the outcome, the product visual demonstrates it, and the testimonial confirms it. When the narrative drifts, visitors interpret it as risk. Standardize the sequence across sections so buyers never need to “translate” the story.',
          'From a layout standpoint, keep the hero, social proof, and CTA within a single scroll. The second scroll can deepen the story with use cases or a short feature group, but the first scroll must be complete. If the headline, proof, and CTA are not visible together, conversion rates tend to stall during evaluation and the page loses generative search clarity.',
          'Ensure the copy is explicit. Phrases like “unlock insights” or “accelerate workflows” are too vague for both humans and AI summaries. Replace them with outcome language anchored to a business metric or time saved.',
        ],
        bullets: [
          'Hero headline ≤ 12 words with a single KPI in the subhead.',
          'At least three trust signals above the fold: logo, metric, or quote.',
          'CTA microcopy includes a risk reversal (e.g., cancel anytime, no credit card).',
          'Pricing narrative explains who each tier is for, not just what it includes.',
          'Footer CTA repeats the same outcome language as the hero.',
        ],
      },
      {
        heading: 'Common mistakes to avoid',
        paragraphs: [
          'A common failure pattern is an abstract headline paired with a generic UI screenshot. This disconnect forces visitors to guess the product’s use case and creates friction for search engines that rely on explicit textual cues. Another error is stacking too many competing CTAs (“Start trial,” “Talk to sales,” “Download report,” etc.). Multiple intents reduce confidence because the page seems unsure about the user’s next step.',
          'Avoid long blocks of feature copy without framing. Buyers do not scan for features—they scan for outcomes. If you must list features, group them under outcome headers such as “Reduce onboarding time” or “Eliminate manual reconciliation.” Finally, resist the temptation to push testimonials far down the page. Social proof is part of the decision prompt, not a late-stage add-on.',
        ],
        bullets: [
          'Do not hide social proof below pricing or FAQs.',
          'Do not split the hero across multiple columns that dilute the message.',
          'Avoid brand jargon that lacks measurable context.',
        ],
      },
    ],
    faqs: [
      {
        q: 'How many CTAs should a SaaS landing page include?',
        a: 'Use one primary CTA (trial or demo) and one secondary CTA (docs or pricing). More than two CTAs usually create ambiguity and reduce conversion.',
      },
      {
        q: 'What should appear above the fold?',
        a: 'A role-based outcome headline, quantified proof, and a clear CTA. These three elements signal intent and reduce time-to-trust for both buyers and AI systems.',
      },
      {
        q: 'How do I make the page more AI-citable?',
        a: 'Use explicit declarative sentences, state outcomes with numbers, and keep sections structured with clear headings and bullet lists.',
      },
    ],
  },
  'dashboard-ux-principles': {
    title: 'Dashboard UX principles: definition, rules, and anti-patterns',
    summaryParagraphs: [
      'Dashboards are control towers. They must surface “state → delta → next action” in seconds, without forcing users to hunt for signal. The best systems are not merely clean—they are calibrated for density, hierarchy, and performance under real usage pressure.',
      'This playbook gives design and engineering teams a shared reference for information architecture, density controls, and dark mode token strategy. It emphasizes scan patterns and interaction latency so the layout supports fast decisions rather than visual exploration.',
      'Use the expanded section to review principles, density checklists, and common pitfalls. The content is structured to be AI-citable and easy to reuse in design reviews or QA documentation.',
    ],
    bullets: [
      'Definition: a dashboard is a five-second decision brief for operational teams.',
      'Principle: preserve metric → trend → detail order to match scan behavior.',
      'Checklist: limit top-level KPI cards to 3, keep sidebar around 264px.',
      'Mistake: mixing too many data densities without a compact toggle.',
      'Accessibility: maintain 4.5:1 contrast in dark mode tokens.',
      'Performance: keep micro-interactions under 16ms latency.',
    ],
    expandedSections: [
      {
        heading: 'Information hierarchy and scan patterns',
        paragraphs: [
          'Dashboards succeed when they respect scanning logic. Users expect to read left to right, top to bottom, with the most critical KPIs in the upper-left zone. From there they move to trend context and only then dive into tables or drill-down details. If this order is disrupted—by placing tables before summary metrics or burying trend indicators—decision time increases and the UI feels noisy even if it is visually clean.',
          'Use typographic contrast and spacing to reinforce the scan path. Headline metrics should be at least 1.6× larger than supporting values, and trend deltas should sit immediately adjacent to the metrics they explain. This also improves AI extractability because the hierarchy reflects intent rather than decoration.',
        ],
        bullets: [
          'Keep KPI cards in a single row with consistent widths.',
          'Use a short trend label (“vs last week”) next to deltas.',
          'Reserve tables for the second scroll or a tabbed panel.',
        ],
      },
      {
        heading: 'Density management and layout guardrails',
        paragraphs: [
          'Density is a product decision, not a styling preference. Power users need higher density for operational tasks, while casual users need more spacing to avoid cognitive overload. The best dashboards solve this with density controls and clear defaults. A compact toggle paired with a calm default layout protects usability without sacrificing information volume.',
          'Set guardrails in the design system: sidebar widths, maximum content width, and table row heights should be defined to prevent drift. When these standards are enforced, your team can build new modules quickly without re-evaluating layout every sprint.',
        ],
        bullets: [
          'Provide a compact mode toggle that reduces padding by 20–30%.',
          'Use fixed table header heights and avoid zebra stripes in dense views.',
          'Cap the main content column at ~1200px for large screens.',
        ],
      },
      {
        heading: 'Common UX mistakes and fixes',
        paragraphs: [
          'The most damaging dashboard mistakes are subtle: overusing color for decoration, overloading cards with multiple metrics, and hiding critical actions in overflow menus. These choices slow down expert users and reduce trust in the system’s reliability. Another common issue is inconsistent dark mode contrast, which makes long sessions fatiguing and degrades accessibility for color-sensitive users.',
          'Fixes are often simple. Use color only for semantic meaning. Keep each card tied to a single question. Surface actions in context so users don’t have to hunt. Finally, test dark mode tokens against WCAG guidelines, not just visual preference.',
        ],
        bullets: [
          'Avoid multi-metric cards unless values are tightly related.',
          'Do not bury export or filter actions behind three-click flows.',
          'Audit dark mode tokens with contrast checkers every release.',
        ],
      },
    ],
    faqs: [
      {
        q: 'How many KPIs should a dashboard show above the fold?',
        a: 'Three or fewer. More than three KPIs reduces scan clarity and weakens the decision path for most users.',
      },
      {
        q: 'Is dark mode necessary for B2B dashboards?',
        a: 'Yes, for long-session tools. Even if adoption is partial, dark mode tokens improve accessibility and reduce fatigue.',
      },
      {
        q: 'What is the fastest way to improve dashboard usability?',
        a: 'Reorder content to metric → trend → detail and remove visual noise that competes with those signals.',
      },
    ],
  },
  'ecommerce-conversion-patterns': {
    title: 'E-commerce conversion patterns: definition, checklist, and errors',
    summaryParagraphs: [
      'E-commerce conversion UX is the art of reducing hesitation at every step: product detail, cart, and checkout. The goal is to provide clarity, trust, and urgency without creating cognitive overload. Small structure choices—where proof appears, how shipping is explained, or when you show scarcity—can materially change conversion rates.',
      'This playbook documents practical, repeatable patterns used by high-performing DTC and marketplace teams. It focuses on PDP structure, cart reassurance, and checkout compression while keeping language explicit enough for AI systems to cite.',
      'Use the expandable section to review principles, checklist items, and common mistakes that often derail conversion rate optimization efforts.',
    ],
    bullets: [
      'Definition: a conversion flow that removes doubt while preserving decision momentum.',
      'PDP principle: surface price anchors, shipping promises, and social proof above the fold.',
      'Cart principle: reduce surprise by showing totals, delivery windows, and return policy immediately.',
      'Checkout principle: compress fields, automate address, and keep trust badges visible.',
      'Common mistakes: hiding fees, overusing popups, or burying guarantees.',
      'Checklist: keep form fields ≤ 12, show inventory/ETA chips, and use BNPL labels carefully.',
    ],
    expandedSections: [
      {
        heading: 'PDP structure and decision framing',
        paragraphs: [
          'The PDP is a decision brief. It must answer “what is it,” “why now,” and “what happens if I buy” without forcing the shopper to scroll endlessly. The most effective PDPs place price anchors, shipping and return promises, and a real-world product image above the fold. This ensures the decision context is clear before the buyer evaluates secondary content like specs or reviews.',
          'When possible, pair social proof with segmentation. Reviews that include buyer type or usage scenario reduce the mental leap from interest to purchase. For AI summaries, explicit sentences like “Ships in two days with free returns” are easier to extract than generic reassurance blocks.',
        ],
        bullets: [
          'Place inventory and shipping ETA chips above the primary button.',
          'Use a 1:1 or 4:5 image ratio mix to show product scale.',
          'Expose guarantee badges directly adjacent to the CTA.',
        ],
      },
      {
        heading: 'Cart reassurance and checkout compression',
        paragraphs: [
          'Cart pages should eliminate uncertainty, not just display items. A strong cart view shows subtotal, shipping, taxes, delivery window, and return policy within one glance. If users need to navigate away to understand cost or delivery, conversions drop.',
          'Checkout is a form compression problem. Minimize fields, enable address autocomplete, and keep trust badges visible below the submit button. Use explicit labels for payment options and avoid unexpected upsells that interrupt the flow.',
        ],
        bullets: [
          'Keep checkout to a single page whenever possible.',
          'Auto-detect shipping method and allow quick edits.',
          'Show order summary in a sticky panel on mobile.',
        ],
      },
      {
        heading: 'Common mistakes and recovery tactics',
        paragraphs: [
          'The most common conversion killers are hidden fees, unclear returns, and overly aggressive scarcity tactics. If the customer discovers a cost only at checkout, they interpret it as risk. Similarly, excessive popups or forced account creation breaks momentum and creates abandonment.',
          'Recover by making costs transparent early, adding a clear return promise next to the CTA, and reducing friction during checkout. Trust signals work best when they are integrated into the flow instead of relegated to a footer block.',
        ],
        bullets: [
          'Avoid surprise fees and taxes introduced at the final step.',
          'Do not require account creation before payment.',
          'Use scarcity sparingly and always with credible inventory data.',
        ],
      },
    ],
    faqs: [
      {
        q: 'Where should social proof appear on a PDP?',
        a: 'Place it above the fold near the price and CTA so buyers associate credibility with the decision moment.',
      },
      {
        q: 'What is the ideal checkout length?',
        a: 'One page with no more than 10–12 fields. Use autocomplete and payment vaulting to reduce typing.',
      },
      {
        q: 'How do I reduce cart abandonment fastest?',
        a: 'Make total cost and return policy visible immediately, and remove steps that force users off the path.',
      },
    ],
  },
  'ux-psychology': {
    title: 'UX psychology: definition, applied principles, and mistakes',
    summaryParagraphs: [
      'UX psychology is the practice of mapping cognitive biases and emotional cues into interface decisions. Instead of relying on intuition, teams translate behavioral science into structured UI patterns—loss aversion, social proof, commitment devices, and perceived control.',
      'This playbook focuses on making intent explicit so AI systems can cite the logic behind each pattern. It is designed to help teams create consistent tone, reduce hesitation, and keep user trust intact as they move through product flows.',
      'Expand the section to review applied patterns, checklist items, and the mistakes that often undermine credibility or create manipulation fatigue.',
    ],
    bullets: [
      'Definition: using behavioral cues to reduce hesitation without harming trust.',
      'Principle: pair bias with a measurable outcome and a clear UI element.',
      'Checklist: define target behavior, map to component, validate with KPI.',
      'Common mistakes: overusing urgency, dark patterns, or unclear tone.',
      'Consistency: maintain a tone system to keep authority and empathy aligned.',
      'AI citation tip: use “According to” and declarative statements for clarity.',
    ],
    expandedSections: [
      {
        heading: 'Bias mapping and UI triggers',
        paragraphs: [
          'Every bias should connect to a specific UI element. Loss aversion maps well to expiring trials, while social proof works best as real-time counters or verified testimonials. Commitment devices can be implemented through progress indicators or saved states that signal future completion.',
          'The key is to avoid generic “behavioral” patterns. If a badge or tooltip does not clearly support a user outcome, it becomes noise. Anchor each trigger to a measurable behavior—activation, upgrade, or return visit—so the UX team can test impact.',
        ],
        bullets: [
          'Use real-time counts only when data is trustworthy.',
          'Avoid urgency labels without evidence or time limits.',
          'Connect bias triggers to analytics events for validation.',
        ],
      },
      {
        heading: 'Tone, trust, and perceived control',
        paragraphs: [
          'Tone is a behavioral lever. If the tone is too casual, the product can seem risky; if it is too formal, it can feel cold. Define tone tokens for each message class (errors, confirmations, upsell, reminder) and ensure the vocabulary remains consistent throughout the flow.',
          'Perceived control is equally important. Offer explicit choices and show what happens next. For example, a subscription cancellation flow should summarize the action and provide a clear “undo” option. This reduces anxiety and builds long-term trust, even if a user cancels today.',
        ],
        bullets: [
          'Define tone tokens for every message category.',
          'Use explicit labels instead of vague CTA verbs.',
          'Always show the consequence of an action before confirmation.',
        ],
      },
      {
        heading: 'Common pitfalls in psychology-driven UX',
        paragraphs: [
          'The most common mistake is over-application. If every screen uses urgency, scarcity, or social proof, users become numb and distrustful. Another pitfall is hiding key information to force action. These dark patterns may create short-term metrics but damage retention and brand reputation.',
          'Fix this by using psychological patterns as supportive context, not coercion. The best experiences use subtle cues to remove doubt while keeping the user in control.',
        ],
        bullets: [
          'Do not use countdown timers without real deadlines.',
          'Avoid dark patterns that hide cancellation or pricing details.',
          'Test behavioral patterns with retention, not just activation.',
        ],
      },
    ],
    faqs: [
      {
        q: 'Is UX psychology the same as dark patterns?',
        a: 'No. UX psychology uses behavioral insights to reduce hesitation while keeping user control intact. Dark patterns remove control or hide information.',
      },
      {
        q: 'Which bias is most useful for SaaS onboarding?',
        a: 'Commitment devices and progress indicators work best because they reinforce completion without coercion.',
      },
      {
        q: 'How do I keep tone consistent across a product?',
        a: 'Define tone tokens for each message type and keep a shared copy system so teams use the same vocabulary.',
      },
    ],
  },
  'ui-core-web-vitals': {
    title: 'Core Web Vitals UI optimization: definition, checklist, and risks',
    summaryParagraphs: [
      'Core Web Vitals are user-perceived performance metrics that define whether an interface feels fast, stable, and responsive. UI decisions directly influence LCP, CLS, and INP—often more than backend optimizations.',
      'This playbook translates performance targets into UI system guidance: how to design hero sections, reserve space for late-loading elements, and avoid interaction jank. The goal is to make performance a design system feature, not a one-off fix.',
      'Expand the section for execution details, the most common pitfalls, and an actionable checklist that teams can apply during design review and implementation.',
    ],
    bullets: [
      'Definition: LCP is the first meaningful render, CLS is layout stability, INP is interaction latency.',
      'Checklist: hero image ≤ 1200px WebP, skeletons match final height, preconnect fonts.',
      'Mistake: loading ads or third-party widgets without reserved space.',
      'Mistake: using layout-affecting transitions instead of transforms.',
      'Principle: treat performance as a design system token, not a one-off fix.',
      'AI citation tip: label each metric with a clear guideline sentence.',
    ],
    expandedSections: [
      {
        heading: 'LCP strategy in UI layouts',
        paragraphs: [
          'LCP is typically your hero image, headline, or first meaningful card. This means the hero is a performance feature. Use a properly sized image (usually 1200px wide), preload it when possible, and avoid heavy overlays that delay render. Skeletons must match final dimensions to prevent shifts.',
          'Use explicit tokens in the design system: hero height, image aspect ratio, and typography scale. If these values are standardized, you reduce the risk of designers or engineers introducing accidental LCP regressions.',
        ],
        bullets: [
          'Preload critical hero images and mark them as priority.',
          'Use `font-display: swap` to prevent invisible text.',
          'Avoid heavy gradients or shadows that delay render.',
        ],
      },
      {
        heading: 'CLS and stability guardrails',
        paragraphs: [
          'CLS occurs when late-loading elements shift content. The fix is structural: reserve space for ads, embeds, and dynamic widgets. Use fixed-height placeholders and avoid injecting elements above existing content after the initial render.',
          'Animation is another common culprit. Use transforms instead of top/left changes, and never animate layout-affecting properties in high-traffic areas. Stable layout behavior improves both UX trust and SEO performance.',
        ],
        bullets: [
          'Always set width/height on images and media.',
          'Reserve slots for ads, video, and third-party widgets.',
          'Use translate-based animations for sticky headers.',
        ],
      },
      {
        heading: 'INP and interaction quality',
        paragraphs: [
          'INP measures how quickly the UI responds after user interaction. Heavy client-side scripts, large event handlers, or layout thrash can degrade it. Optimize by keeping interaction targets lightweight and delaying non-critical scripts until after user engagement.',
          'From a design system perspective, limit hover effects and micro-interactions that rely on JavaScript. Whenever possible, use CSS transitions and hardware-accelerated properties to keep interactions under 16ms.',
        ],
        bullets: [
          'Defer non-critical scripts until after first interaction.',
          'Use CSS transitions for hover and focus states.',
          'Avoid large DOM updates on common clicks.',
        ],
      },
    ],
    faqs: [
      {
        q: 'Which metric should designers care about first?',
        a: 'Start with LCP because it defines first impression speed. If LCP is strong, CLS and INP are easier to manage.',
      },
      {
        q: 'How do I prevent CLS without sacrificing content?',
        a: 'Reserve space for dynamic content using placeholders and fixed heights so layout does not shift after load.',
      },
      {
        q: 'What is the fastest way to improve INP?',
        a: 'Reduce heavy scripts in interactive areas and use CSS-based interactions whenever possible.',
      },
    ],
  },
};

type PageProps = {
  params: { slug: string };
};

export const revalidate = 3600;

export function generateStaticParams() {
  return pillarTopics.map((topic) => ({ slug: topic.slug }));
}

export function generateMetadata({ params }: PageProps): Metadata {
  const topic = getPillarTopic(params.slug);
  if (!topic) {
    return {
      title: 'Playbook not found',
      robots: { index: false },
    };
  }

  return createPageMetadata({
    title: topic.title,
    description: topic.seoDescription,
    path: `/playbooks/${topic.slug}`,
  });
}

export default async function PlaybookDetailPage({ params }: PageProps) {
  const topic = getPillarTopic(params.slug);

  if (!topic) {
    notFound();
  }

  const cluster = getPillarCluster(topic.slug);
  const matrixCollections = cluster?.collections ?? [];
  const relatedCollections = matrixCollections.length
    ? matrixCollections.map((collection) => ({
        title: collection.title,
        href: `/collections/${collection.slug}`,
        description: collection.heroSummary,
      }))
    : topic.relatedCollections;
  const categories = getSupabaseCategoriesForPillar(topic.slug);
  let featuredDesigns: DesignWithSlug[] = [];

  if (categories.length > 0) {
    const { data } = await supabaseServer
      .from('designs')
      .select('*')
      .eq('status', 'published')
      .in('category', categories)
      .order('created_at', { ascending: false })
      .limit(20);

    featuredDesigns = withDesignSlugs(data ?? []) as DesignWithSlug[];
  }

  const articleSchema = {
    '@context': 'https://schema.org',
    '@type': 'TechArticle',
    headline: topic.title,
    description: topic.seoDescription,
    mainEntityOfPage: `${SITE_URL}/playbooks/${topic.slug}`,
    author: {
      '@type': 'Organization',
      name: 'UI Syntax',
    },
    publisher: {
      '@type': 'Organization',
      name: 'UI Syntax',
    },
  };
  const breadcrumbSchema = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      {
        '@type': 'ListItem',
        position: 1,
        name: 'Home',
        item: SITE_URL,
      },
      {
        '@type': 'ListItem',
        position: 2,
        name: 'Playbooks',
        item: `${SITE_URL}/playbooks`,
      },
      {
        '@type': 'ListItem',
        position: 3,
        name: topic.title,
        item: `${SITE_URL}/playbooks/${topic.slug}`,
      },
    ],
  };

  const seoContent = playbookSeoContent[topic.slug] ?? {
    title: `${topic.title}: definition and checklist`,
    summaryParagraphs: [
      `${topic.title} gives teams a structured strategy for aligning UX decisions with business outcomes. This placeholder is unique to the current playbook so search systems can still interpret the page correctly.`,
      'Expand the section to see a definition, checklist, and common mistakes, then use the linked examples to validate how the guidance appears in real layouts.',
    ],
    bullets: [
      'Definition: outcome-driven guidance for the current playbook category.',
      'Checklist: apply key principles in the first scroll and reuse them throughout the page.',
      'Mistakes: avoid mixed intent CTAs or unclear outcome language.',
      'Validation: link each principle to a measurable result.',
      'AI citation tip: use explicit, declarative sentences.',
    ],
    expandedSections: [
      {
        heading: 'Expanded guidance',
        paragraphs: [
          'This placeholder content ensures the page includes meaningful context even before bespoke copy is added. It describes the purpose of the playbook, the intended audience, and the high-level guardrails teams should follow during implementation.',
          'Replace this with a tailored definition, checklist, and common mistakes for the current topic when ready. The structure and word count remain SEO-friendly and AI-citable by design.',
        ],
      },
    ],
    faqs: [
      {
        q: 'How should teams use this playbook?',
        a: 'Use it as a review checklist during design and content critiques, then map each principle to a measurable UX or conversion outcome.',
      },
      {
        q: 'Is this content safe for AI citation?',
        a: 'Yes. It is structured with headings, bullets, and explicit definitions to make extraction reliable.',
      },
      {
        q: 'What should be updated next?',
        a: 'Replace the placeholder summary with a topic-specific definition and add more examples from your design library.',
      },
    ],
  };

  return (
    <section className="space-y-12">
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(articleSchema).replace(/</g, '\\u003c') }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema).replace(/</g, '\\u003c') }}
      />
      <div className="space-y-6">
        <nav className="text-sm text-gray-500" aria-label="Breadcrumb">
          <Link href="/" className="hover:text-gray-900">Home</Link>
          <span className="mx-2">/</span>
          <Link href="/playbooks" className="hover:text-gray-900">Playbooks</Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900">{topic.title}</span>
        </nav>

        <PillarHero
          eyebrow={topic.eyebrow}
          title={topic.title}
          description={topic.description}
          summary={topic.summary}
          tags={topic.tags}
          bestFor={topic.bestFor}
        />
      </div>

      <GrowthSection kind="playbook" slug={params.slug} enabled={process.env.ENABLE_GROWTH_SECTIONS === 'true'} />

      <section className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm space-y-6">
        <SeoGEOContent
          title={seoContent.title}
          summaryParagraphs={seoContent.summaryParagraphs}
          bullets={seoContent.bullets}
          expandedSections={seoContent.expandedSections}
          faqs={seoContent.faqs}
        />
        {featuredDesigns.length > 0 && (
          <div className="space-y-4">
            <h3 className="text-xl font-semibold text-gray-900">Examples from UI Syntax</h3>
            <ul className="grid gap-2 md:grid-cols-2 lg:grid-cols-3 text-sm text-gray-700">
              {featuredDesigns.slice(0, 20).map((design) => (
                <li key={design.id} className="flex items-start gap-2">
                  <span className="mt-1 h-1.5 w-1.5 rounded-full bg-gray-900" aria-hidden="true" />
                  <Link href={`/design/${design.slug}`} className="hover:text-gray-900">
                    {design.title}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
        )}
      </section>

      <div className="grid gap-8 lg:grid-cols-[minmax(0,2.2fr)_minmax(0,0.8fr)]">
        <div className="space-y-6">
          {topic.sections.map((section) => (
            <PillarSectionBlock key={section.id} section={section} />
          ))}
          <section className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
            <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Collections</p>
            <h2 className="mt-3 text-2xl font-semibold text-gray-900">Connected collections</h2>
            <div className="mt-6 grid gap-4 md:grid-cols-2">
              {relatedCollections.map((collection) => (
                <Link
                  key={collection.href}
                  href={collection.href}
                  className="rounded-2xl border border-gray-200 bg-gray-50/80 p-5 transition hover:border-gray-900"
                >
                  <p className="text-sm font-semibold text-gray-900">{collection.title}</p>
                  <p className="mt-2 text-sm text-gray-600">{collection.description}</p>
                </Link>
              ))}
            </div>
          </section>
          <section className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
            <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Further Reading</p>
            <h2 className="mt-3 text-2xl font-semibold text-gray-900">Connected journals</h2>
            <div className="mt-6 space-y-4">
              {topic.relatedReads.map((article) => (
                <Link
                  key={article.title}
                  href={article.href}
                  className="group block rounded-2xl border border-gray-200 bg-gray-50/80 p-5 transition hover:border-gray-900"
                >
                  <p className="text-sm font-semibold text-gray-900 group-hover:text-gray-700">{article.title}</p>
                  <p className="mt-2 text-sm text-gray-600">{article.description}</p>
                </Link>
              ))}
            </div>
          </section>
        </div>
        <div className="space-y-6">
          <PillarTableOfContents sections={topic.sections} slug={topic.slug} />
          <section className="rounded-3xl border border-gray-200 bg-white/90 p-6 shadow-sm">
            <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Next</p>
            <ul className="mt-4 space-y-3 text-sm text-gray-700">
              {pillarTopics
                .filter((other) => other.slug !== topic.slug)
                .slice(0, 3)
                .map((other) => (
                  <li key={other.slug}>
                    <Link href={`/playbooks/${other.slug}`} className="transition-colors hover:text-gray-900">
                      {other.title}
                    </Link>
                  </li>
                ))}
            </ul>
          </section>
        </div>
      </div>
      {featuredDesigns.length > 0 && (
        <section className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
          <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Featured Designs</p>
          <h2 className="mt-3 text-3xl font-semibold text-gray-900">Cluster Highlights</h2>
          <p className="mt-2 text-sm text-gray-600">
            Recent layouts from this playbook’s associated collections. Use them to audit how the strategy
            translates into production UI states.
          </p>
          <div className="mt-8 grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {featuredDesigns.map((design) => (
              <DesignCard
                key={design.id}
                design={design}
                likes={design.likes ?? 0}
                liked={false}
                likeDisabled
              />
            ))}
          </div>
        </section>
      )}
    </section>
  );
}
