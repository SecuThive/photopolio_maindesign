"use client";

import { useEffect, useState, useCallback } from 'react';
import { supabase } from '@/lib/supabase/client';
import { Design, DesignWithSlug } from '@/types/database';
import DesignCard from './DesignCard';
import { withDesignSlugs } from '@/lib/slug';

const ITEMS_PER_PAGE = 12;

const generateLikeToken = () => {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }

  if (typeof window !== 'undefined' && window.crypto?.getRandomValues) {
    const buffer = new Uint32Array(4);
    window.crypto.getRandomValues(buffer);
    return Array.from(buffer)
      .map((segment) => segment.toString(16).padStart(8, '0'))
      .join('');
  }

  return `token-${Date.now()}-${Math.random().toString(16).slice(2)}`;
};

interface DesignGalleryProps {
  initialDesigns: DesignWithSlug[];
  initialCategory: string | null;
}

export default function DesignGallery({ initialDesigns, initialCategory }: DesignGalleryProps) {
  const [designs, setDesigns] = useState<DesignWithSlug[]>(initialDesigns);
  const [page, setPage] = useState(1);
  const [hasMore, setHasMore] = useState(initialDesigns.length === ITEMS_PER_PAGE);
  const [loading, setLoading] = useState(false);
  const [isTransitioning, setIsTransitioning] = useState(true);
  const [activeCategory, setActiveCategory] = useState(initialCategory);
  const [likesMap, setLikesMap] = useState<Record<string, number>>(() => {
    const initialMap: Record<string, number> = {};
    initialDesigns.forEach((design) => {
      initialMap[design.id] = design.likes ?? 0;
    });
    return initialMap;
  });
  const [likeToken, setLikeToken] = useState<string | null>(null);
  const [likedIds, setLikedIds] = useState<Set<string>>(new Set());
  const [pendingLikes, setPendingLikes] = useState<Record<string, boolean>>({});

  useEffect(() => {
    setDesigns(initialDesigns);
    setPage(1);
    setHasMore(initialDesigns.length === ITEMS_PER_PAGE);
    setActiveCategory(initialCategory);
    setLikesMap(() => {
      const next: Record<string, number> = {};
      initialDesigns.forEach((design) => {
        next[design.id] = design.likes ?? 0;
      });
      return next;
    });
    setIsTransitioning(true);
    const timeout = setTimeout(() => {
      setIsTransitioning(false);
    }, 360);
    return () => clearTimeout(timeout);
  }, [initialDesigns, initialCategory]);


  useEffect(() => {
    if (typeof window === 'undefined') return;

    const ensureToken = () => {
      const fallbackToken = generateLikeToken();

      if (typeof window === 'undefined') {
        setLikeToken(fallbackToken);
        return;
      }

      try {
        const storedToken = localStorage.getItem('design_like_token');
        if (storedToken) {
          setLikeToken(storedToken);
          return;
        }
      } catch (error) {
        console.warn('Unable to read like token from storage', error);
      }

      try {
        localStorage.setItem('design_like_token', fallbackToken);
      } catch (error) {
        console.warn('Unable to persist like token, using in-memory fallback', error);
      }

      setLikeToken(fallbackToken);
    };

    const loadLikedDesigns = () => {
      if (typeof window === 'undefined') {
        return;
      }

      try {
        const storedIds = localStorage.getItem('liked_design_ids');
        if (storedIds) {
          const parsed: string[] = JSON.parse(storedIds);
          setLikedIds(new Set(parsed));
        }
      } catch (error) {
        console.warn('Failed to parse liked design ids', error);
      }
    };

    ensureToken();
    loadLikedDesigns();
  }, []);

  const persistLikedIds = useCallback((ids: Set<string>) => {
    if (typeof window === 'undefined') return;
    try {
      localStorage.setItem('liked_design_ids', JSON.stringify(Array.from(ids)));
    } catch (error) {
      console.warn('Failed to persist liked ids', error);
    }
  }, []);

  const loadMore = async () => {
    setLoading(true);
    try {
      const from = page * ITEMS_PER_PAGE;
      const to = (page + 1) * ITEMS_PER_PAGE - 1;

      let query = supabase
        .from('designs')
        .select('*')
        .eq('status', 'published')
        .order('created_at', { ascending: false })
        .range(from, to);

      if (activeCategory) {
        query = query.eq('category', activeCategory);
      }

      const { data, error } = await query;

      if (error) throw error;

      if (data) {
        const fetchedDesigns = withDesignSlugs(data as Design[]);
        setDesigns((prev) => [...prev, ...fetchedDesigns]);
        setHasMore(fetchedDesigns.length === ITEMS_PER_PAGE);
        setPage((prev) => prev + 1);
        setLikesMap((prev) => {
          const next = { ...prev };
          fetchedDesigns.forEach((design) => {
            if (next[design.id] === undefined) {
              next[design.id] = design.likes ?? 0;
            }
          });
          return next;
        });
      }
    } catch (error) {
      console.error('Error loading designs:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleToggleLike = async (designId: string) => {
    if (!likeToken) return;

    const currentlyLiked = likedIds.has(designId);
    setPendingLikes((prev) => ({ ...prev, [designId]: true }));

    setLikesMap((prev) => ({
      ...prev,
      [designId]: Math.max(0, (prev[designId] ?? 0) + (currentlyLiked ? -1 : 1)),
    }));

    setLikedIds((prev) => {
      const next = new Set(prev);
      if (currentlyLiked) {
        next.delete(designId);
      } else {
        next.add(designId);
      }
      persistLikedIds(next);
      return next;
    });

    try {
      const response = await fetch(`/api/designs/${designId}/like`, {
        method: currentlyLiked ? 'DELETE' : 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: likeToken }),
      });

      if (!response.ok) {
        throw new Error('Failed to update like');
      }

      const payload = await response.json();
      if (typeof payload.likes === 'number') {
        setLikesMap((prev) => ({ ...prev, [designId]: payload.likes }));
      }
    } catch (error) {
      console.error('Like toggle failed', error);
      setLikesMap((prev) => ({
        ...prev,
        [designId]: Math.max(0, (prev[designId] ?? 0) + (currentlyLiked ? 1 : -1)),
      }));

      setLikedIds((prev) => {
        const next = new Set(prev);
        if (currentlyLiked) {
          next.add(designId);
        } else {
          next.delete(designId);
        }
        persistLikedIds(next);
        return next;
      });
    } finally {
      setPendingLikes((prev) => {
        const next = { ...prev };
        delete next[designId];
        return next;
      });
    }
  };

  return (
    <>
      <div className="relative">
        <div
          className={`grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 animate-fade-in transition-all duration-500 ${
            isTransitioning ? 'opacity-30 blur-[1px] translate-y-2' : 'opacity-100 blur-0 translate-y-0'
          }`}
          aria-live="polite"
        >
          {designs.map((design, index) => (
            <div
              key={design.id}
              className="animate-slide-up"
              style={{ animationDelay: `${index * 0.05}s` }}
            >
              <DesignCard
                design={design}
                likes={likesMap[design.id] ?? design.likes ?? 0}
                liked={likedIds.has(design.id)}
                onToggleLike={() => handleToggleLike(design.id)}
                likeDisabled={!likeToken || !!pendingLikes[design.id]}
              />
            </div>
          ))}
        </div>

        {isTransitioning && (
          <div className="pointer-events-none absolute inset-0 flex items-center justify-center">
            <div className="flex items-center gap-3 rounded-full bg-white/80 px-6 py-3 text-xs font-semibold tracking-[0.35em] text-gray-600 shadow-xl backdrop-blur">
              <span className="inline-flex h-8 w-8 items-center justify-center rounded-full border-2 border-gray-300 border-t-gray-900 animate-spin" aria-hidden />
              Refreshing gallery
            </div>
          </div>
        )}
      </div>

      {loading && (
        <div className="mt-10 grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8" aria-hidden>
          {Array.from({ length: 4 }).map((_, index) => (
            <div
              key={`skeleton-${index}`}
              className="h-72 rounded-[28px] border border-gray-200 bg-gradient-to-b from-gray-100 to-gray-200 animate-pulse"
            />
          ))}
        </div>
      )}

      {designs.length === 0 && !isTransitioning && (
        <div className="text-center py-20">
          <p className="text-gray-400 text-lg font-light tracking-wide">No designs uploaded yet.</p>
        </div>
      )}

      {hasMore && (
        <div className="flex justify-center mt-16">
          <button
            onClick={loadMore}
            disabled={loading}
            className="flex items-center gap-3 px-10 py-3 bg-black text-white text-sm tracking-widest uppercase font-light hover:bg-gray-900 transition-all duration-300 border border-black hover:shadow-lg disabled:opacity-50"
          >
            {loading ? (
              <>
                <span className="h-4 w-4 rounded-full border border-white/30 border-t-white animate-spin" aria-hidden />
                Loading
              </>
            ) : (
              'Load More'
            )}
          </button>
        </div>
      )}
    </>
  );
}
