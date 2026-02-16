"use client";

import { useRef } from 'react';
import { DesignMetrics } from '@/lib/designAnalysis';

type CodeScoreCardProps = {
  metrics: DesignMetrics;
  matchCount: number;
  bestMatchScore: number;
};

function calculateScores(metrics: DesignMetrics) {
  // Accessibility Score (based on semantic HTML usage)
  const accessibilityScore = metrics.semanticScore;

  // Performance Score (inverse of complexity - simpler is better for performance)
  const performanceScore = Math.max(0, Math.min(100, 100 - metrics.complexity * 0.6));

  // Design Quality Score (balanced structure and interactivity)
  const hasGoodStructure = metrics.sectionCount >= 3 && metrics.sectionCount <= 10;
  const hasGoodCTAs = metrics.buttonCount >= 1 && metrics.buttonCount <= 8;
  const hasColors = metrics.colors.length >= 2 && metrics.colors.length <= 6;
  const hasImages = metrics.imageCount > 0;
  const isResponsive = metrics.responsiveBreakpoints > 0;
  
  let designQuality = 0;
  if (hasGoodStructure) designQuality += 25;
  if (hasGoodCTAs) designQuality += 20;
  if (hasColors) designQuality += 20;
  if (hasImages) designQuality += 15;
  if (isResponsive) designQuality += 20;

  // Modern Patterns Score (grid/flex usage, responsive)
  let modernScore = 0;
  if (metrics.layoutPattern === 'grid') modernScore += 35;
  else if (metrics.layoutPattern === 'flex') modernScore += 30;
  else if (metrics.layoutPattern === 'mixed') modernScore += 40;
  else modernScore += 10;
  
  modernScore += Math.min(30, metrics.responsiveBreakpoints * 10);
  modernScore += metrics.colors.length >= 3 ? 30 : 10;

  return {
    accessibility: Math.round(accessibilityScore),
    performance: Math.round(performanceScore),
    designQuality: Math.round(designQuality),
    modernPatterns: Math.round(modernScore),
    overall: Math.round((accessibilityScore + performanceScore + designQuality + modernScore) / 4),
  };
}

function getGrade(score: number): { grade: string; color: string } {
  if (score >= 90) return { grade: 'A+', color: 'text-emerald-600' };
  if (score >= 80) return { grade: 'A', color: 'text-emerald-500' };
  if (score >= 70) return { grade: 'B+', color: 'text-blue-600' };
  if (score >= 60) return { grade: 'B', color: 'text-blue-500' };
  if (score >= 50) return { grade: 'C', color: 'text-yellow-600' };
  return { grade: 'D', color: 'text-orange-600' };
}

