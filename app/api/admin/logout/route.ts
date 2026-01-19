import { NextRequest, NextResponse } from 'next/server';

export async function POST(request: NextRequest) {
  try {
    const response = NextResponse.json({ success: true });
    response.cookies.set({
      name: 'admin_auth',
      value: '',
      maxAge: 0,
      path: '/',
      secure: request.nextUrl.protocol === 'https:',
      sameSite: 'strict',
      httpOnly: true,
    });
    return response;
  } catch (error) {
    return NextResponse.json({ error: 'Server error' }, { status: 500 });
  }
}
