'use client';

import { useState, useEffect } from 'react';
import { supabase } from '@/lib/supabase/client';
import { Design } from '@/types/database';
import DesignCard from '@/components/DesignCard';
import DesignModal from '@/components/DesignModal';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

const ITEMS_PER_PAGE = 12;

export default function HomePage() {
  const [designs, setDesigns] = useState<Design[]>([]);
  const [loading, setLoading] = useState(true);
  const [hasMore, setHasMore] = useState(true);
  const [page, setPage] = useState(0);
  const [selectedDesign, setSelectedDesign] = useState<Design | null>(null);
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null);

  const loadDesigns = async (pageNum: number, category: string | null = null) => {
    setLoading(true);
    try {
      let query = supabase
        .from('designs')
        .select('*')
        .order('created_at', { ascending: false })
        .range(pageNum * ITEMS_PER_PAGE, (pageNum + 1) * ITEMS_PER_PAGE - 1);

      if (category) {
        query = query.eq('category', category);
      }

      const { data, error } = await query;

      if (error) throw error;

      if (data) {
        if (pageNum === 0) {
          setDesigns(data);
        } else {
          setDesigns((prev) => [...prev, ...data]);
        }
        setHasMore(data.length === ITEMS_PER_PAGE);
      }
    } catch (error) {
      console.error('Error loading designs:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDesigns(0, selectedCategory);
  }, [selectedCategory]);

  const loadMore = () => {
    const nextPage = page + 1;
    setPage(nextPage);
    loadDesigns(nextPage, selectedCategory);
  };

  const handleCategoryChange = (category: string | null) => {
    setSelectedCategory(category);
    setPage(0);
    setDesigns([]);
  };

  return (
    <div className="min-h-screen bg-luxury-white">
      <Header 
        selectedCategory={selectedCategory}
        onCategoryChange={handleCategoryChange}
      />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        {loading && designs.length === 0 ? (
          <div className="flex justify-center items-center h-96">
            <div className="relative">
              <div className="w-16 h-16 border-2 border-gray-200 rounded-full"></div>
              <div className="w-16 h-16 border-2 border-black border-t-transparent rounded-full animate-spin absolute top-0"></div>
            </div>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 animate-fade-in">
              {designs.map((design, index) => (
                <div 
                  key={design.id}
                  className="animate-slide-up"
                  style={{ animationDelay: `${index * 0.05}s` }}
                >
                  <DesignCard
                    design={design}
                    onClick={() => setSelectedDesign(design)}
                  />
                </div>
              ))}
            </div>

            {designs.length === 0 && !loading && (
              <div className="text-center py-20">
                <p className="text-gray-400 text-lg font-light tracking-wide">No designs uploaded yet.</p>
                <p className="text-gray-500 text-sm mt-2 font-light">Check back soon for new creations.</p>
              </div>
            )}

            {hasMore && designs.length > 0 && (
              <div className="flex justify-center mt-16">
                <button
                  onClick={loadMore}
                  disabled={loading}
                  className="px-10 py-3 bg-black text-white text-sm tracking-widest uppercase font-light hover:bg-gray-900 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 border border-black hover:shadow-lg"
                >
                  {loading ? 'Loading...' : 'Load More'}
                </button>
              </div>
            )}
          </>
        )}
      </main>

      {selectedDesign && (
        <DesignModal
          design={selectedDesign}
          onClose={() => setSelectedDesign(null)}
        />
      )}
      
      <Footer />
    </div>
  );
}
