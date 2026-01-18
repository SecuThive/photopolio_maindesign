import { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: '*',
        allow: '/',
        disallow: ['/admin/', '/admin', '/api/admin/', '/api/'],
      },
    ],
    sitemap: 'https://www.ui-syntax.com/sitemap.xml',
  }
}
