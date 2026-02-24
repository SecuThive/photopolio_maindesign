import type { Metadata } from "next";
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import EzoicPlacements from '@/components/EzoicPlacements';
import { getPlacementIds } from '@/lib/ezoic';
import { getPublishedDesignCount, getPublishedDesignLabel } from '@/lib/siteStats';

export async function generateMetadata(): Promise<Metadata> {
  const publishedDesignCount = await getPublishedDesignCount();
  const publishedLabel = getPublishedDesignLabel(publishedDesignCount);

  return {
    title: 'About UI Syntax - AI Design Library for Product Teams',
    description: `UI Syntax curates ${publishedLabel} with copy-paste HTML and React code when available.`,
    alternates: {
      canonical: 'https://ui-syntax.com/about',
    },
    openGraph: {
      title: 'About UI Syntax - AI Design Library for Product Teams',
      description: `Browse ${publishedLabel} with implementation-focused notes.`,
      url: 'https://ui-syntax.com/about',
    },
  };
}

export default async function AboutPage() {
  const publishedDesignCount = await getPublishedDesignCount();
  const publishedLabel = getPublishedDesignLabel(publishedDesignCount);
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
    <div className="min-h-screen bg-luxury-white">
      <Header />

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
            <p className="mt-4">
              The public catalog currently includes <strong>{publishedLabel}</strong>, and the library is updated as new
              design entries pass review.
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
      <Footer />
    </div>
  );
}
