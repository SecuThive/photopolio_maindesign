type SeoExpandedSection = {
  heading: string;
  paragraphs: string[];
  bullets?: string[];
};

type SeoFaq = {
  q: string;
  a: string;
};

type SeoGEOContentProps = {
  title: string;
  summaryParagraphs: string[];
  bullets: string[];
  expandedSections: SeoExpandedSection[];
  faqs?: SeoFaq[];
};

export default function SeoGEOContent({
  title,
  summaryParagraphs,
  bullets,
  expandedSections,
  faqs = [],
}: SeoGEOContentProps) {
  const faqSchema = faqs.length
    ? {
        '@context': 'https://schema.org',
        '@type': 'FAQPage',
        mainEntity: faqs.map((faq) => ({
          '@type': 'Question',
          name: faq.q,
          acceptedAnswer: {
            '@type': 'Answer',
            text: faq.a,
          },
        })),
      }
    : null;

  return (
    <div className="space-y-6">
      {faqSchema && (
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema).replace(/</g, '\u003c') }}
        />
      )}
      <div className="space-y-4">
        <h2 className="text-2xl md:text-3xl font-semibold text-gray-900">{title}</h2>
        {summaryParagraphs.map((paragraph, index) => (
          <p key={`${title}-summary-${index}`} className="text-sm sm:text-base text-gray-700 leading-relaxed">
            {paragraph}
          </p>
        ))}
      </div>

      {bullets.length > 0 && (
        <ul className="space-y-2 text-sm text-gray-700">
          {bullets.map((bullet) => (
            <li key={bullet} className="flex gap-2">
              <span className="mt-1 h-1.5 w-1.5 rounded-full bg-gray-900" aria-hidden="true" />
              <span>{bullet}</span>
            </li>
          ))}
        </ul>
      )}

      {expandedSections.length > 0 && (
        <details className="rounded-2xl border border-gray-200 bg-gray-50/70 p-5">
          <summary className="cursor-pointer text-sm font-semibold uppercase tracking-[0.3em] text-gray-600">
            Read more
          </summary>
          <div className="mt-5 space-y-6">
            {expandedSections.map((section) => (
              <div key={section.heading} className="space-y-3">
                <h3 className="text-lg font-semibold text-gray-900">{section.heading}</h3>
                {section.paragraphs.map((paragraph, index) => (
                  <p key={`${section.heading}-p-${index}`} className="text-sm text-gray-700 leading-relaxed">
                    {paragraph}
                  </p>
                ))}
                {section.bullets && section.bullets.length > 0 && (
                  <ul className="space-y-2 text-sm text-gray-700">
                    {section.bullets.map((bullet) => (
                      <li key={bullet} className="flex gap-2">
                        <span className="mt-1 h-1.5 w-1.5 rounded-full bg-gray-900" aria-hidden="true" />
                        <span>{bullet}</span>
                      </li>
                    ))}
                  </ul>
                )}
              </div>
            ))}
          </div>
        </details>
      )}

      {faqs.length > 0 && (
        <details className="rounded-2xl border border-gray-200 bg-white/90 p-5">
          <summary className="cursor-pointer text-sm font-semibold uppercase tracking-[0.3em] text-gray-600">
            FAQs
          </summary>
          <div className="mt-5 space-y-4">
            {faqs.map((faq) => (
              <div key={faq.q} className="space-y-2">
                <h3 className="text-base font-semibold text-gray-900">{faq.q}</h3>
                <p className="text-sm text-gray-700 leading-relaxed">{faq.a}</p>
              </div>
            ))}
          </div>
        </details>
      )}
    </div>
  );
}
