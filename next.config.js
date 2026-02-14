/** @type {import('next').NextConfig} */
const legacyBlogRedirects = [
  '/2026/01/accordion-with-vanilla-js-full-code.html',
  '/2026/01/elevating-saas-modern-dark-mode-ui-with.html',
  '/2026/01/mastering-minimalist-luxury-editorial.html',
  '/2026/01/modal-with-vanilla-js-full-code.html',
  '/2026/01/modern-split-screen-portfolio-bold.html',
  '/2026/01/next-gen-fintech-ui-blending.html',
  '/2026/01/top-5-adaptive-modal-popup-visuals-for.html',
  '/2026/01/top-5-augmented-input-form-visuals-for.html',
  '/2026/01/top-5-context-aware-navigation-bar.html',
  '/2026/01/top-5-cutting-edge-modal-popup-visuals.html',
];

const nextConfig = {
  compiler: {
    // 최신 브라우저 타겟팅 - 레거시 폴리필 제거
    reactRemoveProperties: process.env.NODE_ENV === 'production',
  },
  // 최신 브라우저만 지원 (ES2020+)
  swcMinify: true,
  images: {
    unoptimized: true,
    remotePatterns: [
      {
        protocol: 'https',
        hostname: '**.supabase.co',
      },
    ],
  },
  async redirects() {
    return [
      {
        source: '/:path*',
        has: [
          {
            type: 'host',
            value: 'www.ui-syntax.com',
          },
        ],
        destination: 'https://ui-syntax.com/:path*',
        permanent: true,
      },
      ...legacyBlogRedirects.map((source) => ({
        source,
        destination: '/',
        permanent: true,
      })),
    ];
  },
};

module.exports = nextConfig;
