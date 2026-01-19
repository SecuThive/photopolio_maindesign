import type { Metadata } from "next";
import Link from 'next/link';
import SimpleHeader from '@/components/SimpleHeader';

export const metadata: Metadata = {
  title: "Contact Us",
  description: "Get in touch with UI Syntax. Have questions, feedback, or want to contribute your AI-generated designs? Contact us at thive8564@gmail.com.",
  alternates: {
    canonical: 'https://www.ui-syntax.com/contact',
  },
  openGraph: {
    title: "Contact UI Syntax - AI Design Gallery",
    description: "Get in touch with UI Syntax. Have questions, feedback, or want to contribute your AI-generated designs?",
    url: 'https://www.ui-syntax.com/contact',
  },
};

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-white">
      <SimpleHeader />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Contact UI Syntax</h1>
        
        <div className="prose prose-lg text-gray-700 space-y-6">
          <section>
            <p className="text-lg">
              We partner with modern SaaS teams, developer tool startups, and agencies. If you have a
              product question, feedback on the gallery, or ideas for new templates, we would love to hear from you.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Get in Touch</h2>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 space-y-6">
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

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Feedback & Suggestions</h2>
            <p>
              Your feedback shapes our roadmap. Share feature ideas, new U.S. market segments, or workflow
              improvements and we&rsquo;ll prioritize them in upcoming drops.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">For Designers</h2>
            <p>
              Interested in contributing your AI-generated designs or partnering on a case study? Send us a short
              introduction with links to your portfolio and we&rsquo;ll follow up with the next steps.
            </p>
          </section>

          <section className="mt-12 pt-8 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              Note: We do not provide technical support for third-party tools or services. 
              For general inquiries only.
            </p>
          </section>
        </div>
      </div>

      {/* Footer */}
      <footer className="bg-black border-t border-gray-900 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h2 className="text-xl font-display font-semibold text-white mb-4">UI SYNTAX</h2>
              <p className="text-gray-400 text-sm">AI-generated web design gallery showcasing creative and innovative designs.</p>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Quick Links</h3>
              <ul className="space-y-2">
                <li><Link href="/" className="text-gray-400 hover:text-white text-sm transition-colors">Home</Link></li>
                <li><Link href="/about" className="text-gray-400 hover:text-white text-sm transition-colors">About</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Legal</h3>
              <ul className="space-y-2">
                <li><Link href="/privacy-policy" className="text-gray-400 hover:text-white text-sm transition-colors">Privacy Policy</Link></li>
                <li><Link href="/contact" className="text-gray-400 hover:text-white text-sm transition-colors">Contact</Link></li>
                <li><a href="/feed.xml" className="text-gray-400 hover:text-white text-sm transition-colors">RSS Feed</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-900">
            <p className="text-center text-gray-500 text-sm">© {new Date().getFullYear()} UI Syntax. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
