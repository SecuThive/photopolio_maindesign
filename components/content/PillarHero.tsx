type PillarHeroProps = {
  eyebrow: string;
  title: string;
  description: string;
  summary: string;
  tags: string[];
  bestFor: string[];
};

export function PillarHero({ eyebrow, title, description, summary, tags, bestFor }: PillarHeroProps) {
  return (
    <section className="space-y-8">
      <div className="flex flex-wrap items-center gap-3 text-[11px] uppercase tracking-[0.35em] text-gray-500">
        <span className="rounded-full border border-gray-200 bg-white/80 px-4 py-1 font-semibold text-gray-700">
          {eyebrow}
        </span>
        <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
        <span>Playbook</span>
      </div>
      <div className="space-y-6">
        <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 tracking-tight leading-tight">
          {title}
        </h1>
        <p className="text-lg text-gray-600 leading-relaxed max-w-3xl">{description}</p>
        <div className="rounded-2xl border border-gray-200 bg-white/90 p-6 shadow-sm">
          <p className="text-sm font-semibold uppercase tracking-[0.3em] text-gray-500">Summary</p>
          <p className="mt-3 text-base text-gray-700 leading-relaxed">{summary}</p>
        </div>
        <div className="flex flex-wrap gap-3">
          {tags.map((tag) => (
            <span key={tag} className="rounded-full border border-gray-300 bg-white px-4 py-1 text-sm font-medium text-gray-700">
              {tag}
            </span>
          ))}
        </div>
      </div>
      <div className="rounded-2xl border border-gray-200 bg-gray-50/80 p-6">
        <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Best For</p>
        <ul className="mt-4 grid gap-3 text-gray-800 md:grid-cols-3">
          {bestFor.map((role) => (
            <li key={role} className="rounded-xl border border-gray-200 bg-white px-4 py-3 text-sm font-semibold text-gray-900">
              {role}
            </li>
          ))}
        </ul>
      </div>
    </section>
  );
}
