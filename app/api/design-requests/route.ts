import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';

const TABLE_NAME = 'design_requests';

function normalizeOptional(value: unknown, maxLength: number) {
  if (typeof value !== 'string') {
    return null;
  }
  const trimmed = value.trim();
  if (!trimmed) {
    return null;
  }
  return trimmed.slice(0, maxLength);
}

export async function GET() {
  try {
    const { data, error } = await (supabaseAdmin as any)
      .from(TABLE_NAME)
      .select('id, title, description, category, status, vote_count, linked_design_id, created_at')
      .in('status', ['pending', 'in_progress', 'completed'])
      .order('vote_count', { ascending: false })
      .order('created_at', { ascending: false })
      .limit(60);

    if (error) {
      if (error.code === 'PGRST205') {
        return NextResponse.json({ requests: [] });
      }
      console.error('Failed to fetch design requests', error);
      return NextResponse.json({ error: 'Failed to load requests.' }, { status: 500 });
    }

    const requests = (data ?? []) as Array<{
      id: string;
      title: string;
      description: string;
      category: string | null;
      status: 'pending' | 'in_progress' | 'completed';
      vote_count: number | null;
      linked_design_id: string | null;
      created_at: string;
    }>;

    const linkedIds = Array.from(
      new Set(
        requests
          .map((item) => item.linked_design_id)
          .filter((item): item is string => Boolean(item))
      )
    );

    let linkedDesignMap = new Map<string, { slug: string | null; title: string; status: string }>();

    if (linkedIds.length > 0) {
      const { data: designs, error: designError } = await (supabaseAdmin as any)
        .from('designs')
        .select('id, slug, title, status')
        .in('id', linkedIds);

      if (designError) {
        console.error('Failed to fetch linked designs', designError);
      } else {
        linkedDesignMap = new Map(
          (designs ?? []).map((design: any) => [
            design.id,
            { slug: design.slug ?? null, title: design.title, status: design.status },
          ])
        );
      }
    }

    const payload = requests.map((item) => {
      const linked = item.linked_design_id ? linkedDesignMap.get(item.linked_design_id) : null;
      return {
        id: item.id,
        title: item.title,
        description: item.description,
        category: item.category,
        status: item.status,
        voteCount: item.vote_count ?? 0,
        createdAt: item.created_at,
        linkedDesign:
          linked && linked.status !== 'archived'
            ? { slug: linked.slug, title: linked.title }
            : null,
      };
    });

    return NextResponse.json({ requests: payload });
  } catch (error) {
    console.error('Design request list API error', error);
    return NextResponse.json({ error: 'Server error.' }, { status: 500 });
  }
}

export async function POST(request: NextRequest) {
  try {
    const payload = (await request.json().catch(() => null)) as Record<string, unknown> | null;
    if (!payload) {
      return NextResponse.json({ error: 'Invalid request body.' }, { status: 400 });
    }

    const honeypot = normalizeOptional(payload.homepage_url, 200);
    if (honeypot) {
      return NextResponse.json({ success: true }, { status: 200 });
    }

    const title = normalizeOptional(payload.title, 120);
    const description = normalizeOptional(payload.description, 4000);
    const category = normalizeOptional(payload.category, 80);
    const targetAudience = normalizeOptional(payload.target_audience, 160);
    const referenceNotes = normalizeOptional(payload.reference_notes, 1000);
    const requesterEmail = normalizeOptional(payload.requester_email, 254);

    if (!title || title.length < 6) {
      return NextResponse.json({ error: 'Title must be at least 6 characters.' }, { status: 400 });
    }

    if (!description || description.length < 30) {
      return NextResponse.json({ error: 'Description must be at least 30 characters.' }, { status: 400 });
    }

    if (requesterEmail && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(requesterEmail)) {
      return NextResponse.json({ error: 'Please enter a valid email.' }, { status: 400 });
    }

    const ipAddress = request.headers.get('x-forwarded-for') || request.headers.get('x-real-ip') || null;
    const userAgent = request.headers.get('user-agent') || null;

    const { error } = await (supabaseAdmin as any)
      .from(TABLE_NAME)
      .insert({
        title,
        description,
        category,
        target_audience: targetAudience,
        reference_notes: referenceNotes,
        requester_email: requesterEmail,
        ip_address: ipAddress,
        user_agent: userAgent,
        status: 'pending',
      });

    if (error) {
      if (error.code === 'PGRST205') {
        return NextResponse.json(
          { error: 'Request feature is being set up. Please try again shortly.' },
          { status: 503 }
        );
      }

      console.error('Failed to insert design request', error);
      return NextResponse.json({ error: 'Failed to submit request.' }, { status: 500 });
    }

    return NextResponse.json({ success: true }, { status: 201 });
  } catch (error) {
    console.error('Design request API error', error);
    return NextResponse.json({ error: 'Server error.' }, { status: 500 });
  }
}
