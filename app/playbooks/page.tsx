import Link from 'next/link';
import type { Metadata } from 'next';
import { pillarTopics } from '@/lib/pillars';
import { createPageMetadata } from '@/lib/seo';

export const metadata: Metadata = createPageMetadata({
  title: 'UI Strategy Playbooks',
  description: 'Playbooks covering SaaS landing pages, dashboards, e-commerce, UX psychology, and Core Web Vitals.',
  path: '/playbooks',
});

export const revalidate = 3600;

export default function PlaybooksIndexPage() {
  return (
    <section className="space-y-10">
      <header className="space-y-4">
        <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Playbook Library</p>
        <h1 className="text-4xl font-semibold text-gray-900">UI Strategy Reference Stack</h1>
        <p className="text-lg text-gray-600 max-w-3xl">
          Every playbook follows a definition → strategy summary → execution checklist → related collection/design structure so both people and generative search engines receive a clear signal.
        </p>
      </header>
      <div className="grid gap-6 md:grid-cols-2">
        {pillarTopics.map((topic) => (
          <Link
            key={topic.slug}
            href={`/playbooks/${topic.slug}`}
            className="group rounded-3xl border border-gray-200 bg-white/90 p-6 shadow-sm transition hover:-translate-y-1 hover:border-gray-900"
          >
            <div className="flex items-center gap-3 text-[11px] uppercase tracking-[0.3em] text-gray-500">
              <span>{topic.eyebrow}</span>
              <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
              <span>Playbook</span>
            </div>
            <h2 className="mt-4 text-2xl font-semibold text-gray-900 group-hover:text-gray-700">
              {topic.title}
            </h2>
            <p className="mt-3 text-sm text-gray-600 leading-relaxed">{topic.summary}</p>
            <div className="mt-5 flex flex-wrap gap-2">
              {topic.tags.slice(0, 3).map((tag) => (
                <span key={tag} className="rounded-full border border-gray-200 px-3 py-1 text-xs font-medium text-gray-700">
                  {tag}
                </span>
              ))}
            </div>
          </Link>
        ))}
      </div>
    </section>
  );
}
