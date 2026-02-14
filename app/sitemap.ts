import { MetadataRoute } from 'next'
import { supabaseServer } from '@/lib/supabase/server'
import { createDesignSlug } from '@/lib/slug'
import { Database } from '@/types/database'
import { pillarTopics } from '@/lib/pillars'

export const revalidate = 60 * 60 // refresh hourly

type DesignRow = Pick<Database['public']['Tables']['designs']['Row'], 'id' | 'title' | 'slug' | 'updated_at'>
type BlogRow = Pick<Database['public']['Tables']['posts']['Row'], 'slug' | 'published_at'>

const COLLECTION_SLUGS = ['best-saas-landing-pages', 'minimalist-dashboards']
const STATIC_PATHS = ['/', '/blog', '/about', '/faq', '/contact', '/privacy-policy', '/terms', '/playbooks', '/collections', '/code-match']
const CHANGE_FREQUENCY_OVERRIDES: Record<string, MetadataRoute.Sitemap[number]['changeFrequency']> = {
  '/blog': 'weekly',
  '/playbooks': 'weekly',
  '/collections': 'weekly',
}
const PRIORITY_OVERRIDES: Record<string, number> = {
  '/blog': 0.7,
  '/playbooks': 0.7,
  '/collections': 0.7,
  '/code-match': 0.5,
}

export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const baseUrl = (process.env.NEXT_PUBLIC_SITE_URL || 'https://ui-syntax.com').replace(/\/$/, '')
  const now = new Date()
  const freshnessCutoffMs = 1000 * 60 * 60 * 24 * 30 // 30일

  const [designRes, postRes] = await Promise.all([
    supabaseServer
      .from('designs')
      .select('id, title, slug, updated_at')
      .eq('status', 'published')
      .order('updated_at', { ascending: false }),
    supabaseServer
      .from('posts')
      .select('slug, published_at')
      .eq('status', 'published')
      .order('published_at', { ascending: false }),
  ])
  const designs = designRes.data
  const posts = (postRes.data as BlogRow[] | null) ?? null

  const baseEntries: MetadataRoute.Sitemap = STATIC_PATHS.map((path) => ({
    url: `${baseUrl}${path === '/' ? '' : path}`,
    lastModified: now,
    changeFrequency: CHANGE_FREQUENCY_OVERRIDES[path] ?? (path === '/' ? 'daily' : 'monthly'),
    priority: PRIORITY_OVERRIDES[path] ?? (path === '/' ? 1 : 0.6),
  }))

  baseEntries.push({
    url: `${baseUrl}/feed.xml`,
    lastModified: now,
    changeFrequency: 'hourly',
    priority: 0.9,
  })

  const collectionEntries: MetadataRoute.Sitemap = COLLECTION_SLUGS.map((slug) => ({
    url: `${baseUrl}/collections/${slug}`,
    lastModified: now,
    changeFrequency: 'weekly',
    priority: 0.75,
  }))

  const playbookEntries: MetadataRoute.Sitemap = pillarTopics.map((topic) => ({
    url: `${baseUrl}/playbooks/${topic.slug}`,
    lastModified: now,
    changeFrequency: 'weekly' as const,
    priority: 0.7,
  }))

  const blogEntries: MetadataRoute.Sitemap = (posts ?? []).map((post) => {
    const publishedAt = post.published_at ? new Date(post.published_at) : now
    const isFresh = now.getTime() - publishedAt.getTime() < freshnessCutoffMs
    return {
      url: `${baseUrl}/blog/${post.slug}`,
      lastModified: publishedAt,
      changeFrequency: isFresh ? 'weekly' : 'monthly',
      priority: isFresh ? 0.65 : 0.5,
    }
  })

  const designEntries: MetadataRoute.Sitemap = (designs ?? []).map((design: DesignRow, index) => {
    const lastModified = design.updated_at ? new Date(design.updated_at) : now
    const isFresh = now.getTime() - lastModified.getTime() < freshnessCutoffMs
    const partitionPriority = index < 200 ? 0.85 : 0.6
    const partitionFrequency = isFresh ? 'weekly' : 'monthly'

    return {
      url: `${baseUrl}/design/${design.slug || createDesignSlug(design.title, design.id)}`,
      lastModified,
      changeFrequency: partitionFrequency,
      priority: partitionPriority,
    }
  })

  return [...baseEntries, ...collectionEntries, ...playbookEntries, ...blogEntries, ...designEntries]
}
