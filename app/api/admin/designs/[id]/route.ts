import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { Database } from '@/types/database';

type DesignImageRow = Pick<Database['public']['Tables']['designs']['Row'], 'image_url'>;

export async function DELETE(
  _request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const cookieStore = await cookies();
    const adminAuth = cookieStore.get('admin_auth');

    if (adminAuth?.value !== 'true') {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const designId = params.id;
    if (!designId) {
      return NextResponse.json({ error: 'Missing design id' }, { status: 400 });
    }

    const { data: design, error: fetchError } = await supabaseAdmin
      .from('designs')
      .select('image_url')
      .eq('id', designId)
      .single<DesignImageRow>();

    if (fetchError) {
      return NextResponse.json({ error: fetchError.message }, { status: 500 });
    }

    const archivePayload: Database['public']['Tables']['designs']['Update'] = {
      status: 'archived',
      updated_at: new Date().toISOString(),
    };

    const { error: archiveError } = await supabaseAdmin
      .from('designs')
      .update(archivePayload as never)
      .eq('id', designId);

    if (archiveError) {
      return NextResponse.json({ error: archiveError.message }, { status: 500 });
    }

    if (design?.image_url) {
      const fileName = decodeURIComponent(design.image_url.split('/').pop() || '');
      if (fileName) {
        const { error: storageError } = await supabaseAdmin.storage
          .from('designs-bucket')
          .remove([`designs/${fileName}`]);

        if (storageError) {
          console.error('Failed to remove storage object:', storageError.message);
        }
      }
    }

    return NextResponse.json({ success: true });
  } catch (error) {
    console.error('Delete design error:', error);
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}
