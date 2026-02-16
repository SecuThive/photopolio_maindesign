"use client";

import { FormEvent, useMemo, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { analyzeMarkup, DesignMetrics } from '@/lib/designAnalysis';
import { DesignWithSlug } from '@/types/database';
import CodeScoreCard from './CodeScoreCard';

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
  // Share feature temporarily disabled
  // const [shareUrl, setShareUrl] = useState<string | null>(null);
  // const [sharing, setSharing] = useState(false);
  // const [shareAvailable, setShareAvailable] = useState(true);

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
      // setShareUrl(null); // Reset share URL on new search
    } catch (requestError) {
      setResults([]);
      setError(requestError instanceof Error ? requestError.message : 'Something went wrong while requesting recommendations.');
    } finally {
      setLoading(false);
    }
  };

  // Share functionality temporarily disabled until Supabase table is ready
  /*
  const handleShare = async () => {
    if (!metrics || !results.length) return;

    setSharing(true);
    try {
      const response = await fetch('/api/code-match/save', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code, metrics, results }),
      });

      const payload = await response.json();
      if (!response.ok) {
        // Handle table not ready error gracefully
        if (payload.code === 'TABLE_NOT_READY') {
          // Hide share button if table is not ready
          setShareAvailable(false);
        } else {
          throw new Error(payload?.error || 'Failed to generate share link');
        }
        return;
      }

      const url = `${window.location.origin}/code-match/${payload.hash}`;
      setShareUrl(url);
      
      // Copy to clipboard
      await navigator.clipboard.writeText(url);
      setNotice('Share link copied to clipboard!');
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to create share link');
    } finally {
      setSharing(false);
    }
  };
  */

  return (
    <section className="space-y-12">
      {/* Main Input Section */}
      <div className="relative overflow-hidden rounded-[52px] border border-gray-900/50 bg-gradient-to-br from-[#030509] via-[#0a1525] to-[#030509] px-10 py-16 text-white shadow-[0_50px_140px_rgba(2,6,23,0.75)]">
        {/* Enhanced background effects */}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top_left,_rgba(16,185,129,0.15),_transparent_50%)]" aria-hidden />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_bottom_right,_rgba(6,182,212,0.15),_transparent_50%)]" aria-hidden />
        <div className="absolute -left-20 -top-20 h-72 w-72 rounded-full bg-emerald-500/25 blur-[140px]" aria-hidden />
        <div className="absolute -right-32 bottom-0 h-96 w-96 rounded-full bg-cyan-500/25 blur-[160px]" aria-hidden />
        
        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.02)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.02)_1px,transparent_1px)] bg-[size:44px_44px]" aria-hidden />

        <div className="relative grid gap-14 lg:grid-cols-[1.1fr_0.9fr]">
          <div className="space-y-10">
            <div className="space-y-5">
              <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 border border-emerald-400/30 px-4 py-2">
                <svg className="h-4 w-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M12.316 3.051a1 1 0 01.633 1.265l-4 12a1 1 0 11-1.898-.632l4-12a1 1 0 011.265-.633zM5.707 6.293a1 1 0 010 1.414L3.414 10l2.293 2.293a1 1 0 11-1.414 1.414l-3-3a1 1 0 010-1.414l3-3a1 1 0 011.414 0zm8.586 0a1 1 0 011.414 0l3 3a1 1 0 010 1.414l-3 3a1 1 0 11-1.414-1.414L16.586 10l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
                </svg>
                <p className="text-xs uppercase tracking-[0.4em] text-emerald-300 font-bold">Paste &amp; Compare</p>
              </div>
              <h2 className="text-5xl font-bold leading-tight bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">Get tailored UI references based on your live code</h2>
              <p className="text-lg text-gray-300 leading-relaxed">
                Paste HTML or React markup and we&apos;ll analyze layout depth, palette, and CTA density across 700+ AI concepts to return the closest matches.
              </p>
            </div>

            {/* Metrics Grid */}
            <div className="grid gap-5 sm:grid-cols-2">
              <MetricTile label="Section depth" value={metrics ? metrics.sectionCount : '—'} detail="layout blocks" icon="📐" />
              <MetricTile label="Action density" value={metrics ? metrics.buttonCount : '—'} detail="buttons/links" icon="🎯" />
              <MetricTile label="Copy weight" value={metrics ? `${metrics.textLength.toLocaleString()} chars` : '—'} detail="text length" icon="📝" />
              <MetricTile label="Media elements" value={metrics ? metrics.imageCount : '—'} detail="images/svg" icon="🖼️" />
              <MetricTile label="Semantic score" value={metrics ? `${metrics.semanticScore}%` : '—'} detail="html quality" icon="✅" />
              <MetricTile label="Layout pattern" value={metrics ? metrics.layoutPattern : '—'} detail="structure type" icon="🏗️" />
              
              {/* Color Palette */}
              <div className="rounded-3xl border border-white/30 bg-gradient-to-br from-white/10 to-white/5 backdrop-blur p-6 hover:border-white/40 transition-colors">
                <div className="flex items-center gap-2 mb-4">
                  <span className="text-2xl">🎨</span>
                  <p className="text-xs uppercase tracking-[0.35em] text-gray-300 font-semibold">Palette</p>
                </div>
                <div className="flex items-center gap-2 flex-wrap">
                  {palette.length === 0 && <span className="text-sm text-gray-400">Waiting for palette...</span>}
                  {palette.map((color) => (
                    <span 
                      key={color} 
                      className="h-12 w-12 rounded-2xl border-2 border-white/30 shadow-lg hover:scale-110 transition-transform" 
                      style={{ backgroundColor: color }} 
                      aria-label={color} 
                      title={color}
                    />
                  ))}
                </div>
              </div>
              
              <MetricTile 
                label="Complexity" 
                value={metrics ? metrics.complexity : '—'} 
                detail={metrics ? `${metrics.responsiveBreakpoints} breakpoints` : 'code density'} 
                icon="⚙️"
              />
            </div>
          </div>

          {/* Input Form */}
          <form onSubmit={handleSubmit} className="flex flex-col gap-5 rounded-[36px] border border-white/25 bg-gradient-to-br from-white/10 to-white/5 p-8 backdrop-blur-xl shadow-2xl h-full">
            <div className="flex items-center gap-3">
              <div className="h-10 w-10 rounded-xl bg-gradient-to-br from-emerald-400 to-cyan-400 flex items-center justify-center">
                <svg className="h-6 w-6 text-gray-900" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 20l4-16m4 4l4 4-4 4M6 16l-4-4 4-4" />
                </svg>
              </div>
              <label htmlFor="code-input" className="text-sm uppercase tracking-[0.35em] text-gray-200 font-bold">
                Code input
              </label>
            </div>
            
            <textarea
              id="code-input"
              name="code"
              value={code}
              onChange={(event) => setCode(event.target.value)}
              placeholder={'<section class="hero">\n  <h1>Welcome</h1>\n  <button>Get Started</button>\n</section>'}
              className="flex-1 min-h-[400px] w-full resize-none rounded-3xl border-2 border-white/30 bg-black/40 p-5 font-mono text-base text-white placeholder:text-gray-500 focus:border-emerald-400 focus:outline-none focus:ring-4 focus:ring-emerald-500/20 transition-all"
            />
            
            <div className="flex flex-wrap items-center justify-between gap-4 text-sm">
              <div className="flex items-center gap-2">
                <div className={`h-2 w-2 rounded-full ${meetsMinimum ? 'bg-emerald-400' : 'bg-gray-500'}`} />
                <span className={meetsMinimum ? 'text-emerald-300 font-semibold' : 'text-gray-400'}>
                  {characterCount.toLocaleString()} chars · min 50
                </span>
              </div>
              <span className="text-gray-400 text-xs uppercase tracking-wider">Supports HTML · JSX · TSX</span>
            </div>
            
            {error && (
              <div className="rounded-2xl bg-rose-500/20 border border-rose-400/30 px-5 py-4 text-sm text-rose-200 flex items-start gap-3">
                <svg className="h-5 w-5 text-rose-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
                <span>{error}</span>
              </div>
            )}
            
            {notice && !error && (
              <div className="rounded-2xl bg-emerald-500/20 border border-emerald-400/30 px-5 py-4 text-sm text-emerald-100 flex items-start gap-3">
                <svg className="h-5 w-5 text-emerald-400 flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                <span>{notice}</span>
              </div>
            )}
            
            <button
              type="submit"
              disabled={!meetsMinimum || loading}
              className="group relative inline-flex items-center justify-center gap-3 rounded-full bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 px-8 py-4 text-sm font-bold uppercase tracking-[0.35em] text-gray-900 transition-all hover:shadow-[0_0_40px_rgba(16,185,129,0.5)] hover:scale-[1.02] disabled:cursor-not-allowed disabled:opacity-40 disabled:hover:scale-100 disabled:hover:shadow-none"
            >
              {loading && <span className="h-5 w-5 rounded-full border-3 border-gray-900/30 border-t-gray-900 animate-spin" aria-hidden />}
              {loading ? 'Analyzing...' : 'Get matches'}
              {!loading && (
                <svg className="h-5 w-5 group-hover:translate-x-1 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                </svg>
              )}
            </button>
          </form>
        </div>
      </div>

      {/* Results Section */}
      <div className="space-y-8 rounded-[44px] border border-gray-200 bg-gradient-to-br from-white to-gray-50 p-10 shadow-[0_30px_90px_rgba(15,23,42,0.12)]">
        <div className="flex flex-wrap items-center justify-between gap-4">
          <div className="space-y-2">
            <p className="text-xs uppercase tracking-[0.4em] text-gray-500 font-semibold">Recommendations</p>
            <h3 className="text-3xl font-bold text-gray-900">Personalized matches {results.length > 0 ? `(${results.length})` : ''}</h3>
          </div>
          <div className="flex items-center gap-3">
            {metrics && (
              <span className="rounded-full border border-gray-200 px-4 py-2 text-xs font-medium uppercase tracking-[0.3em] text-gray-500">
                {metrics.sectionCount} sections · {metrics.buttonCount} ctas
              </span>
            )}
            {/* Share button temporarily hidden until Supabase table is ready */}
          </div>
        </div>

        {/* Share URL display temporarily hidden
        {shareUrl && (
          <div className="rounded-3xl border border-emerald-200 bg-emerald-50 p-4">
            <div className="flex items-center justify-between gap-3">
              <div className="flex-1">
                <p className="text-xs font-semibold uppercase tracking-[0.3em] text-emerald-900 mb-1">Share Link</p>
                <p className="text-sm text-emerald-700 truncate">{shareUrl}</p>
              </div>
              <button
                onClick={() => {
                  navigator.clipboard.writeText(shareUrl);
                  setNotice('Link copied again!');
                }}
                className="rounded-full bg-emerald-600 px-4 py-2 text-xs font-semibold text-white hover:bg-emerald-700"
              >
                Copy
              </button>
            </div>
          </div>
        )}
        */}

        {results.length === 0 && (
          <div className="rounded-[36px] border-2 border-dashed border-gray-300 bg-gradient-to-br from-gray-50 to-white p-16 text-center">
            <div className="inline-flex h-20 w-20 items-center justify-center rounded-3xl bg-gradient-to-br from-gray-100 to-gray-200 text-4xl mb-4">
              🔍
            </div>
            <p className="text-xl font-semibold text-gray-800 mb-2">No matches yet.</p>
            <p className="text-base text-gray-600">Paste your markup and press &ldquo;Get matches&rdquo; to see recommendations.</p>
          </div>
        )}

        {results.length > 0 && (
          <>
            <div className="grid gap-6 md:grid-cols-2 xl:grid-cols-3">
              {results.map((entry) => (
                <ResultCard key={entry.design.id} entry={entry} />
              ))}
            </div>
          </>
        )}
      </div>

      {/* Code Score Card - shown after results */}
      {results.length > 0 && metrics && (
        <div className="space-y-6">
          <div className="text-center space-y-3">
            <p className="text-xs uppercase tracking-[0.45em] text-gray-500 font-semibold">Your Analysis</p>
            <h3 className="text-4xl md:text-5xl font-bold text-gray-900">Code Quality Report</h3>
            <p className="text-lg text-gray-600 max-w-2xl mx-auto">See how your code stacks up across key metrics and get personalized improvement tips</p>
          </div>
          <CodeScoreCard 
            metrics={metrics} 
            matchCount={results.length}
            bestMatchScore={results[0]?.score || 0}
          />
        </div>
      )}
    </section>
  );
}

