import type { Metadata } from "next";
import Link from 'next/link';
import SimpleHeader from '@/components/SimpleHeader';

export const metadata: Metadata = {
  title: "About Us",
  description: "Learn about Base Syntax, a curated gallery of AI-generated web designs featuring landing pages, dashboards, e-commerce platforms, and portfolios. Discover our mission and technology.",
  alternates: {
    canonical: 'https://www.ui-syntax.com/about',
  },
  openGraph: {
    title: "About Base Syntax - AI Design Gallery",
    description: "Learn about Base Syntax, a curated gallery of AI-generated web designs featuring landing pages, dashboards, e-commerce platforms, and portfolios.",
    url: 'https://www.ui-syntax.com/about',
  },
};

export default function AboutPage() {
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'Base Syntax',
    url: 'https://www.ui-syntax.com',
    logo: 'https://www.ui-syntax.com/logo.png',
    description: 'AI-generated web design gallery showcasing creative and innovative designs',
    email: 'thive8564@gmail.com',
    sameAs: [],
  };

  return (
    <div className="min-h-screen bg-white">
      <SimpleHeader />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">About Base Syntax</h1>
        
        <div className="prose prose-lg text-gray-700 space-y-6">
          <section>
            <p className="text-xl leading-relaxed">
              Welcome to <strong>Base Syntax</strong> - a curated gallery of AI-generated web designs 
              that pushes the boundaries of digital creativity.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Our Mission</h2>
            <p>
              We believe in the power of AI to inspire and transform web design. Our gallery showcases 
              innovative UI/UX designs across various categories including landing pages, dashboards, 
              e-commerce platforms, portfolios, and more.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">What We Offer</h2>
            <ul className="list-disc pl-6 space-y-2">
              <li>
                <strong>AI-Generated Designs:</strong> Cutting-edge web designs created using advanced AI technology
              </li>
              <li>
                <strong>Diverse Categories:</strong> From landing pages to dashboards, covering all major design types
              </li>
              <li>
                <strong>Design Inspiration:</strong> A constantly updated collection to inspire your next project
              </li>
              <li>
                <strong>Free Access:</strong> Browse and explore all designs completely free
              </li>
            </ul>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">The Technology</h2>
            <p>
              Our designs are generated using state-of-the-art AI models that understand modern 
              design principles, user experience best practices, and current web design trends. 
              Each design is carefully curated to ensure quality and innovation.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Get in Touch</h2>
            <p>
              Have questions or feedback? We&rsquo;d love to hear from you! 
              Reach out to us at{" "}
              <a href="mailto:thive8564@gmail.com" className="text-blue-600 hover:text-blue-800 underline">
                thive8564@gmail.com
              </a>
            </p>
          </section>

          <section className="mt-12 pt-8 border-t border-gray-200">
            <p className="text-center text-gray-600 italic">
              &ldquo;Empowering creativity through AI-driven design innovation&rdquo;
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
