import type { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import SavedDesignsClient from '@/components/SavedDesignsClient';
import { createPageMetadata } from '@/lib/seo';

export const metadata: Metadata = createPageMetadata({
  title: 'Saved Designs',
  description: 'Your saved UI Syntax designs, stored locally for quick review and sharing.',
  path: '/saved',
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

        <SavedDesignsClient />
      </main>

      <Footer />
    </div>
  );
}
