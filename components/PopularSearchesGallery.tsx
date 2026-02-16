"use client";

import { useEffect, useState } from 'react';
import Link from 'next/link';
import { DesignMetrics } from '@/lib/designAnalysis';

type PopularMatch = {
  hash: string;
  metrics: DesignMetrics;
  views: number;
  createdAt: string;
};

export default function PopularSearchesGallery() {
  const [matches, setMatches] = useState<PopularMatch[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchPopular = async () => {
      try {
        const response = await fetch('/api/code-match/popular');
        if (!response.ok) {
          // If table doesn't exist yet, just skip silently
          setLoading(false);
          return;
        }
        const data = await response.json();
        setMatches(data.matches || []);
      } catch (error) {
        // Silently fail - this feature requires the table to be properly set up
        console.log('Popular searches not available yet');
      } finally {
        setLoading(false);
      }
    };

    fetchPopular();
  }, []);

  // Don't show anything while loading or if no matches
  if (loading || matches.length === 0) {
    return null;
  }

  return (
    <section className="space-y-6">
      <div className="text-center space-y-3">
        <p className="text-xs uppercase tracking-[0.45em] text-gray-500">Trending</p>
        <h2 className="text-3xl font-semibold text-gray-900">Popular Code Match Searches</h2>
        <p className="text-gray-600 max-w-2xl mx-auto">
          Explore what other developers are analyzing. Click any card to see full results.
        </p>
      </div>

      <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4">
        {matches.map((match) => (
          <PopularMatchCard key={match.hash} match={match} />
        ))}
      </div>
    </section>
  );
}

function PopularMatchCard({ match }: { match: PopularMatch }) {
  const { hash, metrics, views } = match;
  const palette = metrics.colors?.slice(0, 4) || [];

  // Calculate a simple quality indicator
  const qualityScore = Math.round(
    (metrics.semanticScore * 0.4 + 
     (100 - Math.min(100, metrics.complexity * 0.6)) * 0.3 +
     (metrics.responsiveBreakpoints > 0 ? 20 : 0) +
     (metrics.layoutPattern !== 'basic' ? 10 : 0))
  );

  return (
    <Link
      href={`/code-match/${hash}`}
      className="group relative overflow-hidden rounded-[32px] border border-gray-200 bg-gradient-to-br from-white to-gray-50 p-6 shadow-[0_20px_60px_rgba(15,23,42,0.06)] transition hover:-translate-y-1 hover:shadow-[0_35px_90px_rgba(15,23,42,0.12)]"
    >
      {/* Trending badge */}
      <div className="absolute top-4 right-4 rounded-full bg-gradient-to-r from-emerald-400 to-cyan-400 px-3 py-1 text-xs font-semibold text-gray-900">
        🔥 {views} views
      </div>

      <div className="space-y-4 mt-8">
        {/* Main metrics */}
        <div className="grid grid-cols-2 gap-3">
          <MetricBadge label="Sections" value={metrics.sectionCount} />
          <MetricBadge label="CTAs" value={metrics.buttonCount} />
          <MetricBadge label="Images" value={metrics.imageCount} />
          <MetricBadge 
            label="Quality" 
            value={`${qualityScore}%`}
            highlight={qualityScore >= 70}
          />
        </div>

        {/* Color palette */}
        {palette.length > 0 && (
          <div className="space-y-2">
            <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Color Palette</p>
            <div className="flex gap-2">
              {palette.map((color) => (
                <div
                  key={color}
                  className="h-8 w-8 rounded-xl border border-gray-300 shadow-sm"
                  style={{ backgroundColor: color }}
                  title={color}
                />
              ))}
            </div>
          </div>
        )}

        {/* Layout pattern */}
        <div className="flex items-center justify-between pt-3 border-t border-gray-200">
          <span className="text-xs uppercase tracking-[0.3em] text-gray-500">
            {metrics.layoutPattern} layout
          </span>
          <span className="text-sm font-semibold text-gray-900 group-hover:text-emerald-600 transition">
            View →
          </span>
        </div>
      </div>
    </Link>
  );
}

function MetricBadge({ 
  label, 
  value, 
  highlight = false 
}: { 
  label: string; 
  value: string | number; 
  highlight?: boolean;
}) {
  return (
    <div className={`rounded-2xl border p-3 ${
      highlight 
        ? 'border-emerald-200 bg-emerald-50' 
        : 'border-gray-200 bg-white'
    }`}>
      <p className={`text-lg font-semibold ${
        highlight ? 'text-emerald-700' : 'text-gray-900'
      }`}>
        {value}
      </p>
      <p className={`text-[10px] uppercase tracking-[0.3em] ${
        highlight ? 'text-emerald-600' : 'text-gray-500'
      }`}>
        {label}
      </p>
    </div>
  );
}
