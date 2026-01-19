import { ImageResponse } from 'next/og'

export const runtime = 'edge'

export const alt = 'UI Syntax - AI Design Gallery'
export const size = {
  width: 1200,
  height: 630,
}

export const contentType = 'image/png'

export default async function Image() {
  return new ImageResponse(
    (
      <div
        style={{
          fontSize: 128,
          background: 'black',
          width: '100%',
          height: '100%',
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          justifyContent: 'center',
          color: 'white',
        }}
      >
        <div
          style={{
            fontSize: 80,
            fontWeight: 700,
            letterSpacing: '-0.05em',
            marginBottom: 20,
          }}
        >
          UI SYNTAX
        </div>
        <div
          style={{
            fontSize: 32,
            color: '#999',
            letterSpacing: '0.1em',
            textTransform: 'uppercase',
          }}
        >
          AI Design Gallery
        </div>
        <div
          style={{
            position: 'absolute',
            bottom: 40,
            fontSize: 24,
            color: '#666',
          }}
        >
          www.ui-syntax.com
        </div>
      </div>
    ),
    {
      ...size,
    }
  )
}
