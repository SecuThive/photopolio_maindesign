"use client";

import { useState, useRef, useEffect } from 'react';
import Image from 'next/image';

interface DesignPreviewProps {
  imageUrl: string;
  title: string;
  colors?: string[];
  htmlCode?: string | null;
}

export default function DesignPreview({ imageUrl, title, colors, htmlCode }: DesignPreviewProps) {
  const [selectedColor, setSelectedColor] = useState<string | null>(null);
  const [viewMode, setViewMode] = useState<'image' | 'live'>('image');
  const iframeRef = useRef<HTMLIFrameElement>(null);

  // iframe에 HTML 주입 및 색상 변경
  useEffect(() => {
    if (viewMode === 'live' && iframeRef.current && htmlCode) {
      const iframeDoc = iframeRef.current.contentDocument;
      if (!iframeDoc) return;

      // 1920px 기준으로 렌더링 후 50%로 축소
      const htmlContent = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=1920">
          <style>
            :root {
              --primary-color: ${selectedColor || '#3B82F6'};
              --secondary-color: ${selectedColor || '#10B981'};
              --accent-color: ${selectedColor || '#F59E0B'};
            }
            
            * {
              margin: 0;
              padding: 0;
              box-sizing: border-box;
            }
            
            html, body {
              width: 1920px;
              font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
              background: white;
            }
            
            /* 버튼 스타일 */
            button:not(.outline):not(.ghost),
            .btn:not(.btn-outline):not(.btn-ghost),
            .button,
            input[type="submit"],
            input[type="button"],
            [class*="btn-primary"],
            [class*="button-primary"] {
              background-color: var(--primary-color) !important;
              border-color: var(--primary-color) !important;
            }
            
            /* 배경색 */
            .bg-primary,
            [class*="bg-blue"],
            [class*="bg-indigo"] {
              background-color: var(--primary-color) !important;
            }
            
            /* 텍스트 색상 */
            .text-primary,
            [class*="text-blue"]:not([class*="bg"]) {
              color: var(--primary-color) !important;
            }
            
            /* 헤더 */
            header,
            nav,
            .header,
            .navbar {
              background-color: var(--primary-color) !important;
            }
            
            /* 링크 */
            a:not(.btn):not(.button):hover {
              color: var(--primary-color) !important;
            }
          </style>
        </head>
        <body>
          ${htmlCode}
        </body>
        </html>
      `;

      iframeDoc.open();
      iframeDoc.write(htmlContent);
      iframeDoc.close();
    }
  }, [viewMode, htmlCode, selectedColor]);

  const hasLivePreview = htmlCode && htmlCode.trim().length > 0;

  return (
    <div className="space-y-6">
      {/* 뷰 모드 토글 - 임시 주석처리 */}
      {/* {hasLivePreview && (
        <div className="flex gap-2 justify-center">
          <button
            onClick={() => setViewMode('image')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all ${
              viewMode === 'image'
                ? 'bg-black text-white'
                : 'bg-white text-gray-700 border border-gray-300 hover:border-black'
            }`}
          >
            📷 Screenshot
          </button>
          <button
            onClick={() => setViewMode('live')}
            className={`px-4 py-2 rounded-lg text-xs font-semibold uppercase tracking-wider transition-all ${
              viewMode === 'live'
                ? 'bg-black text-white'
                : 'bg-white text-gray-700 border border-gray-300 hover:border-black'
            }`}
          >
            ⚡ Live Preview
          </button>
        </div>
      )} */}

      {/* Preview Container */}
      <div className="relative overflow-hidden rounded-[32px] border border-gray-200 shadow-[0_25px_70px_rgba(0,0,0,0.12)] bg-white">
        {/* {viewMode === 'image' ? ( */}
          <div className="relative aspect-[3/2]">
            <Image
              src={imageUrl}
              alt={title}
              fill
              className="object-cover object-top"
              sizes="(max-width: 1024px) 100vw, 70vw"
              priority
            />
          </div>
        {/* ) : (
          <div className="relative w-full bg-white" style={{ paddingBottom: '66.67%' }}>
            <div className="absolute inset-0 overflow-auto">
              <div 
                style={{
                  transform: 'scale(0.5)',
                  transformOrigin: 'top left',
                  width: '200%',
                }}
              >
                <iframe
                  ref={iframeRef}
                  className="w-full border-0"
                  style={{ 
                    height: '1280px',
                    minHeight: '1280px'
                  }}
                  title="Live Design Preview"
                  sandbox="allow-same-origin"
                />
              </div>
            </div>
          </div>
        )} */}
      </div>

      {/* Color Palette - 임시 주석처리 */}
      {/* {colors && colors.length > 0 && (
        <div className="bg-white border border-gray-200 p-6 shadow-sm">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-xs uppercase tracking-[0.3em] text-gray-400">Color Palette</h3>
            {selectedColor && (
              <button
                onClick={() => setSelectedColor(null)}
                className="text-[10px] uppercase tracking-[0.3em] text-gray-500 hover:text-black transition-colors"
              >
                Reset
              </button>
            )}
          </div>
          <div className="flex flex-wrap gap-3">
            {colors.map((color, index) => (
              <button
                key={index}
                onClick={() => setSelectedColor(selectedColor === color ? null : color)}
                className={`group relative flex flex-col items-center gap-2 transition-all duration-200 ${
                  selectedColor === color ? 'scale-110' : 'hover:scale-105'
                }`}
                title={`Apply ${color} to components`}
              >
                <div 
                  className={`w-14 h-14 rounded-lg border-2 transition-all shadow-sm ${
                    selectedColor === color 
                      ? 'border-black shadow-lg ring-2 ring-black ring-offset-2' 
                      : 'border-gray-200 hover:border-gray-400'
                  }`}
                  style={{ backgroundColor: color }}
                />
                <span className="text-[10px] font-mono text-gray-600 uppercase tracking-wider">
                  {color}
                </span>
              </button>
            ))}
          </div>
          {hasLivePreview && (
            <div className="mt-4 p-4 bg-gradient-to-r from-purple-50 to-pink-50 border border-purple-200 rounded-lg">
              <p className="text-xs text-purple-900 font-medium mb-1">
                ⚡ Interactive Color Preview
              </p>
              <p className="text-xs text-purple-700">
                Switch to <strong>Live Preview</strong> and click any color to see it applied instantly to buttons, headers, links, and UI components.
              </p>
            </div>
          )}
        </div>
      )} */}
    </div>
  );
}
