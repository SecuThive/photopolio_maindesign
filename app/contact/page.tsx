import type { Metadata } from "next";
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import EzoicPlacements from '@/components/EzoicPlacements';
import { getPlacementIds } from '@/lib/ezoic';

export const metadata: Metadata = {
  title: "Contact Us",
  description: "Get in touch with UI Syntax. Have questions, feedback, or want to contribute your AI-generated designs? Contact us at thive8564@gmail.com.",
  alternates: {
    canonical: 'https://ui-syntax.com/contact',
  },
  openGraph: {
    title: "Contact UI Syntax - AI Design Gallery",
    description: "Get in touch with UI Syntax. Have questions, feedback, or want to contribute your AI-generated designs?",
    url: 'https://ui-syntax.com/contact',
  },
};

export default function ContactPage() {
  const placementIds = getPlacementIds('NEXT_PUBLIC_EZOIC_PLACEMENTS_CONTACT');
  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12 sm:py-16">
        <h1 className="text-3xl sm:text-4xl font-bold text-gray-900 mb-6 sm:mb-10">Contact UI Syntax</h1>
        
        <div className="prose prose-base md:prose-lg text-gray-700 space-y-6 md:space-y-8">
          <section>
            <p className="text-base md:text-lg">
              We partner with modern SaaS teams, developer tool startups, and agencies. If you have a
              product question, feedback on the gallery, or ideas for new templates, we would love to hear from you.
            </p>
          </section>

          <section className="mt-10 md:mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Get in Touch</h2>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-6 sm:p-8 space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Email</h3>
                <p className="text-gray-700">
                  <a href="mailto:thive8564@gmail.com" className="text-blue-600 hover:text-blue-800 underline">
                    thive8564@gmail.com
                  </a>
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Business Hours (Pacific Time)</h3>
                <p className="text-gray-700">
                  Monday - Friday: 9:00 AM - 6:00 PM PT<br />
                  Saturday - Sunday: Offline
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Response Time</h3>
                <p className="text-gray-700">
                  We typically respond within 24-48 hours on business days.
                </p>
              </div>
            </div>
          </section>

          <section className="mt-10 md:mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Feedback & Suggestions</h2>
            <p>
              Your feedback shapes our roadmap. Share feature ideas, new U.S. market segments, or workflow
              improvements and we&rsquo;ll prioritize them in upcoming drops.
            </p>
          </section>

          <section className="mt-10 md:mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">For Designers</h2>
            <p>
              Interested in contributing your AI-generated designs or partnering on a case study? Send us a short
              introduction with links to your portfolio and we&rsquo;ll follow up with the next steps.
            </p>
          </section>

          <section className="mt-10 md:mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Frequently Asked Questions</h2>
            <div className="space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Can I use these designs in my projects?</h3>
                <p className="text-gray-700">
                  Yes! Our designs are meant to serve as inspiration and reference for your own projects. While the specific implementations are showcased for educational purposes, you&rsquo;re welcome to draw inspiration and adapt design patterns to your needs. For commercial licensing inquiries, please contact us directly.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">How often do you add new designs?</h3>
                <p className="text-gray-700">
                  We update our gallery regularly with new AI-generated designs, typically adding fresh content weekly. Our curation process ensures that each design meets our quality standards and provides genuine value to the design community.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Do you offer custom design services?</h3>
                <p className="text-gray-700">
                  While UI Syntax primarily focuses on curating and showcasing AI-generated designs, we occasionally collaborate with teams on custom projects. Contact us at thive8564@gmail.com to discuss your specific needs and we&rsquo;ll explore how we can help.
                </p>
              </div>
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">What makes UI Syntax different?</h3>
                <p className="text-gray-700">
                  Unlike generic design galleries, UI Syntax specifically focuses on AI-generated designs with detailed annotations and practical implementation insights. We bridge the gap between AI capabilities and real-world design needs, providing context, best practices, and technical considerations alongside each showcase.
                </p>
              </div>
            </div>
          </section>

          <section className="mt-10 md:mt-12 pt-6 md:pt-8 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              Note: We do not provide technical support for third-party tools or services. 
              For general inquiries only.
            </p>
          </section>
        </div>
      </div>

      {placementIds.length > 0 && (
        <EzoicPlacements placementIds={placementIds} wrapperClassName="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 my-12 sm:my-16" />
      )}
      <Footer />
    </div>
  );
}
