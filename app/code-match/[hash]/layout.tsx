import type { Metadata } from 'next';

const ENABLE_GROWTH_SAFE_SEO_FIXES = process.env.ENABLE_GROWTH_SAFE_SEO_FIXES === 'true';

export const metadata: Metadata = {
  robots: ENABLE_GROWTH_SAFE_SEO_FIXES
    ? {
        index: false,
        follow: true,
      }
    : {
        index: true,
        follow: true,
      },
};

export default function CodeMatchHashLayout({ children }: { children: React.ReactNode }) {
  return children;
}
