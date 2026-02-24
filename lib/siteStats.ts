import { cache } from 'react';
import { supabaseServer } from '@/lib/supabase/server';

export const getPublishedDesignCount = cache(async (): Promise<number> => {
  const { count, error } = await supabaseServer
    .from('designs')
    .select('id', { count: 'exact', head: true })
    .eq('status', 'published');

  if (error) {
    console.error('Failed to fetch published design count', error);
    return 0;
  }

  return count ?? 0;
});

export function getPublishedDesignLabel(count: number): string {
  if (count <= 0) {
    return 'published designs (growing weekly)';
  }
  return `${count.toLocaleString('en-US')} published designs (growing weekly)`;
}
