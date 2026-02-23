"use client";

import Link from 'next/link';
import { useEffect, useMemo, useState } from 'react';
import DesignCard from '@/components/DesignCard';
import { supabase } from '@/lib/supabase/client';
import { withDesignSlugs } from '@/lib/slug';
import type { Design, DesignWithSlug } from '@/types/database';

const STORAGE_KEY = 'saved_design_ids';

function readSavedIds(): string[] {
  if (typeof window === 'undefined') return [];
  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) return [];
    const parsed = JSON.parse(stored) as string[];
    return Array.isArray(parsed) ? parsed : [];
  } catch (error) {
    console.warn('Failed to read saved designs', error);
    return [];
  }
}

export default function SavedDesignsClient() {
  const [savedIds, setSavedIds] = useState<string[]>([]);
  const [designs, setDesigns] = useState<DesignWithSlug[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const ids = readSavedIds();
    setSavedIds(ids);
  }, []);

  useEffect(() => {
    let isMounted = true;

    const fetchSavedDesigns = async () => {
      if (savedIds.length === 0) {
        if (isMounted) {
          setDesigns([]);
          setLoading(false);
        }
        return;
      }

      setLoading(true);
      const { data, error } = await supabase
        .from('designs')
        .select('*')
        .in('id', savedIds)
        .eq('status', 'published');

      if (!isMounted) return;

      if (error || !data) {
        console.error('Failed to fetch saved designs', error);
        setDesigns([]);
        setLoading(false);
        return;
      }

      const withSlugs = withDesignSlugs(data as Design[]) as DesignWithSlug[];
      const designMap = new Map(withSlugs.map((design) => [design.id, design]));
      const ordered = savedIds
        .map((id) => designMap.get(id))
        .filter(Boolean) as DesignWithSlug[];

      setDesigns(ordered);
      setLoading(false);
    };

    fetchSavedDesigns();

    return () => {
      isMounted = false;
    };
  }, [savedIds]);

  const emptyState = useMemo(() => savedIds.length === 0, [savedIds.length]);

  if (loading) {
    return (
      <div className="rounded-3xl border border-gray-200 bg-white/90 p-8 space-y-4">
        <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Saved Queue</p>
        <p className="text-sm text-gray-700 leading-relaxed">
          Saved items are read from your browser storage. If this is your first visit, start by browsing the gallery
          and saving references you want to review later.
        </p>
        <div className="flex flex-wrap gap-3">
          <Link
            href="/"
            className="inline-flex items-center rounded-full border border-gray-900 bg-gray-900 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-white transition hover:bg-black"
          >
            Browse Designs
          </Link>
          <Link
            href="/collections"
            className="inline-flex items-center rounded-full border border-gray-300 bg-white px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-gray-700 transition hover:border-gray-900 hover:text-gray-900"
          >
            Explore Collections
          </Link>
        </div>
      </div>
    );
  }

  if (emptyState) {
    return (
      <div className="rounded-3xl border border-dashed border-gray-300 bg-white/90 p-8 space-y-4">
        <p className="text-sm text-gray-700 leading-relaxed">
          You have not saved any designs yet. Open any design and use Save to build a shortlist for reviews and
          handoffs.
        </p>
        <Link
          href="/"
          className="inline-flex items-center rounded-full border border-gray-900 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-gray-900 transition hover:bg-gray-900 hover:text-white"
        >
          Start Browsing
        </Link>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {designs.map((design) => (
          <DesignCard
            key={design.id}
            design={design}
            likes={design.likes ?? 0}
            liked={false}
            likeDisabled
          />
        ))}
      </div>
    </div>
  );
}
