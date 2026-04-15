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
  className?: string;
}

export default function CategoryFilterBar({ selectedCategory, className }: CategoryFilterBarProps) {
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

  const rootClassName = [
    'sticky top-16 z-30 bg-white/80 backdrop-blur-xl border-b border-gray-200/80',
    className,
  ]
    .filter(Boolean)
    .join(' ');

  return (
    <div className={rootClassName}>
      {isPending && (
        <div className="absolute top-0 left-0 h-0.5 w-full overflow-hidden">
          <div className="h-full w-1/3 bg-gray-900 animate-[shimmer_1s_ease-in-out_infinite] rounded-full" />
        </div>
      )}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-3">
        <div className="flex items-center gap-2 overflow-x-auto scrollbar-hide -mx-1 px-1">
          {categories.map((category) => {
            const isActive = optimisticCategory === category.value;
            return (
              <button
                key={category.value || 'all'}
                type="button"
                onClick={() => navigateToCategory(category.value)}
                className={`shrink-0 rounded-lg px-3.5 py-1.5 text-sm font-medium transition-all duration-200 ${
                  isActive
                    ? 'bg-gray-900 text-white'
                    : 'text-gray-500 hover:text-gray-900 hover:bg-gray-100'
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
