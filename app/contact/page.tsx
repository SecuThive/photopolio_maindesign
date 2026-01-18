import type { Metadata } from "next";
import Link from 'next/link';

export const metadata: Metadata = {
  title: "Contact Us",
  description: "Get in touch with Base Syntax. Have questions, feedback, or want to contribute your AI-generated designs? Contact us at thive8564@gmail.com.",
  alternates: {
    canonical: 'https://www.ui-syntax.com/contact',
  },
  openGraph: {
    title: "Contact Base Syntax - AI Design Gallery",
    description: "Get in touch with Base Syntax. Have questions, feedback, or want to contribute your AI-generated designs?",
    url: 'https://www.ui-syntax.com/contact',
  },
};

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-black border-b border-gray-900 sticky top-0 z-40 backdrop-blur-sm bg-opacity-95">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            <div className="flex items-center">
              <h1 className="text-2xl md:text-3xl font-display font-semibold text-white tracking-tight">
                <Link href="/" className="hover:opacity-80 transition-opacity">
                  BASE SYNTAX
                </Link>
              </h1>
              <span className="ml-3 text-xs text-gray-500 font-light tracking-widest uppercase hidden sm:block">
                AI Design Gallery
              </span>
            </div>
          </div>
        </div>
      </header>

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Contact Us</h1>
        
        <div className="prose prose-lg text-gray-700 space-y-6">
          <section>
            <p className="text-lg">
              We'd love to hear from you! Whether you have a question, feedback, or just want to say hello, 
              feel free to reach out.
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
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Business Hours</h3>
                <p className="text-gray-700">
                  Monday - Friday: 9:00 AM - 6:00 PM (KST)<br />
                  Saturday - Sunday: Closed
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
              Your feedback helps us improve! If you have any suggestions for new features, 
              design categories, or improvements to our gallery, we'd love to hear them.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">For Designers</h2>
            <p>
              Interested in contributing your AI-generated designs to our gallery? 
              Please reach out to us via email with your portfolio and we'll get back to you.
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
              <h2 className="text-xl font-display font-semibold text-white mb-4">BASE SYNTAX</h2>
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
            <p className="text-center text-gray-500 text-sm">© {new Date().getFullYear()} Base Syntax. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
