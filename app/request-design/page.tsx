import type { Metadata } from 'next';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import DesignRequestForm from '@/components/DesignRequestForm';
import DesignRequestBoard from '@/components/DesignRequestBoard';
import { createPageMetadata } from '@/lib/seo';

const ENABLE_GROWTH_SAFE_SEO_FIXES = process.env.ENABLE_GROWTH_SAFE_SEO_FIXES === 'true';

export const metadata: Metadata = createPageMetadata({
  title: 'Request a Design',
  description: 'Submit the exact UI design you want. We review requests and generate selected designs for the gallery.',
  path: '/request-design',
  robots: ENABLE_GROWTH_SAFE_SEO_FIXES
    ? {
        index: false,
        follow: true,
      }
    : undefined,
});

export default function RequestDesignPage() {
  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-8">
        <header className="space-y-4">
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Community Requests</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 tracking-tight">Request a design</h1>
          <p className="text-lg text-gray-600 max-w-3xl">
            Tell us exactly what you need. Clear requests with practical constraints are prioritized.
          </p>
        </header>

        <section className="rounded-3xl border border-gray-200 bg-white/90 p-6 sm:p-8 space-y-4">
          <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Queue Preview</p>
          <p className="text-sm sm:text-base text-gray-700 leading-relaxed">
            The request queue loads after page hydration. To keep this page useful for both users and crawlers,
            we render this static guide first: submit a precise brief, then browse current collection references
            while the live voting board initializes.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="#request-form"
              className="inline-flex items-center rounded-full border border-gray-900 bg-gray-900 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-white transition hover:bg-black"
            >
              Submit Brief
            </Link>
            <Link
              href="/collections"
              className="inline-flex items-center rounded-full border border-gray-300 bg-white px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-gray-700 transition hover:border-gray-900 hover:text-gray-900"
            >
              Browse Collections
            </Link>
          </div>
        </section>

        <section id="request-form">
          <DesignRequestForm />
        </section>
        <DesignRequestBoard />
      </main>

      <Footer />
    </div>
  );
}
