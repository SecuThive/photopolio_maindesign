import { supabaseServer } from '@/lib/supabase/server';
import DesignGallery from '@/components/DesignGallery';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default async function HomePage({
  searchParams,
}: {
  searchParams: { category?: string };
}) {
  const category = searchParams?.category;

  let query = supabaseServer
    .from('designs')
    .select('*')
    .order('created_at', { ascending: false })
    .range(0, 11);

  if (category) {
    query = query.eq('category', category);
  }

  const { data: initialDesigns } = await query;

  return (
    <div className="min-h-screen bg-luxury-white">
      <Header selectedCategory={category || null} />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <DesignGallery initialDesigns={initialDesigns || []} initialCategory={category || null} />
      </main>

      <Footer />
    </div>
  );
}
