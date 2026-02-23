type DesignEditorialSectionProps = {
  title: string;
  description?: string;
  features?: string[];
  usage?: string;
  category?: string;
  tags?: string[];
  colors?: string[];
  hasReactCode: boolean;
  hasHtmlCode: boolean;
};

type CategoryKey = 'landing-page' | 'dashboard' | 'e-commerce' | 'portfolio' | 'blog' | 'component' | 'general';

type CategoryTemplate = {
  why: string[];
  bestForExamples: string[];
  fallbackTakeaways: string[];
  accessibilityChecklist: string[];
  implementationChecklist: string[];
};

const CATEGORY_TEMPLATES: Record<CategoryKey, CategoryTemplate> = {
  'landing-page': {
    why: [
      'Landing page patterns convert best when one core value proposition is repeated in the hero, proof blocks, and call-to-action hierarchy.',
      'Clear section rhythm helps visitors scan quickly, compare trust signals, and move toward a next step without guessing where to click.',
    ],
    bestForExamples: [
      'SaaS launch pages that need a focused trial signup flow.',
      'Product marketing pages for a single feature set or campaign.',
      'Paid traffic destinations where message match and trust elements are critical.',
    ],
    fallbackTakeaways: [
      'Keep the hero headline tied to one measurable outcome.',
      'Place social proof near first and second CTA moments.',
      'Use one primary CTA style throughout the page.',
      'Group feature content by user goal, not by internal team structure.',
      'Reserve supporting visuals for sections that remove buying friction.',
    ],
    accessibilityChecklist: [
      'Verify hero text contrast remains readable on image or gradient backgrounds.',
      'Ensure CTA buttons expose clear accessible names and focus states.',
      'Use semantic heading order so screen readers can navigate sections quickly.',
      'Keep form labels persistent, even when inline hint text is shown.',
      'Confirm keyboard users can reach pricing and FAQ links without traps.',
    ],
    implementationChecklist: [
      'Use a shared spacing scale across hero, proof, and CTA sections.',
      'Defer non-critical scripts to protect first interaction readiness.',
      'Extract repeated CTA blocks into reusable React components.',
      'Keep Tailwind utility clusters readable with small composition helpers.',
      'Pre-allocate image space to prevent layout shifts during loading.',
    ],
  },
  dashboard: {
    why: [
      'Dashboard layouts succeed when information hierarchy follows decision priority, so key metrics appear before secondary diagnostic data.',
      'Stable card structures and predictable control placement reduce context switching during repeated daily workflows.',
    ],
    bestForExamples: [
      'Operations dashboards tracking incidents, queues, or throughput.',
      'Analytics consoles that need fast cross-filtering and drilldowns.',
      'Internal tools where teams monitor status and take corrective actions.',
    ],
    fallbackTakeaways: [
      'Surface one primary metric per card before adding detail.',
      'Keep filters persistent and close to the data they modify.',
      'Use color as state encoding, not as decoration.',
      'Balance dense data with consistent whitespace and separators.',
      'Make alert severity visible without forcing tooltip dependency.',
    ],
    accessibilityChecklist: [
      'Use descriptive table headers and associations for screen readers.',
      'Provide non-color indicators for status and chart categories.',
      'Ensure keyboard focus can move through dense controls in logical order.',
      'Keep chart summaries available in plain text near the visualization.',
      'Support zoom and text scaling without clipping critical metrics.',
    ],
    implementationChecklist: [
      'Virtualize long tables only when real interaction data justifies it.',
      'Memoize expensive chart transforms in React server/client boundaries.',
      'Centralize tokenized status colors for consistent state rendering.',
      'Define table and panel breakpoints to preserve scanability.',
      'Avoid deeply nested Tailwind class chains in repeated widgets.',
    ],
  },
  'e-commerce': {
    why: [
      'Commerce interfaces work best when product context, confidence signals, and purchase actions stay aligned in one predictable flow.',
      'Reducing ambiguity around price, delivery, and returns improves completion because users can evaluate risk without leaving the page.',
    ],
    bestForExamples: [
      'Product detail pages with variant selection and trust messaging.',
      'Collection pages balancing discovery, filtering, and add-to-cart actions.',
      'Checkout-adjacent flows that prioritize completion clarity.',
    ],
    fallbackTakeaways: [
      'Show total cost context before the user reaches payment.',
      'Keep variant selectors explicit and reversible.',
      'Use trust content near decision-heavy blocks, not only in the footer.',
      'Limit competing promotions in checkout-progress moments.',
      'Preserve cart context across device and session transitions.',
    ],
    accessibilityChecklist: [
      'Confirm form errors are announced and linked to the right fields.',
      'Use clear labels for quantity, size, color, and shipping options.',
      'Ensure promotional banners do not interrupt keyboard navigation.',
      'Keep product galleries operable without drag gestures.',
      'Provide readable focus indicators on all purchase actions.',
    ],
    implementationChecklist: [
      'Model pricing and variant state in predictable React state slices.',
      'Use Tailwind tokens for spacing consistency across product cards.',
      'Reserve image dimensions to avoid checkout-step layout shifts.',
      'Keep cart actions idempotent to prevent double submissions.',
      'Instrument funnel events around add-to-cart and checkout transitions.',
    ],
  },
  portfolio: {
    why: [
      'Portfolio pages perform when they present a narrative of capability, process, and outcome instead of only visual snapshots.',
      'Strong case-study structure helps reviewers understand decisions, constraints, and execution quality with minimal back-and-forth.',
    ],
    bestForExamples: [
      'Freelancer portfolios highlighting conversion-focused web work.',
      'Agency showcases with multiple service lines and proof points.',
      'Personal product design pages that need clear project storytelling.',
    ],
    fallbackTakeaways: [
      'Lead with a concise specialization statement and audience fit.',
      'Use project summaries that include measurable outcomes.',
      'Show process steps to build credibility beyond final visuals.',
      'Keep navigation simple so portfolio sections stay scannable.',
      'Add clear collaboration or contact pathways near proof blocks.',
    ],
    accessibilityChecklist: [
      'Provide descriptive alt text for project thumbnails and media.',
      'Ensure animated transitions do not hide essential project context.',
      'Keep typography readable across large and small viewport widths.',
      'Support reduced-motion preferences for reveal interactions.',
      'Maintain visible focus states on portfolio navigation links.',
    ],
    implementationChecklist: [
      'Define reusable project-card variants to avoid inconsistent markup.',
      'Use semantic sections for about, work, and contact groupings.',
      'Optimize media delivery with responsive image sizing strategies.',
      'Keep Tailwind utility patterns consistent across case-study pages.',
      'Separate content data from presentation for easier updates.',
    ],
  },
  blog: {
    why: [
      'Editorial layouts retain attention when typography hierarchy, reading width, and navigation cues are balanced for long-form scanning.',
      'Readers trust content more when structure is predictable and supporting links appear at the point of decision, not as an afterthought.',
    ],
    bestForExamples: [
      'Product blogs publishing implementation and UX guidance.',
      'Knowledge bases that combine tutorial and reference content.',
      'Editorial pages where readability and skimmability are primary goals.',
    ],
    fallbackTakeaways: [
      'Use a stable heading rhythm to signal topic transitions.',
      'Keep line length and paragraph spacing optimized for readability.',
      'Surface related resources near relevant sections.',
      'Use concise summary blocks to support quick scanning.',
      'Avoid visual noise that competes with article hierarchy.',
    ],
    accessibilityChecklist: [
      'Use semantic article structure with meaningful heading levels.',
      'Ensure links are identifiable without relying on color alone.',
      'Support keyboard navigation for TOC and inline interactive blocks.',
      'Maintain minimum contrast for body text and metadata labels.',
      'Avoid autoplay media that disrupts reading flow.',
    ],
    implementationChecklist: [
      'Componentize prose primitives for consistent rendering.',
      'Apply Tailwind typography styles with explicit spacing overrides.',
      'Use server-rendered markdown transforms for stable output.',
      'Guard embedded media with fixed aspect-ratio containers.',
      'Track scroll depth and outbound clicks for content quality feedback.',
    ],
  },
  component: {
    why: [
      'Component-driven interfaces scale when each piece has a clear responsibility, predictable states, and explicit composition boundaries.',
      'Reusable modules reduce QA overhead because behavior and styling can be validated once and propagated consistently.',
    ],
    bestForExamples: [
      'Design system libraries that need maintainable UI primitives.',
      'Product teams assembling feature screens from reusable blocks.',
      'Admin tools where consistency across modules matters more than novelty.',
    ],
    fallbackTakeaways: [
      'Define variant boundaries before introducing visual permutations.',
      'Keep component APIs focused on intent rather than styling shortcuts.',
      'Document states for loading, empty, and error conditions.',
      'Use tokens to align spacing, color, and typography decisions.',
      'Favor composition over deeply branching monolithic components.',
    ],
    accessibilityChecklist: [
      'Ensure interactive components expose keyboard and focus support.',
      'Use ARIA only when semantic HTML cannot express the pattern.',
      'Document required labels for icon-only actions.',
      'Validate disabled and error states with screen reader announcements.',
      'Keep hit targets large enough for touch and pointer interactions.',
    ],
    implementationChecklist: [
      'Establish shared prop contracts for common primitives.',
      'Use Tailwind class composition utilities for repeatable variants.',
      'Add unit and interaction tests around state transitions.',
      'Prevent style leakage with scoped component boundaries.',
      'Keep component stories aligned with production usage patterns.',
    ],
  },
  general: {
    why: [
      'Interface patterns tend to perform when visual hierarchy, copy intent, and interaction outcomes align around one primary user goal.',
      'Consistency across spacing, typography, and action treatment lowers cognitive load and improves confidence in navigation choices.',
    ],
    bestForExamples: [
      'Product pages that require clear scanning and action prioritization.',
      'Internal tools balancing clarity with implementation speed.',
      'Marketing surfaces that need reliable structure for iterative testing.',
    ],
    fallbackTakeaways: [
      'Define one primary action per major section.',
      'Use consistent spacing and type scale to reinforce hierarchy.',
      'Keep support content adjacent to the interaction it explains.',
      'Treat motion and color as guidance, not decoration.',
      'Document assumptions so future iterations stay coherent.',
    ],
    accessibilityChecklist: [
      'Validate contrast and focus indicators across all interactive elements.',
      'Keep heading structure sequential and descriptive.',
      'Ensure keyboard navigation covers all actionable controls.',
      'Provide descriptive labels for forms, links, and icon actions.',
      'Test layouts at zoomed text sizes for clipping issues.',
    ],
    implementationChecklist: [
      'Extract repeated patterns into reusable React modules.',
      'Use tokenized Tailwind classes for maintainable styling.',
      'Protect layout stability with reserved media dimensions.',
      'Keep data flow explicit to simplify debugging and QA.',
      'Review generated markup for semantic HTML correctness.',
    ],
  },
};

