# QA & Monitoring - 2026-02-14

## Automated Checks

| Check | Command | Result | Notes |
| --- | --- | --- | --- |
| ESLint (Next.js ruleset) | `npm run lint` | ✅ Completed with warnings | `<img>` usages remain on the journal listing and detail templates while we decide whether to migrate to `next/image`. See [app/blog/page.tsx#L95-L144](app/blog/page.tsx#L95-L144) and [app/blog/[slug]/page.tsx#L85-L134](app/blog/%5Bslug%5D/page.tsx#L85-L134). |
| Production build | `npm run build` | ✅ Completed | Build succeeds; the only warnings mirror the lint output plus font preconnect notices that stem from our manual `<link>` strategy in [app/layout.tsx#L135-L187](app/layout.tsx#L135-L187). |

**Open items:**
- Decide whether to refactor the journal templates to `next/image` or suppress `@next/next/no-img-element` (current blockers: we stream external Supabase image URLs that may not be optimized via Next Image without additional configuration).
- Either add Google Font `<link rel="preconnect">` tags to `pages/_document.tsx` or migrate to `next/font` to silence `@next/next/no-page-custom-font`.

## Structured Data Audit

| Surface | Schema Types | Evidence |
| --- | --- | --- |
| Design detail | `CreativeWork`, `BreadcrumbList` | Generated via `buildDesignCreativeWorkSchema` plus runtime breadcrumbs before the main layout in [app/design/[slug]/page.tsx#L360-L385](app/design/%5Bslug%5D/page.tsx#L360-L385). |
| Collections | `ItemList`, `FAQPage` | Both schemas are assembled from Supabase data and inlined at render time in [app/collections/[slug]/page.tsx#L50-L83](app/collections/%5Bslug%5D/page.tsx#L50-L83). |
| Blog listing | `ItemList` | The feed emits an ItemList for all published posts in [app/blog/page.tsx#L45-L57](app/blog/page.tsx#L45-L57). |
| Blog detail | `BlogPosting` | Each article injects a page-level payload sourced from `buildBlogPostingSchema` in [app/blog/[slug]/page.tsx#L72-L95](app/blog/%5Bslug%5D/page.tsx#L72-L95). |
| Global layout | `Organization` | The site-wide `structuredData` blob continues to load inside the document head in [app/layout.tsx#L184-L187](app/layout.tsx#L184-L187). |

**Validation approach:**
1. Run `npm run build` to ensure every route prerenders without JSON serialization errors.
2. For spot checks, start `npm run dev`, open a target page (e.g., `/design/slug`), and paste the `View Source` JSON-LD blocks into Google's Rich Results Test.
3. Because every schema payload is generated through shared helpers in [lib/structuredData.ts](lib/structuredData.ts), updating them automatically propagates to all surfaces above.

## Lighthouse & Search Console Playbook

1. **Local Lighthouse sweeps**
   - Run `npm run build && npm run start` locally.
   - Open Chrome DevTools Lighthouse against `/`, `/collections/<slug>`, `/design/<slug>`, `/blog`, and `/playbooks/<slug>`.
   - Archive the JSON export in `docs/qa-monitoring` with the date stamp for future regressions.
2. **Search Console**
   - Use the URL Inspection tool after deployment for representative routes (home, collection, design, blog detail) to confirm indexing and enhanced result eligibility.
   - Submit sitemap partitions (`/sitemap.xml`, `/sitemap-playbooks.xml`, `/sitemap-collections.xml`, etc.) through the Sitemaps panel to prime recrawl after large content batches.
3. **Structured data spot checks**
   - Plug each JSON-LD block into Rich Results Test and Schema Markup Validator when introducing new fields.
   - Track failures in this document with a short reproduction description and resolution link.
4. **Performance budgets**
   - Capture Lighthouse performance and CLS scores for the hero templates; treat >10% regressions as release blockers.

## Monitoring Dashboard Wishlist

- **Supabase metrics**: Create a scheduled job (Daily) that logs row counts for `designs`, `posts`, and `metrics` tables so we can detect ingestion stalls.
- **Edge runtime coverage**: Document which routes still use Edge (see `next build` summary). Add synthetic checks if any critical funnel page depends on Edge functions.
- **Alert hooks**: Hook Vercel build webhooks into Slack to surface lint/build regressions immediately.

## Next Actions

1. Decide on the `next/image` strategy for the blog pages or formally suppress the lint rule.
2. Evaluate migrating to `next/font` to eliminate the remaining font warnings and guarantee preconnect coverage.
3. Schedule the Lighthouse & Search Console sweeps above once the deployment hits production; attach exports or screenshots back into this doc for sign-off.
