import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { Database } from '@/types/database';

type DesignLikesRow = Pick<Database['public']['Tables']['designs']['Row'], 'likes' | 'status'>;
type DesignLikeEntry = Database['public']['Tables']['design_likes']['Row'];
type DesignLikeInsert = Database['public']['Tables']['design_likes']['Insert'];

type LikeTokenPayload = {
  token?: string;
};

async function getDesignRecord(designId: string) {
  const { data, error } = await supabaseAdmin
    .from('designs')
    .select('likes, status')
    .eq('id', designId)
    .maybeSingle<DesignLikesRow>();

  if (error) {
    throw new Error(error.message);
  }

  return data ?? null;
}

function isArchived(design: DesignLikesRow | null) {
  return design?.status === 'archived';
}

export async function POST(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const { token }: LikeTokenPayload = await request.json();
    const designId = params.id;

    if (!token) {
      return NextResponse.json({ error: 'Missing like token' }, { status: 400 });
    }

    const design = await getDesignRecord(designId);

    if (!design) {
      return NextResponse.json({ error: 'Design not found' }, { status: 404 });
    }

    if (isArchived(design)) {
      return NextResponse.json({ error: 'Design archived' }, { status: 410 });
    }

    const { data: existing } = await supabaseAdmin
      .from('design_likes')
      .select('id')
      .eq('design_id', designId)
      .eq('token', token)
      .maybeSingle<Pick<DesignLikeEntry, 'id'>>();

    if (existing) {
      return NextResponse.json({ likes: design.likes ?? 0 });
    }

    const insertPayload: DesignLikeInsert = { design_id: designId, token };
    const { error: insertError } = await (supabaseAdmin as any)
      .from('design_likes')
      .insert(insertPayload);

    if (insertError) {
      return NextResponse.json({ error: insertError.message }, { status: 500 });
    }

    const currentLikes = design.likes ?? 0;
    const nextLikes = currentLikes + 1;

    const { error: updateError } = await (supabaseAdmin as any)
      .from('designs')
      .update({ likes: nextLikes })
      .eq('id', designId);

    if (updateError) {
      return NextResponse.json({ error: updateError.message }, { status: 500 });
    }

    return NextResponse.json({ likes: nextLikes });
  } catch (error) {
    console.error('Like POST error', error);
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}

export async function DELETE(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const { token }: LikeTokenPayload = await request.json();
    const designId = params.id;

    if (!token) {
      return NextResponse.json({ error: 'Missing like token' }, { status: 400 });
    }

    const design = await getDesignRecord(designId);

    if (!design) {
      return NextResponse.json({ error: 'Design not found' }, { status: 404 });
    }

    if (isArchived(design)) {
      return NextResponse.json({ error: 'Design archived' }, { status: 410 });
    }

    const { data: existing, error: fetchError } = await supabaseAdmin
      .from('design_likes')
      .select('id')
      .eq('design_id', designId)
      .eq('token', token)
      .maybeSingle<Pick<DesignLikeEntry, 'id'>>();

    if (fetchError) {
      return NextResponse.json({ error: fetchError.message }, { status: 500 });
    }

    if (!existing) {
      return NextResponse.json({ likes: design.likes ?? 0 });
    }

    const { error: deleteError } = await supabaseAdmin
      .from('design_likes')
      .delete()
      .eq('id', existing.id);

    if (deleteError) {
      return NextResponse.json({ error: deleteError.message }, { status: 500 });
    }

    const currentLikes = design.likes ?? 0;
    const nextLikes = Math.max(0, currentLikes - 1);

    const { error: updateError } = await (supabaseAdmin as any)
      .from('designs')
      .update({ likes: nextLikes })
      .eq('id', designId);

    if (updateError) {
      return NextResponse.json({ error: updateError.message }, { status: 500 });
    }

    return NextResponse.json({ likes: nextLikes });
  } catch (error) {
    console.error('Like DELETE error', error);
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}
