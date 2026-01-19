import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { Database } from '@/types/database';

const TABLE_MISSING_CODE = 'PGRST205';

export async function POST(request: NextRequest) {
  try {
    const body = await request.json().catch(() => ({}));
    const page = typeof body?.page === 'string' ? body.page : '/';
    const referer = request.headers.get('referer');
    const userAgent = request.headers.get('user-agent');

    const payload: Database['public']['Tables']['page_views']['Insert'] = {
      page,
      referer,
      user_agent: userAgent?.slice(0, 500) ?? null,
    };

    const { error } = await (supabaseAdmin.from('page_views') as any).insert(payload);

    if (error) {
      if (error.code === TABLE_MISSING_CODE) {
        console.warn('Page view tracking skipped: create page_views table to enable analytics.');
        return NextResponse.json({ success: false, missingTable: true });
      }
      console.error('Failed to record page view', error);
      return NextResponse.json({ success: false }, { status: 500 });
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Page view tracking error', error);
    return NextResponse.json({ success: false }, { status: 500 });
  }
}
