import type { Metadata } from 'next';
import Link from 'next/link';
import { notFound } from 'next/navigation';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import { supabaseServer } from '@/lib/supabase/server';
import type { Database } from '@/types/database';

const siteUrl = 'https://ui-syntax.com';

export const revalidate = 300;

type PageProps = {
  params: { slug: string };
};

export async function generateMetadata({ params }: PageProps): Promise<Metadata> {
  type BlogMetaRow = Pick<Database['public']['Tables']['posts']['Row'], 'slug' | 'title' | 'excerpt' | 'status'>;

  const { data: post } = (await supabaseServer
    .from('posts')
    .select('slug, title, excerpt, status')
    .eq('slug', params.slug)
    .eq('status', 'published')
    .maybeSingle()) as { data: BlogMetaRow | null };

  if (!post) {
    return {
      title: 'Post Not Found',
      robots: { index: false, follow: false },
    };
  }

  return {
    title: post.title,
    description: post.excerpt || 'UI Syntax journal entry.',
    alternates: {
      canonical: `${siteUrl}/blog/${post.slug}`,
    },
    openGraph: {
      title: post.title,
      description: post.excerpt || 'UI Syntax journal entry.',
      url: `${siteUrl}/blog/${post.slug}`,
      type: 'article',
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.excerpt || 'UI Syntax journal entry.',
    },
  };
}

const calculateReadingTime = (content: string) => {
  const words = content.trim().split(/\s+/).filter(Boolean).length;
  const minutes = Math.max(1, Math.ceil(words / 200));
  return `${minutes} min read`;
};

export default async function BlogPostPage({ params }: PageProps) {
  type BlogRow = Database['public']['Tables']['posts']['Row'];

  const { data: post } = (await supabaseServer
    .from('posts')
    .select('slug, title, excerpt, content, category, author, author_role, author_avatar_url, cover_image_url, tags, published_at, status')
    .eq('slug', params.slug)
    .eq('status', 'published')
    .maybeSingle()) as { data: BlogRow | null };

  if (!post) {
    notFound();
  }

  const readingTime = calculateReadingTime(post.content);

  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <main className="relative overflow-hidden">
        <div className="absolute inset-0 bg-[radial-gradient(circle_at_top,_rgba(10,10,10,0.08),_transparent_55%)]" aria-hidden />
        <div className="relative max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
          <div className="mb-10">
            <Link href="/blog" className="text-xs uppercase tracking-[0.3em] text-gray-500">
              Back to Blog
            </Link>
          </div>

          <header className="rounded-3xl border border-gray-200 bg-white/90 px-8 py-10 shadow-[0_24px_60px_rgba(10,10,10,0.1)]">
            {post.cover_image_url && (
              <div className="mb-8 overflow-hidden rounded-2xl bg-gray-100">
                <img
                  src={post.cover_image_url}
                  alt={post.title}
                  className="h-64 w-full object-cover"
                  loading="lazy"
                />
              </div>
            )}
            <div className="flex flex-wrap items-center gap-3 text-[11px] uppercase tracking-[0.3em] text-gray-500">
              <span>{post.category || 'General'}</span>
              <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
              <span>{post.published_at ? post.published_at.slice(0, 10) : 'Draft'}</span>
              <span className="h-1 w-1 rounded-full bg-gray-400" aria-hidden />
              <span>{readingTime}</span>
            </div>
            <h1 className="mt-4 text-3xl md:text-5xl font-display font-semibold text-gray-900 tracking-tight text-balance">
              {post.title}
            </h1>
            <div className="mt-6 flex flex-wrap items-center gap-4">
              <div className="flex items-center gap-3">
                {post.author_avatar_url ? (
                  <img
                    src={post.author_avatar_url}
                    alt={post.author || 'Author'}
                    className="h-12 w-12 rounded-full object-cover"
                    loading="lazy"
                  />
                ) : (
                  <div className="h-12 w-12 rounded-full bg-gray-200" aria-hidden />
                )}
                <div>
                  <p className="text-sm font-semibold text-gray-900">
                    {post.author || 'UI Syntax Studio'}
                  </p>
                  <p className="text-xs uppercase tracking-[0.3em] text-gray-500">
                    {post.author_role || 'Product Engineering'}
                  </p>
                </div>
              </div>
              {post.tags && post.tags.length > 0 && (
                <div className="flex flex-wrap gap-2">
                  {post.tags.slice(0, 6).map((tag) => (
                    <span
                      key={tag}
                      className="rounded-full border border-gray-200 px-3 py-1 text-[11px] uppercase tracking-[0.25em] text-gray-500"
                    >
                      {tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
            <p className="mt-5 text-lg text-gray-600 leading-relaxed max-w-3xl">
              {post.excerpt || 'A UI Syntax journal entry.'}
            </p>
          </header>

          <div className="mt-12 grid gap-12 lg:grid-cols-[minmax(0,1fr)_240px]">
            <article className="blog-body rounded-3xl border border-gray-200 bg-white/90 px-8 py-10 shadow-[0_20px_50px_rgba(10,10,10,0.08)]">
              <ReactMarkdown remarkPlugins={[remarkGfm]}>{post.content}</ReactMarkdown>
            </article>

            <aside className="hidden lg:block">
              <div className="sticky top-28 rounded-2xl border border-gray-200 bg-white/90 px-6 py-6 shadow-[0_16px_40px_rgba(10,10,10,0.08)]">
                <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Outline</p>
                <ul className="mt-4 space-y-3 text-sm text-gray-700">
                  {post.content
                    .split('\n')
                    .filter((line) => line.startsWith('## '))
                    .map((line) => line.replace(/^##\s+/, ''))
                    .slice(0, 10)
                    .map((heading) => (
                      <li key={heading} className="leading-relaxed">
                        {heading}
                      </li>
                    ))}
                </ul>
              </div>
            </aside>
          </div>
        </div>
      </main>

      <Footer />
    </div>
  );
}
