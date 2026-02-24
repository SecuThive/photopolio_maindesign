import { NextResponse } from 'next/server';

const SITE_URL = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '');

export async function GET() {
  const body = [
    'User-agent: *',
    'Allow: /',
    'Disallow: /api/',
    'Disallow: /admin/',
    `Sitemap: ${SITE_URL}/sitemap.xml`,
  ].join('\n');

  return new NextResponse(`${body}\n`, {
    status: 200,
    headers: {
      'Content-Type': 'text/plain; charset=utf-8',
      'Cache-Control': 'public, max-age=0, must-revalidate',
    },
  });
}
