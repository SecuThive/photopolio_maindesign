import React from 'react';
import Link from 'next/link';

export default function Footer() {
  return (
    <footer className="bg-black border-t border-gray-900 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {/* Brand Section */}
          <div>
            <h2 className="text-xl font-display font-semibold text-white mb-4">
              UI SYNTAX
            </h2>
            <p className="text-gray-400 text-sm">
              UI Syntax is your premier destination for AI-generated web design inspiration. We curate cutting-edge designs across landing pages, dashboards, e-commerce interfaces, and mobile applications. Explore modern design patterns, color palettes, and innovative layouts tailored for SaaS founders, product designers, developers, and creative professionals. Discover the future of web design with AI-powered creativity and human-curated quality.
            </p>
          </div>

          {/* Quick Links */}
          <div>
            <h3 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">
              Quick Links
            </h3>
            <ul className="space-y-2">
              <li>
                <Link href="/" className="text-gray-400 hover:text-white text-sm transition-colors">
                  Home
                </Link>
              </li>
              <li>
                <Link href="/about" className="text-gray-400 hover:text-white text-sm transition-colors">
                  About
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-gray-400 hover:text-white text-sm transition-colors">
                  Contact
                </Link>
              </li>
              <li>
                <Link href="/faq" className="text-gray-400 hover:text-white text-sm transition-colors">
                  FAQ
                </Link>
              </li>
            </ul>
          </div>

          {/* Legal */}
          <div>
            <h3 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">
              Legal
            </h3>
            <ul className="space-y-2">
              <li>
                <Link href="/privacy-policy" className="text-gray-400 hover:text-white text-sm transition-colors">
                  Privacy Policy
                </Link>
              </li>
              <li>
                <Link href="/terms" className="text-gray-400 hover:text-white text-sm transition-colors">
                  Terms of Service
                </Link>
              </li>
              <li>
                <Link href="/contact" className="text-gray-400 hover:text-white text-sm transition-colors">
                  Contact
                </Link>
              </li>
              <li>
                <a href="/feed.xml" className="text-gray-400 hover:text-white text-sm transition-colors">
                  RSS Feed
                </a>
              </li>
            </ul>
          </div>
        </div>

        {/* Copyright */}
        <div className="mt-8 pt-8 border-t border-gray-900">
          <p className="text-center text-gray-500 text-sm">
            © {new Date().getFullYear()} UI Syntax. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
