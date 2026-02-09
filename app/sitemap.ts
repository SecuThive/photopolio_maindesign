import { MetadataRoute } from 'next'
import { supabaseServer } from '@/lib/supabase/server'
import { createDesignSlug } from '@/lib/slug'

export const revalidate = 0

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '')

  const { data: designs } = await supabaseServer
    .from('designs')
    .select('id, title, slug, updated_at')
    .eq('status', 'published')
    .order('updated_at', { ascending: false })

  const now = new Date()

  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: now,
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: `${baseUrl}/feed.xml`,
      lastModified: now,
      changeFrequency: 'hourly',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/blog`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/privacy-policy`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/terms`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/contact`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/faq`,
      lastModified: now,
      changeFrequency: 'monthly',
      priority: 0.7,
    },
    {
      url: `${baseUrl}/collections/best-saas-landing-pages`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/collections/minimalist-dashboards`,
      lastModified: now,
      changeFrequency: 'weekly',
      priority: 0.8,
    },
  ]

  const designPages: MetadataRoute.Sitemap = (designs || []).map((design) => ({
    url: `${baseUrl}/design/${design.slug || createDesignSlug(design.title, design.id)}`,
    lastModified: design.updated_at ? new Date(design.updated_at) : now,
    changeFrequency: 'daily' as const,
    priority: 0.8,
  }))

  return [...staticPages, ...designPages]
}