export default function CodeScoreCard({ metrics, matchCount, bestMatchScore }: CodeScoreCardProps) {
  const cardRef = useRef<HTMLDivElement>(null);
  const scores = calculateScores(metrics);
  const overallGrade = getGrade(scores.overall);

  const handleShareCard = async () => {
    const message = `My Code Quality Score: ${scores.overall}/100 (${overallGrade.grade})

🎯 Accessibility: ${scores.accessibility}/100
⚡ Performance: ${scores.performance}/100
🎨 Design Quality: ${scores.designQuality}/100
✨ Modern Patterns: ${scores.modernPatterns}/100

Found ${matchCount} matching UI designs on UI Syntax!
Try it: ${window.location.origin}/code-match`;

    try {
      // Try Web Share API first (mobile & modern browsers)
      if (navigator.share) {
        await navigator.share({
          title: 'My Code Quality Score',
          text: message,
          url: `${window.location.origin}/code-match`,
        });
      } else {
        // Fallback to clipboard copy
        await navigator.clipboard.writeText(message);
        alert('Score card copied to clipboard! Share it on social media.');
      }
    } catch (err) {
      // If user cancels share or clipboard fails, try clipboard as fallback
      if (err instanceof Error && err.name !== 'AbortError') {
        try {
          await navigator.clipboard.writeText(message);
          alert('Score card copied to clipboard! Share it on social media.');
        } catch (clipboardErr) {
          console.error('Failed to share or copy:', clipboardErr);
          alert('Unable to share. Please try again.');
        }
      }
    }
  };

  return (
    <div className="space-y-6">
      <div
        ref={cardRef}
        className="relative overflow-hidden rounded-[44px] border-2 border-gray-900 bg-gradient-to-br from-gray-900 via-[#0f172a] to-gray-900 p-12 text-white shadow-[0_50px_140px_rgba(2,6,23,0.9)]"
      >
        {/* Enhanced background decorations */}
        <div className="absolute -top-32 -right-32 h-96 w-96 rounded-full bg-gradient-to-br from-emerald-500/30 to-teal-500/30 blur-[120px]" aria-hidden />
        <div className="absolute -bottom-32 -left-32 h-96 w-96 rounded-full bg-gradient-to-br from-cyan-500/30 to-blue-500/30 blur-[120px]" aria-hidden />
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_center,_rgba(16,185,129,0.08),_transparent_70%)]" aria-hidden />
        
        {/* Grid pattern overlay */}
        <div className="absolute inset-0 bg-[linear-gradient(rgba(255,255,255,0.03)_1px,transparent_1px),linear-gradient(90deg,rgba(255,255,255,0.03)_1px,transparent_1px)] bg-[size:40px_40px]" aria-hidden />
        
        <div className="relative space-y-8">
          {/* Header */}
          <div className="text-center space-y-4">
            <div className="inline-flex items-center gap-2 rounded-full bg-emerald-500/10 border border-emerald-400/30 px-5 py-2">
              <svg className="h-4 w-4 text-emerald-400" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
              </svg>
              <p className="text-xs uppercase tracking-[0.4em] text-emerald-300 font-bold">Code Quality Score</p>
            </div>
            
            <div className="inline-flex flex-col items-center">
              <div className={`text-8xl font-black ${overallGrade.color} drop-shadow-2xl tracking-tight`}>
                {overallGrade.grade}
              </div>
              <div className="text-6xl font-bold bg-gradient-to-r from-white via-gray-100 to-gray-300 bg-clip-text text-transparent mt-3">
                {scores.overall}/100
              </div>
            </div>
            
            <p className="text-base text-gray-300">
              Analyzed <span className="font-semibold text-white">{metrics.sectionCount}</span> sections · <span className="font-semibold text-white">{metrics.buttonCount}</span> CTAs · <span className="font-semibold text-white">{metrics.colors.length}</span> colors
            </p>
          </div>

          {/* Score breakdown */}
          <div className="grid grid-cols-2 gap-5">
            <ScoreItem label="Accessibility" score={scores.accessibility} icon="🎯" />
            <ScoreItem label="Performance" score={scores.performance} icon="⚡" />
            <ScoreItem label="Design Quality" score={scores.designQuality} icon="🎨" />
            <ScoreItem label="Modern Patterns" score={scores.modernPatterns} icon="✨" />
          </div>

          {/* Match info */}
          <div className="rounded-[32px] border-2 border-white/20 bg-gradient-to-br from-white/15 to-white/5 backdrop-blur-xl p-8 text-center">
            <div className="inline-flex items-center justify-center h-16 w-16 rounded-2xl bg-gradient-to-br from-emerald-400 to-cyan-400 text-4xl mb-4 shadow-xl">
              🎯
            </div>
            <p className="text-4xl font-black text-white mb-2">{matchCount}</p>
            <p className="text-sm uppercase tracking-[0.35em] text-gray-300 font-semibold">Matching Designs</p>
            <div className="mt-4 pt-4 border-t border-white/20">
              <p className="text-base text-emerald-300 font-semibold">
                Best match: {Math.round(bestMatchScore * 100)}%
              </p>
            </div>
          </div>

          {/* Footer branding */}
          <div className="text-center pt-6 border-t border-white/20">
            <p className="text-sm uppercase tracking-[0.4em] text-gray-300 font-bold">UI Syntax</p>
            <p className="text-xs text-gray-500 mt-1">Code Match Analysis</p>
          </div>
        </div>
      </div>

      {/* Action buttons */}
      <div className="flex gap-4">
        <button
          onClick={handleShareCard}
          className="group flex-1 inline-flex items-center justify-center gap-3 rounded-full bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 px-8 py-4 text-base font-bold text-gray-900 transition-all hover:shadow-[0_0_40px_rgba(16,185,129,0.6)] hover:scale-[1.02] active:scale-[0.98]"
        >
          <svg className="h-6 w-6 group-hover:rotate-12 transition-transform" fill="none" viewBox="0 0 24 24" stroke="currentColor">
            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2.5} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
          </svg>
          <span className="tracking-wide">Share Your Score</span>
        </button>
      </div>

      {/* Tips section */}
      <div className="rounded-[36px] border-2 border-gray-200 bg-gradient-to-br from-gray-50 to-white p-8">
        <div className="flex items-center gap-3 mb-5">
          <div className="h-12 w-12 rounded-2xl bg-gradient-to-br from-yellow-400 to-orange-400 flex items-center justify-center text-2xl shadow-lg">
            💡
          </div>
          <h4 className="text-lg font-black text-gray-900 uppercase tracking-wide">Improve Your Score</h4>
        </div>
        <ul className="space-y-4">
          {scores.accessibility < 70 && (
            <li className="flex items-start gap-4 p-4 rounded-2xl bg-emerald-50 border border-emerald-200">
              <div className="flex-shrink-0 h-8 w-8 rounded-xl bg-emerald-500 flex items-center justify-center text-white font-bold mt-0.5">
                →
              </div>
              <div className="flex-1">
                <p className="font-semibold text-gray-900 mb-1">🎯 Accessibility</p>
                <p className="text-sm text-gray-700">Use semantic HTML tags like <code className="bg-gray-200 px-2 py-1 rounded font-mono text-xs">&lt;section&gt;</code>, <code className="bg-gray-200 px-2 py-1 rounded font-mono text-xs">&lt;article&gt;</code>, <code className="bg-gray-200 px-2 py-1 rounded font-mono text-xs">&lt;nav&gt;</code></p>
              </div>
            </li>
          )}
          {scores.performance < 70 && (
            <li className="flex items-start gap-4 p-4 rounded-2xl bg-blue-50 border border-blue-200">
              <div className="flex-shrink-0 h-8 w-8 rounded-xl bg-blue-500 flex items-center justify-center text-white font-bold mt-0.5">
                →
              </div>
              <div className="flex-1">
                <p className="font-semibold text-gray-900 mb-1">⚡ Performance</p>
                <p className="text-sm text-gray-700">Simplify your structure - aim for 3-8 main sections</p>
              </div>
            </li>
          )}
          {scores.modernPatterns < 70 && (
            <li className="flex items-start gap-4 p-4 rounded-2xl bg-purple-50 border border-purple-200">
              <div className="flex-shrink-0 h-8 w-8 rounded-xl bg-purple-500 flex items-center justify-center text-white font-bold mt-0.5">
                →
              </div>
              <div className="flex-1">
                <p className="font-semibold text-gray-900 mb-1">✨ Modern Patterns</p>
                <p className="text-sm text-gray-700">Use modern CSS like Flexbox or Grid, and add responsive breakpoints</p>
              </div>
            </li>
          )}
          {scores.designQuality < 70 && (
            <li className="flex items-start gap-4 p-4 rounded-2xl bg-orange-50 border border-orange-200">
              <div className="flex-shrink-0 h-8 w-8 rounded-xl bg-orange-500 flex items-center justify-center text-white font-bold mt-0.5">
                →
              </div>
              <div className="flex-1">
                <p className="font-semibold text-gray-900 mb-1">🎨 Design Quality</p>
                <p className="text-sm text-gray-700">Balance your CTAs (1-8 buttons), add images, and use a color palette (2-6 colors)</p>
              </div>
            </li>
          )}
        </ul>
      </div>
    </div>
  );
}

function ScoreItem({ label, score, icon }: { label: string; score: number; icon: string }) {
  const percentage = Math.min(100, score);
  const grade = getGrade(score);

  return (
    <div className="group rounded-[32px] border-2 border-white/30 bg-gradient-to-br from-white/10 to-white/5 backdrop-blur-xl p-6 hover:border-white/40 hover:bg-white/15 transition-all duration-300">
      <div className="flex items-center justify-between mb-3">
        <span className="text-3xl group-hover:scale-110 transition-transform">{icon}</span>
        <span className={`text-3xl font-black ${grade.color} drop-shadow-lg`}>{score}</span>
      </div>
      <p className="text-xs uppercase tracking-[0.35em] text-gray-200 font-semibold mb-4">{label}</p>
      <div className="relative h-3 rounded-full bg-white/10 overflow-hidden">
        <div
          className="absolute inset-0 rounded-full bg-gradient-to-r from-emerald-400 via-teal-400 to-cyan-400 transition-all duration-1000 shadow-[0_0_20px_rgba(16,185,129,0.5)]"
          style={{ width: `${percentage}%` }}
        />
      </div>
    </div>
  );
}
