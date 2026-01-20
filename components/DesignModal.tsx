import React, { useEffect, useState } from 'react';
import Image from 'next/image';
import { Design } from '@/types/database';
import LikeButton from './LikeButton';

interface DesignModalProps {
  design: Design;
  onClose: () => void;
  likes: number;
  liked: boolean;
  onToggleLike: () => void;
  likeDisabled?: boolean;
}

const COLOR_THEMES = [
  { name: "Purple Dream", primary: "#667eea", secondary: "#764ba2", accent: "#f093fb" },
  { name: "Pink Sunset", primary: "#f093fb", secondary: "#f5576c", accent: "#fbbf24" },
  { name: "Ocean Blue", primary: "#4facfe", secondary: "#00f2fe", accent: "#43e97b" },
  { name: "Green Forest", primary: "#11998e", secondary: "#38ef7d", accent: "#7bed9f" },
  { name: "Orange Fire", primary: "#fc4a1a", secondary: "#f7b733", accent: "#ee5a24" },
  { name: "Violet Night", primary: "#8e2de2", secondary: "#4a00e0", accent: "#a55eea" },
  { name: "Red Passion", primary: "#eb3349", secondary: "#f45c43", accent: "#fc5c65" },
  { name: "Blue Steel", primary: "#2c3e50", secondary: "#3498db", accent: "#74b9ff" },
];

