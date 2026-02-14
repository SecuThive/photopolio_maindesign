import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { Database } from '@/types/database';

const TABLE_MISSING_CODE = 'PGRST205';

type WebVitalInsert = Database['public']['Tables']['web_vitals_events']['Insert'];

type IncomingPayload = {
  metric?: string;
  value?: number;
  delta?: number;
  rating?: string;
  label?: string;
  id?: string;
  page?: string;
  navigationType?: string;
  blockedThirdParty?: boolean;
  connection?: {
    effectiveType?: string | null;
    saveData?: boolean | null;
  } | null;
};

function buildConnectionString(connection: IncomingPayload['connection']): string | null {
  if (!connection) {
    return null;
  }

  const parts: string[] = [];
  if (connection.effectiveType) {
    parts.push(connection.effectiveType);
  }
  if (connection.saveData) {
    parts.push('save-data');
  }

  return parts.length > 0 ? parts.join('|') : null;
}

export async function POST(request: NextRequest) {
  let payload: IncomingPayload | null = null;

  try {
    payload = (await request.json().catch(() => null)) as IncomingPayload | null;
  } catch (error) {
    console.warn('Invalid JSON payload for web vitals endpoint', error);
  }

  if (!payload || typeof payload.metric !== 'string' || typeof payload.value !== 'number') {
    return NextResponse.json({ error: 'Invalid payload' }, { status: 400 });
  }

  const body: WebVitalInsert = {
    metric: payload.metric,
    value: payload.value,
    delta: typeof payload.delta === 'number' ? payload.delta : null,
    rating: typeof payload.rating === 'string' ? payload.rating : null,
    label: typeof payload.label === 'string' ? payload.label : null,
    page: typeof payload.page === 'string' ? payload.page : null,
    session_id: typeof payload.id === 'string' ? payload.id : null,
    navigation_type: typeof payload.navigationType === 'string' ? payload.navigationType : null,
    blocked_third_party: Boolean(payload.blockedThirdParty ?? false),
    connection: buildConnectionString(payload.connection ?? null),
    user_agent: request.headers.get('user-agent'),
  };

  try {
    const { error } = await (supabaseAdmin as unknown as {
      from: (table: 'web_vitals_events') => {
        insert: (values: WebVitalInsert) => Promise<{ error: { code?: string } | null }>;
      };
    }).from('web_vitals_events').insert(body);

    if (error) {
      if (error.code === TABLE_MISSING_CODE) {
        console.warn('web_vitals_events table missing. Metrics stored in-flight only.');
        return NextResponse.json({ stored: false, reason: 'table-missing' }, { status: 202 });
      }

      throw error;
    }

    return NextResponse.json({ stored: true });
  } catch (error) {
    console.error('Failed to persist web vitals metric', error);
    return NextResponse.json({ stored: false }, { status: 202 });
  }
}
