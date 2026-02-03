import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { resend } from '@/lib/resend';
import { WeeklyDigestEmail } from '@/emails/WeeklyDigestEmail';

// Vercel Cron Job - runs every Monday at 10:00 AM UTC
export async function GET(request: NextRequest) {
  try {
    // Verify the request is from Vercel Cron
    const authHeader = request.headers.get('authorization');
    if (authHeader !== `Bearer ${process.env.CRON_SECRET}`) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    console.log('Starting weekly newsletter cron job...');

    // Get all active subscribers
    const { data: subscribers, error: subscribersError } = await (supabaseAdmin as any)
      .from('newsletter_subscribers')
      .select('email')
      .eq('is_active', true);

    if (subscribersError) {
      console.error('Error fetching subscribers:', subscribersError);
      return NextResponse.json(
        { error: 'Failed to fetch subscribers' },
        { status: 500 }
      );
    }

    if (!subscribers || subscribers.length === 0) {
      console.log('No active subscribers found');
      return NextResponse.json({ message: 'No subscribers to send to' });
    }

    // Get latest designs from the past week
    const oneWeekAgo = new Date();
    oneWeekAgo.setDate(oneWeekAgo.getDate() - 7);

    const { data: designs, error: designsError } = await (supabaseAdmin as any)
      .from('designs')
      .select('title, slug, image_url, category')
      .eq('status', 'published')
      .gte('created_at', oneWeekAgo.toISOString())
      .order('created_at', { ascending: false })
      .limit(6);

    if (designsError) {
      console.error('Error fetching designs:', designsError);
      return NextResponse.json(
        { error: 'Failed to fetch designs' },
        { status: 500 }
      );
    }

    // If no new designs this week, get the latest 6 designs
    let featuredDesigns = designs;
    if (!designs || designs.length === 0) {
      const { data: latestDesigns } = await (supabaseAdmin as any)
        .from('designs')
        .select('title, slug, image_url, category')
        .eq('status', 'published')
        .order('created_at', { ascending: false })
        .limit(6);
      
      featuredDesigns = latestDesigns || [];
    }

    if (featuredDesigns.length === 0) {
      console.log('No designs to feature');
      return NextResponse.json({ message: 'No designs available' });
    }

    // Send emails in batches to avoid rate limits
    const batchSize = 50;
    let sentCount = 0;
    let errorCount = 0;

    for (let i = 0; i < subscribers.length; i += batchSize) {
      const batch = subscribers.slice(i, i + batchSize);
      
      const emailPromises = batch.map(async (subscriber: { email: string }) => {
        try {
          await resend.emails.send({
            from: 'UI Syntax <newsletter@uisyntax.com>',
            to: subscriber.email,
            subject: `✨ This Week's AI Design Inspiration - UI Syntax`,
            react: WeeklyDigestEmail({ designs: featuredDesigns }),
          });
          sentCount++;
        } catch (error) {
          console.error(`Failed to send to ${subscriber.email}:`, error);
          errorCount++;
        }
      });

      await Promise.all(emailPromises);
      
      // Add a small delay between batches to avoid rate limiting
      if (i + batchSize < subscribers.length) {
        await new Promise(resolve => setTimeout(resolve, 1000));
      }
    }

    console.log(`Newsletter sent: ${sentCount} successful, ${errorCount} failed`);

    return NextResponse.json({
      success: true,
      message: `Newsletter sent to ${sentCount} subscribers`,
      designs: featuredDesigns.length,
      errors: errorCount,
    });

  } catch (error) {
    console.error('Cron job error:', error);
    return NextResponse.json(
      { error: 'Internal server error' },
      { status: 500 }
    );
  }
}
