import { NextRequest, NextResponse } from 'next/server';
import { cookies } from 'next/headers';

export async function POST(request: NextRequest) {
  try {
    const { path } = await request.json();
    const secretPath = process.env.ADMIN_SECRET_PATH || 'secret-admin-dashboard-x9k2p';
    
    // Validate that the requested path matches the secret slug
    if (path !== secretPath) {
      return NextResponse.json({ error: 'Invalid path' }, { status: 404 });
    }
    
    return NextResponse.json({ valid: true });
  } catch (error) {
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}

export async function GET(request: NextRequest) {
  try {
    const cookieStore = await cookies();
    const adminAuth = cookieStore.get('admin_auth');

    if (adminAuth?.value === 'true') {
      return NextResponse.json({ authenticated: true });
    } else {
      return NextResponse.json({ authenticated: false }, { status: 401 });
    }
  } catch (error) {
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}