function normalizeCategory(category?: string): CategoryKey {
  const raw = (category || '').toLowerCase();
  if (raw.includes('landing')) return 'landing-page';
  if (raw.includes('dashboard') || raw.includes('admin')) return 'dashboard';
  if (raw.includes('commerce') || raw.includes('e-commerce') || raw.includes('shop') || raw.includes('checkout')) return 'e-commerce';
  if (raw.includes('portfolio')) return 'portfolio';
  if (raw.includes('blog') || raw.includes('editorial')) return 'blog';
  if (raw.includes('component')) return 'component';
  return 'general';
}

function toSentenceCase(input: string): string {
  const trimmed = input.trim();
  if (!trimmed) return trimmed;
  return trimmed[0].toUpperCase() + trimmed.slice(1);
}

function compactSentence(input?: string): string {
  if (!input) return '';
  return input.replace(/\s+/g, ' ').trim();
}

function uniqueItems(items: string[]): string[] {
  const seen = new Set<string>();
  const result: string[] = [];
  for (const item of items) {
    const normalized = item.toLowerCase();
    if (!normalized || seen.has(normalized)) {
      continue;
    }
    seen.add(normalized);
    result.push(item);
  }
  return result;
}

function mergeChecklist(base: string[], extras: string[], count = 5): string[] {
  return uniqueItems([...base, ...extras]).slice(0, count);
}

