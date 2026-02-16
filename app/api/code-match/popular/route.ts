import { NextResponse } from 'next/server';
import { supabaseServer } from '@/lib/supabase/server';
import { CodeMatch } from '@/types/database';

export async function GET() {
  try {
    // Get most viewed code matches from the last 30 days
    const thirtyDaysAgo = new Date();
    thirtyDaysAgo.setDate(thirtyDaysAgo.getDate() - 30);

    const { data, error } = await supabaseServer
      .from('code_matches')
      .select('hash, metrics, views, created_at')
      .gte('created_at', thirtyDaysAgo.toISOString())
      .order('views', { ascending: false })
      .limit(12);

    if (error) {
      // If table doesn't exist in schema cache yet, return empty gracefully
      if (error.code === 'PGRST205') {
        return NextResponse.json({ matches: [] });
      }
      console.error('Failed to fetch popular code matches:', error);
      return NextResponse.json(
        { error: 'Failed to fetch popular searches' },
        { status: 500 }
      );
    }

    const matches = data as Pick<CodeMatch, 'hash' | 'metrics' | 'views' | 'created_at'>[];
    
    const popularMatches = (matches || []).map((match) => ({
      hash: match.hash,
      metrics: match.metrics,
      views: match.views,
      createdAt: match.created_at,
    }));

    return NextResponse.json({ matches: popularMatches });
  } catch (error) {
    console.error('Popular code matches API error:', error);
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}
