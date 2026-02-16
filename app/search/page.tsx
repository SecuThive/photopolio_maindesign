import type { Metadata } from 'next';
import { Suspense } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import Link from 'next/link';

export const metadata: Metadata = {
  title: 'Search Designs - UI Syntax',
  description: 'Search through 700+ free AI web designs. Find the perfect landing page, dashboard, or component for your project.',
  robots: {
    index: true, // Allow indexing to capture "search" queries, can change to false if preferred
    follow: true,
  },
};

function SearchContent() {
  return (
    <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <div className="text-center mb-12">
        <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Search Designs
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Use ⌘K or Ctrl+K anywhere on the site to open the quick search palette
        </p>
      </div>

      <div className="space-y-8">
        {/* Quick Links */}
        <div className="bg-gray-50 rounded-2xl p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Popular Categories</h2>
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {[
              { name: 'Landing Page', href: '/category/landing-page' },
              { name: 'Dashboard', href: '/category/dashboard' },
              { name: 'E-commerce', href: '/category/e-commerce' },
              { name: 'Blog', href: '/category/blog' },
              { name: 'Portfolio', href: '/category/portfolio' },
              { name: 'Components', href: '/category/components' },
            ].map((category) => (
              <Link
                key={category.name}
                href={category.href}
                className="p-4 border border-gray-200 rounded-lg bg-white hover:border-gray-900 hover:shadow-sm transition-all text-center font-medium text-gray-700 hover:text-gray-900"
              >
                {category.name}
              </Link>
            ))}
          </div>
        </div>

        {/* Collections */}
        <div className="bg-gray-50 rounded-2xl p-8">
          <h2 className="text-xl font-semibold text-gray-900 mb-4">Browse Collections</h2>
          <Link
            href="/collections"
            className="inline-flex items-center px-6 py-3 bg-gray-900 text-white rounded-lg font-medium hover:bg-gray-800 transition-colors"
          >
            View All Collections →
          </Link>
        </div>

        {/* Command Palette Hint */}
        <div className="border-2 border-dashed border-gray-300 rounded-2xl p-8 text-center">
          <div className="text-4xl mb-3">⌘</div>
          <h3 className="text-lg font-semibold text-gray-900 mb-2">Quick Search</h3>
          <p className="text-gray-600 max-w-md mx-auto">
            Press <kbd className="px-2 py-1 bg-gray-200 rounded text-sm font-mono">⌘K</kbd> or{' '}
            <kbd className="px-2 py-1 bg-gray-200 rounded text-sm font-mono">Ctrl+K</kbd> to open
            the command palette and search across all designs, collections, and pages.
          </p>
        </div>
      </div>
    </div>
  );
}

export default function SearchPage() {
  return (
    <div className="min-h-screen bg-luxury-white flex flex-col">
      <Header />
      <main className="flex-grow">
        <Suspense fallback={<div className="p-8 text-center">Loading...</div>}>
          <SearchContent />
        </Suspense>
      </main>
      <Footer />
    </div>
  );
}
