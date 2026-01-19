import type { Metadata } from "next";
import { GoogleAnalytics } from '@next/third-parties/google';
import CommandPalette from '@/components/CommandPalette';
import "./globals.css";

export const metadata: Metadata = {
  metadataBase: new URL('https://www.ui-syntax.com'),
  title: {
    default: "Base Syntax - AI Design Gallery",
    template: "%s | Base Syntax"
  },
  description: "Discover stunning AI-generated web designs. Browse our curated gallery of landing pages, dashboards, e-commerce sites, portfolios, and more. Get inspired for your next project.",
  keywords: ["AI design", "web design", "UI design", "UX design", "design gallery", "landing page", "dashboard design", "e-commerce design", "portfolio design", "AI generated", "design inspiration"],
  authors: [{ name: "Base Syntax" }],
  creator: "Base Syntax",
  publisher: "Base Syntax",
  alternates: {
    canonical: 'https://www.ui-syntax.com',
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
    locale: 'ko_KR',
    url: 'https://www.ui-syntax.com',
    title: "Base Syntax - AI Design Gallery",
    description: "Discover stunning AI-generated web designs. Browse our curated gallery of landing pages, dashboards, e-commerce sites, portfolios, and more.",
    siteName: 'Base Syntax',
  },
  twitter: {
    card: 'summary_large_image',
    title: "Base Syntax - AI Design Gallery",
    description: "Discover stunning AI-generated web designs. Browse our curated gallery of landing pages, dashboards, e-commerce sites, portfolios, and more.",
  },
  verification: {
    google: 'your-google-verification-code',
  },
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="ko">
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
      </head>
      <body>
        {children}
        <CommandPalette />
      </body>
      <GoogleAnalytics gaId="G-VPZWQWHW6Y" />
    </html>
  );
}
