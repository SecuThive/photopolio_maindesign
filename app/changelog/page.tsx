import type { Metadata } from 'next';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { changelogItems } from '@/lib/changelog';
import { createPageMetadata } from '@/lib/seo';

export const metadata: Metadata = createPageMetadata({
  title: 'Product Changelog',
  description: 'Track latest UI Syntax features, improvements, and fixes with direct links to shipped updates.',
  path: '/changelog',
  robots: {
    index: false,
    follow: true,
  },
});

const typeStyle: Record<string, string> = {
  feature: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  improvement: 'bg-blue-50 text-blue-700 border-blue-200',
  fix: 'bg-amber-50 text-amber-700 border-amber-200',
};

export default function ChangelogPage() {
  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-10">
        <header className="space-y-4">
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Product Updates</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 tracking-tight">Changelog</h1>
          <p className="text-lg text-gray-600 max-w-3xl">
            A running timeline of shipped features, improvements, and fixes.
          </p>
        </header>

        <section className="space-y-5">
          {changelogItems.map((item) => (
            <article key={`${item.date}-${item.title}`} className="rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
              <div className="flex flex-wrap items-center gap-3">
                <time className="text-xs uppercase tracking-[0.25em] text-gray-500">{item.date}</time>
                <span className={`rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] ${typeStyle[item.type]}`}>
                  {item.type}
                </span>
              </div>
              <h2 className="mt-3 text-2xl font-semibold text-gray-900">{item.title}</h2>
              <p className="mt-2 text-sm text-gray-600 leading-relaxed">{item.summary}</p>
              {item.links && item.links.length > 0 && (
                <div className="mt-4 flex flex-wrap gap-2">
                  {item.links.map((link) => (
                    <Link
                      key={`${item.title}-${link.href}`}
                      href={link.href}
                      className="rounded-full border border-gray-300 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gray-700 hover:border-gray-900 hover:text-gray-900"
                    >
                      {link.label}
                    </Link>
                  ))}
                </div>
              )}
            </article>
          ))}
        </section>
      </main>

      <Footer />
    </div>
  );
}
