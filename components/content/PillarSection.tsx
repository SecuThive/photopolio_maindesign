import type { PillarSection } from '@/lib/pillars';
import { buildDefinition, buildSummary, buildChecklist } from '@/lib/content/patterns';

type PillarSectionProps = {
  section: PillarSection;
};

export function PillarSectionBlock({ section }: PillarSectionProps) {
  const { heading, definition, summary, listTitle, bullets, label, id } = section;
  const definitionBlock = buildDefinition(definition);
  const summaryBlock = buildSummary(summary);
  const checklist = buildChecklist(bullets);

  return (
    <section id={id} aria-labelledby={`${id}-heading`} className="rounded-3xl border border-gray-200 bg-white/90 p-8 shadow-sm">
      <p className="text-xs uppercase tracking-[0.3em] text-gray-400">{label}</p>
      <h2 id={`${id}-heading`} className="mt-3 text-2xl font-semibold text-gray-900">
        {heading}
      </h2>
      <p className="mt-4 text-base text-gray-600 leading-relaxed" {...definitionBlock.props}>
        {definitionBlock.text}
      </p>
      <div className="mt-6 rounded-2xl border border-gray-100 bg-gray-50/80 p-6" {...summaryBlock.containerProps}>
        <p className="text-sm font-semibold uppercase tracking-[0.3em] text-gray-500">Structured Summary</p>
        <p className="mt-3 text-base text-gray-800 leading-relaxed" {...summaryBlock.textProps}>
          {summaryBlock.text}
        </p>
      </div>
      {checklist.items.length > 0 && (
        <div className="mt-6">
          <p className="text-sm font-semibold text-gray-900">{listTitle ?? 'Execution steps'}</p>
          <ul className="mt-3 space-y-3 text-gray-700" {...checklist.listProps}>
            {checklist.items.map((item) => (
              <li key={`${id}-${item.position}`} className="flex gap-3" {...item.itemProps}>
                <meta itemProp="position" content={String(item.position)} />
                <span className="mt-1 h-2 w-2 rounded-full bg-gray-900" aria-hidden />
                <span>{item.text}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </section>
  );
}
