import type { PillarSection } from '@/lib/pillars';
import Link from 'next/link';

type PillarTocProps = {
  sections: PillarSection[];
  slug: string;
};

export function PillarTableOfContents({ sections, slug }: PillarTocProps) {
  if (sections.length === 0) {
    return null;
  }

  return (
    <nav aria-label="Table of contents" className="sticky top-24 rounded-3xl border border-gray-200 bg-white/90 p-6 shadow-sm">
      <p className="text-xs uppercase tracking-[0.3em] text-gray-500">On this playbook</p>
      <ol className="mt-4 space-y-3 text-sm text-gray-700">
        {sections.map((section) => (
          <li key={section.id}>
            <Link href={`/playbooks/${slug}#${section.id}`} className="transition-colors hover:text-gray-900">
              {section.heading}
            </Link>
          </li>
        ))}
      </ol>
    </nav>
  );
}
