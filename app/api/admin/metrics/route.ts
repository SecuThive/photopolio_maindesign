import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { supabaseAdmin } from '@/lib/supabase/admin';

const CATEGORIES = [
  'Landing Page',
  'Dashboard',
  'E-commerce',
  'Portfolio',
  'Blog',
  'Components',
];

const TABLE_MISSING_CODE = 'PGRST205';

function startOfDay(date: Date) {
  const copy = new Date(date);
  copy.setHours(0, 0, 0, 0);
  return copy;
}

function endOfDay(date: Date) {
  const copy = new Date(date);
  copy.setHours(23, 59, 59, 999);
  return copy;
}

export async function GET(request: NextRequest) {
  const cookieStore = await cookies();
  const adminAuth = cookieStore.get('admin_auth');

  if (adminAuth?.value !== 'true') {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  }

  const isMissingPageViews = (error: { code?: string } | null | undefined) =>
    error?.code === TABLE_MISSING_CODE;

  try {
    const [totalDesignRes, totalViewRes, todayViewRes] = await Promise.all([
      supabaseAdmin
        .from('designs')
        .select('id', { count: 'exact', head: true }),
      supabaseAdmin
        .from('page_views')
        .select('id', { count: 'exact', head: true }),
      supabaseAdmin
        .from('page_views')
        .select('id', { count: 'exact', head: true })
        .gte('created_at', startOfDay(new Date()).toISOString())
        .lte('created_at', endOfDay(new Date()).toISOString()),
    ]);

    if (totalDesignRes.error) {
      throw totalDesignRes.error;
    }

    if (totalViewRes.error && !isMissingPageViews(totalViewRes.error)) {
      throw totalViewRes.error;
    }

    if (todayViewRes.error && !isMissingPageViews(todayViewRes.error)) {
      throw todayViewRes.error;
    }

    const missingAnalyticsData =
      isMissingPageViews(totalViewRes.error) || isMissingPageViews(todayViewRes.error);

    if (missingAnalyticsData) {
      console.warn('Analytics table missing: create page_views table to enable full metrics.');
    }

    const totalViews = isMissingPageViews(totalViewRes.error) ? 0 : totalViewRes.count ?? 0;
    const todayViews = isMissingPageViews(todayViewRes.error) ? 0 : todayViewRes.count ?? 0;

    const categoryCounts = await Promise.all(
      CATEGORIES.map(async (category) => {
        const { count } = await supabaseAdmin
          .from('designs')
          .select('id', { count: 'exact', head: true })
          .eq('category', category);
        return { category, count: count ?? 0 };
      })
    );

    const since = startOfDay(new Date());
    since.setDate(since.getDate() - 6);

    const { data: recentViews, error: recentViewsError } = await supabaseAdmin
      .from('page_views')
      .select('created_at')
      .gte('created_at', since.toISOString());

    if (recentViewsError && !isMissingPageViews(recentViewsError)) {
      throw recentViewsError;
    }

    const dailyMap: Record<string, number> = {};
    for (let i = 0; i < 7; i++) {
      const date = new Date(since);
      date.setDate(since.getDate() + i);
      const key = date.toISOString().split('T')[0];
      dailyMap[key] = 0;
    }

    const safeRecentViews = isMissingPageViews(recentViewsError)
      ? []
      : ((recentViews ?? []) as { created_at: string }[]);
    safeRecentViews.forEach((view) => {
      const key = new Date(view.created_at).toISOString().split('T')[0];
      if (dailyMap[key] === undefined) {
        dailyMap[key] = 0;
      }
      dailyMap[key] += 1;
    });

    const dailyViews = Object.entries(dailyMap).map(([date, count]) => ({ date, count }));

    return NextResponse.json({
      totalDesigns: totalDesignRes.count ?? 0,
      totalViews,
      todayViews,
      categoryCounts,
      dailyViews,
    });
  } catch (error) {
    console.error('Failed to load metrics', error);
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}
