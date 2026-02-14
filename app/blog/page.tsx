import type { Metadata } from 'next';
import Link from 'next/link';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { supabaseServer } from '@/lib/supabase/server';
import type { Database } from '@/types/database';
import { createPageMetadata } from '@/lib/seo';
import { buildBlogItemListSchema } from '@/lib/structuredData';

export async function generateMetadata(): Promise<Metadata> {
  const { count } = await supabaseServer
    .from('posts')
    .select('id', { count: 'exact', head: true })
    .eq('status', 'published');

  const totalPosts = count ?? 0;
  const description = totalPosts > 0
    ? `Read ${totalPosts}+ engineering notes, UI breakdowns, and implementation guides curated by UI Syntax.`
    : 'Read engineering notes, UI breakdowns, and implementation guides curated by UI Syntax.';

  return createPageMetadata({
    title: 'UI Syntax Journal',
    description,
    path: '/blog',
  });
}

export const revalidate = 0;

const calculateReadingTime = (content: string) => {
  const words = content.trim().split(/\s+/).filter(Boolean).length;
  const minutes = Math.max(1, Math.ceil(words / 200));
  return `${minutes} min read`;
};

type BlogRow = Database['public']['Tables']['posts']['Row'];

export default async function BlogPage() {
  const { data: posts } = await supabaseServer
    .from('posts')
    .select('slug, title, excerpt, content, category, author, author_role, author_avatar_url, cover_image_url, tags, published_at, updated_at, status')
    .eq('status', 'published')
    .order('published_at', { ascending: false });

  const publishedPosts = (posts ?? []) as BlogRow[];
  const blogListSchema = buildBlogItemListSchema(publishedPosts);

  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <main className="relative overflow-hidden">
        {blogListSchema && (
          <script
            type="application/ld+json"
            dangerouslySetInnerHTML={{ __html: JSON.stringify(blogListSchema) }}
          />
        )}
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(10,10,10,0.08),_transparent_55%)]" aria-hidden />
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
          <section className="mb-16 space-y-5">
            <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Engineering Notes</p>
            <h1 className="text-4xl md:text-6xl font-display font-semibold text-gray-900 tracking-tight">
              UI Syntax Journal
            </h1>
            <p className="text-lg text-gray-600 max-w-3xl leading-relaxed">
              A focused, text-first space for product engineering teams. Essays, UI system
              breakdowns, and implementation notes that sit apart from the gallery.
            </p>
            <div className="flex flex-wrap items-center gap-4 text-xs uppercase tracking-[0.3em] text-gray-500">
              <span>Curated</span>
              <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
              <span>High-signal</span>
              <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
              <span>Engineering-led</span>
            </div>
          </section>

          <div className="space-y-6">
            {publishedPosts.length === 0 && (
              <div className="rounded-3xl border border-gray-200 bg-white/90 p-10 text-center shadow-[0_16px_40px_rgba(10,10,10,0.08)]">
                <p className="text-sm uppercase tracking-[0.3em] text-gray-500">No posts yet</p>
                <p className="mt-4 text-lg text-gray-600">
                  New engineering notes will appear here soon.
                </p>
              </div>
            )}
            {publishedPosts.map((post) => (
              <article
                key={post.slug}
                className="group overflow-hidden rounded-3xl border border-gray-200 bg-white/90 shadow-[0_16px_40px_rgba(10,10,10,0.08)] transition-transform duration-300 hover:-translate-y-1"
              >
                {post.cover_image_url && (
                  <div className="h-56 w-full overflow-hidden bg-gray-100">
                    <img
                      src={post.cover_image_url}
                      alt={post.title}
                      className="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                      loading="lazy"
                    />
                  </div>
                )}
                <div className="p-8">
                  <div className="flex flex-wrap items-center gap-3 text-[11px] uppercase tracking-[0.3em] text-gray-500">
                    <span>{post.category || 'General'}</span>
                    <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
                    <span>{post.published_at ? post.published_at.slice(0, 10) : 'Draft'}</span>
                    <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
                    <span>{calculateReadingTime(post.content)}</span>
                  </div>
                  <h2 className="mt-4 text-2xl md:text-3xl font-semibold text-gray-900 tracking-tight">
                    <Link
                      href={`/blog/${post.slug}`}
                      className="hover:text-gray-700 transition-colors"
                    >
                      {post.title}
                    </Link>
                  </h2>
                  <p className="mt-4 text-base text-gray-600 leading-relaxed max-w-3xl">
                    {post.excerpt || 'A new UI Syntax journal entry.'}
                  </p>
                  {post.tags && post.tags.length > 0 && (
                    <div className="mt-5 flex flex-wrap gap-2">
                      {post.tags.slice(0, 4).map((tag) => (
                        <span
                          key={tag}
                          className="rounded-full border border-gray-200 px-3 py-1 text-[11px] uppercase tracking-[0.25em] text-gray-500"
                        >
                          {tag}
                        </span>
                      ))}
                    </div>
                  )}
                  {(post.author || post.author_role) && (
                    <div className="mt-6 flex items-center gap-3">
                      {post.author_avatar_url ? (
                        <img
                          src={post.author_avatar_url}
                          alt={post.author || 'Author'}
                          className="h-10 w-10 rounded-full object-cover"
                          loading="lazy"
                        />
                      ) : (
                        <div className="h-10 w-10 rounded-full bg-gray-200" aria-hidden />
                      )}
                      <div>
                        <p className="text-xs uppercase tracking-[0.3em] text-gray-500">
                          {post.author || 'UI Syntax Studio'}
                        </p>
                        {post.author_role && (
                          <p className="text-xs text-gray-400">{post.author_role}</p>
                        )}
                      </div>
                    </div>
                  )}
                  <div className="mt-6">
                    <Link
                      href={`/blog/${post.slug}`}
                      className="inline-flex items-center gap-2 text-sm font-semibold text-gray-900 uppercase tracking-[0.3em]"
                    >
                      Read Article
                      <span className="text-lg" aria-hidden>
                        -&gt;
                      </span>
                    </Link>
                  </div>
                </div>
              </article>
            ))}
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
