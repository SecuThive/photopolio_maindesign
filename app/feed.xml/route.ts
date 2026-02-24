import RSS from 'rss';
import { createClient } from '@supabase/supabase-js';
import { createDesignSlug } from '@/lib/slug';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL!;
const supabaseKey = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY!;

export async function GET() {
  try {
    const supabase = createClient(supabaseUrl, supabaseKey);

    const { data: designs, error } = await supabase
      .from('designs')
      .select('*')
      .eq('status', 'published')
      .order('created_at', { ascending: false })
      .limit(50);

    if (error) {
      throw error;
    }

    const feed = new RSS({
      title: 'UI Syntax - AI Design Gallery',
      description: 'Latest AI-generated web designs including landing pages, dashboards, e-commerce sites, portfolios, and more.',
      site_url: 'https://ui-syntax.com',
      feed_url: 'https://ui-syntax.com/feed.xml',
      copyright: `${new Date().getFullYear()} UI Syntax`,
      language: 'en-US',
      pubDate: new Date(),
      ttl: 60,
    });

    designs?.forEach((design) => {
      feed.item({
        title: design.title,
        description: design.description || `${design.category} design - ${design.title}`,
        url: `https://ui-syntax.com/design/${createDesignSlug(design.title, design.id)}`,
        guid: design.id,
        categories: design.category ? [design.category] : [],
        date: new Date(design.created_at),
        enclosure: design.image_url ? {
          url: design.image_url,
          type: 'image/png',
        } : undefined,
      });
    });

    return new Response(feed.xml({ indent: true }), {
      status: 200,
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=0, must-revalidate',
      },
    });
  } catch (error) {
    console.error('feed.xml route error', error);
    const fallbackXml = `<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>UI Syntax - AI Design Gallery</title>
    <link>https://ui-syntax.com</link>
    <description>Latest AI-generated web designs.</description>
  </channel>
</rss>`;

    return new Response(fallbackXml, {
      status: 200,
      headers: {
        'Content-Type': 'application/xml; charset=utf-8',
        'Cache-Control': 'public, max-age=0, must-revalidate',
      },
    });
  }
}
