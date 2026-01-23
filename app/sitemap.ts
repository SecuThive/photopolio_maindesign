import { MetadataRoute } from 'next'
import { createClient } from '@supabase/supabase-js'
import { createDesignSlug } from '@/lib/slug'

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = 'https://www.ui-syntax.com'
  const supabase = createClient(supabaseUrl, supabaseKey)

  // Fetch all designs from Supabase
  const { data: designs } = await supabase
    .from('designs')
    .select('id, title, created_at, category')
    .order('created_at', { ascending: false })

  // Static pages
  const staticPages: MetadataRoute.Sitemap = [
    {
      url: baseUrl,
      lastModified: new Date(),
      changeFrequency: 'daily',
      priority: 1,
    },
    {
      url: `${baseUrl}/feed.xml`,
      lastModified: new Date(),
      changeFrequency: 'hourly',
      priority: 0.9,
    },
    {
      url: `${baseUrl}/about`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/privacy-policy`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/terms`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/contact`,
      lastModified: new Date(),
      changeFrequency: 'monthly',
      priority: 0.5,
    },
    {
      url: `${baseUrl}/collections/best-saas-landing-pages`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
    {
      url: `${baseUrl}/collections/minimalist-dashboards`,
      lastModified: new Date(),
      changeFrequency: 'weekly',
      priority: 0.8,
    },
  ]

  // Dynamic design pages
  const designPages: MetadataRoute.Sitemap = designs?.map((design) => ({
    url: `${baseUrl}/design/${createDesignSlug(design.title, design.id)}`,
    lastModified: new Date(design.created_at),
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  })) || []

  // Combine static and dynamic pages
  return [...staticPages, ...designPages]
}
