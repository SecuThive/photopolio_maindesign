import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';
import type { Database } from '@/types/database';

type DesignLikesRow = Pick<Database['public']['Tables']['designs']['Row'], 'likes'>;
type DesignLikeEntry = Database['public']['Tables']['design_likes']['Row'];
type DesignLikeInsert = Database['public']['Tables']['design_likes']['Insert'];

type LikeTokenPayload = {
  token?: string;
};

async function getDesignLikes(designId: string) {
  const { data, error } = await supabaseAdmin
    .from('designs')
    .select('likes')
    .eq('id', designId)
    .single<DesignLikesRow>();

  if (error) {
    throw new Error(error.message);
  }

  return data?.likes ?? 0;
}

async function respondWithLikes(designId: string) {
  const likes = await getDesignLikes(designId);
  return NextResponse.json({ likes });
}

export async function POST(request: NextRequest, { params }: { params: { id: string } }) {
  try {
    const { token }: LikeTokenPayload = await request.json();
    const designId = params.id;

    if (!token) {
      return NextResponse.json({ error: 'Missing like token' }, { status: 400 });
    }

    const { data: existing } = await supabaseAdmin
      .from('design_likes')
      .select('id')
      .eq('design_id', designId)
      .eq('token', token)
      .maybeSingle<Pick<DesignLikeEntry, 'id'>>();

    if (existing) {
      return respondWithLikes(designId);
    }

    const insertPayload: DesignLikeInsert = { design_id: designId, token };
    const { error: insertError } = await (supabaseAdmin as any)
      .from('design_likes')
      .insert(insertPayload);

    if (insertError) {
      return NextResponse.json({ error: insertError.message }, { status: 500 });
    }

    const currentLikes = await getDesignLikes(designId);
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
      return respondWithLikes(designId);
    }

    const { error: deleteError } = await supabaseAdmin
      .from('design_likes')
      .delete()
      .eq('id', existing.id);

    if (deleteError) {
      return NextResponse.json({ error: deleteError.message }, { status: 500 });
    }

    const currentLikes = await getDesignLikes(designId);
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
