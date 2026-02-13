'use client';

import React, { useState } from 'react';
import Link from 'next/link';

export default function SimpleHeader() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);

  return (
    <header className="bg-black border-b border-gray-900 sticky top-0 z-40 backdrop-blur-sm bg-opacity-95">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-20">
          <div className="flex items-center">
            <h1 className="text-2xl md:text-3xl font-display font-semibold text-white tracking-tight">
              <Link href="/" className="hover:opacity-80 transition-opacity">
                UI SYNTAX
              </Link>
            </h1>
            <span className="ml-3 text-xs text-gray-500 font-light tracking-widest uppercase hidden sm:block">
              AI Design Gallery
            </span>
          </div>

          {/* Mobile Menu Button */}
          <button
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
            className="lg:hidden text-white p-2 bg-gray-900 hover:bg-gray-800 rounded transition-colors"
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
      </div>

      {/* Mobile Dropdown Menu */}
      {mobileMenuOpen && (
        <>
          {/* Dropdown Menu - slide-down animation */}
          <div className="lg:hidden bg-gray-950 border-t border-gray-800 shadow-lg animate-slideDown">
            <nav className="space-y-1 px-4 py-6 max-w-7xl mx-auto">
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
