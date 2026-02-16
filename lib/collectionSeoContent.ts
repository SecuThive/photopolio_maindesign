export type CollectionSeoData = {
  title: string;
  summaryParagraphs: string[];
  bullets: string[];
  expandedSections: {
    heading: string;
    paragraphs: string[];
    bullets: string[];
  }[];
  faqs: {
    q: string;
    a: string;
  }[];
};

export const collectionSeoContent: Record<string, CollectionSeoData> = {
  "best-saas-landing-pages": {
    title: "Best SaaS Landing Pages Collection",
    summaryParagraphs: [
      "This collection showcases SaaS landing pages that excel in conversion architecture. Each design demonstrates measurable clarity in value proposition delivery, strategic social proof placement, and friction-minimized CTAs. Unlike generic marketingpages, these examples follow conversion-centered design principles: above-the-fold clarity, proof proximity to claims, and progressive disclosure of technical details.",
      "All designs in this collection are production-ready Tailwind CSS + React implementations. Every component includes responsive breakpoints, accessible markup, and performance-optimized asset loading. Use these as reference implementations for conversion-focused SaaS landing pages."
    ],
    bullets: [
      "Headline clarity test: value proposition visible within 3 seconds",
      "Social proof positioning: logos/metrics above fold or within first scroll",
      "CTA hierarchy: primary action visible without scrolling",
      "Trust signals: security badges, compliance mentions near signup",
      "Responsive design: mobile-first layout with desktop enhancements"
    ],
    expandedSections: [
      {
        heading: "Selection criteria and scoring rules",
        paragraphs: [
          "Every landing page in this collection is evaluated against a simple rubric: clarity, proof, and action. Clarity means the product's outcome and persona are obvious in the first five seconds. Proof means metrics, logos, or testimonials are positioned close to the headline. Action means the CTA ladder is visible without forcing the user to scroll.",
          "If a page relies on generic all-in-one platform language or hides proof behind multiple sections, it does not qualify. Likewise, pages with conflicting CTAs are excluded because they weaken intent and reduce conversion performance."
        ],
        bullets: [
          "Headline states role + outcome; subhead explains mechanism.",
          "Proof block appears above the fold or within first scroll.",
          "Primary CTA uses action verb; secondary CTA offers low-friction alternative.",
          "Feature section uses outcome-based copy, not feature lists.",
          "Footer includes trust signals: security, compliance, testimonials."
        ]
      },
      {
        heading: "Common implementation mistakes to avoid",
        paragraphs: [
          "Most failed SaaS landing pages suffer from vague headlines, hidden proof, or CTA overload. A headline like 'Transform Your Workflow' says nothing actionable. Replace it with 'Turn Support Tickets Into Product Roadmaps in 48 Hours' to specify role, outcome, and timeframe.",
          "Another frequent error is burying social proof in a dedicated section below the fold. Instead, position logos or metrics immediately after the headline to validate claims before users scroll. Finally, avoid multiple competing CTAs above the fold. One primary action (Start Free Trial) plus one secondary (Watch Demo) is the proven maximum."
        ],
        bullets: [
          "Do not use abstract headlines; specify role, outcome, and timeframe.",
          "Do not hide proof; place logos or metrics within the hero section.",
          "Do not present more than two CTAs above the fold.",
          "Do not use feature-first copy; lead with outcomes, then explain how.",
          "Do not omit mobile optimization; 60%+ of SaaS traffic is mobile."
        ]
      }
    ],
    faqs: [
      {
        q: "Can I use these landing pages for non-SaaS products?",
        a: "Yes, but adjust brand tokens and copy to match your product's audience and positioning."
      },
      {
        q: "Are these designs optimized for mobile devices?",
        a: "Every design uses mobile-first Tailwind breakpoints with touch-friendly CTAs and readable typography."
      },
      {
        q: "Do these pages include A/B testing markup?",
        a: "No, but all CTAs and headlines use semantic class names that make variant testing straightforward."
      }
    ]
  },

  "minimalist-dashboards": {
    title: "Minimalist Dashboard UI Collection",
    summaryParagraphs: [
      "This collection features dashboards that prioritize signal over noise. Each design applies information hierarchy principles: primary metrics dominate visual weight, secondary data is grouped by context, and actionable elements are clearly separated from read-only content. These are not minimal in features but minimal in cognitive load.",
      "All implementations use Tailwind CSS with systematic spacing scales, accessible color contrast, and responsive grid layouts. Components are built with React and include keyboard navigation, screen reader labels, and performance-optimized data rendering. Use these as templates for analytics dashboards, admin panels, or operational monitoring tools."
    ],
    bullets: [
      "Visual hierarchy: primary KPIs use larger typography and dominant positioning",
      "Grouping strategy: related metrics clustered with clear section dividers",
      "Actionable vs. informational: buttons/inputs visually distinct from static data",
      "Whitespace discipline: consistent spacing between cards and sections",
      "Accessibility compliance: WCAG 2.1 AA contrast ratios and ARIA labels"
    ],
    expandedSections: [
      {
        heading: "Design principles for cognitive load reduction",
        paragraphs: [
          "Minimalist dashboards reduce cognitive load through three mechanisms: hierarchy, grouping, and restraint. Hierarchy means the most important metric is the largest element. Grouping means related data shares visual proximity and container styling. Restraint means removing decorative elements that do not aid decision-making.",
          "A dashboard fails minimalism when it treats all metrics equally or uses visual effects for decoration rather than encoding meaning. For example, a gradient background on a card is decorative; a red border on an anomaly warning is semantic."
        ],
        bullets: [
          "Establish clear hierarchy: primary metric dominates space and contrast.",
          "Group related data: use card containers or background tints to cluster context.",
          "Eliminate decoration: remove shadows, gradients, or icons that do not encode data.",
          "Use color sparingly: reserve color for status encoding, not aesthetics.",
          "Optimize whitespace: consistent spacing improves scannability and reduces fatigue."
        ]
      },
      {
        heading: "Common mistakes in dashboard design",
        paragraphs: [
          "The most frequent error is treating all metrics with equal visual weight. If revenue, page views, and server uptime all use the same font size and card styling, users cannot prioritize. Instead, size metrics by decision impact or update frequency.",
          "Another mistake is using color for decoration instead of semantic encoding. A blue card and a green card should signify different states or categories, not just visual variety. Reserve color for status indicators: green for healthy, yellow for warning, red for critical."
        ],
        bullets: [
          "Do not give all metrics equal visual weight; prioritize by impact.",
          "Do not use color for decoration; reserve it for semantic encoding.",
          "Do not overcrowd cards; one card should represent one decision context.",
          "Do not omit loading states; skeleton screens improve perceived performance.",
          "Do not ignore accessibility; ensure sufficient contrast and keyboard navigation."
        ]
      }
    ],
    faqs: [
      {
        q: "Can I add charts to these minimalist dashboards?",
        a: "Yes, but choose chart types that match the data structure and avoid decorative effects like 3D or shadows."
      },
      {
        q: "Are these dashboards suitable for real-time data?",
        a: "Yes, the React components support state updates, but you will need to integrate WebSocket or polling logic."
      },
      {
        q: "Do these designs work for mobile dashboards?",
        a: "All layouts use responsive grids, but high-density dashboards are better suited for tablet or desktop viewports."
      }
    ]
  },

  "high-conversion-hero-sections": {
    title: "High-Conversion Hero Sections Collection",
    summaryParagraphs: [
      "This collection contains hero sections engineered for conversion, not aesthetics. Each design applies clarity-first principles: headline specifies role and outcome, subhead explains mechanism or differentiation, CTA uses action verbs, and social proof validates claims. These are not generic above-the-fold layouts but conversion-optimized entry points.",
      "All hero sections are built with Tailwind CSS and React, using semantic HTML for accessibility and performance-optimized images with lazy loading. Use these as starting templates for landing pages, product pages, or campaign-specific microsites."
    ],
    bullets: [
      "Headline formula: [Role] + [Outcome] + [Timeframe or constraint]",
      "Subhead purpose: explain how the outcome is achieved or what makes it unique",
      "CTA positioning: primary action visible without scrolling, secondary CTA offers low-friction alternative",
      "Social proof placement: logos, metrics, or testimonials positioned near headline",
      "Visual hierarchy: headline dominates, subhead supports, CTA contrasts"
    ],
    expandedSections: [
      {
        heading: "Anatomy of a high-conversion hero section",
        paragraphs: [
          "A high-conversion hero section answers three questions in order: Who is this for? What do they get? Why should they believe you? The headline answers the first two, the subhead explains differentiation, and social proof validates the claim. CTAs convert intent into action.",
          "Weak hero sections fail because they answer these questions out of order or omit them. A headline like 'Welcome to ProductName' tells users nothing. A headline like 'Turn Customer Feedback Into Product Roadmaps in 2 Weeks' specifies role (product teams), outcome (roadmaps), and timeframe (2 weeks)."
        ],
        bullets: [
          "Headline: specify role, outcome, and constraint in 8-12 words.",
          "Subhead: explain mechanism or unique differentiation in 15-20 words.",
          "CTA primary: use action verb + outcome (e.g., Start Free Trial).",
          "CTA secondary: offer low-friction alternative (e.g., Watch 2-Min Demo).",
          "Social proof: position logos or metrics within hero container."
        ]
      },
      {
        heading: "Common hero section mistakes",
        paragraphs: [
          "The most damaging mistake is vague headlines. 'Revolutionize Your Business' is meaningless. Replace it with a specific outcome: 'Reduce Customer Support Load by 40% With AI-Powered Ticket Routing.' Another common error is CTA overload. More than two CTAs above the fold creates decision paralysis.",
          "Finally, many hero sections fail to include social proof within the viewport. If users must scroll to see logos or testimonials, they are making a trust decision without validation. Position proof elements within the hero container or immediately below the headline."
        ],
        bullets: [
          "Do not use vague headlines; specify role, outcome, and timeframe.",
          "Do not present more than two CTAs; one primary, one secondary maximum.",
          "Do not hide social proof; position logos or metrics within hero section.",
          "Do not use decorative images; use product screenshots or outcome visuals.",
          "Do not omit mobile optimization; hero sections must work at 375px width."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I include a background image in my hero section?",
        a: "Only if it reinforces the product outcome. Decorative images reduce clarity and slow page load."
      },
      {
        q: "How many CTAs should I include above the fold?",
        a: "One primary CTA (high intent) plus one secondary CTA (low friction). More than two creates decision paralysis."
      },
      {
        q: "Can I use these hero sections for B2B SaaS products?",
        a: "Yes, but emphasize outcomes over features and include enterprise trust signals like compliance badges."
      }
    ]
  },

  "saas-pricing-pages": {
    title: "SaaS Pricing Pages Collection",
    summaryParagraphs: [
      "This collection showcases pricing pages optimized for decision velocity. Each design uses comparison clarity, feature anchoring, and CTA hierarchy to reduce friction. These are not generic pricing tables but conversion-engineered layouts that guide users to the plan that matches their intent.",
      "All pricing components use Tailwind CSS with accessible markup, keyboard navigation, and responsive layouts. React state management handles plan toggles (monthly/annual) and feature comparisons. Use these as templates for SaaS pricing pages, upgrade flows, or self-service checkout experiences."
    ],
    bullets: [
      "Comparison clarity: feature differences highlighted, not buried in fine print",
      "Anchoring strategy: most popular plan visually emphasized to guide selection",
      "CTA hierarchy: primary plan CTA uses high-contrast color, others use neutral",
      "Billing toggle: monthly/annual switcher with savings percentage displayed",
      "Trust signals: money-back guarantee, free trial mention, secure checkout badge"
    ],
    expandedSections: [
      {
        heading: "Pricing page design principles",
        paragraphs: [
          "A high-converting pricing page removes uncertainty by making differences obvious and anchoring users to the recommended plan. The most popular plan should use visual emphasis: a border, a badge, or a contrasting background. Feature lists should highlight what changes between plans, not repeat shared features.",
          "Weak pricing pages fail because they treat all plans equally or hide key differences. If your Starter and Pro plans look identical except for a bullet point, users will default to the cheaper option. Instead, make the Pro plan's unique value visually dominant."
        ],
        bullets: [
          "Emphasize recommended plan: use border, badge, or background contrast.",
          "Highlight feature differences: bold or color-code unique features.",
          "Position CTAs consistently: all plan CTAs should align vertically.",
          "Show savings for annual billing: display percentage discount prominently.",
          "Include trust signals: free trial, money-back guarantee, or testimonials."
        ]
      },
      {
        heading: "Common pricing page mistakes",
        paragraphs: [
          "The most common mistake is treating all plans with equal visual weight. If your Basic, Pro, and Enterprise cards look identical, users will choose based on price alone. Instead, visually anchor users to the plan with the best margin by using a Recommended badge or contrasting color.",
          "Another frequent error is listing all features for every plan without highlighting differences. Users do not want to compare 20 bullet points. Instead, show shared features once and bold or color-code the unique features for each tier."
        ],
        bullets: [
          "Do not treat all plans equally; anchor users to the recommended tier.",
          "Do not list all features per plan; highlight differences, not repetition.",
          "Do not hide pricing; show costs upfront without requiring signup.",
          "Do not omit annual billing option; it increases LTV and reduces churn.",
          "Do not ignore mobile layout; test pricing tables on 375px screens."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I include a free plan in my pricing page?",
        a: "Only if it drives Product-Led Growth. Free plans reduce friction but can cannibalize paid conversions."
      },
      {
        q: "How many pricing tiers should I offer?",
        a: "Three is optimal for most SaaS products: entry, recommended, and enterprise. More than four creates decision paralysis."
      },
      {
        q: "Should I show annual discounts as percentage or dollar amount?",
        a: "Percentage works better for small discounts (10-20%), dollar amount for large ones ($500+ savings)."
      }
    ]
  },

  "onboarding-activation-flows": {
    title: "Onboarding & Activation Flows Collection",
    summaryParagraphs: [
      "This collection features onboarding flows designed to reach activation milestones, not just complete steps. Each design applies progressive disclosure: ask for information only when needed, show value before requesting effort, and provide exit points without losing progress. These are not generic signup forms but activation-engineered experiences.",
      "All flows are built with Tailwind CSS and React, using form validation, progress indicators, and accessible error handling. Components support multi-step flows with state persistence and analytics event tracking. Use these as templates for SaaS onboarding, account setup wizards, or trial activation experiences."
    ],
    bullets: [
      "Progressive disclosure: request information only when needed, not upfront",
      "Value-first sequencing: show product benefit before asking for configuration",
      "Progress indication: visual stepper or percentage complete to reduce uncertainty",
      "Exit preservation: save progress if user abandons flow mid-step",
      "Validation clarity: inline error messages with actionable correction guidance"
    ],
    expandedSections: [
      {
        heading: "Activation-focused onboarding principles",
        paragraphs: [
          "A high-activation onboarding flow prioritizes reaching a meaningful milestone over collecting complete data. The milestone varies by product: for a dashboard tool, it is seeing live data; for a collaboration tool, it is inviting a teammate. Delay non-critical fields until after activation.",
          "Weak onboarding flows fail because they front-load effort without demonstrating value. If your flow asks for company size, role, and goals before showing the product, users will abandon. Instead, show a sample dashboard or pre-filled data, then ask for customization."
        ],
        bullets: [
          "Define activation milestone: first value moment, not signup completion.",
          "Sequence steps by urgency: ask only what is needed to reach activation.",
          "Show value before effort: display sample data or pre-configured views.",
          "Provide skip options: allow users to defer non-critical configuration.",
          "Track drop-off points: instrument analytics to identify friction steps."
        ]
      },
      {
        heading: "Common onboarding mistakes",
        paragraphs: [
          "The most damaging mistake is asking for too much information before showing value. If your onboarding flow has five steps before the user sees the product, you are losing users to friction. Instead, show a working demo or pre-filled data on step one, then ask for customization.",
          "Another common error is unclear progress indication. If users do not know how many steps remain, they will abandon. Use a visual stepper or percentage indicator to reduce uncertainty."
        ],
        bullets: [
          "Do not front-load data collection; show value before asking for effort.",
          "Do not hide progress; use stepper or percentage indicator.",
          "Do not force linear flows; allow skipping non-critical steps.",
          "Do not ignore abandonment; save progress and send re-engagement emails.",
          "Do not omit validation; inline error messages improve completion rates."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I use a multi-step flow or a single-page form?",
        a: "Multi-step works better for complex onboarding; single-page for low-friction signups."
      },
      {
        q: "How many steps should my onboarding flow have?",
        a: "As few as possible to reach activation. Most high-performing flows have 2-4 steps."
      },
      {
        q: "Should I allow users to skip onboarding steps?",
        a: "Yes, for non-critical configuration. Always allow skipping personalization or team invites."
      }
    ]
  },

  "product-tour-pages": {
    title: "Product Tour Pages Collection",
    summaryParagraphs: [
      "This collection contains product tour pages that demonstrate functionality through structured narrative. Each design uses progressive disclosure: start with the core workflow, expand into advanced features, and end with a clear activation CTA. These are not feature lists but guided walkthroughs that show users how to achieve specific outcomes.",
      "All tour pages use Tailwind CSS with scroll-driven animations, lazy-loaded media, and accessible navigation. React components handle step progression, video embeds, and mobile-optimized layouts. Use these as templates for product education, feature launch pages, or sales enablement content."
    ],
    bullets: [
      "Narrative structure: start with core workflow, expand to advanced features",
      "Visual progression: use scroll animations or step indicators to show flow",
      "Outcome-focused copy: explain what users accomplish, not just what features exist",
      "Media optimization: lazy-load videos and images to maintain performance",
      "CTA placement: end each section with relevant next-step action"
    ],
    expandedSections: [
      {
        heading: "Building effective product tour narratives",
        paragraphs: [
          "A high-quality product tour follows a narrative arc: problem introduction, core workflow demonstration, advanced capabilities, and activation CTA. The core workflow section should show the most common use case with screenshots or video. Advanced sections branch into specialization or power user features.",
          "Weak product tours fail because they list features without context or dump all information without hierarchy. Instead, sequence content by user journey: show how a new user accomplishes their first task, then how an experienced user optimizes their workflow."
        ],
        bullets: [
          "Start with problem statement: articulate the pain point your product solves.",
          "Demonstrate core workflow: show step-by-step how to accomplish primary task.",
          "Expand to advanced features: branch into specialization after core workflow.",
          "Use real screenshots or videos: avoid generic mockups or placeholder content.",
          "End with activation CTA: guide users to sign up or start trial after tour."
        ]
      },
      {
        heading: "Common product tour mistakes",
        paragraphs: [
          "The most common mistake is feature dumping: listing every capability without narrative structure. Users do not care about features; they care about outcomes. Instead of listing 'Advanced Filters,' show 'Find High-Value Customers in 10 Seconds With Behavior Filters.'",
          "Another frequent error is using static images without context. A screenshot of a dashboard means nothing without annotation. Add captions, arrows, or highlight boxes to direct attention to the relevant UI element."
        ],
        bullets: [
          "Do not list features; show outcome-based workflows.",
          "Do not use static images without annotation; add captions or highlights.",
          "Do not ignore mobile layout; product tours must work on small screens.",
          "Do not omit video options; some users prefer video over text.",
          "Do not end without CTA; guide users to next step after tour completion."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I use video or screenshots for product tours?",
        a: "Use both. Screenshots work for scannable content; video works for complex workflows."
      },
      {
        q: "How long should a product tour page be?",
        a: "Long enough to demonstrate core workflow and 2-3 advanced features. Typically 3-5 sections."
      },
      {
        q: "Should I include pricing information on product tour pages?",
        a: "Yes, include a pricing CTA at the bottom, but do not lead with it. Show value first."
      }
    ]
  },

  "developer-docs-layouts": {
    title: "Developer Documentation Layouts Collection",
    summaryParagraphs: [
      "This collection showcases documentation layouts optimized for developer workflows. Each design applies information architecture principles: primary navigation by use case, secondary navigation by API reference, search prominence, and code example clarity. These are not generic doc sites but developer-focused knowledge bases.",
      "All layouts use Tailwind CSS with syntax-highlighted code blocks, responsive sidebars, and accessible navigation. React components handle search, version switching, and dark mode. Use these as templates for API documentation, SDK guides, or technical knowledge bases."
    ],
    bullets: [
      "Navigation hierarchy: use-case guides prominent, API reference secondary",
      "Search placement: search bar positioned in header with keyboard shortcut",
      "Code example clarity: syntax highlighting, copy button, language switcher",
      "Dark mode support: developer preference for dark themes",
      "Responsive sidebar: collapsible navigation for mobile viewports"
    ],
    expandedSections: [
      {
        heading: "Information architecture for developer docs",
        paragraphs: [
          "High-quality developer documentation prioritizes use-case guides over exhaustive reference. Most developers arrive with a specific task: integrate authentication, paginate API results, or handle webhooks. Start with these workflows, then provide comprehensive reference for advanced users.",
          "Weak documentation fails because it leads with API reference or dumps all endpoints without context. Instead, create a quickstart that accomplishes a meaningful outcome in under 10 minutes, then link to detailed reference."
        ],
        bullets: [
          "Prioritize quickstart: show a working integration in under 10 minutes.",
          "Organize by use case: group guides by developer intent, not technical structure.",
          "Provide code examples: every endpoint or method should include runnable code.",
          "Include search: developers use search more than navigation for docs.",
          "Support dark mode: most developers prefer dark themes for reading code."
        ]
      },
      {
        heading: "Common documentation layout mistakes",
        paragraphs: [
          "The most damaging mistake is leading with API reference instead of use-case guides. Developers do not read documentation for fun; they arrive with a specific task. If your homepage is a list of endpoints, they will leave. Instead, feature a quickstart or popular integration guide.",
          "Another frequent error is omitting code examples. A method description without a code sample forces developers to guess at implementation. Every endpoint, method, or component should include a working code example with expected output."
        ],
        bullets: [
          "Do not lead with API reference; feature use-case guides.",
          "Do not omit code examples; every method needs runnable sample code.",
          "Do not hide search; position search prominently in header.",
          "Do not ignore dark mode; developers expect theme switching.",
          "Do not use generic navigation; organize by developer intent and workflow."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I include API reference and guides in separate sections?",
        a: "Yes, but link between them. Guides should reference specific API methods with inline links."
      },
      {
        q: "How should I handle versioned documentation?",
        a: "Use a version switcher in the header and maintain docs for current + previous major version."
      },
      {
        q: "Do I need dark mode for documentation?",
        a: "Yes, most developers prefer dark themes. Use a toggle in the header with localStorage persistence."
      }
    ]
  },

  "fintech-trust-screens": {
    title: "Fintech Trust Screens Collection",
    summaryParagraphs: [
      "This collection features trust-building screens for financial products. Each design applies credibility signaling: regulatory compliance badges, security certifications, encryption mentions, and testimonial specificity. These are not generic About pages but trust-engineered layouts that reduce perceived risk.",
      "All screens use Tailwind CSS with accessible markup, semantic HTML, and performance-optimized images. React components handle certification modal details and testimonial carousels. Use these as templates for fintech landing pages, security pages, or compliance documentation."
    ],
    bullets: [
      "Regulatory compliance: display certifications (SOC 2, ISO 27001, PCI DSS) prominently",
      "Security transparency: explain encryption, data storage, and access controls",
      "Testimonial specificity: include verifiable details (company name, role, outcome)",
      "Risk reduction: money-back guarantee, free trial, or no-commitment messaging",
      "Visual trust signals: use official certification logos, not generic icons"
    ],
    expandedSections: [
      {
        heading: "Building trust in financial products",
        paragraphs: [
          "Financial products face higher trust barriers than other SaaS categories. Users need proof of security, regulatory compliance, and operational reliability before sharing payment information or financial data. Trust screens address these concerns through certification display, security explanations, and specific testimonials.",
          "Weak trust pages fail because they use generic security language without specifics. Saying 'We take security seriously' means nothing. Instead, state 'All data encrypted with AES-256 at rest and TLS 1.3 in transit, SOC 2 Type II certified, annual third-party penetration testing.'"
        ],
        bullets: [
          "Display certifications: show SOC 2, ISO 27001, or PCI DSS badges with verification links.",
          "Explain encryption: specify standards (AES-256, TLS 1.3) and scope (data at rest, in transit).",
          "Reference audits: mention third-party security audits or penetration testing.",
          "Use specific testimonials: include company name, role, and measurable outcome.",
          "Provide transparency: link to security whitepaper or compliance documentation."
        ]
      },
      {
        heading: "Common trust-building mistakes",
        paragraphs: [
          "The most common mistake is using generic security language without specifics. 'Bank-level security' is meaningless. Instead, state which encryption standards you use, which certifications you hold, and when you were last audited. Specificity builds trust; vagueness destroys it.",
          "Another frequent error is using stock testimonials without verification details. A quote from 'John D., CEO' is not believable. Include company name, verifiable LinkedIn profile, or video testimonial to increase credibility."
        ],
        bullets: [
          "Do not use vague security claims; specify encryption standards and certifications.",
          "Do not show fake certification badges; use official logos with verification links.",
          "Do not omit testimonial details; include company name, role, and outcome.",
          "Do not hide compliance documentation; link to security whitepapers or audit reports.",
          "Do not ignore mobile trust signals; compliance badges must be readable on small screens."
        ]
      }
    ],
    faqs: [
      {
        q: "Which security certifications matter most for fintech products?",
        a: "SOC 2 Type II, ISO 27001, and PCI DSS (if handling card data). Display prominently with verification links."
      },
      {
        q: "Should I include a dedicated security page?",
        a: "Yes, and link to it from the footer. Include encryption details, compliance certifications, and audit information."
      },
      {
        q: "How detailed should security explanations be?",
        a: "Specific enough to be credible: mention encryption standards, audit frequency, and data retention policies."
      }
    ]
  },

  "ecommerce-product-detail-pages": {
    title: "E-commerce Product Detail Pages Collection",
    summaryParagraphs: [
      "This collection showcases product detail pages (PDPs) optimized for conversion. Each design applies merchandising principles: hero image prominence, variant selection clarity, social proof positioning, and add-to-cart friction reduction. These are not generic product pages but conversion-engineered layouts.",
      "All PDPs use Tailwind CSS with image galleries, variant selectors, and accessible markup. React components handle image zoom, size selection, quantity input, and cart integration. Use these as templates for e-commerce product pages, marketplace listings, or catalog detail views."
    ],
    bullets: [
      "Hero image quality: high-resolution product photography with zoom capability",
      "Variant selection: size, color, or material options with visual feedback",
      "Social proof: star ratings, review count, and recent purchase indicators",
      "Add-to-cart clarity: prominent CTA with inventory availability messaging",
      "Product information: specifications, materials, and care instructions in tabs"
    ],
    expandedSections: [
      {
        heading: "Product detail page conversion principles",
        paragraphs: [
          "A high-converting PDP answers three questions immediately: What is this? Is it available? How much does it cost? The hero image answers the first, the add-to-cart button answers the second, and the price answers the third. Everything else supports these fundamentals.",
          "Weak PDPs fail because they hide critical information or create unnecessary friction. If users must scroll to see the price or click multiple times to select a size, you are losing conversions. Position price, availability, and variant selectors above the fold."
        ],
        bullets: [
          "Show price immediately: position prominently near product title.",
          "Display availability: show in-stock status or estimated delivery date.",
          "Simplify variant selection: use dropdown or button group for size/color.",
          "Position add-to-cart above fold: users should not scroll to purchase.",
          "Include social proof: show star rating and review count near title."
        ]
      },
      {
        heading: "Common PDP mistakes",
        paragraphs: [
          "The most damaging mistake is low-quality product images. If users cannot see product details, they will not buy. Use high-resolution images with zoom capability and show multiple angles. Another frequent error is hiding the add-to-cart button below the fold. The purchase action should be visible without scrolling.",
          "Finally, many PDPs fail to communicate availability clearly. If a product is out of stock, say so immediately and offer a restock notification option. Do not let users select variants and click add-to-cart only to see an error message."
        ],
        bullets: [
          "Do not use low-resolution images; provide zoom capability and multiple angles.",
          "Do not hide add-to-cart button; position prominently above fold.",
          "Do not obscure availability; show in-stock status or backorder estimate.",
          "Do not omit size guides; include measurement charts for apparel.",
          "Do not ignore mobile layout; PDPs must work on 375px screens."
        ]
      }
    ],
    faqs: [
      {
        q: "How many product images should I include?",
        a: "Minimum 4-6 angles for most products. Apparel needs front, back, side, and detail shots."
      },
      {
        q: "Should I include customer reviews on PDPs?",
        a: "Yes, display star rating and review count above fold, full reviews below description."
      },
      {
        q: "How should I handle out-of-stock products?",
        a: "Show 'Out of Stock' status immediately and offer email notifications for restock alerts."
      }
    ]
  },

  "checkout-cart-flows": {
    title: "Checkout & Cart Flows Collection",
    summaryParagraphs: [
      "This collection features checkout and cart flows optimized for completion. Each design applies friction reduction principles: progress indication, address autofill, payment method clarity, and error prevention. These are not generic checkout forms but conversion-engineered payment experiences.",
      "All checkout flows use Tailwind CSS with form validation, accessible error handling, and responsive layouts. React components handle payment processing, address validation, and order summary updates. Use these as templates for e-commerce checkout, subscription signup, or donation flows."
    ],
    bullets: [
      "Progress indication: visual stepper showing cart, shipping, payment, confirmation",
      "Form simplification: request only essential information, use address autofill",
      "Payment clarity: accepted payment methods displayed prominently",
      "Error prevention: inline validation with specific correction guidance",
      "Trust signals: security badges, money-back guarantee near payment input"
    ],
    expandedSections: [
      {
        heading: "Checkout flow optimization principles",
        paragraphs: [
          "A high-converting checkout flow minimizes steps, reduces form fields, and provides clear progress indication. The optimal flow has three steps: cart review, shipping address, and payment. Merge billing address with payment to reduce an extra step. Use address autofill and saved payment methods for returning customers.",
          "Weak checkout flows fail because they request unnecessary information or hide progress. If you ask for phone number, company name, or marketing preferences during checkout, you are introducing friction. Defer non-essential data collection until after purchase confirmation."
        ],
        bullets: [
          "Minimize steps: aim for 3-4 steps maximum (cart, shipping, payment, confirmation).",
          "Reduce form fields: request only essential information for order fulfillment.",
          "Use address autofill: integrate Google Places or browser autocomplete.",
          "Show progress: use stepper or breadcrumb to indicate current step.",
          "Provide guest checkout: do not force account creation before purchase."
        ]
      },
      {
        heading: "Common checkout mistakes",
        paragraphs: [
          "The most damaging mistake is forcing account creation before checkout. Users want to complete their purchase quickly; requiring signup introduces friction and increases abandonment. Always offer guest checkout with optional account creation after purchase.",
          "Another frequent error is unclear error messaging. If a credit card is declined, do not show 'Payment failed.' Instead, show 'Card declined. Please try another payment method or contact your bank.' Specific guidance improves recovery."
        ],
        bullets: [
          "Do not force account creation; offer guest checkout with post-purchase registration.",
          "Do not hide checkout costs; show shipping and tax estimates before payment step.",
          "Do not use generic errors; provide specific correction guidance for failed validation.",
          "Do not omit progress indication; users need to know how many steps remain.",
          "Do not ignore mobile optimization; checkout must work on 375px screens."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I use a single-page or multi-step checkout?",
        a: "Multi-step works better for most e-commerce. Single-page is suitable for low-SKU or donation flows."
      },
      {
        q: "How should I handle discount codes in checkout?",
        a: "Include a collapsible 'Have a promo code?' link, do not make it prominent and distract from purchase."
      },
      {
        q: "Should I show security badges in the checkout flow?",
        a: "Yes, display trust signals (SSL badge, payment icons) near payment input to reduce abandonment."
      }
    ]
  },

  "subscription-management-ui": {
    title: "Subscription Management UI Collection",
    summaryParagraphs: [
      "This collection contains subscription management interfaces designed to reduce churn. Each design applies retention principles: upgrade paths prominently displayed, cancellation flows with pause options, billing history transparency, and plan comparison clarity. These are not generic account settings but retention-engineered experiences.",
      "All subscription UIs use Tailwind CSS with accessible forms, modal dialogs, and responsive layouts. React components handle plan switching, payment updates, and cancellation workflows. Use these as templates for SaaS account management, membership portals, or subscription services."
    ],
    bullets: [
      "Upgrade visibility: prominently display plan upgrade options with feature comparison",
      "Cancellation retention: offer pause or downgrade before confirming cancellation",
      "Billing transparency: show upcoming charges, payment history, and invoice downloads",
      "Payment updates: support card changes without service interruption",
      "Usage visibility: display plan limits and current usage to guide upgrade decisions"
    ],
    expandedSections: [
      {
        heading: "Retention-focused subscription UI design",
        paragraphs: [
          "A retention-optimized subscription UI makes upgrades obvious and cancellations difficult (but not deceptive). Display upgrade paths on the main account screen with clear feature differentiation. When users attempt to cancel, offer alternatives: pause subscription, downgrade to cheaper plan, or apply discount.",
          "Weak subscription UIs fail because they make cancellation easier than upgrading or hide billing information. If your cancel button is more prominent than your upgrade CTA, you are optimizing for churn. Instead, feature upgrade benefits and relegate cancellation to account settings."
        ],
        bullets: [
          "Promote upgrades: display plan comparison and upgrade CTA on main screen.",
          "Retain on cancellation: offer pause, downgrade, or discount before confirming.",
          "Show usage metrics: display current usage vs. plan limits to guide decisions.",
          "Simplify payment updates: allow card changes without re-entering billing info.",
          "Provide billing transparency: show next charge date and invoice history."
        ]
      },
      {
        heading: "Common subscription UI mistakes",
        paragraphs: [
          "The most damaging mistake is making cancellation too easy. If your cancel button is on the main account screen, you are encouraging churn. Instead, require users to visit settings, then present retention offers before confirming cancellation. This is not dark patterns; it is giving users alternatives they might prefer.",
          "Another frequent error is hiding usage metrics. If users do not know they are approaching plan limits, they cannot make informed upgrade decisions. Display current usage and plan capacity prominently to guide natural upgrades."
        ],
        bullets: [
          "Do not make cancel button prominent; place it in settings with retention offers.",
          "Do not hide usage data; show current limits and capacity on main screen.",
          "Do not skip retention offers; offer pause or downgrade before confirming cancel.",
          "Do not obscure billing; show next charge date and payment history clearly.",
          "Do not make payment updates difficult; support card changes without service interruption."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I make cancellation difficult to reduce churn?",
        a: "No, but offer alternatives (pause, downgrade, discount) before confirming cancellation."
      },
      {
        q: "How should I display plan upgrade options?",
        a: "Show feature comparison and upgrade CTA on main account screen, not buried in settings."
      },
      {
        q: "Should I send notifications before billing?",
        a: "Yes, send email 3-7 days before charge with invoice preview and payment method confirmation."
      }
    ]
  },

  "analytics-kpi-dashboards": {
    title: "Analytics & KPI Dashboards Collection",
    summaryParagraphs: [
      "This collection features analytics dashboards optimized for decision-making. Each design applies data hierarchy principles: primary KPIs dominate space, trends are visualized with context, and drill-down paths are clear. These are not generic reporting screens but decision-engineered analytics interfaces.",
      "All dashboards use Tailwind CSS with accessible charts, responsive grids, and semantic markup. React components handle data visualization, date range selection, and export functionality. Use these as templates for business intelligence dashboards, marketing analytics, or operational monitoring."
    ],
    bullets: [
      "KPI prominence: primary metrics use largest typography and dominant positioning",
      "Trend visualization: sparklines or mini charts show change direction and magnitude",
      "Comparison context: show current value vs. previous period or target",
      "Drill-down clarity: interactive charts link to detailed breakdowns",
      "Export options: support CSV or PDF download for sharing and reporting"
    ],
    expandedSections: [
      {
        heading: "Designing decision-focused analytics dashboards",
        paragraphs: [
          "A high-quality analytics dashboard answers three questions immediately: What is the current state? How does it compare to expectations? What needs attention? Primary KPIs answer the first, comparison metrics answer the second, and alerts or anomalies answer the third.",
          "Weak analytics dashboards fail because they treat all metrics equally or omit comparison context. A revenue number without a trend or target tells users nothing. Instead, show current revenue, percentage change from last month, and visual indicator of whether it is above or below target."
        ],
        bullets: [
          "Prioritize KPIs: size metrics by business impact, not data availability.",
          "Provide comparison: show current value vs. previous period or target.",
          "Visualize trends: use sparklines or mini bar charts for change direction.",
          "Highlight anomalies: use color or badges to flag metrics needing attention.",
          "Support drill-down: make charts interactive with links to detailed views."
        ]
      },
      {
        heading: "Common analytics dashboard mistakes",
        paragraphs: [
          "The most common mistake is displaying too many metrics without hierarchy. If your dashboard has 20 equal-sized cards, users cannot prioritize. Instead, allocate space by decision impact: primary KPIs should be 2-3x larger than secondary metrics.",
          "Another frequent error is omitting comparison context. A number without a reference point is meaningless. Always show percentage change, previous period value, or progress toward target to enable interpretation."
        ],
        bullets: [
          "Do not treat all metrics equally; prioritize by decision impact.",
          "Do not omit comparison context; show change from previous period or target.",
          "Do not use decoration; reserve color for semantic encoding (good/bad/neutral).",
          "Do not ignore loading states; show skeleton screens during data fetch.",
          "Do not skip export options; support CSV or PDF for reporting and sharing."
        ]
      }
    ],
    faqs: [
      {
        q: "How many KPIs should I display on a dashboard?",
        a: "3-5 primary KPIs maximum. More than that creates cognitive overload and reduces decision clarity."
      },
      {
        q: "Should I use real-time data or cached metrics?",
        a: "Depends on use case. Real-time for operational monitoring, cached (hourly/daily) for strategic KPIs."
      },
      {
        q: "What chart types work best for dashboard KPIs?",
        a: "Sparklines for trends, bar charts for comparisons, gauge charts for progress toward goal."
      }
    ]
  },

  "admin-operations-tables": {
    title: "Admin & Operations Tables Collection",
    summaryParagraphs: [
      "This collection showcases data tables optimized for operational tasks. Each design applies information scannability principles: column prioritization, bulk action clarity, filter discoverability, and pagination performance. These are not generic HTML tables but task-engineered data management interfaces.",
      "All tables use Tailwind CSS with accessible markup, responsive layouts, and keyboard navigation. React components handle sorting, filtering, pagination, and bulk operations. Use these as templates for admin panels, CRM interfaces, or operational dashboards."
    ],
    bullets: [
      "Column prioritization: most important data in leftmost columns",
      "Bulk actions: checkbox selection with action bar for multi-item operations",
      "Filter discoverability: search and filter controls positioned prominently",
      "Pagination clarity: current page, total records, and per-page options visible",
      "Row actions: edit, delete, or view controls positioned consistently per row"
    ],
    expandedSections: [
      {
        heading: "Designing task-optimized data tables",
        paragraphs: [
          "A high-quality operations table optimizes for scannability and task completion. The most critical information (ID, name, status) should occupy the leftmost columns. Action columns (edit, delete) should anchor to the right. Bulk actions should appear in a persistent action bar when rows are selected.",
          "Weak data tables fail because they dump all columns without prioritization or hide critical actions. If users must horizontal-scroll to see row actions or cannot filter by status, you are introducing friction. Optimize column order by task frequency and provide prominent filters."
        ],
        bullets: [
          "Prioritize columns: place ID, name, status in leftmost positions.",
          "Anchor actions: position edit/delete icons in rightmost column.",
          "Support bulk operations: show action bar when multiple rows selected.",
          "Provide filters: include search, status, and date range filtering.",
          "Optimize pagination: show current page, total records, and per-page selector."
        ]
      },
      {
        heading: "Common data table mistakes",
        paragraphs: [
          "The most damaging mistake is showing too many columns without prioritization. If your table has 15 visible columns, users cannot scan efficiently. Instead, display only essential columns by default and allow users to show/hide others via column selector.",
          "Another frequent error is unclear bulk actions. If users select multiple rows but see no action bar, they will assume bulk operations are not supported. Display a sticky action bar with available operations (delete, export, update status) when rows are selected."
        ],
        bullets: [
          "Do not show all columns; display essentials with column selector for optional fields.",
          "Do not hide bulk actions; show action bar when rows are selected.",
          "Do not omit filters; provide search, status, and date filtering.",
          "Do not ignore pagination; support per-page selection and total record count.",
          "Do not skip keyboard navigation; support arrow keys and keyboard shortcuts."
        ]
      }
    ],
    faqs: [
      {
        q: "How many columns should I display by default?",
        a: "5-7 columns maximum for desktop, 3-4 for tablet. Provide column selector for additional fields."
      },
      {
        q: "Should I support infinite scroll or pagination?",
        a: "Pagination for operational tables. Infinite scroll works better for content feeds, not data management."
      },
      {
        q: "How should I handle mobile table layouts?",
        a: "Use card-based layout for mobile, not horizontal scrolling. Stack key fields vertically per item."
      }
    ]
  },

  "portfolio-case-studies": {
    title: "Portfolio & Case Studies Collection",
    summaryParagraphs: [
      "This collection features portfolio and case study layouts optimized for credibility. Each design applies narrative structure: problem statement, solution approach, measurable outcome, and supporting visuals. These are not generic project showcases but results-engineered portfolio pieces.",
      "All case studies use Tailwind CSS with accessible markup, lazy-loaded images, and responsive layouts. React components handle image galleries, video embeds, and scroll animations. Use these as templates for agency portfolios, consultant case studies, or product showcases."
    ],
    bullets: [
      "Narrative structure: problem, solution, outcome in clear sections",
      "Metric prominence: quantifiable results displayed in large typography",
      "Visual proof: before/after comparisons, screenshots, or product demos",
      "Client attribution: company name, logo, and testimonial quote",
      "CTA clarity: contact or project inquiry action at case study end"
    ],
    expandedSections: [
      {
        heading: "Building credible case study narratives",
        paragraphs: [
          "A high-credibility case study follows a clear structure: introduce the client and problem, explain the solution approach with specifics, and present measurable outcomes with proof. The outcome section should use numbers: percentage increase, dollar value, time saved, or user growth.",
          "Weak case studies fail because they use vague descriptions or omit measurable results. Saying 'We helped them improve their website' is not credible. Instead, state 'We redesigned their checkout flow, reducing cart abandonment from 68% to 41% and increasing monthly revenue by $47K.'"
        ],
        bullets: [
          "State the problem: describe client's specific challenge or constraint.",
          "Explain the solution: detail approach, methodology, or unique insight.",
          "Quantify outcomes: use percentage change, dollar value, or user metrics.",
          "Provide proof: include screenshots, testimonials, or third-party validation.",
          "Include CTA: guide readers to contact you or view similar work."
        ]
      },
      {
        heading: "Common case study mistakes",
        paragraphs: [
          "The most damaging mistake is using vague language or omitting measurable results. Case studies without numbers lack credibility. Always include quantified outcomes: revenue increase, conversion lift, time savings, or user growth. If you cannot quantify, use qualitative proof like client testimonials or third-party press coverage.",
          "Another frequent error is burying the outcome. Users scan case studies to assess credibility quickly. Position the measurable result prominently at the top or in a highlighted section, not buried in paragraph text."
        ],
        bullets: [
          "Do not use vague descriptions; specify problem, solution, and quantified outcome.",
          "Do not omit metrics; include percentage change, dollar value, or growth numbers.",
          "Do not hide results; position outcomes prominently in summary or dedicated section.",
          "Do not skip visuals; use screenshots, before/after images, or video demos.",
          "Do not ignore client attribution; include company name, logo, and testimonial."
        ]
      }
    ],
    faqs: [
      {
        q: "How long should a case study be?",
        a: "Long enough to establish credibility: 400-800 words plus visuals. Prioritize outcome clarity over length."
      },
      {
        q: "Should I include client logos in case studies?",
        a: "Yes, logos add credibility. Get client permission and display prominently in case study header."
      },
      {
        q: "What if I cannot share specific metrics?",
        a: "Use ranges (increased conversion by 30-40%) or qualitative proof (client testimonial, press mention)."
      }
    ]
  },

  "agency-landing-pages": {
    title: "Agency Landing Pages Collection",
    summaryParagraphs: [
      "This collection showcases agency landing pages optimized for lead generation. Each design applies service clarity principles: specialization statement, process transparency, case study proof, and contact friction reduction. These are not generic About pages but lead-engineered agency homepages.",
      "All landing pages use Tailwind CSS with accessible markup, performance-optimized images, and responsive layouts. React components handle case study carousels, contact forms, and testimonial displays. Use these as templates for agency websites, consultancy homepages, or professional services."
    ],
    bullets: [
      "Specialization clarity: state who you serve and what problem you solve",
      "Process transparency: outline engagement steps or methodology",
      "Case study proof: display client logos, outcomes, or project examples",
      "Contact simplification: reduce form fields to essential information only",
      "Positioning differentiation: explain what makes your approach unique"
    ],
    expandedSections: [
      {
        heading: "Agency landing page conversion principles",
        paragraphs: [
          "A high-converting agency landing page answers four questions: Who do you serve? What problem do you solve? Why should I believe you? How do I get started? The headline answers the first two, case studies answer the third, and contact form answers the fourth.",
          "Weak agency pages fail because they use generic positioning or hide proof. A headline like 'We build amazing websites' is meaningless. Instead, use 'We help B2B SaaS companies increase trial signups by 40%+ through conversion-optimized landing pages.' This specifies audience, outcome, and method."
        ],
        bullets: [
          "Specify your audience: name the industry, company size, or role you serve.",
          "State the outcome: quantify the result clients achieve (revenue, growth, savings).",
          "Explain your method: outline process steps or unique methodology.",
          "Display proof: show client logos, case study metrics, or testimonials.",
          "Simplify contact: request only name, email, and brief project description."
        ]
      },
      {
        heading: "Common agency page mistakes",
        paragraphs: [
          "The most damaging mistake is generic positioning. If your headline could apply to any agency, it is not working. Specificity builds credibility: instead of 'Digital Marketing Agency,' use 'PPC & Conversion Optimization for DTC Brands Scaling Past $1M ARR.' This filters unqualified leads and attracts ideal clients.",
          "Another frequent error is hiding case studies or client logos. Proof should be prominent on the homepage, not buried in a separate portfolio section. Display 3-5 best client outcomes with metrics above the fold."
        ],
        bullets: [
          "Do not use generic positioning; specify industry, role, or company size.",
          "Do not hide proof; display client logos and case study metrics prominently.",
          "Do not overwhelm with services; focus on 2-3 core offerings, not 15 capabilities.",
          "Do not complicate contact; request minimal information in initial form.",
          "Do not ignore mobile layout; most agency traffic is mobile."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I list all services on my agency homepage?",
        a: "No, focus on 2-3 core offerings. Too many services dilute positioning and confuse visitors."
      },
      {
        q: "How many case studies should I feature on the homepage?",
        a: "3-5 best results with quantified outcomes. Link to full portfolio for additional examples."
      },
      {
        q: "Should I include pricing on my agency landing page?",
        a: "Only if you offer standardized packages. For custom work, use 'starting at' ranges or guide to contact."
      }
    ]
  },

  "community-event-pages": {
    title: "Community & Event Pages Collection",
    summaryParagraphs: [
      "This collection features community and event pages optimized for registration. Each design applies urgency principles: date and location prominence, agenda clarity, speaker credibility, and ticketing friction reduction. These are not generic event listings but conversion-engineered event pages.",
      "All event pages use Tailwind CSS with accessible markup, countdown timers, and responsive layouts. React components handle ticket selection, speaker bios, and schedule displays. Use these as templates for conferences, webinars, meetups, or virtual events."
    ],
    bullets: [
      "Date and location prominence: display event details in hero section",
      "Agenda transparency: show schedule, topics, and speaker lineup",
      "Speaker credibility: include photos, bios, and social proof for presenters",
      "Registration simplification: reduce ticketing form to essential fields",
      "Urgency signals: countdown timer, limited seats, or early-bird pricing"
    ],
    expandedSections: [
      {
        heading: "Event page conversion principles",
        paragraphs: [
          "A high-converting event page answers four questions immediately: When and where? Who is speaking? What will I learn? How do I register? The hero section answers the first, speaker section answers the second, agenda answers the third, and registration CTA answers the fourth.",
          "Weak event pages fail because they hide critical details or create registration friction. If users must scroll to find the date or click multiple times to buy tickets, you are losing registrations. Position all essential information above the fold with a prominent registration CTA."
        ],
        bullets: [
          "Display date and location: show event details prominently in hero section.",
          "Highlight speakers: include photos, bios, and credentials for credibility.",
          "Outline agenda: provide schedule with session topics and speaker names.",
          "Simplify registration: request only name, email, and ticket selection.",
          "Add urgency: use countdown timer or limited seats messaging."
        ]
      },
      {
        heading: "Common event page mistakes",
        paragraphs: [
          "The most damaging mistake is hiding the event date or location. If users must hunt for this information, they will leave. Position the date, time, and venue prominently in the hero section with a clear format: 'March 15, 2024 | 9 AM - 5 PM PT | San Francisco, CA.'",
          "Another frequent error is unclear agenda. If users do not know what they will learn or who is speaking, they will not register. Provide a detailed schedule with session titles, speaker names, and time slots."
        ],
        bullets: [
          "Do not hide date or location; display prominently in hero section.",
          "Do not omit agenda; show schedule with session titles and speakers.",
          "Do not skip speaker bios; include photos and credentials for credibility.",
          "Do not complicate registration; request minimal information upfront.",
          "Do not ignore urgency; use countdown or limited seat messaging."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I include speaker headshots on event pages?",
        a: "Yes, photos increase credibility. Use professional headshots with speaker name and title."
      },
      {
        q: "How detailed should the event agenda be?",
        a: "Show session titles, speaker names, and time slots. Link to full descriptions for more detail."
      },
      {
        q: "Should I use early-bird pricing for events?",
        a: "Yes, tiered pricing with deadlines increases urgency and drives early registrations."
      }
    ]
  },

  "waitlist-early-access": {
    title: "Waitlist & Early Access Pages Collection",
    summaryParagraphs: [
      "This collection contains waitlist and early access pages optimized for signup momentum. Each design applies anticipation-building principles: value proposition clarity, exclusivity framing, social proof display, and signup friction elimination. These are not generic coming soon pages but launch-engineered pre-registration experiences.",
      "All waitlist pages use Tailwind CSS with accessible forms, email validation, and responsive layouts. React components handle form submission, confirmation messaging, and referral tracking. Use these as templates for product launches, beta programs, or pre-order campaigns."
    ],
    bullets: [
      "Value proposition clarity: state what the product does and who it serves",
      "Exclusivity framing: position early access as limited or invite-only",
      "Social proof: display signup count, user testimonials, or investor logos",
      "Signup simplification: request email only, defer additional fields",
      "Confirmation clarity: immediate feedback after signup with next steps"
    ],
    expandedSections: [
      {
        heading: "Building effective waitlist pages",
        paragraphs: [
          "A high-converting waitlist page answers three questions: What is this? Why should I care? How do I get access? The headline answers the first, the value proposition answers the second, and the email form answers the third. Everything else supports these fundamentals.",
          "Weak waitlist pages fail because they use vague descriptions or create signup friction. If users do not understand what they are signing up for or must fill out multiple fields, they will leave. Use a specific headline and request email only."
        ],
        bullets: [
          "Clarify the product: state what it does and who it serves in one sentence.",
          "Frame exclusivity: use 'early access,' 'limited beta,' or 'invite-only' language.",
          "Show momentum: display signup count or waitlist position after registration.",
          "Minimize form fields: request email only, defer name or preferences.",
          "Provide confirmation: show success message with expected timeline or next steps."
        ]
      },
      {
        heading: "Common waitlist page mistakes",
        paragraphs: [
          "The most damaging mistake is vague positioning. If your headline is 'Something awesome is coming,' users will not sign up. Instead, use 'AI-Powered Email Assistant That Writes Replies in Your Voice (Beta Launching March 2024).' This specifies product, benefit, and timeline.",
          "Another frequent error is requesting too much information. If your waitlist form asks for name, email, company, and role, you are introducing friction. Request email only and gather additional details after signup confirmation."
        ],
        bullets: [
          "Do not use vague headlines; specify product, benefit, and launch timeline.",
          "Do not request multiple fields; email-only signup maximizes conversions.",
          "Do not omit social proof; show signup count, testimonials, or investor logos.",
          "Do not skip confirmation; provide immediate success message with next steps.",
          "Do not ignore referral incentives; offer priority access for referrals to accelerate growth."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I show the waitlist count on signup pages?",
        a: "Yes, displaying signup momentum (e.g., '12,487 people waiting') increases perceived demand and urgency."
      },
      {
        q: "How much information should I request for waitlist signup?",
        a: "Email only. Defer additional fields until after confirmation or during onboarding."
      },
      {
        q: "Should I offer referral incentives for waitlist pages?",
        a: "Yes, priority access or bonus features for referrals accelerates list growth and engagement."
      }
    ]
  },

  "knowledge-base-help-centers": {
    title: "Knowledge Base & Help Centers Collection",
    summaryParagraphs: [
      "This collection showcases knowledge base and help center layouts optimized for self-service support. Each design applies information findability principles: category prominence, search discoverability, article hierarchy, and contact escalation. These are not generic FAQ pages but support-engineered help systems.",
      "All help centers use Tailwind CSS with accessible navigation, search autocomplete, and responsive layouts. React components handle article search, category filtering, and feedback collection. Use these as templates for product documentation, customer support portals, or community knowledge bases."
    ],
    bullets: [
      "Category organization: group articles by user intent (getting started, billing, troubleshooting)",
      "Search prominence: search bar positioned in header with autocomplete suggestions",
      "Article hierarchy: clear headings, table of contents, and related article links",
      "Contact escalation: support contact option visible when self-service fails",
      "Feedback collection: helpful/not helpful buttons to improve article quality"
    ],
    expandedSections: [
      {
        heading: "Organizing knowledge bases for self-service success",
        paragraphs: [
          "A high-quality knowledge base organizes content by user intent, not company structure. Categories should reflect common tasks: Getting Started, Billing & Pricing, Troubleshooting, Integrations. Within each category, articles should be ordered by frequency of access, not alphabetically.",
          "Weak help centers fail because they organize by internal teams or technical architecture. Users do not care about 'Platform Features' or 'API Documentation' as top-level categories. Instead, use task-based organization: 'How do I connect my CRM?' or 'Why is my data not syncing?'"
        ],
        bullets: [
          "Organize by user intent: use task-based categories, not company structure.",
          "Prioritize by frequency: order articles by access count, not alphabetically.",
          "Provide search: position prominently with autocomplete and suggested articles.",
          "Include visuals: use screenshots, GIFs, or videos to illustrate steps.",
          "Offer escalation: show contact support option if article does not resolve issue."
        ]
      },
      {
        heading: "Common help center mistakes",
        paragraphs: [
          "The most damaging mistake is organizing content by internal structure instead of user intent. If your top-level categories are 'Product,' 'API,' and 'Platform,' users cannot find answers. Instead, use Getting Started, Account Management, Troubleshooting, and Integrations.",
          "Another frequent error is omitting search. Users should be able to find answers through search without browsing categories. Position search prominently in the header with autocomplete suggestions."
        ],
        bullets: [
          "Do not organize by company structure; use task-based categories.",
          "Do not hide search; position prominently with autocomplete.",
          "Do not skip visuals; use screenshots or videos to clarify steps.",
          "Do not omit contact escalation; show support option if self-service fails.",
          "Do not ignore article feedback; collect helpful/not helpful data to improve content."
        ]
      }
    ],
    faqs: [
      {
        q: "How should I organize help center categories?",
        a: "By user intent: Getting Started, Billing, Troubleshooting, Integrations. Not by company structure."
      },
      {
        q: "Should I include videos in help articles?",
        a: "Yes, for complex workflows. Use short screen recordings (30-90 seconds) with captions."
      },
      {
        q: "How do I know which articles to write first?",
        a: "Analyze support tickets by frequency. Write articles for the top 10 most common questions first."
      }
    ]
  },

  "design-system-libraries": {
    title: "Design System & Component Libraries Collection",
    summaryParagraphs: [
      "This collection features design system and component library pages optimized for developer adoption. Each design applies documentation clarity principles: component previews, prop specifications, usage examples, and accessibility guidance. These are not generic style guides but developer-focused design systems.",
      "All design system pages use Tailwind CSS with syntax-highlighted code blocks, live component previews, and responsive layouts. React components handle code copying, theme switching, and interactive examples. Use these as templates for internal design systems, open-source UI libraries, or component documentation."
    ],
    bullets: [
      "Component previews: live interactive examples with variant demonstrations",
      "Prop documentation: list all props with types, defaults, and descriptions",
      "Usage examples: show code snippets for common implementation patterns",
      "Accessibility guidance: include ARIA labels, keyboard navigation, and WCAG compliance",
      "Copy functionality: one-click code copying for component examples"
    ],
    expandedSections: [
      {
        heading: "Documenting design systems for developer adoption",
        paragraphs: [
          "A high-quality design system page includes four components: live preview, prop list, usage code, and accessibility notes. The preview shows the component in action with variant toggles. The prop list specifies all available properties with types and defaults. Usage code provides copy-paste examples. Accessibility notes explain keyboard navigation and ARIA requirements.",
          "Weak design system docs fail because they omit one of these elements or provide generic descriptions without specifics. Developers need working code, not conceptual explanations. Every component should include runnable examples that can be copied directly into projects."
        ],
        bullets: [
          "Show live preview: render component with interactive variant switcher.",
          "List props with types: include property name, type, default, and description.",
          "Provide usage examples: show code snippets for common patterns.",
          "Include accessibility: explain keyboard navigation, ARIA labels, and focus management.",
          "Support code copying: add copy button to all code examples."
        ]
      },
      {
        heading: "Common design system documentation mistakes",
        paragraphs: [
          "The most damaging mistake is omitting code examples. If developers must guess at implementation details, they will not adopt your design system. Every component should include at least one working code example with expected output.",
          "Another frequent error is poor prop documentation. Listing props without types or defaults forces developers to inspect source code. Instead, create a structured table with property name, type, default value, and description."
        ],
        bullets: [
          "Do not omit code examples; every component needs runnable sample code.",
          "Do not skip prop documentation; list types, defaults, and descriptions.",
          "Do not hide accessibility notes; explain keyboard navigation and ARIA requirements.",
          "Do not ignore variants; show all component states (default, hover, disabled, error).",
          "Do not forget theming; demonstrate how components adapt to color or size tokens."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I include Figma files with my design system documentation?",
        a: "Yes, link to Figma library from component docs to support designer-developer handoff."
      },
      {
        q: "How should I document component variants?",
        a: "Show a live preview, list props with types, include do/don't usage examples, and link to accessibility guidelines."
      },
      {
        q: "Should design systems include dark mode variants?",
        a: "Yes, if your product supports dark mode. Show theme switcher and document color token mappings."
      }
    ]
  },

  "app-shell-layouts": {
    title: "App Shell Layouts Collection",
    summaryParagraphs: [
      "This collection showcases application shell layouts optimized for SaaS products. Each design applies navigation hierarchy principles: primary actions in sidebar, contextual actions in header, global search prominence, and responsive collapsibility. These are not generic admin templates but product-engineered app frameworks.",
      "All app shells use Tailwind CSS with accessible navigation, keyboard shortcuts, and responsive breakpoints. React components handle sidebar state, user menus, and notification systems. Use these as templates for SaaS dashboards, web applications, or admin panels."
    ],
    bullets: [
      "Navigation hierarchy: primary navigation in sidebar, secondary in header",
      "Search prominence: global search positioned in header with keyboard shortcut",
      "User context: account menu and notifications in top-right corner",
      "Responsive collapsibility: sidebar collapses to icon-only or mobile menu",
      "Breadcrumb clarity: show current location within navigation hierarchy"
    ],
    expandedSections: [
      {
        heading: "Designing effective app shell navigation",
        paragraphs: [
          "A high-quality app shell separates primary navigation (sidebar) from contextual actions (header). Primary navigation links to major product areas: Dashboard, Projects, Settings. Contextual actions apply to current view: Create New, Filter, Export. This separation improves scannability and reduces cognitive load.",
          "Weak app shells fail because they mix navigation levels or hide critical actions. If your sidebar includes both major sections and page-specific filters, users cannot distinguish hierarchy. Instead, reserve the sidebar for top-level navigation and place contextual actions in the header or content area."
        ],
        bullets: [
          "Separate navigation levels: sidebar for primary, header for contextual.",
          "Position global search: place in header with keyboard shortcut (⌘K).",
          "Group user actions: account menu, notifications, and help in top-right.",
          "Support keyboard navigation: assign shortcuts for common actions.",
          "Collapse responsively: sidebar becomes icon-only or mobile menu."
        ]
      },
      {
        heading: "Common app shell mistakes",
        paragraphs: [
          "The most damaging mistake is overloading the sidebar with too many navigation items. If your sidebar has 15+ links, users cannot scan efficiently. Limit primary navigation to 5-7 major sections and use nested menus or secondary navigation for sub-items.",
          "Another frequent error is unclear active state. If users cannot tell which page they are on, navigation fails. Use background color, border, or font weight to indicate the active navigation item."
        ],
        bullets: [
          "Do not overload sidebar; limit to 5-7 primary navigation items.",
          "Do not hide active state; clearly indicate current page in navigation.",
          "Do not mix navigation levels; separate primary (sidebar) from contextual (header).",
          "Do not omit keyboard shortcuts; support ⌘K search and ⌘/ help.",
          "Do not ignore mobile; sidebar must collapse to hamburger menu on small screens."
        ]
      }
    ],
    faqs: [
      {
        q: "Should I use a sidebar or top navigation for SaaS apps?",
        a: "Sidebar works best for products with 5+ primary sections. Top nav works for simpler apps with 3-4 sections."
      },
      {
        q: "How should I handle nested navigation in app shells?",
        a: "Use collapsible sidebar sections or secondary navigation in header. Avoid nesting beyond 2 levels."
      },
      {
        q: "Should I include breadcrumbs in app navigation?",
        a: "Yes, for multi-level hierarchies. Position breadcrumbs in header to show current location."
      }
    ]
  }
};
