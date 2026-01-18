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
      </div>

      {/* Mobile Sidebar Menu */}
      {mobileMenuOpen && (
        <>
          {/* Backdrop */}
          <div 
            className="fixed inset-0 bg-black bg-opacity-70 z-40 lg:hidden"
            onClick={() => setMobileMenuOpen(false)}
          />
          
          {/* Sidebar - 완전 불투명하게 수정 */}
          <div className="fixed top-0 right-0 h-full w-64 bg-black z-50 lg:hidden shadow-2xl">
            <div className="p-6">
              <button
                onClick={() => setMobileMenuOpen(false)}
                className="absolute top-4 right-4 text-white hover:text-gray-300"
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
                  className="block text-gray-300 hover:text-white transition-colors py-2 text-base"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Home
                </Link>
                <Link 
                  href="/about" 
                  className="block text-gray-300 hover:text-white transition-colors py-2 text-base"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  About
                </Link>
                <Link 
                  href="/contact" 
                  className="block text-gray-300 hover:text-white transition-colors py-2 text-base"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Contact
                </Link>
                <Link 
                  href="/privacy-policy" 
                  className="block text-gray-300 hover:text-white transition-colors py-2 text-base"
                  onClick={() => setMobileMenuOpen(false)}
                >
                  Privacy Policy
                </Link>
                <a 
                  href="/feed.xml" 
                  className="block text-gray-300 hover:text-white transition-colors py-2 text-base"
                  target="_blank"
                  rel="noopener noreferrer"
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
