import type { Metadata } from 'next';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import SavedDesignsClient from '@/components/SavedDesignsClient';
import { createPageMetadata } from '@/lib/seo';

const ENABLE_GROWTH_SAFE_SEO_FIXES = process.env.ENABLE_GROWTH_SAFE_SEO_FIXES === 'true';

export const metadata: Metadata = createPageMetadata({
  title: 'Saved Designs',
  description: 'Your saved UI Syntax designs, stored locally for quick review and sharing.',
  path: '/saved',
  robots: ENABLE_GROWTH_SAFE_SEO_FIXES
    ? {
        index: false,
        follow: true,
      }
    : undefined,
});

export default function SavedPage() {
  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-10">
        <header className="space-y-4">
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Saved</p>
          <h1 className="text-4xl font-semibold text-gray-900">Saved designs</h1>
          <p className="text-lg text-gray-600 max-w-3xl">
            This list is stored on your device. Save any design to keep a personal shortlist for reviews, handoffs,
            or inspiration sessions.
          </p>
        </header>

        <section className="rounded-3xl border border-gray-200 bg-white/90 p-6 sm:p-8 space-y-4">
          <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Empty State Guide</p>
          <p className="text-sm sm:text-base text-gray-700 leading-relaxed">
            Saved items are read from your browser storage, so this page starts with a static default state.
            If your shortlist is empty, open any design and use Save to build a review set for your next sprint.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="/"
              className="inline-flex items-center rounded-full border border-gray-900 bg-gray-900 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-white transition hover:bg-black"
            >
              Browse Designs
            </Link>
            <Link
              href="/collections"
              className="inline-flex items-center rounded-full border border-gray-300 bg-white px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-gray-700 transition hover:border-gray-900 hover:text-gray-900"
            >
              View Collections
            </Link>
          </div>
        </section>

        <SavedDesignsClient />
      </main>

      <Footer />
    </div>
  );
}
