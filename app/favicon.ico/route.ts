import { NextResponse } from 'next/server';
import path from 'path';
import { promises as fs } from 'fs';

const ICON_PATH = path.join(process.cwd(), 'app', 'icon.png');

export async function GET() {
  try {
    const icon = await fs.readFile(ICON_PATH);
    return new NextResponse(icon, {
      status: 200,
      headers: {
        'Content-Type': 'image/png',
        'Cache-Control': 'public, max-age=31536000, immutable',
      },
    });
  } catch (error) {
    return NextResponse.json(
      { error: 'favicon not available' },
      { status: 500 }
    );
  }
}
