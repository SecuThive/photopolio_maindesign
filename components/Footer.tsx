'use client';

import React, { useState } from 'react';
import Link from 'next/link';

export default function Footer() {
  const [email, setEmail] = useState('');
  const [agreed, setAgreed] = useState(false);
  const [status, setStatus] = useState<'idle' | 'loading' | 'success' | 'error'>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!agreed) {
      setStatus('error');
      setMessage('Please agree to the privacy policy to subscribe.');
      return;
    }

    setStatus('loading');
    setMessage('');

    try {
      const response = await fetch('/api/newsletter/subscribe', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });

      const data = await response.json();

      if (response.ok) {
        setStatus('success');
        setMessage(data.message);
        setEmail('');
        setAgreed(false);
      } else {
        setStatus('error');
        setMessage(data.error || 'An error occurred while processing your subscription.');
      }
    } catch (error) {
      setStatus('error');
      setMessage('A network error occurred.');
    }
  };

  return (
    <footer className="border-t border-gray-200 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Newsletter */}
        <div className="py-10 border-b border-gray-200">
          <div className="max-w-xl">
            <h3 className="text-base font-semibold text-gray-900">Stay in the loop</h3>
            <p className="mt-1 text-sm text-gray-500">
              Weekly picks of the best AI-generated designs, straight to your inbox.
            </p>
            <form onSubmit={handleSubmit} className="mt-4 space-y-3">
              <div className="flex gap-2">
                <input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="you@company.com"
                  required
                  disabled={status === 'loading'}
                  className="flex-1 rounded-lg border border-gray-300 bg-white px-4 py-2.5 text-sm text-gray-900 placeholder-gray-400 focus:outline-none focus:ring-2 focus:ring-gray-900/10 focus:border-gray-400 disabled:opacity-50 transition-all"
                />
                <button
                  type="submit"
                  disabled={status === 'loading' || !agreed}
                  className="rounded-lg bg-gray-900 px-5 py-2.5 text-sm font-medium text-white hover:bg-gray-800 disabled:opacity-40 transition-colors whitespace-nowrap"
                >
                  {status === 'loading' ? (
                    <svg className="animate-spin h-4 w-4" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z" />
                    </svg>
                  ) : 'Subscribe'}
                </button>
              </div>
              <div className="flex items-start gap-2">
                <input
                  type="checkbox"
                  id="privacy-consent"
                  checked={agreed}
                  onChange={(e) => setAgreed(e.target.checked)}
                  className="mt-0.5 h-4 w-4 rounded border-gray-300 text-gray-900 focus:ring-gray-900/20"
                />
                <label htmlFor="privacy-consent" className="text-xs text-gray-500 cursor-pointer select-none">
                  I agree to the{' '}
                  <Link href="/privacy-policy" className="text-gray-700 hover:text-gray-900 underline underline-offset-2">
                    Privacy Policy
                  </Link>
                  . Unsubscribe anytime.
                </label>
              </div>
              {message && (
                <div className={`rounded-lg border px-3 py-2.5 text-xs flex items-center gap-2 ${
                  status === 'success'
                    ? 'bg-emerald-50 border-emerald-200 text-emerald-700'
                    : 'bg-red-50 border-red-200 text-red-700'
                }`}>
                  <span>{message}</span>
                </div>
              )}
            </form>
          </div>
        </div>

        {/* Links */}
        <div className="py-10 grid grid-cols-2 md:grid-cols-4 gap-8">
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-4">Product</h4>
            <ul className="space-y-2.5">
              {[
                { href: '/playbooks', label: 'Playbooks' },
                { href: '/collections', label: 'Collections' },
                { href: '/blog', label: 'Blog' },
                { href: '/code-match', label: 'Code Match' },
                { href: '/request-design', label: 'Request Design' },
              ].map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-sm text-gray-500 hover:text-gray-900 transition-colors">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-4">Resources</h4>
            <ul className="space-y-2.5">
              {[
                { href: '/changelog', label: 'Changelog' },
                { href: '/faq', label: 'FAQ' },
                { href: '/about', label: 'About' },
                { href: '/contact', label: 'Contact' },
              ].map((item) => (
                <li key={item.href}>
                  <Link href={item.href} className="text-sm text-gray-500 hover:text-gray-900 transition-colors">
                    {item.label}
                  </Link>
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-4">Legal</h4>
            <ul className="space-y-2.5">
              {[
                { href: '/privacy-policy', label: 'Privacy' },
                { href: '/terms', label: 'Terms' },
                { href: '/feed.xml', label: 'RSS Feed', external: true },
              ].map((item) => (
                <li key={item.href}>
                  {item.external ? (
                    <a href={item.href} className="text-sm text-gray-500 hover:text-gray-900 transition-colors">
                      {item.label}
                    </a>
                  ) : (
                    <Link href={item.href} className="text-sm text-gray-500 hover:text-gray-900 transition-colors">
                      {item.label}
                    </Link>
                  )}
                </li>
              ))}
            </ul>
          </div>
          <div>
            <h4 className="text-sm font-medium text-gray-900 mb-4">UI Syntax</h4>
            <p className="text-sm text-gray-500 leading-relaxed">
              AI-generated web design inspiration with copy-paste code. Free for commercial use.
            </p>
          </div>
        </div>

        {/* Copyright */}
        <div className="py-6 border-t border-gray-200">
          <p className="text-xs text-gray-400">
            &copy; {new Date().getFullYear()} UI Syntax. All rights reserved.
          </p>
        </div>
      </div>
    </footer>
  );
}
