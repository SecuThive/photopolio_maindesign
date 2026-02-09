import { NextRequest, NextResponse } from 'next/server';
import { supabaseServer } from '@/lib/supabase/server';
import { withDesignSlugs } from '@/lib/slug';
import { analyzeMarkup, similarityScore, DesignMetrics } from '@/lib/designAnalysis';
import { Design } from '@/types/database';

type ScoredDesign = {
  design: Design;
  metrics: DesignMetrics;
  score: number;
};

export async function POST(request: NextRequest) {
  try {
    const payload = await request.json();
    const code: string | undefined = payload?.code;

    if (!code || typeof code !== 'string' || code.trim().length < 50) {
      return NextResponse.json(
        { error: 'Please include at least 50 characters of HTML or React markup.' },
        { status: 400 }
      );
    }

    const userMetrics = analyzeMarkup(code);
    if (!userMetrics) {
      return NextResponse.json(
        { error: 'We could not analyze that snippet. Please try again with valid markup.' },
        { status: 400 }
      );
    }

    const { data, error } = await supabaseServer
      .from('designs')
      .select('*')
      .eq('status', 'published')
      .not('code', 'is', null)
      .limit(60);

    if (error) {
      console.error('Failed to load designs for recommendation', error);
      return NextResponse.json({ error: 'Failed to load design data for recommendations.' }, { status: 500 });
    }

    const designRows = (data || []) as Design[];
    const scored = designRows
      .map((design) => {
        const metrics = analyzeMarkup(design.code);
        if (!metrics) return null;
        return {
          design,
          metrics,
          score: similarityScore(userMetrics, metrics),
        };
      })
      .filter((entry): entry is ScoredDesign => Boolean(entry))
      .sort((a, b) => b.score - a.score)
      .slice(0, 6);

    const response = withDesignSlugs(scored.map((entry) => entry.design)).map((design, index) => ({
      design,
      score: scored[index]?.score ?? 0,
    }));

    return NextResponse.json({ recommendations: response });
  } catch (error) {
    console.error('Recommendation API error', error);
    return NextResponse.json({ error: 'An unexpected error occurred while generating recommendations.' }, { status: 500 });
  }
}
