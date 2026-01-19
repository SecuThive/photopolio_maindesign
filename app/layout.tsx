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
        {/* DNS Prefetch & Preconnect - 최우선 최적화 */}
        <link rel="dns-prefetch" href="https://fonts.googleapis.com" />
        <link rel="dns-prefetch" href="https://fonts.gstatic.com" />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        
        {/* Preload Critical Fonts - LCP 개선 (h1용 Inter 600) */}
        <link 
          rel="preload" 
          href="https://fonts.gstatic.com/s/inter/v13/UcCO3FwrK3iLTeHuS_fvQtMwCp50KnMw2boKoduKmMEVuLyfAZ9hiA.woff2" 
          as="font" 
          type="font/woff2" 
          crossOrigin="anonymous"
        />
        
        {/* Google Fonts with display=optional - 더 적극적인 폴백 */}
        <link 
          href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;500;600;700&family=Inter:wght@300;400;500;600;700&display=optional" 
          rel="stylesheet"
        />
        
        {/* Critical CSS - 첫 화면 렌더링 최적화 */}
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
