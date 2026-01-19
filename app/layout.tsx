import type { Metadata } from "next";
import { GoogleAnalytics } from '@next/third-parties/google';
import { Analytics } from '@vercel/analytics/next';
import { SpeedInsights } from '@vercel/speed-insights/next';
import CommandPalette from '@/components/CommandPalette';
import "./globals.css";

const siteUrl = 'https://www.ui-syntax.com';
const siteDescription = 'UI Syntax is a Silicon Valley standard AI web design gallery for SaaS founders, product designers, and front-end engineers who need production-ready inspiration.';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  applicationName: 'UI Syntax',
  category: 'technology',
  title: {
    default: 'UI Syntax - Production-Ready AI Web Design Inspiration for Modern Teams',
    template: '%s | UI Syntax',
  },
  description: siteDescription,
  keywords: [
    'US web design inspiration',
    'AI design gallery',
    'SaaS landing page examples',
    'developer tools marketing site',
    'dashboard UI inspiration',
    'product design gallery',
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
    title: 'UI Syntax - Production-Ready AI Web Design Inspiration for Modern Teams',
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
    title: 'UI Syntax - Production-Ready AI Web Design Inspiration for Modern Teams',
    description: siteDescription,
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
        {/* Preconnect to Google Fonts - 성능 향상 */}
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        
        {/* Google Fonts with display=swap - CLS 방지 */}
        <link 
          href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=swap" 
          rel="stylesheet"
        />
        
        {/* AdSense - async로 차단 방지 */}
        <script 
          async 
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2091277631590195"
          crossOrigin="anonymous"
        />
        
        <link 
          rel="alternate" 
          type="application/rss+xml" 
          title="UI Syntax RSS Feed" 
          href="https://www.ui-syntax.com/feed.xml" 
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