export default function DesignModal({ design, onClose, likes, liked, onToggleLike, likeDisabled }: DesignModalProps) {
  const [copied, setCopied] = useState(false);
  const [selectedTheme, setSelectedTheme] = useState(0);
  const [previewCode, setPreviewCode] = useState(design.code);
  const [isLoadingPreview, setIsLoadingPreview] = useState(false);
  const [previewMode, setPreviewMode] = useState<'desktop' | 'tablet' | 'mobile'>('desktop');

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

  // Detect which theme the original design used
  const getOriginalColors = (code: string) => {
    for (const theme of COLOR_THEMES) {
      // Check if the code includes the theme's primary color
      if (code.toLowerCase().includes(theme.primary.toLowerCase())) {
        return theme;
      }
    }
    return COLOR_THEMES[0]; // Fallback theme
  };

  // Update the rendered code when the color theme changes
  useEffect(() => {
    if (!design.code) return;
    
    setIsLoadingPreview(true);
    const originalTheme = getOriginalColors(design.code);
    const newTheme = COLOR_THEMES[selectedTheme];
    
    let updatedCode = design.code;
    
    // Replace the original theme colors with the newly selected theme
    // Match colors without case sensitivity
    updatedCode = updatedCode.replace(new RegExp(originalTheme.primary, 'gi'), newTheme.primary);
    updatedCode = updatedCode.replace(new RegExp(originalTheme.secondary, 'gi'), newTheme.secondary);
    updatedCode = updatedCode.replace(new RegExp(originalTheme.accent, 'gi'), newTheme.accent);
    
    setPreviewCode(updatedCode);
    
    // Finish the preview loading state
    setTimeout(() => setIsLoadingPreview(false), 300);
  }, [selectedTheme, design.code]);

  useEffect(() => {
    setPreviewMode('desktop');
  }, [design.id]);

  const handleCopyCode = async () => {
    const codeToCopy = previewCode || design.code;
    if (codeToCopy) {
      try {
        await navigator.clipboard.writeText(codeToCopy);
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

        {/* Image - Live Preview with iframe */}
        <div className="w-full bg-gray-50 px-4 py-6 border-b border-gray-100">
          <div className="flex flex-wrap items-center gap-3 text-xs uppercase tracking-[0.3em] text-gray-500">
            <span className="text-[10px] text-gray-400">Responsive Preview</span>
            <div className="flex items-center gap-2 rounded-full border border-gray-200 bg-white p-1">
              {[
                { label: 'Desktop', value: 'desktop', icon: 'desktop' },
                { label: 'Tablet', value: 'tablet', icon: 'tablet' },
                { label: 'Mobile', value: 'mobile', icon: 'mobile' },
              ].map((option) => (
                <button
                  key={option.value}
                  type="button"
                  onClick={() => setPreviewMode(option.value as 'desktop' | 'tablet' | 'mobile')}
                  className={`flex items-center gap-2 rounded-full px-4 py-2 text-[11px] font-semibold transition-colors ${
                    previewMode === option.value
                      ? 'bg-black text-white'
                      : 'text-gray-500 hover:text-black'
                  }`}
                >
                  <PreviewIcon type={option.icon} active={previewMode === option.value} />
                  <span className="hidden sm:inline">{option.label}</span>
                </button>
              ))}
            </div>
            <span className="ml-auto text-[10px] tracking-[0.4em] text-gray-400">
              {previewMode === 'desktop' ? 'FULL WIDTH' : previewMode === 'tablet' ? '768PX' : '375PX'}
            </span>
          </div>

          <div className="mt-8 flex justify-center">
            <div
              className="relative overflow-hidden rounded-[32px] border border-gray-200 bg-white shadow-[0_20px_60px_rgba(0,0,0,0.12)]"
              style={{ width: previewMode === 'desktop' ? '100%' : previewMode === 'tablet' ? '768px' : '375px' }}
            >
              {isLoadingPreview && (
                <div className="absolute inset-0 bg-white/80 flex items-center justify-center z-10">
                  <div className="text-center">
                    <div className="animate-spin rounded-full h-10 w-10 border-b-2 border-black mx-auto mb-3"></div>
                    <p className="text-xs uppercase tracking-[0.3em] text-gray-500">Updating</p>
                  </div>
                </div>
              )}
              <iframe
                srcDoc={previewCode || design.code || ''}
                className="w-full border-0"
                style={{ minHeight: '640px' }}
                title="Design Preview"
                sandbox="allow-scripts"
              />
            </div>
          </div>
        </div>

        {/* Details */}
        <div className="p-12">
          <div className="flex flex-wrap items-start justify-between gap-4 mb-6">
            <div className="flex-1 min-w-[240px]">
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
            <LikeButton
              likes={likes}
              liked={liked}
              onToggle={onToggleLike}
              disabled={likeDisabled}
              variant="modal"
            />
          </div>

          {design.description && (
            <div className="mb-8 pb-8 border-b border-gray-100">
              <h3 className="text-xs uppercase tracking-widest text-gray-400 mb-4 font-light">Description</h3>
              <p className="text-gray-700 leading-relaxed font-light text-lg">
                {design.description}
              </p>
            </div>
          )}

          {/* Color Theme Selector */}
          <div className="mb-8 pb-8 border-b border-gray-100">
            <h3 className="text-xs uppercase tracking-widest text-gray-400 mb-4 font-light">Color Theme</h3>
            <div className="flex gap-4 overflow-x-auto pb-2 scroll-smooth">
              {COLOR_THEMES.map((theme, index) => (
                <button
                  key={index}
                  onClick={() => setSelectedTheme(index)}
                  className={`flex-shrink-0 min-w-[180px] p-4 border-2 transition-all ${
                    selectedTheme === index 
                      ? 'border-black bg-gray-50' 
                      : 'border-gray-200 hover:border-gray-400'
                  }`}
                >
                  <div className="flex items-center gap-3 mb-2">
                    <div className="w-6 h-6 rounded-full" style={{ background: theme.primary }}></div>
                    <div className="w-6 h-6 rounded-full" style={{ background: theme.secondary }}></div>
                    <div className="w-6 h-6 rounded-full" style={{ background: theme.accent }}></div>
                  </div>
                  <div className="text-xs uppercase tracking-widest font-light">
                    {theme.name}
                  </div>
                </button>
              ))}
            </div>
            <p className="text-xs text-gray-500 mt-3">
              Select a color theme to preview the design with different colors
            </p>
          </div>

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
                <h3 className="text-xs uppercase tracking-widest text-gray-400 font-light">
                  Source Code {selectedTheme > 0 && `(${COLOR_THEMES[selectedTheme].name})`}
                </h3>
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
              <pre className="text-green-400 text-sm font-mono leading-relaxed overflow-x-auto max-h-96">
                <code>{previewCode}</code>
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

function PreviewIcon({ type, active }: { type: string; active: boolean }) {
  const stroke = active ? '#FFFFFF' : '#9CA3AF';
  const common = {
    fill: 'none',
    stroke,
    strokeWidth: 1.5,
    strokeLinecap: 'round' as const,
    strokeLinejoin: 'round' as const,
  };

  if (type === 'tablet') {
    return (
      <svg className="h-4 w-4" viewBox="0 0 24 24" {...common}>
        <rect x="5" y="3" width="14" height="18" rx="2" />
        <circle cx="12" cy="18" r="0.5" fill={stroke} />
      </svg>
    );
  }

  if (type === 'mobile') {
    return (
      <svg className="h-4 w-4" viewBox="0 0 24 24" {...common}>
        <rect x="8" y="2" width="8" height="20" rx="2" />
        <circle cx="12" cy="18" r="0.5" fill={stroke} />
      </svg>
    );
  }

  return (
    <svg className="h-4 w-4" viewBox="0 0 24 24" {...common}>
      <rect x="3" y="5" width="18" height="14" rx="2" />
      <path d="M8 20h8" />
    </svg>
  );
}
