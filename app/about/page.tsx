import type { Metadata } from "next";
import Link from 'next/link';
import SimpleHeader from '@/components/SimpleHeader';
import EzoicPlacements from '@/components/EzoicPlacements';
import { getPlacementIds } from '@/lib/ezoic';

export const metadata: Metadata = {
  title: "About Us",
  description: "Learn how UI Syntax curates production-ready AI web designs for SaaS, developer tools, and commerce teams with annotated inspiration and launch support.",
  alternates: {
    canonical: 'https://ui-syntax.com/about',
  },
  openGraph: {
    title: "About UI Syntax - AI Design Gallery",
    description: "See how UI Syntax curates annotated AI web designs aligned to modern SaaS, fintech, and commerce standards.",
    url: 'https://ui-syntax.com/about',
  },
};

export default function AboutPage() {
  const placementIds = getPlacementIds('NEXT_PUBLIC_EZOIC_PLACEMENTS_ABOUT');
  const jsonLd = {
    '@context': 'https://schema.org',
    '@type': 'Organization',
    name: 'UI Syntax',
    url: 'https://ui-syntax.com',
    logo: 'https://ui-syntax.com/logo.png',
    description: 'Production-ready AI web design gallery curated for SaaS, fintech, and commerce teams',
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
        <h1 className="text-4xl font-bold text-gray-900 mb-8">About UI Syntax</h1>
        
        <div className="prose prose-lg text-gray-700 space-y-6">
          <section>
            <p className="text-xl leading-relaxed">
              Welcome to <strong>UI Syntax</strong>, a Silicon Valley standard gallery of AI-generated web designs built for
              SaaS founders, developer tools, and agencies shipping products to modern markets.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Our Mission</h2>
            <p>
              We believe AI accelerates high-quality shipping when it is curated with intent. Our gallery highlights
              landing pages, dashboards, commerce flows, and marketing systems that reflect modern accessibility and
              conversion best practices.
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
                <strong>Design Inspiration:</strong> Weekly drops mapped to enterprise SaaS, developer, and commerce trends
              </li>
              <li>
                <strong>Launch Support:</strong> Implementation-ready notes so product and engineering teams move faster
              </li>
              <li>
                <strong>Instant Code Handoff:</strong> Every design detail page ships with clean HTML and auto-generated React code so engineers can copy and paste into production.
              </li>
            </ul>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">The Technology</h2>
            <p>
              Our concepts originate from state-of-the-art diffusion and language models trained on modern
              SaaS, fintech, and commerce references. Human curators annotate the layouts so teams understand why each
              section resonates with global buyers.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Why UI Syntax?</h2>
            <p className="mb-4">
              In today&rsquo;s fast-paced digital landscape, staying ahead of design trends is crucial. UI Syntax bridges the gap between AI capabilities and practical design needs. We analyze thousands of AI-generated designs monthly, selecting only those that demonstrate exceptional user experience, visual hierarchy, and technical implementation potential.
            </p>
            <p className="mb-4">
              Our gallery serves designers seeking fresh perspectives, developers looking for implementation-ready mockups, and product managers exploring modern interface patterns. Each design includes detailed annotations covering color theory, typography choices, layout strategies, and accessibility considerations that make great designs work in production.
            </p>
            <p>
              Whether you&rsquo;re building a SaaS dashboard, e-commerce platform, marketing landing page, or mobile application, our curated collection provides the visual foundation to accelerate your design process while maintaining the quality standards expected by modern users.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Get in Touch</h2>
            <p>
              Have questions or feedback? We&rsquo;d love to hear from you. Reach out at{" "}
              <a href="mailto:thive8564@gmail.com" className="text-blue-600 hover:text-blue-800 underline">
                thive8564@gmail.com
              </a>
            </p>
          </section>

          <section className="mt-12 pt-8 border-t border-gray-200">
            <p className="text-center text-gray-600 italic">
              &ldquo;Empowering modern product teams with AI-driven design systems&rdquo;
            </p>
          </section>
        </div>
      </div>

      {placementIds.length > 0 && (
        <EzoicPlacements placementIds={placementIds} wrapperClassName="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 my-16" />
      )}

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
