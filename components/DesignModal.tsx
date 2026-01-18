import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { Design } from '@/types/database';

interface DesignModalProps {
  design: Design;
  onClose: () => void;
}

export default function DesignModal({ design, onClose }: DesignModalProps) {
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape') onClose();
    };
    
    document.addEventListener('keydown', handleEscape);
    document.body.style.overflow = 'hidden';
    
    return () => {
      document.removeEventListener('keydown', handleEscape);
      document.body.style.overflow = 'unset';
    };
  }, [onClose]);

  const handleCopyCode = async () => {
    if (design.code) {
      try {
        await navigator.clipboard.writeText(design.code);
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (err) {
        console.error('Failed to copy code:', err);
      }
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center bg-black bg-opacity-90 p-4 backdrop-blur-sm animate-fade-in"
      onClick={onClose}
    >
      <div
        className="relative bg-white max-w-6xl w-full max-h-[90vh] overflow-y-auto animate-slide-up"
        onClick={(e) => e.stopPropagation()}
      >
        {/* Close Button */}
        <button
          onClick={onClose}
          className="absolute top-6 right-6 z-10 bg-white p-3 hover:bg-gray-100 transition-colors group"
        >
          <svg
            className="w-5 h-5 text-black"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={1.5}
              d="M6 18L18 6M6 6l12 12"
            />
          </svg>
        </button>

        {/* Image */}
        <div className="relative w-full aspect-[16/10] bg-gray-100">
          <Image
            src={design.image_url}
            alt={design.title}
            fill
            className="object-contain"
            sizes="(max-width: 1280px) 100vw, 1280px"
            priority
          />
        </div>

        {/* Details */}
        <div className="p-12">
          <div className="flex items-start justify-between mb-6">
            <div className="flex-1">
              <h2 className="font-display text-4xl font-semibold text-black mb-3 tracking-tight">
                {design.title}
              </h2>
              
              <div className="flex items-center gap-6 text-sm text-gray-400 font-light tracking-wide">
                <span>{formatDate(design.created_at)}</span>
                {design.category && (
                  <span className="px-4 py-1 bg-black text-white text-xs uppercase tracking-widest">
                    {design.category}
                  </span>
                )}
              </div>
            </div>
          </div>

          {design.description && (
            <div className="mb-8 pb-8 border-b border-gray-100">
              <h3 className="text-xs uppercase tracking-widest text-gray-400 mb-4 font-light">Description</h3>
              <p className="text-gray-700 leading-relaxed font-light text-lg">
                {design.description}
              </p>
            </div>
          )}

          {design.prompt && (
            <div className="bg-gray-50 p-8 mb-8">
              <h3 className="text-xs uppercase tracking-widest text-gray-400 mb-4 font-light">AI Prompt</h3>
              <p className="text-gray-600 text-sm font-mono leading-relaxed">
                {design.prompt}
              </p>
            </div>
          )}

          {design.code && (
            <div className="bg-black p-8 mb-8 relative group">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-xs uppercase tracking-widest text-gray-400 font-light">Source Code</h3>
                <button
                  onClick={handleCopyCode}
                  className="px-4 py-2 bg-white text-black text-xs uppercase tracking-widest font-light hover:bg-gray-100 transition-colors flex items-center gap-2"
                >
                  {copied ? (
                    <>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
                      </svg>
                      Copied!
                    </>
                  ) : (
                    <>
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                      </svg>
                      Copy Code
                    </>
                  )}
                </button>
              </div>
              <pre className="text-green-400 text-sm font-mono leading-relaxed overflow-x-auto">
                <code>{design.code}</code>
              </pre>
            </div>
          )}

          {/* Action Button */}
          <div className="flex justify-end">
            <a
              href={design.image_url}
              target="_blank"
              rel="noopener noreferrer"
              className="px-10 py-4 bg-black text-white text-xs uppercase tracking-widest font-light hover:bg-gray-900 transition-colors"
            >
              View Original
            </a>
          </div>
        </div>
      </div>
    </div>
  );
}
