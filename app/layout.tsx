import type { Metadata } from "next";
import Script from "next/script";
import { GoogleAnalytics } from '@next/third-parties/google';
import { Analytics } from '@vercel/analytics/next';
import { SpeedInsights } from '@vercel/speed-insights/next';
import CommandPalette from '@/components/CommandPalette';
import "./globals.css";

const siteUrl = 'https://ui-syntax.com';
const siteDescription = 'Discover 700+ production-ready AI web designs with copy-paste HTML & React code. Save 20+ hours per project with proven SaaS landing pages, dashboards & e-commerce flows trusted by Silicon Valley teams.';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  applicationName: 'UI Syntax',
  category: 'technology',
  title: {
    default: '700+ Free AI Web Designs with Copy-Paste Code | UI Syntax',
    template: '%s | UI Syntax',
  },
  description: siteDescription,
  keywords: [
    'free web design inspiration',
    'AI design gallery',
    'SaaS landing page examples',
    'copy paste HTML code',
    'React component library',
    'dashboard UI inspiration',
    'product design gallery',
    'free UI templates',
  ],
  authors: [{ name: 'UI Syntax' }],
  creator: 'UI Syntax',
  publisher: 'UI Syntax',
  alternates: {
    canonical: siteUrl,
    languages: {
      'en-US': siteUrl,
    },
  },
  icons: {
    icon: [{ url: '/icon.png', type: 'image/png' }],
    shortcut: ['/icon.png'],
    apple: [{ url: '/icon.png', sizes: '180x180' }],
  },
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      'max-video-preview': -1,
      'max-image-preview': 'large',
      'max-snippet': -1,
    },
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: siteUrl,
    title: '700+ Free AI Web Designs with Copy-Paste Code',
    description: siteDescription,
    siteName: 'UI Syntax',
    images: [
      {
        url: `${siteUrl}/opengraph-image.png`,
        width: 1200,
        height: 630,
        alt: 'UI Syntax - AI Web Design Inspiration',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: '700+ Free AI Web Designs with Copy-Paste Code',
    description: siteDescription,
    creator: '@uisyntax',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const structuredData = {
    '@context': 'https://schema.org',
    '@type': 'WebSite',
    name: 'UI Syntax',
    url: siteUrl,
    description: siteDescription,
    inLanguage: 'en-US',
    publisher: {
      '@type': 'Organization',
      name: 'UI Syntax',
      logo: {
        '@type': 'ImageObject',
        url: `${siteUrl}/opengraph-image.png`,
      },
    },
    audience: {
      '@type': 'Audience',
      audienceType: 'Product designers and software engineers in the United States',
    },
    potentialAction: {
      '@type': 'SearchAction',
      target: `${siteUrl}/?category={category}`,
      'query-input': 'required name=category',
    },
  };

  return (
    <html lang="en">
      <head>
        {/* Privacy consent scripts must execute before any other trackers */}
        <Script
          data-cfasync="false"
          src="https://cmp.gatekeeperconsent.com/min.js"
          strategy="beforeInteractive"
        />
        <Script
          data-cfasync="false"
          src="https://the.gatekeeperconsent.com/cmp.min.js"
          strategy="beforeInteractive"
        />

        {/* Ezoic header bootstrap */}
        <Script
          src="//www.ezojs.com/ezoic/sa.min.js"
          strategy="beforeInteractive"
        />
        <Script id="ezstandalone-init" strategy="beforeInteractive">
          {`
            window.ezstandalone = window.ezstandalone || {};
            ezstandalone.cmd = ezstandalone.cmd || [];
          `}
        </Script>

        {/* DNS Prefetch & Preconnect - highest priority optimization */}
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://fonts.gstatic.com" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        
        {/* Preload Critical Fonts - improve LCP (Inter 600 for hero headings) */}
        <link 
          rel="preload" 
          href="https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiA.woff2" 
          as="font" 
          type="font/woff2" 
          crossOrigin="anonymous"
        />
        
        {/* Google Fonts with display=optional - more aggressive fallback */}
        <link 
          href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=optional" 
          rel="stylesheet"
        />
        
        {/* Critical CSS - optimize above-the-fold rendering */}
        <style dangerouslySetInnerHTML={{ __html: `
          body{margin:0;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}
          .min-h-screen{min-height:100vh}
          .bg-luxury-white{background-color:#fafafa}
          .text-4xl{font-size:2.25rem;line-height:2.5rem}
          .md\\:text-5xl{font-size:3rem;line-height:1}
          .font-semibold{font-weight:600}
          .text-gray-900{color:rgb(17 24 39)}
          .tracking-tight{letter-spacing:-0.025em}
          @media(min-width:768px){.md\\:text-5xl{font-size:3rem;line-height:1}}
        ` }} />
        
        {/* AdSense - keep async to avoid blocking */}
        <Script
          async
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2091277631590195"
          crossOrigin="anonymous"
          strategy="afterInteractive"
        />
        
        <link 
          rel="alternate" 
          type="application/rss+xml" 
          title="UI Syntax RSS Feed" 
          href="https://ui-syntax.com/feed.xml" 
        />
        
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(structuredData) }}
        />
      </head>
      <body>
        <div className="bg-black/95 text-[12px] uppercase tracking-[0.25em] text-gray-200 text-center py-2 px-4 border-b border-white/10">
          Every design detail page now includes both clean HTML and auto-generated React code for instant developer handoff.
        </div>
        {children}
        <CommandPalette />
        <Analytics />
        <SpeedInsights />
      </body>
      <GoogleAnalytics gaId="G-VPZWQWHW6Y" />
    </html>
  );
}
