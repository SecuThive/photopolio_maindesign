import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { Database } from '@/types/database';

type DesignAsset = Pick<Database['public']['Tables']['designs']['Row'], 'id' | 'image_url'>;

export async function POST(request: NextRequest) {
  try {
    const cookieStore = await cookies();
    const adminAuth = cookieStore.get('admin_auth');

    if (adminAuth?.value !== 'true') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const body = (await request.json().catch(() => null)) as { ids?: unknown } | null;
    if (!body) {
      return NextResponse.json({ error: 'Invalid request body' }, { status: 400 });
    }

    const ids = Array.isArray(body.ids) ? body.ids : [];
    const validIds = Array.from(
      new Set(
        ids.filter((id): id is string => typeof id === 'string' && id.trim().length > 0)
      )
    );

    if (!validIds.length) {
      return NextResponse.json({ error: 'No design ids provided' }, { status: 400 });
    }

    const { data: designsData, error: fetchError } = await supabaseAdmin
      .from('designs')
      .select('id, image_url')
      .in('id', validIds);

    if (fetchError) {
      return NextResponse.json({ error: fetchError.message }, { status: 500 });
    }

    const designs = (designsData ?? []) as DesignAsset[];

    const archivePayload: Database['public']['Tables']['designs']['Update'] = {
      status: 'archived',
      updated_at: new Date().toISOString(),
    };

    const { error: archiveError } = await supabaseAdmin
      .from('designs')
      .update(archivePayload as never)
      .in('id', validIds);

    if (archiveError) {
      return NextResponse.json({ error: archiveError.message }, { status: 500 });
    }

    const storageKeys = designs
      .map((design) => {
        if (!design.image_url) return null;
        const fileName = decodeURIComponent(design.image_url.split('/').pop() ?? '');
        return fileName ? `designs/${fileName}` : null;
      })
      .filter((path): path is string => Boolean(path));

    if (storageKeys.length) {
      const { error: storageError } = await supabaseAdmin.storage
        .from('designs-bucket')
        .remove(storageKeys);

      if (storageError) {
        console.error('Failed to remove storage objects:', storageError.message);
      }
    }

    return NextResponse.json({ success: true, archivedIds: validIds });
  } catch (error) {
    console.error('Bulk delete designs error:', error);
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}
