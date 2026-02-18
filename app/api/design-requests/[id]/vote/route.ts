import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';

type VotePayload = {
  token?: string;
};

function isUuid(value: string) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
}

export async function POST(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const requestId = params.id;
    const { token }: VotePayload = await request.json().catch(() => ({}));

    if (!requestId || !isUuid(requestId)) {
      return NextResponse.json({ error: 'Invalid request id.' }, { status: 400 });
    }

    if (!token || token.length < 8) {
      return NextResponse.json({ error: 'Missing vote token.' }, { status: 400 });
    }

    const { data: requestRow, error: requestError } = await (supabaseAdmin as any)
      .from('design_requests')
      .select('id, vote_count')
      .eq('id', requestId)
      .maybeSingle();

    if (requestError) {
      if (requestError.code === 'PGRST205') {
        return NextResponse.json({ error: 'Request feature is being set up.' }, { status: 503 });
      }
      return NextResponse.json({ error: requestError.message }, { status: 500 });
    }

    if (!requestRow) {
      return NextResponse.json({ error: 'Request not found.' }, { status: 404 });
    }

    const { data: existing } = await (supabaseAdmin as any)
      .from('design_request_votes')
      .select('id')
      .eq('request_id', requestId)
      .eq('token', token)
      .maybeSingle();

    if (existing) {
      return NextResponse.json({ voteCount: requestRow.vote_count ?? 0, alreadyVoted: true });
    }

    const { error: insertError } = await (supabaseAdmin as any)
      .from('design_request_votes')
      .insert({
        request_id: requestId,
        token,
      });

    if (insertError) {
      if (insertError.code === 'PGRST205') {
        return NextResponse.json({ error: 'Voting feature is being set up.' }, { status: 503 });
      }
      return NextResponse.json({ error: insertError.message }, { status: 500 });
    }

    const nextVoteCount = (requestRow.vote_count ?? 0) + 1;
    const { error: updateError } = await (supabaseAdmin as any)
      .from('design_requests')
      .update({ vote_count: nextVoteCount })
      .eq('id', requestId);

    if (updateError) {
      return NextResponse.json({ error: updateError.message }, { status: 500 });
    }

    return NextResponse.json({ voteCount: nextVoteCount, alreadyVoted: false });
  } catch (error) {
    console.error('Design request vote API error', error);
    return NextResponse.json({ error: 'Server error.' }, { status: 500 });
  }
}
