import type { NextRequest } from 'next/server';
import { NextResponse } from 'next/server';

const BYPASS_PREFIXES = ['/playbooks', '/collections'];
const BYPASS_EXACT = new Set(['/sitemap.xml', '/feed.xml']);

function shouldBypass(pathname: string) {
  if (BYPASS_EXACT.has(pathname)) {
    return true;
  }
  return BYPASS_PREFIXES.some((prefix) => pathname === prefix || pathname.startsWith(`${prefix}/`));
}

export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  if (shouldBypass(pathname)) {
    return NextResponse.next();
  }

  return NextResponse.next();
}

export const config = {
  matcher: ['/((?!playbooks|collections|sitemap\\.xml|feed\\.xml).*)'],
};
