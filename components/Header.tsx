"use client";

import { useState } from 'react';
import Link from 'next/link';

export default function Header() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const openCommandPalette = () => {
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new Event('open-command-palette'));
    }
  };

  return (
    <header className="sticky top-0 z-40 bg-white/80 backdrop-blur-xl border-b border-gray-200/80">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <div className="flex items-center gap-8">
            <Link href="/" className="flex items-center gap-2 group">
              <span className="text-xl font-bold text-gray-900 tracking-tight">
                UI Syntax
              </span>
              <span className="hidden sm:inline rounded-full bg-gray-900 px-2 py-0.5 text-[10px] font-medium text-white">
                Gallery
              </span>
            </Link>

            <nav className="hidden lg:flex items-center gap-1">
              {[
                { href: '/playbooks', label: 'Playbooks' },
                { href: '/collections', label: 'Collections' },
                { href: '/blog', label: 'Blog' },
                { href: '/code-match', label: 'Code Match', isNew: true },
              ].map((item) => (
                <Link
                  key={item.href}
                  href={item.href}
                  className="relative px-3 py-2 text-sm text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100 transition-colors"
                >
                  {item.label}
                  {item.isNew && (
                    <span className="absolute -top-1 -right-1 flex h-4 w-4 items-center justify-center rounded-full bg-emerald-500 text-[8px] font-bold text-white">
                      N
                    </span>
                  )}
                </Link>
              ))}
              <Link
                href="/request-design"
                className="px-3 py-2 text-sm text-gray-600 hover:text-gray-900 rounded-lg hover:bg-gray-100 transition-colors"
              >
                Request
              </Link>
            </nav>
          </div>

          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={openCommandPalette}
              className="hidden sm:inline-flex items-center gap-2 rounded-lg border border-gray-200 bg-gray-50 px-3 py-1.5 text-sm text-gray-500 transition-colors hover:border-gray-300 hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-gray-900/20"
              aria-label="Open search"
            >
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="7" />
                <line x1="16.65" y1="16.65" x2="21" y2="21" />
              </svg>
              <span>Search designs...</span>
              <kbd className="hidden md:inline rounded border border-gray-300 bg-white px-1.5 py-0.5 text-[11px] font-medium text-gray-400">
                /
              </kbd>
            </button>

            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="lg:hidden p-2 text-gray-600 hover:text-gray-900 hover:bg-gray-100 rounded-lg transition-colors"
              aria-label="Toggle menu"
            >
              <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                {mobileMenuOpen ? (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
                ) : (
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
                )}
              </svg>
            </button>
          </div>
        </div>
      </div>

      {mobileMenuOpen && (
        <div className="lg:hidden border-t border-gray-200 bg-white animate-slideDown">
          <nav className="max-w-7xl mx-auto px-4 py-3 space-y-1">
            <button
              type="button"
              onClick={() => { openCommandPalette(); setMobileMenuOpen(false); }}
              className="mb-2 flex w-full items-center gap-3 rounded-lg bg-gray-50 border border-gray-200 px-4 py-3 text-sm text-gray-600"
            >
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="7" />
                <line x1="16.65" y1="16.65" x2="21" y2="21" />
              </svg>
              <span className="flex-1 text-left">Search designs...</span>
            </button>
            {[
              { href: '/', label: 'Home' },
              { href: '/playbooks', label: 'Playbooks' },
              { href: '/collections', label: 'Collections' },
              { href: '/blog', label: 'Blog' },
              { href: '/code-match', label: 'Code Match' },
              { href: '/request-design', label: 'Request Design' },
              { href: '/about', label: 'About' },
              { href: '/changelog', label: 'Changelog' },
              { href: '/contact', label: 'Contact' },
            ].map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="block px-4 py-2.5 text-sm text-gray-700 hover:text-gray-900 hover:bg-gray-50 rounded-lg transition-colors"
                onClick={() => setMobileMenuOpen(false)}
              >
                {item.label}
              </Link>
            ))}
          </nav>
        </div>
      )}
    </header>
  );
}
