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
    <header className="relative bg-black border-b border-gray-900 sticky top-0 z-40 backdrop-blur-sm bg-opacity-95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-wrap items-center justify-between gap-4 py-6">
          <div className="flex items-center gap-3">
            <h1 className="text-2xl md:text-3xl font-display font-semibold text-white tracking-tight">
              <Link href="/" className="hover:opacity-80 transition-opacity">
                UI SYNTAX
              </Link>
            </h1>
            <span className="hidden sm:inline text-xs text-gray-500 font-light tracking-[0.3em] uppercase">
              AI Design Gallery
            </span>
          </div>

          <nav className="hidden lg:flex items-center gap-8 text-sm text-gray-400">
            <Link href="/about" className="hover:text-white transition-colors">
              About
            </Link>
            <Link href="/contact" className="hover:text-white transition-colors">
              Contact
            </Link>
            <Link href="/playbooks" className="hover:text-white transition-colors">
              Playbooks
            </Link>
            <Link href="/collections" className="hover:text-white transition-colors">
              Collections
            </Link>
            <Link href="/blog" className="hover:text-white transition-colors">
              Blog
            </Link>
            <Link
              href="/code-match"
              className="inline-flex items-center gap-2 rounded-full bg-white/95 px-4 py-2 text-[10px] font-semibold uppercase tracking-[0.35em] text-gray-900 transition hover:bg-white"
            >
              <span>Code Match</span>
              <span className="text-[9px] font-bold text-emerald-600">NEW</span>
            </Link>
            <button
              type="button"
              onClick={openCommandPalette}
              className="group inline-flex items-center gap-2 rounded-full border border-gray-800 px-4 py-2 text-xs uppercase tracking-[0.3em] text-gray-300 transition-colors hover:border-gray-600 hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-white/50"
              aria-label="Open search"
            >
              <svg className="h-4 w-4" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                <circle cx="11" cy="11" r="7" />
                <line x1="16.65" y1="16.65" x2="21" y2="21" />
              </svg>
              <span>Search</span>
              <span className="rounded border border-gray-700 px-1 py-0.5 text-[10px] text-gray-400">⌘K</span>
            </button>
          </nav>

          <div className="flex items-center gap-3 lg:hidden">
            <button
              onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
              className="text-white p-2 bg-gray-900 hover:bg-gray-800 rounded transition-colors"
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
          </div>
        </div>
      </div>

      {/* Mobile Dropdown Menu */}
      {mobileMenuOpen && (
        <>
          {/* Dropdown Menu - slide-down animation */}
          <div className="lg:hidden bg-gray-950 border-t border-gray-800 shadow-lg animate-slideDown">
            <nav className="space-y-1 px-4 py-6 max-w-7xl mx-auto">
              {/* Search Button in Mobile Menu */}
              <button
                type="button"
                onClick={() => {
                  openCommandPalette();
                  setMobileMenuOpen(false);
                }}
                className="mb-3 flex w-full items-center gap-3 rounded-lg border border-gray-800 px-4 py-3 text-sm text-gray-200 hover:bg-gray-900 transition-colors"
              >
                <svg className="h-5 w-5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="7" />
                  <line x1="16.65" y1="16.65" x2="21" y2="21" />
                </svg>
                <span className="flex-1 text-left font-medium">Search Designs</span>
                <span className="text-xs text-gray-500">⌘K</span>
              </button>

              <Link 
                href="/" 
                className="block text-gray-300 hover:text-white hover:bg-gray-900 transition-colors py-3 px-4 rounded text-base"
                onClick={() => setMobileMenuOpen(false)}
              >
                Home
              </Link>
              <Link 
                href="/about" 
                className="block text-gray-300 hover:text-white hover:bg-gray-900 transition-colors py-3 px-4 rounded text-base"
                onClick={() => setMobileMenuOpen(false)}
              >
                About
              </Link>
              <Link 
                href="/contact" 
                className="block text-gray-300 hover:text-white hover:bg-gray-900 transition-colors py-3 px-4 rounded text-base"
                onClick={() => setMobileMenuOpen(false)}
              >
                Contact
              </Link>
              <Link 
                href="/playbooks" 
                className="block text-gray-300 hover:text-white hover:bg-gray-900 transition-colors py-3 px-4 rounded text-base"
                onClick={() => setMobileMenuOpen(false)}
              >
                Playbooks
              </Link>
              <Link 
                href="/collections" 
                className="block text-gray-300 hover:text-white hover:bg-gray-900 transition-colors py-3 px-4 rounded text-base"
                onClick={() => setMobileMenuOpen(false)}
              >
                Collections
              </Link>
              <Link 
                href="/blog" 
                className="block text-gray-300 hover:text-white hover:bg-gray-900 transition-colors py-3 px-4 rounded text-base"
                onClick={() => setMobileMenuOpen(false)}
              >
                Blog
              </Link>
              <Link 
                href="/code-match" 
                className="block text-gray-200 bg-gradient-to-r from-emerald-500/80 to-cyan-500/80 hover:from-emerald-400 hover:to-cyan-400 transition-[colors,transform] py-3 px-4 rounded-xl text-sm font-semibold tracking-[0.3em] uppercase"
                onClick={() => setMobileMenuOpen(false)}
              >
                Code Match
              </Link>
              <Link 
                href="/privacy-policy" 
                className="block text-gray-300 hover:text-white hover:bg-gray-900 transition-colors py-3 px-4 rounded text-base"
                onClick={() => setMobileMenuOpen(false)}
              >
                Privacy Policy
              </Link>
              <a 
                href="/feed.xml" 
                className="block text-gray-300 hover:text-white hover:bg-gray-900 transition-colors py-3 px-4 rounded text-base"
                target="_blank"
                rel="noopener noreferrer"
              >
                RSS Feed
              </a>
            </nav>
          </div>
        </>
      )}
    </header>
  );
}
