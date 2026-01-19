import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const { password } = await request.json();
    const adminPassword = process.env.ADMIN_PASSWORD;

    if (password === adminPassword) {
      const response = NextResponse.json({ success: true });
      response.cookies.set({
        name: 'admin_auth',
        value: 'true',
        httpOnly: true,
        secure: request.nextUrl.protocol === 'https:',
        sameSite: 'strict',
        path: '/',
        maxAge: 60 * 60 * 24,
      });
      return response;
    } else {
      return NextResponse.json({ error: 'Invalid password' }, { status: 401 });
    }
  } catch (error) {
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}
