import React, { useState } from 'react';
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
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

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

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden text-white p-2"
            aria-label="Toggle menu"
          >
            <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              {mobileMenuOpen ? (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              ) : (
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              )}
            </svg>
          </button>

          {/* Desktop Navigation */}
          <nav className="hidden lg:flex space-x-6">
            <Link href="/about" className="text-gray-400 hover:text-white text-sm transition-colors">
              About
            </Link>
            <Link href="/contact" className="text-gray-400 hover:text-white text-sm transition-colors">
              Contact
            </Link>
          </nav>
        </div>

        {/* Desktop Category Filter */}
        <div className="pb-6 overflow-x-auto scrollbar-hide hidden lg:block">
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

        {/* Mobile Category Filter - Always Visible on Mobile */}
        <div className="pb-4 overflow-x-auto scrollbar-hide lg:hidden">
          <div className="flex space-x-2">
            {categories.map((category) => (
              <button
                key={category.value || 'all'}
                onClick={() => onCategoryChange(category.value)}
                className={`px-4 py-2 text-xs whitespace-nowrap transition-all duration-300 font-light tracking-wide ${
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

      {/* Mobile Sidebar Menu */}
      {mobileMenuOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 bg-black bg-opacity-50 z-40 lg:hidden"
            onClick={() => setMobileMenuOpen(false)}
          />
          
          {/* Sidebar */}
          <div className="fixed top-0 right-0 h-full w-64 bg-black border-l border-gray-800 z-50 lg:hidden transform transition-transform duration-300 ease-in-out">
            <div className="p-6">
              <button
                onClick={() => setMobileMenuOpen(false)}
                className="absolute top-4 right-4 text-white"
                aria-label="Close menu"
              >
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>

              <h2 className="text-xl font-semibold text-white mb-8 mt-8">Menu</h2>

              <nav className="space-y-4">
                <Link 
                  href="/" 
                  className="block text-gray-400 hover:text-white transition-colors py-2"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Home
                </Link>
                <Link 
                  href="/about" 
                  className="block text-gray-400 hover:text-white transition-colors py-2"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  About
                </Link>
                <Link 
                  href="/contact" 
                  className="block text-gray-400 hover:text-white transition-colors py-2"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Contact
                </Link>
                <Link 
                  href="/privacy-policy" 
                  className="block text-gray-400 hover:text-white transition-colors py-2"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Privacy Policy
                </Link>
                <a 
                  href="/feed.xml" 
                  className="block text-gray-400 hover:text-white transition-colors py-2"
                >
                  RSS Feed
                </a>
              </nav>
            </div>
          </div>
        </>
      )}
    </header>
  );
}
