import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { Database } from '@/types/database';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => ({}));
    const designId = typeof body?.designId === 'string' ? body.designId : null;

    if (!designId) {
      return NextResponse.json({ success: false, error: 'Missing designId' }, { status: 400 });
    }

    type ViewRow = { views: number | null; status: 'published' | 'archived' };
    const { data, error } = await supabaseAdmin
      .from('designs')
      .select('views, status')
      .eq('id', designId)
      .single<ViewRow>();

    if (error || !data) {
      console.error('Failed to read design views', error);
      return NextResponse.json({ success: false }, { status: 500 });
    }

    if (data.status === 'archived') {
      return NextResponse.json({ success: false, error: 'Design archived' }, { status: 410 });
    }

    const nextViews = (data.views ?? 0) + 1;
    const updates: Database['public']['Tables']['designs']['Update'] = {
      views: nextViews,
    };
    const { error: updateError } = await supabaseAdmin
      .from('designs')
      .update(updates as never)
      .eq('id', designId);

    if (updateError) {
      console.error('Failed to update design views', updateError);
      return NextResponse.json({ success: false }, { status: 500 });
    }

    return NextResponse.json({ success: true, views: nextViews });
  } catch (error) {
    console.error('Page view tracking error', error);
    return NextResponse.json({ success: false }, { status: 500 });
  }
}
