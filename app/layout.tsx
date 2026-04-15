import type { Metadata } from "next";
import Script from "next/script";
import { GoogleAnalytics } from '@next/third-parties/google';
import { Analytics } from '@vercel/analytics/next';
import { SpeedInsights } from '@vercel/speed-insights/next';
import CommandPalette from '@/components/CommandPalette';
import "./globals.css";

const siteUrl = 'https://ui-syntax.com';
const siteDescription = 'Discover published AI web designs with copy-paste HTML and React code when available. Explore SaaS landing pages, dashboards, and e-commerce flows curated for product teams.';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  applicationName: 'UI Syntax',
  category: 'technology',
  title: {
    default: 'Published AI Web Designs with Copy-Paste Code | UI Syntax',
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
  verification: {
    google: process.env.GOOGLE_SITE_VERIFICATION || undefined,
  },
  openGraph: {
    type: 'website',
    locale: 'en_US',
    url: siteUrl,
    title: 'Published AI Web Designs with Copy-Paste Code',
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
    title: 'Published AI Web Designs with Copy-Paste Code',
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
        
        {/* Google Fonts with display=optional */}
        <link
          href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=optional"
          rel="stylesheet"
        />
        
        {/* Critical CSS - above-the-fold */}
        <style dangerouslySetInnerHTML={{ __html: `
          body{margin:0;font-family:'Inter',system-ui,-apple-system,sans-serif;-webkit-font-smoothing:antialiased}
          .min-h-screen{min-height:100vh}
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
        {children}
        <CommandPalette />
        <Analytics />
        <SpeedInsights />
      </body>
      <GoogleAnalytics gaId="G-VPZWQWHW6Y" />
    </html>
  );
}
