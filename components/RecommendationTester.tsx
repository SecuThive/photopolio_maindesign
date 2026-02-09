"use client";

import { FormEvent, useMemo, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { analyzeMarkup, DesignMetrics } from '@/lib/designAnalysis';
import { DesignWithSlug } from '@/types/database';

type RecommendationResult = {
  design: DesignWithSlug;
  score: number;
};

export default function RecommendationTester() {
  const [code, setCode] = useState('');
  const [metrics, setMetrics] = useState<DesignMetrics | null>(null);
  const [results, setResults] = useState<RecommendationResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);

  const characterCount = code.length;
  const meetsMinimum = code.trim().length >= 50;

  const palette = useMemo(() => {
    if (!metrics?.colors?.length) return [];
    return metrics.colors.slice(0, 5);
  }, [metrics]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setNotice(null);

    const snippet = code.trim();
    if (snippet.length < 50) {
      setError('Please paste at least 50 characters of markup.');
      return;
    }

    const analyzed = analyzeMarkup(snippet);
    setMetrics(analyzed);

    setLoading(true);
    try {
      const response = await fetch('/api/recommendations/match', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code: snippet }),
      });

      const payload = await response.json();
      if (!response.ok) {
        throw new Error(payload?.error || 'We couldn\'t generate recommendations.');
      }

      setResults(Array.isArray(payload?.recommendations) ? payload.recommendations : []);
      setNotice('Here are your latest matches.');
    } catch (requestError) {
      setResults([]);
      setError(requestError instanceof Error ? requestError.message : 'Something went wrong while requesting recommendations.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <section className="space-y-10">
      <div className="relative overflow-hidden rounded-[48px] border border-gray-900/40 bg-[#030509] px-8 py-12 text-white shadow-[0_45px_120px_rgba(2,6,23,0.65)]">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(16,185,129,0.25),_rgba(3,5,9,0.9))]" aria-hidden />
        <div className="absolute -left-12 -top-16 h-56 w-56 rounded-full bg-emerald-500/20 blur-[120px]" aria-hidden />
        <div className="absolute -right-24 bottom-0 h-80 w-80 rounded-full bg-cyan-500/20 blur-[140px]" aria-hidden />

        <div className="relative grid gap-12 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-8">
            <div className="space-y-4">
              <p className="text-xs uppercase tracking-[0.5em] text-emerald-200">Paste &amp; Compare</p>
              <h2 className="text-4xl font-semibold leading-tight">Get tailored UI references based on your live code</h2>
              <p className="text-base text-gray-300">
                Paste HTML or React markup and we&apos;ll analyze layout depth, palette, and CTA density across 700+ AI concepts to return the closest matches.
              </p>
            </div>

            <div className="grid gap-4 sm:grid-cols-2">
              <MetricTile label="Section depth" value={metrics ? metrics.sectionCount : '—'} detail="layout blocks" />
              <MetricTile label="Action density" value={metrics ? metrics.buttonCount : '—'} detail="buttons/links" />
              <MetricTile label="Copy weight" value={metrics ? `${metrics.textLength.toLocaleString()} chars` : '—'} detail="text length" />
              <div className="rounded-3xl border border-white/20 bg-white/5 p-5">
                <p className="text-xs uppercase tracking-[0.4em] text-gray-400">Palette</p>
                <div className="mt-4 flex items-center gap-2">
                  {palette.length === 0 && <span className="text-sm text-gray-500">Waiting for palette...</span>}
                  {palette.map((color) => (
                    <span key={color} className="h-10 w-10 rounded-2xl border border-white/20" style={{ backgroundColor: color }} aria-label={color} />
                  ))}
                </div>
              </div>
            </div>
          </div>

          <form onSubmit={handleSubmit} className="flex flex-col gap-4 rounded-[32px] border border-white/15 bg-white/5 p-6 backdrop-blur">
            <label htmlFor="code-input" className="text-sm uppercase tracking-[0.4em] text-gray-400">
              Code input
            </label>
            <textarea
              id="code-input"
              name="code"
              value={code}
              onChange={(event) => setCode(event.target.value)}
              placeholder={'<section class="hero">...'}
              className="h-64 w-full resize-none rounded-2xl border border-white/20 bg-black/30 p-4 font-mono text-sm text-white placeholder:text-gray-600 focus:border-emerald-300 focus:outline-none"
            />
            <div className="flex flex-wrap items-center justify-between gap-3 text-xs text-gray-400">
              <span className={meetsMinimum ? 'text-emerald-300' : ''}>
                {characterCount.toLocaleString()} chars · min 50
              </span>
              <span>Supports HTML · JSX · TSX</span>
            </div>
            {error && <p className="rounded-2xl bg-rose-500/15 px-4 py-3 text-sm text-rose-200">{error}</p>}
            {notice && !error && <p className="rounded-2xl bg-emerald-500/15 px-4 py-3 text-sm text-emerald-100">{notice}</p>}
            <button
              type="submit"
              disabled={!meetsMinimum || loading}
              className="inline-flex items-center justify-center gap-3 rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-6 py-3 text-[11px] font-semibold uppercase tracking-[0.4em] text-gray-900 transition hover:from-emerald-300 hover:to-cyan-300 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {loading && <span className="h-4 w-4 rounded-full border-2 border-gray-900/30 border-t-gray-900 animate-spin" aria-hidden />}
              Get matches
            </button>
          </form>
        </div>
      </div>

      <div className="space-y-6 rounded-[40px] border border-gray-100 bg-white p-6 shadow-[0_25px_70px_rgba(15,23,42,0.08)]">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs uppercase tracking-[0.4em] text-gray-500">Recommendations</p>
            <h3 className="text-2xl font-semibold text-gray-900">Personalized matches {results.length > 0 ? `(${results.length})` : ''}</h3>
          </div>
          {metrics && (
            <span className="rounded-full border border-gray-200 px-4 py-2 text-xs font-medium uppercase tracking-[0.3em] text-gray-500">
              {metrics.sectionCount} sections · {metrics.buttonCount} ctas
            </span>
          )}
        </div>

        {results.length === 0 && (
          <div className="rounded-3xl border border-dashed border-gray-200 bg-gray-50/80 p-10 text-center text-gray-500">
            <p className="text-base font-medium text-gray-700">No matches yet.</p>
            <p className="mt-2 text-sm text-gray-500">Paste your markup and press &ldquo;Get matches&rdquo; to see recommendations.</p>
          </div>
        )}

        {results.length > 0 && (
          <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
            {results.map((entry) => (
              <ResultCard key={entry.design.id} entry={entry} />
            ))}
          </div>
        )}
      </div>
    </section>
  );
}