function buildTagExtras(tags: string[]) {
  const normalized = new Set(tags.map((tag) => tag.toLowerCase()));
  const accessibility: string[] = [];
  const implementation: string[] = [];

  if (normalized.has('accessibility')) {
    accessibility.push('Review landmark regions and skip links so keyboard users can bypass repeated navigation.');
    implementation.push('Add accessibility assertions in component tests for focus order and ARIA naming.');
  }
  if (normalized.has('dark-mode')) {
    accessibility.push('Validate contrast in both light and dark themes rather than inheriting light-mode token assumptions.');
    implementation.push('Centralize dark-mode tokens and avoid hard-coded utility overrides per component.');
  }
  if (normalized.has('table')) {
    accessibility.push('Ensure sticky headers and horizontally scrollable tables remain readable with keyboard focus.');
    implementation.push('Split table rendering and data logic to keep sorting and pagination predictable.');
  }
  if (normalized.has('onboarding')) {
    accessibility.push('Keep step indicators and progress labels readable for assistive technology users.');
    implementation.push('Model onboarding step state explicitly so resume and back-navigation behavior stay stable.');
  }

  return { accessibility, implementation };
}

function buildCustomizationBullets(tags: string[], colors: string[] | undefined, hasReactCode: boolean, hasHtmlCode: boolean): string[] {
  const normalizedTags = uniqueItems(tags.map((tag) => tag.trim()).filter(Boolean)).slice(0, 3);
  const palettePreview = (colors ?? []).filter(Boolean).slice(0, 3).join(', ');

  const colorBullet = palettePreview
    ? `Set primary and accent tokens from this palette first (${palettePreview}) before adjusting component-level overrides.`
    : 'Start by defining brand color tokens for primary actions, neutral surfaces, and semantic states.';

  const tagBullet = normalizedTags.length > 0
    ? `Prioritize variations around the active tags (${normalizedTags.join(', ')}) to keep customization aligned with use-case intent.`
    : 'Prioritize one use-case direction first, then expand variants only after core interactions are stable.';

  let codeBullet = 'Use a staged implementation plan: lock structure first, then layer styling and behavior with QA checkpoints.';
  if (hasReactCode && hasHtmlCode) {
    codeBullet = 'Use the provided HTML as structure reference and React code as the reusable component baseline for faster iteration.';
  } else if (hasReactCode) {
    codeBullet = 'Start from the provided React code, then extract reusable props and variants before introducing new visual options.';
  } else if (hasHtmlCode) {
    codeBullet = 'Use the provided HTML as semantic scaffolding, then wrap sections into React components with explicit props.';
  }

  return [colorBullet, tagBullet, codeBullet];
}

