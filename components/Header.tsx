import React from 'react';
import Link from 'next/link';

interface HeaderProps {
  selectedCategory: string | null;
  onCategoryChange: (category: string | null) => void;
}

const categories = [
  { value: null, label: 'All' },
  { value: 'Landing Page', label: 'Landing Page' },
  { value: 'Dashboard', label: 'Dashboard' },
  { value: 'E-commerce', label: 'E-commerce' },
  { value: 'Portfolio', label: 'Portfolio' },
  { value: 'Blog', label: 'Blog' },
  { value: 'Components', label: 'Components' },
];

export default function Header({ selectedCategory, onCategoryChange }: HeaderProps) {
  return (
    <header className="bg-black border-b border-gray-900 sticky top-0 z-40 backdrop-blur-sm bg-opacity-95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center">
            <h1 className="text-2xl md:text-3xl font-display font-semibold text-white tracking-tight">
              <Link href="/" className="hover:opacity-80 transition-opacity">
                BASE SYNTAX
              </Link>
            </h1>
            <span className="ml-3 text-xs text-gray-500 font-light tracking-widest uppercase hidden sm:block">
              AI Design Gallery
            </span>
          </div>
        </div>

        {/* Category Filter */}
        <div className="pb-6 overflow-x-auto scrollbar-hide">
          <div className="flex space-x-3">
            {categories.map((category) => (
              <button
                key={category.value || 'all'}
                onClick={() => onCategoryChange(category.value)}
                className={`px-5 py-2 text-sm whitespace-nowrap transition-all duration-300 font-light tracking-wide ${
                  selectedCategory === category.value
                    ? 'bg-white text-black'
                    : 'bg-transparent text-gray-400 hover:text-white border border-gray-800 hover:border-gray-600'
                } rounded-sm`}
              >
                {category.label}
              </button>
            ))}
          </div>
        </div>
      </div>
    </header>
  );
}
