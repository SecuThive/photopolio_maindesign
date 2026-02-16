import { NextRequest, NextResponse } from 'next/server';
import { supabaseServer } from '@/lib/supabase/server';
import { CodeMatch } from '@/types/database';

export async function GET(
  request: NextRequest,
  { params }: { params: { hash: string } }
) {
  try {
    const { hash } = params;

    if (!hash || typeof hash !== 'string') {
      return NextResponse.json(
        { error: 'Invalid hash parameter' },
        { status: 400 }
      );
    }

    // Fetch the code match
    const { data, error } = await supabaseServer
      .from('code_matches')
      .select('*')
      .eq('hash', hash)
      .single();

    if (error || !data) {
      return NextResponse.json(
        { error: 'Code match not found' },
        { status: 404 }
      );
    }

    const codeMatch = data as CodeMatch;

    // Increment view count
    (supabaseServer.from('code_matches') as any)
      .update({ views: (codeMatch.views || 0) + 1 })
      .eq('hash', hash);

    return NextResponse.json({
      code: codeMatch.code,
      metrics: codeMatch.metrics,
      results: codeMatch.results,
      views: (codeMatch.views || 0) + 1,
      createdAt: codeMatch.created_at,
    });
  } catch (error) {
    console.error('Code match fetch API error:', error);
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}