function MetricTile({ label, value, detail }: { label: string; value: string | number; detail: string }) {
  return (
    <div className="rounded-3xl border border-white/20 bg-white/5 p-5">
      <p className="text-xs uppercase tracking-[0.4em] text-gray-400">{label}</p>
      <p className="mt-4 text-3xl font-semibold">{value}</p>
      <p className="text-xs uppercase tracking-[0.4em] text-gray-500">{detail}</p>
    </div>
  );
}

function ResultCard({ entry }: { entry: RecommendationResult }) {
  const scorePercent = Math.round(entry.score * 100);
  const href = `/design/${entry.design.slug}`;

  return (
    <Link
      href={href}
      className="group flex flex-col overflow-hidden rounded-[32px] border border-gray-100 bg-white shadow-[0_20px_60px_rgba(15,23,42,0.06)] transition hover:-translate-y-1 hover:shadow-[0_35px_90px_rgba(15,23,42,0.12)]"
    >
      <div className="relative h-48 w-full overflow-hidden bg-gray-100">
        <Image
          src={entry.design.image_url}
          alt={entry.design.title}
          fill
          className="h-full w-full object-cover transition duration-700 group-hover:scale-105"
          sizes="(max-width: 768px) 100vw, 33vw"
        />
        <div className="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-black/65 to-transparent" aria-hidden />
        <span className="absolute top-4 left-4 inline-flex items-center gap-1 rounded-full bg-white/95 px-3 py-1 text-[11px] font-semibold tracking-[0.3em] text-gray-900">
          {scorePercent}% match
        </span>
      </div>
      <div className="flex flex-1 flex-col gap-3 p-6">
        <div>
          <p className="text-xs uppercase tracking-[0.35em] text-gray-400">{entry.design.category || 'General'}</p>
          <h4 className="mt-2 text-lg font-semibold text-gray-900 line-clamp-1">{entry.design.title}</h4>
        </div>
        <p className="text-sm text-gray-500 line-clamp-2">
          {entry.design.description || 'Open the detail page to read the full description.'}
        </p>
        <div className="mt-auto flex items-center justify-between text-xs text-gray-500">
          <span>{entry.design.likes ?? 0} likes</span>
          <span className="font-medium text-gray-900">Open →</span>
        </div>
      </div>
    </Link>
  );
}
