import { NextRequest, NextResponse } from 'next/server';
import { supabaseServer } from '@/lib/supabase/server';
import { DesignMetrics } from '@/lib/designAnalysis';
import { CodeMatch } from '@/types/database';

function generateHash(length = 8): string {
  const chars = 'abcdefghijklmnopqrstuvwxyz0123456789';
  let hash = '';
  for (let i = 0; i < length; i++) {
    hash += chars[Math.floor(Math.random() * chars.length)];
  }
  return hash;
}

export async function POST(request: NextRequest) {
  try {
    const payload = await request.json();
    const { code, metrics, results } = payload;

    if (!code || !metrics || !results) {
      return NextResponse.json(
        { error: 'Missing required fields: code, metrics, results' },
        { status: 400 }
      );
    }

    // Generate unique hash
    let hash = generateHash();
    let attempts = 0;
    const maxAttempts = 5;

    while (attempts < maxAttempts) {
      const { data: existing } = await supabaseServer
        .from('code_matches')
        .select('hash')
        .eq('hash', hash)
        .single();

      if (!existing) break;
      hash = generateHash();
      attempts++;
    }

    if (attempts >= maxAttempts) {
      return NextResponse.json(
        { error: 'Failed to generate unique hash' },
        { status: 500 }
      );
    }

    // Save to database
    const { data, error } = await supabaseServer
      .from('code_matches')
      .insert({
        hash,
        code,
        metrics,
        results,
      } as any)
      .select('hash')
      .single();

    if (error) {
      // If table doesn't exist in schema cache yet, return helpful message
      if (error.code === 'PGRST205') {
        return NextResponse.json(
          { 
            error: 'Share feature is being set up. Please try again in a few minutes.',
            code: 'TABLE_NOT_READY'
          },
          { status: 503 }
        );
      }
      console.error('Failed to save code match:', error);
      return NextResponse.json(
        { error: 'Failed to save code match result' },
        { status: 500 }
      );
    }

    const savedMatch = data as CodeMatch;

    return NextResponse.json({ hash: savedMatch.hash });
  } catch (error) {
    console.error('Code match save API error:', error);
    return NextResponse.json(
      { error: 'An unexpected error occurred' },
      { status: 500 }
    );
  }
}