function MetricTile({ label, value, detail, icon }: { label: string; value: string | number; detail: string; icon?: string }) {
  return (
    <div className="group rounded-3xl border border-white/30 bg-gradient-to-br from-white/10 to-white/5 backdrop-blur p-6 hover:border-white/40 hover:bg-white/15 transition-all duration-300">
      <div className="flex items-center justify-between mb-3">
        <p className="text-xs uppercase tracking-[0.35em] text-gray-300 font-semibold">{label}</p>
        {icon && <span className="text-2xl group-hover:scale-110 transition-transform">{icon}</span>}
      </div>
      <p className="text-4xl font-bold bg-gradient-to-r from-white to-gray-300 bg-clip-text text-transparent">{value}</p>
      <p className="mt-2 text-xs uppercase tracking-[0.35em] text-gray-400">{detail}</p>
    </div>
  );
}

function ResultCard({ entry }: { entry: RecommendationResult }) {
  const scorePercent = Math.round(entry.score * 100);
  const href = `/design/${entry.design.slug}`;
  
  // Color code the match percentage
  const getScoreColor = (score: number) => {
    if (score >= 80) return 'from-emerald-500 to-teal-500';
    if (score >= 60) return 'from-blue-500 to-cyan-500';
    if (score >= 40) return 'from-amber-500 to-orange-500';
    return 'from-gray-500 to-gray-600';
  };

  return (
    <Link
      href={href}
      className="group flex flex-col overflow-hidden rounded-[36px] border border-gray-200 bg-white shadow-[0_20px_60px_rgba(15,23,42,0.08)] transition-all duration-300 hover:-translate-y-2 hover:shadow-[0_40px_100px_rgba(15,23,42,0.15)] hover:border-gray-300"
    >
      <div className="relative h-56 w-full overflow-hidden bg-gradient-to-br from-gray-100 to-gray-200">
        <Image
          src={entry.design.image_url}
          alt={entry.design.title}
          fill
          className="h-full w-full object-cover transition duration-700 group-hover:scale-110"
          sizes="(max-width: 768px) 100vw, 33vw"
        />
        <div className="absolute inset-0 bg-gradient-to-t from-black/70 via-black/20 to-transparent opacity-60" aria-hidden />
        
        {/* Match Score Badge */}
        <div className="absolute top-5 left-5">
          <div className={`inline-flex items-center gap-2 rounded-2xl bg-gradient-to-r ${getScoreColor(scorePercent)} px-4 py-2 shadow-xl`}>
            <svg className="h-4 w-4 text-white" fill="currentColor" viewBox="0 0 20 20">
              <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
            </svg>
            <span className="text-sm font-bold text-white tracking-wide">
              {scorePercent}%
            </span>
          </div>
        </div>
      </div>
      
      <div className="flex flex-1 flex-col gap-4 p-7">
        <div className="space-y-2">
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500 font-semibold">{entry.design.category || 'General'}</p>
          <h4 className="text-xl font-bold text-gray-900 line-clamp-1 group-hover:text-emerald-600 transition-colors">{entry.design.title}</h4>
        </div>
        
        <p className="text-sm text-gray-600 line-clamp-2 leading-relaxed">
          {entry.design.description || 'Open the detail page to read the full description.'}
        </p>
        
        <div className="mt-auto pt-4 border-t border-gray-100 flex items-center justify-between">
          <div className="flex items-center gap-2 text-sm text-gray-500">
            <svg className="h-4 w-4" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M3.172 5.172a4 4 0 015.656 0L10 6.343l1.172-1.171a4 4 0 115.656 5.656L10 17.657l-6.828-6.829a4 4 0 010-5.656z" clipRule="evenodd" />
            </svg>
            <span className="font-medium">{entry.design.likes ?? 0}</span>
          </div>
          <div className="flex items-center gap-2 text-emerald-600 font-semibold group-hover:gap-3 transition-all">
            <span className="text-sm">View Design</span>
            <svg className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
            </svg>
          </div>
        </div>
      </div>
    </Link>
  );
}
