import type { Metadata } from "next";
import { GoogleAnalytics } from '@next/third-parties/google';
import { Analytics } from '@vercel/analytics/next';
import { SpeedInsights } from '@vercel/speed-insights/next';
import CommandPalette from '@/components/CommandPalette';
import "./globals.css";

const siteUrl = 'https://www.ui-syntax.com';
const siteDescription = 'Base Syntax is a U.S.-based AI web design gallery for SaaS founders, product designers, and front-end engineers who need production-ready inspiration.';

export const metadata: Metadata = {
  metadataBase: new URL(siteUrl),
  applicationName: 'Base Syntax',
  category: 'technology',
  title: {
    default: 'Base Syntax - AI Web Design Inspiration for U.S. Product Teams',
    template: '%s | Base Syntax',
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
  authors: [{ name: 'Base Syntax' }],
  creator: 'Base Syntax',
  publisher: 'Base Syntax',
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
    title: 'Base Syntax - AI Web Design Inspiration for U.S. Product Teams',
    description: siteDescription,
    siteName: 'Base Syntax',
    images: [
      {
        url: `${siteUrl}/opengraph-image.png`,
        width: 1200,
        height: 630,
        alt: 'Base Syntax - AI Web Design Inspiration',
      },
    ],
  },
  twitter: {
    card: 'summary_large_image',
    title: 'Base Syntax - AI Web Design Inspiration for U.S. Product Teams',
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
    name: 'Base Syntax',
    url: siteUrl,
    description: siteDescription,
    inLanguage: 'en-US',
    publisher: {
      '@type': 'Organization',
      name: 'Base Syntax',
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
        <script 
          async 
          src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-2091277631590195"
          crossOrigin="anonymous"
        />
        <link 
          rel="alternate" 
          type="application/rss+xml" 
          title="Base Syntax RSS Feed" 
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
