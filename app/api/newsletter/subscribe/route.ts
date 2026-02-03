import { NextRequest, NextResponse } from 'next/server';
import { supabaseAdmin } from '@/lib/supabase/admin';
import { resend } from '@/lib/resend';
import { WelcomeEmail } from '@/emails/WelcomeEmail';
import type { Database } from '@/types/database';

export async function POST(request: NextRequest) {
  try {
    const { email } = await request.json();

    // Validate email
    if (!email || typeof email !== 'string') {
      return NextResponse.json(
        { error: 'Please enter your email address.' },
        { status: 400 }
      );
    }

    // Basic email validation
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(email)) {
      return NextResponse.json(
        { error: 'Please enter a valid email address.' },
        { status: 400 }
      );
    }

    // Get IP address and user agent for analytics
    const ip = request.headers.get('x-forwarded-for') || 
               request.headers.get('x-real-ip') || 
               'unknown';
    const userAgent = request.headers.get('user-agent') || 'unknown';

    // Insert subscriber
    const { data, error } = await (supabaseAdmin as any)
      .from('newsletter_subscribers')
      .insert({
        email: email.toLowerCase().trim(),
        ip_address: ip,
        user_agent: userAgent,
      })
      .select();

    if (error) {
      // Check for duplicate email
      if (error.code === '23505') {
        return NextResponse.json(
          { error: 'This email is already subscribed.' },
          { status: 409 }
        );
      }

      console.error('Newsletter subscription error:', error);
      return NextResponse.json(
        { error: 'An error occurred while processing your subscription.' },
        { status: 500 }
      );
    // Send welcome email
    try {
      await resend.emails.send({
        from: 'UI Syntax <newsletter@uisyntax.com>',
        to: email.toLowerCase().trim(),
        subject: 'Welcome to UI Syntax - Your Weekly AI Design Digest',
        react: WelcomeEmail({ email: email.toLowerCase().trim() }),
      });
    } catch (emailError) {
      // Log error but don't fail the subscription
      console.error('Failed to send welcome email:', emailError);
      // Subscription still successful, just email failed
    }

    }

    return NextResponse.json(
      { 
        success: true, 
        message: 'Thank you for subscribing! You\'ll receive weekly AI design trends in your inbox.' 
      },
      { status: 201 }
    );

  } catch (error) {
    console.error('Newsletter API error:', error);
    return NextResponse.json(
      { error: 'A server error occurred.' },
      { status: 500 }
    );
  }
}
