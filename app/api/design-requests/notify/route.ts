import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { resend, isResendEnabled, mailFrom, mailReplyTo } from '@/lib/resend';
import { DesignRequestReadyEmail } from '@/emails/DesignRequestReadyEmail';

const TABLE_NAME = 'design_requests';

function isUuid(value: string) {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
}

export async function POST(request: NextRequest) {
  try {
    const secret = process.env.REQUEST_NOTIFY_SECRET;
    if (!secret) {
      return NextResponse.json({ error: 'Notify secret not configured.' }, { status: 500 });
    }

    const authHeader = request.headers.get('authorization') || '';
    if (authHeader !== `Bearer ${secret}`) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    const payload = (await request.json().catch(() => null)) as {
      requestId?: string;
      designId?: string;
    } | null;

    const requestId = payload?.requestId || '';
    const designId = payload?.designId || '';

    if (!isUuid(requestId) || !isUuid(designId)) {
      return NextResponse.json({ error: 'Invalid request payload.' }, { status: 400 });
    }

    const { data: requestRow, error: requestError } = await (supabaseAdmin as any)
      .from(TABLE_NAME)
      .select('id, title, requester_email, status, notified_at, linked_design_id')
      .eq('id', requestId)
      .maybeSingle();

    if (requestError || !requestRow) {
      return NextResponse.json({ error: 'Request not found.' }, { status: 404 });
    }

    if (requestRow.notified_at) {
      return NextResponse.json({ success: true, skipped: 'already_notified' });
    }

    if (!requestRow.requester_email) {
      return NextResponse.json({ success: true, skipped: 'no_email' });
    }

    const { data: designRow, error: designError } = await (supabaseAdmin as any)
      .from('designs')
      .select('id, title, slug, status')
      .eq('id', designId)
      .maybeSingle();

    if (designError || !designRow) {
      return NextResponse.json({ error: 'Design not found.' }, { status: 404 });
    }

    if (designRow.status === 'archived') {
      return NextResponse.json({ success: true, skipped: 'archived_design' });
    }

    if (!isResendEnabled || !resend) {
      return NextResponse.json({ success: true, skipped: 'email_disabled' });
    }

    const siteUrl = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');
    const slug = designRow.slug || designRow.id;
    const designUrl = `${siteUrl}/design/${slug}`;

    await resend.emails.send({
      from: mailFrom,
      to: requestRow.requester_email,
      replyTo: mailReplyTo,
      subject: `Your requested design is ready: ${designRow.title}`,
      react: DesignRequestReadyEmail({
        requestTitle: requestRow.title,
        designTitle: designRow.title,
        designUrl,
      }),
    });

    const { error: updateError } = await (supabaseAdmin as any)
      .from(TABLE_NAME)
      .update({ notified_at: new Date().toISOString() })
      .eq('id', requestId);

    if (updateError) {
      console.error('Failed to set notified_at:', updateError);
    }

    return NextResponse.json({ success: true, designUrl });
  } catch (error) {
    console.error('Design request notify API error:', error);
    return NextResponse.json({ error: 'Server error.' }, { status: 500 });
  }
}
