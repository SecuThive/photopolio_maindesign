"use client";

import { useEffect, useState } from 'react';
import { supabase } from '@/lib/supabase/client';
import { Design } from '@/types/database';
import DesignCard from './DesignCard';
import DesignModal from './DesignModal';

const ITEMS_PER_PAGE = 12;

interface DesignGalleryProps {
  initialDesigns: Design[];
  initialCategory: string | null;
}

export default function DesignGallery({ initialDesigns, initialCategory }: DesignGalleryProps) {
  const [designs, setDesigns] = useState<Design[]>(initialDesigns);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(initialDesigns.length === ITEMS_PER_PAGE);
  const [loading, setLoading] = useState(false);
  const [selectedDesign, setSelectedDesign] = useState<Design | null>(null);
  const [activeCategory, setActiveCategory] = useState(initialCategory);

  useEffect(() => {
    setDesigns(initialDesigns);
    setPage(1);
    setHasMore(initialDesigns.length === ITEMS_PER_PAGE);
    setActiveCategory(initialCategory);
  }, [initialDesigns, initialCategory]);

  useEffect(() => {
    const recordView = async () => {
      try {
        await fetch('/api/metrics/track', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ page: window.location.pathname }),
        });
      } catch (error) {
        console.error('Failed to record page view', error);
      }
    };

    recordView();
  }, []);

  const loadMore = async () => {
    setLoading(true);
    try {
      const from = page * ITEMS_PER_PAGE;
      const to = (page + 1) * ITEMS_PER_PAGE - 1;

      let query = supabase
        .from('designs')
        .select('*')
        .order('created_at', { ascending: false })
        .range(from, to);

      if (activeCategory) {
        query = query.eq('category', activeCategory);
      }

      const { data, error } = await query;

      if (error) throw error;

      if (data) {
        setDesigns((prev) => [...prev, ...data]);
        setHasMore(data.length === ITEMS_PER_PAGE);
        setPage((prev) => prev + 1);
      }
    } catch (error) {
      console.error('Error loading designs:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 animate-fade-in">
        {designs.map((design, index) => (
          <div
            key={design.id}
            className="animate-slide-up"
            style={{ animationDelay: `${index * 0.05}s` }}
          >
            <DesignCard design={design} onClick={() => setSelectedDesign(design)} />
          </div>
        ))}
      </div>
      {designs.length === 0 && (
        <div className="text-center py-20">
          <p className="text-gray-400 text-lg font-light tracking-wide">No designs uploaded yet.</p>
        </div>
      )}

      {hasMore && (
        <div className="flex justify-center mt-16">
          <button
            onClick={loadMore}
            disabled={loading}
            className="px-10 py-3 bg-black text-white text-sm tracking-widest uppercase font-light hover:bg-gray-900 transition-all duration-300 border border-black hover:shadow-lg disabled:opacity-50"
          >
            {loading ? 'Loading...' : 'Load More'}
          </button>
        </div>
      )}

      {selectedDesign && (
        <DesignModal design={selectedDesign} onClose={() => setSelectedDesign(null)} />
      )}
    </>
  );
}
