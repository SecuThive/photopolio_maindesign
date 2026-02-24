import type { Metadata } from "next";
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import EzoicPlacements from '@/components/EzoicPlacements';
import { getPlacementIds } from '@/lib/ezoic';
import { buildFAQSchema } from '@/lib/richSnippets';

export const metadata: Metadata = {
  title: "FAQ - Free AI Design Tool Questions Answered (2026)",
  description: "Get instant answers about using UI Syntax web designs. Learn about licensing, copy-paste code, customization, and implementation.",
  alternates: {
    canonical: 'https://ui-syntax.com/faq',
  },
  openGraph: {
    title: "FAQ - Your Free AI Design Questions Answered",
    description: "Everything you need to know about using UI Syntax designs with copy-paste code.",
    url: 'https://ui-syntax.com/faq',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function FAQPage() {
  const placementIds = getPlacementIds('NEXT_PUBLIC_EZOIC_PLACEMENTS_FAQ');
  
  const faqs = [
    {
      category: "Getting Started",
      questions: [
        {
          q: "What is UI Syntax?",
          a: "UI Syntax is a curated gallery of AI-generated web design inspiration specifically created for SaaS founders, product designers, and front-end engineers. We provide production-ready design patterns and layouts that follow modern web standards and best practices."
        },
        {
          q: "How are the designs created?",
          a: "All designs in our gallery are generated using advanced AI models trained on contemporary web design patterns. Each design is carefully curated to ensure it meets professional standards and represents current industry trends in SaaS, fintech, and commerce."
        },
        {
          q: "Is UI Syntax free to use?",
          a: "Yes! UI Syntax is completely free to browse and use. All designs can be viewed, referenced, and implemented in your projects without any cost."
        }
      ]
    },
    {
      category: "Usage & Licensing",
      questions: [
        {
          q: "Can I use these designs in my commercial projects?",
          a: "Absolutely! All designs on UI Syntax can be freely used for both personal and commercial projects. You can implement the design patterns, layouts, and concepts in client work, SaaS products, or any commercial application without restrictions."
        },
        {
          q: "Do I need to provide attribution?",
          a: "While attribution to UI Syntax is appreciated, it is not required. You're free to use the designs without crediting our platform, though we always love to see what you create!"
        },
        {
          q: "Can I modify the designs?",
          a: "Yes! Feel free to customize, modify, and adapt any design to fit your specific needs. The designs are meant to serve as inspiration and starting points for your own unique implementations."
        },
        {
          q: "Can I share these designs with my team?",
          a: "Absolutely! You can share design links with your team, clients, or colleagues. However, please don't redistribute the entire gallery or substantial portions as your own collection."
        }
      ]
    },
    {
      category: "Design Implementation",
      questions: [
        {
          q: "How do I implement these designs?",
          a: "Each design page provides HTML with Tailwind CSS classes plus React component code that you can copy and paste as a starting point. Adapt the code to your preferred framework (Next.js, Vue, Angular, etc.) and styling approach. All designs serve as templates and inspiration for your own implementations."
        },
        {
          q: "Are the designs responsive?",
          a: "Most designs follow modern responsive design principles. However, you may need to adjust breakpoints and mobile layouts to match your specific requirements and target devices."
        },
        {
          q: "What frameworks do these designs support?",
          a: "Design pages provide HTML with Tailwind CSS utility classes and React component code when available. You can adapt these patterns to modern frameworks including Next.js, Vue, Angular, and Svelte."
        },
        {
          q: "Do the designs include JavaScript functionality?",
          a: "The designs focus primarily on layout and visual design. Interactive elements and complex functionality will need to be implemented separately based on your technology stack and requirements."
        }
      ]
    },
    {
      category: "Design Categories & Features",
      questions: [
        {
          q: "What types of designs are available?",
          a: "Our gallery includes a wide variety of web design patterns including landing pages, dashboards, pricing tables, hero sections, navigation menus, forms, cards, components, and full-page layouts across different industries."
        },
        {
          q: "How often are new designs added?",
          a: "We regularly add new designs to the gallery. Follow us or check back frequently to see the latest additions to our collection."
        },
        {
          q: "Can I request specific design types?",
          a: "We welcome suggestions! Contact us at thive8564@gmail.com with your design requests or ideas. While we can't guarantee every request will be fulfilled, we do consider community feedback when curating new designs."
        },
        {
          q: "How do I find designs similar to one I like?",
          a: "Each design page shows related designs in the same category. You can also use the category filters on the homepage or browse our curated collections for themed design sets."
        }
      ]
    },
    {
      category: "Technical Questions",
      questions: [
        {
          q: "What browsers are supported?",
          a: "Designs are created with modern web standards and should work in all contemporary browsers including Chrome, Firefox, Safari, and Edge. Older browsers (like IE11) may require polyfills or additional adjustments."
        },
        {
          q: "Are designs optimized for performance?",
          a: "The base HTML/CSS is lightweight and follows performance best practices. However, final performance depends on your implementation, image optimization, and hosting setup."
        },
        {
          q: "Can I use these with Tailwind CSS?",
          a: "Yes. Design pages provide HTML with Tailwind utility classes and React component code when available. You can use the HTML directly in Tailwind projects or adapt the structure to your preferred framework."
        },
        {
          q: "Do designs follow accessibility standards?",
          a: "We aim for accessible markup, but you should always test and enhance accessibility based on WCAG guidelines for your specific use case, including proper ARIA labels, keyboard navigation, and screen reader compatibility."
        }
      ]
    },
    {
      category: "Account & Support",
      questions: [
        {
          q: "Do I need to create an account?",
          a: "No account is required to browse and use the designs. All content is freely accessible without registration."
        },
        {
          q: "How can I get support?",
          a: "For questions, feedback, or support, please contact us at thive8564@gmail.com. We typically respond within 24-48 hours."
        },
        {
          q: "Can I contribute designs to UI Syntax?",
          a: "We're currently focused on curating AI-generated designs, but we're open to community contributions. Contact us to discuss collaboration opportunities."
        },
        {
          q: "Is there a newsletter or updates list?",
          a: "Stay updated by following our RSS feed at /feed.xml or checking back regularly for new designs and features."
        }
      ]
    }
  ];

  // Create FAQ Schema for Rich Snippets (top 10 most important FAQs)
  const faqSchemaData = [
    { question: "Is UI Syntax free to use?", answer: "Yes. UI Syntax is free to browse and use. Published designs can be viewed, referenced, and implemented in your projects without cost." },
    { question: "Can I use these designs in my commercial projects?", answer: "Absolutely! All designs on UI Syntax can be freely used for both personal and commercial projects. You can implement the design patterns, layouts, and concepts in client work, SaaS products, or any commercial application without restrictions." },
    { question: "Do I need to provide attribution?", answer: "While attribution to UI Syntax is appreciated, it is not required. You're free to use the designs without crediting our platform, though we always love to see what you create!" },
    { question: "How do I implement these designs?", answer: "Each design page provides HTML with Tailwind CSS classes plus React component code that you can copy and paste as a starting point. Adapt the code to your preferred framework and styling approach. All designs serve as templates and inspiration for your own implementations." },
    { question: "Are the designs responsive?", answer: "Most designs follow modern responsive design principles. However, you may need to adjust breakpoints and mobile layouts to match your specific requirements and target devices." },
    { question: "What frameworks do these designs support?", answer: "Design pages provide HTML with Tailwind CSS utility classes and React component code when available. You can adapt these patterns to frameworks including Next.js, Vue, Angular, and Svelte." },
    { question: "Can I modify the designs?", answer: "Yes! Feel free to customize, modify, and adapt any design to fit your specific needs. The designs are meant to serve as inspiration and starting points for your own unique implementations." },
    { question: "Do I need to create an account?", answer: "No account is required to browse and use the designs. All content is freely accessible without registration." },
    { question: "Can I use these with Tailwind CSS?", answer: "Yes! The provided code already uses Tailwind CSS utility classes, so you can copy-paste the markup directly into your Tailwind projects and customize the design tokens to match your brand." },
    { question: "What types of designs are available?", answer: "Our gallery includes landing pages, dashboards, pricing tables, hero sections, navigation menus, forms, cards, components, and full-page layouts for SaaS, fintech, and e-commerce." },
  ];

  const faqSchema = buildFAQSchema(faqSchemaData);

  return (
    <div className="min-h-screen bg-luxury-white flex flex-col">
      {/* FAQ Schema for Rich Snippets */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(faqSchema) }}
      />
      
      <Header />

      <main className="flex-grow">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="text-center mb-12">
            <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Frequently Asked Questions
            </h1>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">
              Everything you need to know about using UI Syntax for your design projects
            </p>
          </div>

          <EzoicPlacements placementIds={placementIds.slice(0, 1)} wrapperClassName="my-8" />

          <div className="space-y-12">
            {faqs.map((section, idx) => (
              <section key={idx} className="border-t border-gray-200 pt-8 first:border-t-0 first:pt-0">
                <h2 className="text-2xl font-semibold text-gray-900 mb-6">
                  {section.category}
                </h2>
                <div className="space-y-6">
                  {section.questions.map((faq, qIdx) => (
                    <div key={qIdx} className="bg-gray-50 rounded-lg p-6 hover:bg-gray-100 transition-colors">
                      <h3 className="text-lg font-semibold text-gray-900 mb-3">
                        {faq.q}
                      </h3>
                      <p className="text-gray-700 leading-relaxed">
                        {faq.a}
                      </p>
                    </div>
                  ))}
                </div>
              </section>
            ))}
          </div>

          <EzoicPlacements placementIds={placementIds.slice(1, 2)} wrapperClassName="my-12" />

          {/* CTA Section */}
          <div className="mt-16 bg-gradient-to-br from-gray-900 to-black rounded-2xl p-8 md:p-12 text-center">
            <h2 className="text-2xl md:text-3xl font-bold text-white mb-4">
              Still have questions?
            </h2>
            <p className="text-gray-300 mb-6 max-w-2xl mx-auto">
              We&rsquo;re here to help! Reach out to our team for personalized assistance with your design needs.
            </p>
            <div className="flex flex-col sm:flex-row gap-4 justify-center">
              <Link
                href="/contact"
                className="inline-flex items-center justify-center px-6 py-3 bg-white text-gray-900 font-semibold rounded-lg hover:bg-gray-100 transition-colors"
              >
                Contact Us
              </Link>
              <Link
                href="/"
                className="inline-flex items-center justify-center px-6 py-3 bg-transparent border-2 border-white text-white font-semibold rounded-lg hover:bg-white hover:text-gray-900 transition-colors"
              >
                Browse Designs
              </Link>
            </div>
          </div>

          {/* Quick Links */}
          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <Link
              href="/about"
              className="p-6 border border-gray-200 rounded-lg hover:border-gray-900 hover:shadow-md transition-all"
            >
              <h3 className="font-semibold text-gray-900 mb-2">About UI Syntax</h3>
              <p className="text-sm text-gray-600">Learn more about our mission and team</p>
            </Link>
            <Link
              href="/terms"
              className="p-6 border border-gray-200 rounded-lg hover:border-gray-900 hover:shadow-md transition-all"
            >
              <h3 className="font-semibold text-gray-900 mb-2">Terms of Service</h3>
              <p className="text-sm text-gray-600">Read our terms and conditions</p>
            </Link>
            <Link
              href="/privacy-policy"
              className="p-6 border border-gray-200 rounded-lg hover:border-gray-900 hover:shadow-md transition-all"
            >
              <h3 className="font-semibold text-gray-900 mb-2">Privacy Policy</h3>
              <p className="text-sm text-gray-600">How we protect your information</p>
            </Link>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
