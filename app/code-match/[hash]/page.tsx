"use client";

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import Image from 'next/image';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { DesignMetrics } from '@/lib/designAnalysis';
import { DesignWithSlug } from '@/types/database';

type CodeMatchData = {
  code: string;
  metrics: DesignMetrics;
  results: Array<{ design: DesignWithSlug; score: number }>;
  views: number;
  createdAt: string;
};

export default function SharedCodeMatchPage() {
  const params = useParams();
  const hash = params?.hash as string;
  
  const [data, setData] = useState<CodeMatchData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    if (!hash) return;

    const fetchData = async () => {
      try {
        const response = await fetch(`/api/code-match/${hash}`);
        if (!response.ok) {
          throw new Error('Code match not found');
        }
        const result = await response.json();
        setData(result);
      } catch (err) {
        setError(err instanceof Error ? err.message : 'Failed to load code match');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [hash]);

  const palette = data?.metrics?.colors?.slice(0, 5) || [];

  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-12">
        {loading && (
          <div className="flex items-center justify-center py-20">
            <div className="h-12 w-12 rounded-full border-4 border-gray-200 border-t-gray-900 animate-spin" />
          </div>
        )}

        {error && (
          <div className="rounded-3xl border border-red-200 bg-red-50 p-12 text-center">
            <h2 className="text-2xl font-semibold text-red-900">Code Match Not Found</h2>
            <p className="mt-4 text-red-700">{error}</p>
            <Link
              href="/code-match"
              className="mt-6 inline-block rounded-full bg-gray-900 px-6 py-3 text-sm font-semibold text-white hover:bg-gray-800"
            >
              Try Code Match
            </Link>
          </div>
        )}

        {data && (
          <>
            <section className="space-y-6 text-center">
              <div className="flex items-center justify-center gap-3">
                <p className="text-xs uppercase tracking-[0.45em] text-gray-500">Shared Match</p>
                <span className="rounded-full bg-gray-100 px-3 py-1 text-xs font-medium text-gray-600">
                  {data.views.toLocaleString()} views
                </span>
              </div>
              <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 tracking-tight">
                Code Match Results
              </h1>
              <p className="text-lg text-gray-600 max-w-3xl mx-auto">
                Analysis of user-submitted code with {data.results.length} matching UI designs.
              </p>
              <div className="flex items-center justify-center gap-4">
                <Link
                  href="/code-match"
                  className="inline-flex items-center gap-2 rounded-full bg-gray-900 px-6 py-3 text-sm font-semibold text-white hover:bg-gray-800"
                >
                  Try Your Own Code
                </Link>
                <button
                  onClick={() => {
                    navigator.clipboard.writeText(window.location.href);
                    alert('Link copied to clipboard!');
                  }}
                  className="inline-flex items-center gap-2 rounded-full border border-gray-300 bg-white px-6 py-3 text-sm font-semibold text-gray-900 hover:bg-gray-50"
                >
                  <svg className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                  </svg>
                  Share
                </button>
              </div>
            </section>

            <div className="rounded-[48px] border border-gray-200 bg-white p-8 shadow-[0_25px_70px_rgba(15,23,42,0.08)]">
              <h2 className="text-2xl font-semibold text-gray-900 mb-6">Code Analysis</h2>
              <div className="grid gap-6 md:grid-cols-4">
                <MetricCard label="Sections" value={data.metrics.sectionCount} detail="layout blocks" />
                <MetricCard label="CTAs" value={data.metrics.buttonCount} detail="interactive" />
                <MetricCard label="Content" value={`${data.metrics.textLength} chars`} detail="text" />
                <MetricCard label="Images" value={data.metrics.imageCount} detail="media" />
                <MetricCard label="Semantic" value={`${data.metrics.semanticScore}%`} detail="html quality" />
                <MetricCard label="Layout" value={data.metrics.layoutPattern} detail="structure" />
                <MetricCard label="Complexity" value={data.metrics.complexity} detail="score" />
                <div className="rounded-3xl border border-gray-200 bg-gray-50 p-5">
                  <p className="text-xs uppercase tracking-[0.35em] text-gray-500 mb-3">Palette</p>
                  <div className="flex items-center gap-2">
                    {palette.length === 0 && <span className="text-sm text-gray-400">No colors</span>}
                    {palette.map((color) => (
                      <span
                        key={color}
                        className="h-8 w-8 rounded-xl border border-gray-300"
                        style={{ backgroundColor: color }}
                        title={color}
                      />
                    ))}
                  </div>
                </div>
              </div>
            </div>

            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <h2 className="text-3xl font-semibold text-gray-900">
                  Matched Designs ({data.results.length})
                </h2>
              </div>

              <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
                {data.results.map((entry) => (
                  <ResultCard key={entry.design.id} entry={entry} />
                ))}
              </div>
            </div>

            <div className="rounded-3xl border border-gray-200 bg-gray-50 p-8">
              <h3 className="text-lg font-semibold text-gray-900 mb-4">Original Code Snippet</h3>
              <pre className="overflow-x-auto rounded-2xl bg-gray-900 p-6 text-sm text-gray-100">
                <code>{data.code}</code>
              </pre>
            </div>
          </>
        )}
      </main>

      <Footer />
    </div>
  );
}

function MetricCard({ label, value, detail }: { label: string; value: string | number; detail: string }) {
  return (
    <div className="rounded-3xl border border-gray-200 bg-gray-50 p-5">
      <p className="text-xs uppercase tracking-[0.35em] text-gray-500">{label}</p>
      <p className="mt-3 text-2xl font-semibold text-gray-900">{value}</p>
      <p className="text-xs text-gray-500 mt-1">{detail}</p>
    </div>
  );
}

function ResultCard({ entry }: { entry: { design: DesignWithSlug; score: number } }) {
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
