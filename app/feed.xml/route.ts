import RSS from 'rss';
import { createClient } from '@supabase/supabase-js';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export async function GET() {
  const supabase = createClient(supabaseUrl, supabaseKey);

  // Get latest 50 designs from Supabase
  const { data: designs, error } = await supabase
    .from('designs')
    .select('*')
    .order('created_at', { ascending: false })
    .limit(50);

  if (error) {
    console.error('Error fetching designs:', error);
    return new Response('Error generating feed', { status: 500 });
  }

  const feed = new RSS({
    title: 'Base Syntax - AI Design Gallery',
    description: 'Latest AI-generated web designs including landing pages, dashboards, e-commerce sites, portfolios, and more.',
    site_url: 'https://www.ui-syntax.com',
    feed_url: 'https://www.ui-syntax.com/feed.xml',
    copyright: `${new Date().getFullYear()} Base Syntax`,
    language: 'ko',
    pubDate: new Date(),
    ttl: 60, // Cache for 60 minutes
  });

  // Add each design to the feed
  designs?.forEach((design) => {
    feed.item({
      title: design.title,
      description: design.description || `${design.category} design - ${design.title}`,
      url: `https://www.ui-syntax.com/?design=${design.id}`,
      guid: design.id,
      categories: [design.category],
      date: new Date(design.created_at),
      enclosure: design.image_url ? {
        url: design.image_url,
        type: 'image/png',
      } : undefined,
      custom_elements: [
        { 'design:category': design.category },
        { 'design:style': design.style || 'modern' },
      ],
    });
  });

  return new Response(feed.xml({ indent: true }), {
    headers: {
      'Content-Type': 'application/xml; charset=utf-8',
      'Cache-Control': 'public, max-age=3600', // Cache for 1 hour
    },
  });
}
