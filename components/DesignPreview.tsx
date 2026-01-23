"use client";

import { useState } from 'react';
import Image from 'next/image';

interface DesignPreviewProps {
  imageUrl: string;
  title: string;
  colors?: string[];
}

export default function DesignPreview({ imageUrl, title, colors }: DesignPreviewProps) {
  const [selectedColor, setSelectedColor] = useState<string | null>(null);

  return (
    <div className="space-y-6">
      {/* Main Image Preview */}
      <div 
        className="relative aspect-[3/2] overflow-hidden rounded-[32px] border border-gray-200 shadow-[0_25px_70px_rgba(0,0,0,0.12)] transition-all duration-300"
        style={selectedColor ? { 
          backgroundColor: selectedColor,
          boxShadow: `0 25px 70px ${selectedColor}40, inset 0 0 0 2px ${selectedColor}50`
        } : undefined}
      >
        <Image
          src={imageUrl}
          alt={title}
          fill
          className={`object-cover object-top transition-all duration-500 ${
            selectedColor ? 'opacity-90 mix-blend-multiply' : ''
          }`}
          sizes="(max-width: 1024px) 100vw, 70vw"
          priority
        />
      </div>

      {/* Color Palette */}
      {colors && colors.length > 0 && (
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
                title={`Apply ${color}`}
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
          <p className="mt-4 text-xs text-gray-500 italic">
            Click a color to preview it with the design
          </p>
        </div>
      )}
    </div>
  );
}
