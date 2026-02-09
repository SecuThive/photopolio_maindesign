"use client";

import { useEffect, useState, useTransition } from 'react';
import { useRouter } from 'next/navigation';

const categories = [
  { value: null, label: 'All' },
  { value: 'Landing Page', label: 'Landing Page' },
  { value: 'Dashboard', label: 'Dashboard' },
  { value: 'E-commerce', label: 'E-commerce' },
  { value: 'Portfolio', label: 'Portfolio' },
  { value: 'Blog', label: 'Blog' },
  { value: 'Components', label: 'Components' },
];

interface CategoryFilterBarProps {
  selectedCategory: string | null;
}

export default function CategoryFilterBar({ selectedCategory }: CategoryFilterBarProps) {
  const router = useRouter();
  const [optimisticCategory, setOptimisticCategory] = useState<string | null>(selectedCategory ?? null);
  const [isPending, startTransition] = useTransition();

  useEffect(() => {
    setOptimisticCategory(selectedCategory ?? null);
  }, [selectedCategory]);

  const navigateToCategory = (value: string | null) => {
    const href = value ? `/?category=${encodeURIComponent(value)}` : '/';
    setOptimisticCategory(value);
    startTransition(() => {
      router.push(href, { scroll: false });
    });
  };

  return (
    <div className="sticky top-16 md:top-20 z-30 border-y border-gray-200 bg-white/90 backdrop-blur-md">
      {isPending && <div className="h-1 w-full bg-gradient-to-r from-gray-900 via-gray-600 to-gray-900 animate-[pulse_1.4s_ease-in-out_infinite]" aria-hidden />}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
        <div className="text-[11px] uppercase tracking-[0.35em] text-gray-400 mb-3 flex items-center gap-3">
          <span>Filter</span>
          <span className="h-px flex-1 bg-gray-200" aria-hidden />
        </div>
        <div className="flex items-center gap-2 overflow-x-auto scrollbar-hide">
          {categories.map((category) => {
            const isActive = optimisticCategory === category.value;
            return (
              <button
                key={category.value || 'all'}
                type="button"
                onClick={() => navigateToCategory(category.value)}
                className={`rounded-full border px-4 py-2 text-xs font-medium tracking-wide transition-all duration-300 ${
                  isActive
                    ? 'border-black bg-black text-white shadow-sm'
                    : 'border-gray-200 bg-white text-gray-500 hover:text-black hover:border-black'
                } ${isPending && isActive ? 'opacity-70' : ''}`}
                disabled={isPending && isActive}
                aria-pressed={isActive}
              >
                {category.label}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