export default function DesignEditorialSection({
  title,
  description,
  features,
  usage,
  category,
  tags,
  colors,
  hasReactCode,
  hasHtmlCode,
}: DesignEditorialSectionProps) {
  const categoryKey = normalizeCategory(category);
  const template = CATEGORY_TEMPLATES[categoryKey];
  const tagList = (tags ?? []).filter(Boolean);
  const descriptionText = compactSentence(description);
  const usageText = compactSentence(usage);
  const tagExtras = buildTagExtras(tagList);

  const whyParagraphs: string[] = [];
  if (descriptionText) {
    whyParagraphs.push(
      `${title} centers the visual narrative around this core direction: ${descriptionText}`
    );
  } else {
    whyParagraphs.push(
      `${title} follows a practical ${category ? category.toLowerCase() : 'product interface'} structure that keeps major actions and supporting context in predictable places.`
    );
  }
  whyParagraphs.push(template.why[0]);
  whyParagraphs.push(template.why[1]);
  if (hasReactCode || hasHtmlCode) {
    whyParagraphs.push(
      hasReactCode
        ? 'Because reusable code is available, teams can validate structure and interaction assumptions quickly instead of rebuilding the pattern from scratch.'
        : 'Because semantic HTML is available, teams can preserve structure while gradually layering framework-specific behavior.'
    );
  }

  const bestForIntro = usageText
    ? `Use this pattern when the product goal matches this operating context: ${usageText}`
    : `Use this pattern when you need a ${category ? category.toLowerCase() : 'high-signal interface'} that balances clarity, speed, and maintainable implementation.`;

  const rawFeatureBullets = (features ?? [])
    .map((item) => compactSentence(item))
    .filter(Boolean)
    .map(toSentenceCase);
  const takeaways = uniqueItems([...rawFeatureBullets, ...template.fallbackTakeaways]).slice(0, 5);

  const accessibilityChecklist = mergeChecklist(
    template.accessibilityChecklist,
    tagExtras.accessibility,
    5
  );

  const implementationAvailability: string[] = [];
  if (hasReactCode) {
    implementationAvailability.push('Use the React implementation as the source of truth for reusable state and variant APIs.');
  } else {
    implementationAvailability.push('Define React wrappers with explicit props so future states remain testable and predictable.');
  }
  if (hasHtmlCode) {
    implementationAvailability.push('Keep semantic HTML landmarks intact when refactoring into reusable components.');
  } else {
    implementationAvailability.push('Start with semantic section and heading structure before styling to keep accessibility intact.');
  }

  const implementationChecklist = mergeChecklist(
    [...implementationAvailability, ...template.implementationChecklist],
    tagExtras.implementation,
    5
  );

  const customizeQuickly = buildCustomizationBullets(tagList, colors, hasReactCode, hasHtmlCode);

  return (
    <section className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
      <h2 className="text-2xl font-semibold text-gray-900">Design Notes</h2>

      <div className="mt-5">
        <h3 className="text-lg font-semibold text-gray-900">Why this pattern works</h3>
        <div className="mt-3 space-y-3 text-sm text-gray-700 leading-relaxed">
          {whyParagraphs.slice(0, 4).map((paragraph, index) => (
            <p key={`why-${index}`}>{paragraph}</p>
          ))}
        </div>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-900">Best for</h3>
        <details className="mt-2 rounded-xl border border-gray-200 bg-gray-50/70 p-4">
          <summary className="cursor-pointer text-sm font-medium text-gray-700">View recommended use cases</summary>
          <p className="mt-3 text-sm text-gray-700 leading-relaxed">{bestForIntro}</p>
          <ul className="mt-3 space-y-2 text-sm text-gray-700">
            {template.bestForExamples.map((example, index) => (
              <li key={`best-for-${index}`} className="flex gap-2">
                <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 rounded-full bg-gray-900" />
                <span>{example}</span>
              </li>
            ))}
          </ul>
        </details>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-900">Key takeaways</h3>
        <details className="mt-2 rounded-xl border border-gray-200 bg-gray-50/70 p-4">
          <summary className="cursor-pointer text-sm font-medium text-gray-700">View key points</summary>
          <ul className="mt-3 space-y-2 text-sm text-gray-700">
            {takeaways.map((takeaway, index) => (
              <li key={`takeaway-${index}`} className="flex gap-2">
                <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 rounded-full bg-gray-900" />
                <span>{takeaway}</span>
              </li>
            ))}
          </ul>
        </details>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-900">Accessibility checklist</h3>
        <details className="mt-2 rounded-xl border border-gray-200 bg-gray-50/70 p-4">
          <summary className="cursor-pointer text-sm font-medium text-gray-700">View accessibility checks</summary>
          <ul className="mt-3 space-y-2 text-sm text-gray-700">
            {accessibilityChecklist.map((item, index) => (
              <li key={`a11y-${index}`} className="flex gap-2">
                <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 rounded-full bg-gray-900" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </details>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-900">Implementation checklist</h3>
        <details className="mt-2 rounded-xl border border-gray-200 bg-gray-50/70 p-4">
          <summary className="cursor-pointer text-sm font-medium text-gray-700">View implementation steps</summary>
          <ul className="mt-3 space-y-2 text-sm text-gray-700">
            {implementationChecklist.map((item, index) => (
              <li key={`impl-${index}`} className="flex gap-2">
                <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 rounded-full bg-gray-900" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </details>
      </div>

      <div className="mt-6">
        <h3 className="text-lg font-semibold text-gray-900">Customize quickly</h3>
        <details className="mt-2 rounded-xl border border-gray-200 bg-gray-50/70 p-4">
          <summary className="cursor-pointer text-sm font-medium text-gray-700">View quick customization plan</summary>
          <ul className="mt-3 space-y-2 text-sm text-gray-700">
            {customizeQuickly.map((item, index) => (
              <li key={`custom-${index}`} className="flex gap-2">
                <span aria-hidden="true" className="mt-1.5 h-1.5 w-1.5 rounded-full bg-gray-900" />
                <span>{item}</span>
              </li>
            ))}
          </ul>
        </details>
      </div>
    </section>
  );
}
