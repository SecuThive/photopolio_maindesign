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
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(0.5);
  const DESIGN_WIDTH = 1920;
  const DESIGN_HEIGHT = Math.round((1920 * 2) / 3); // keep 3:2 aspect
  const [contentSize, setContentSize] = useState({ width: DESIGN_WIDTH, height: DESIGN_HEIGHT });

  // Calculate the scale based on the current container width
  useEffect(() => {
    const updateScale = () => {
      if (containerRef.current) {
        const containerWidth = containerRef.current.clientWidth;
        // Leave a small margin so the preview always fits inside
        const safeWidth = containerWidth - 2;
        const nextScale = Math.min(Math.max(safeWidth / contentSize.width, 0.05), 1);
        setScale(nextScale);
      }
    };

    updateScale();
    const resizeObserver = new ResizeObserver(updateScale);
    if (containerRef.current) {
      resizeObserver.observe(containerRef.current);
    }
    window.addEventListener('resize', updateScale);
    
    return () => {
      resizeObserver.disconnect();
      window.removeEventListener('resize', updateScale);
    };
  }, [contentSize.width]);

  // Inject HTML into the iframe for live previewing
  useEffect(() => {
    if (iframeRef.current && htmlCode) {
      const iframeDoc = iframeRef.current.contentDocument;
      if (!iframeDoc) return;

      const trimmed = htmlCode.trim();
      const containsFullDocument = /^<!DOCTYPE|<html/i.test(trimmed);

      const htmlContent = containsFullDocument
        ? trimmed
        : `
        <!DOCTYPE html>
        <html lang="en">
        <head>
          <meta charset="UTF-8">
          <meta name="viewport" content="width=1920">
          <style>
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
          </style>
        </head>
        <body>
          ${trimmed}
        </body>
        </html>
      `;

      iframeDoc.open();
      iframeDoc.write(htmlContent);
      iframeDoc.close();

      const measure = () => {
        const body = iframeRef.current?.contentDocument?.body;
        if (!body) return;
        const width = Math.max(body.scrollWidth, DESIGN_WIDTH);
        const height = Math.max(body.scrollHeight, DESIGN_HEIGHT);
        setContentSize({ width, height });
      };

      iframeRef.current.onload = measure;
      setTimeout(measure, 50);
    }
  }, [htmlCode, DESIGN_HEIGHT, DESIGN_WIDTH]);

  const hasLivePreview = htmlCode && htmlCode.trim().length > 0;

  return (
    <div className="space-y-6 max-w-full">
      {/* Preview Container */}
      <div 
        ref={containerRef}
        className="relative w-full max-w-full overflow-hidden rounded-[32px] border border-gray-200 shadow-[0_25px_70px_rgba(0,0,0,0.12)] bg-white"
      >
        {hasLivePreview ? (
          <div className="relative w-full" style={{ paddingBottom: `${(contentSize.height / contentSize.width) * 100}%` }}>
            <div className="absolute inset-0 overflow-hidden">
              <div className="w-full h-full overflow-hidden">
                <iframe
                  ref={iframeRef}
                  className="border-0 origin-top-left block"
                  style={{
                    transform: `scale(${scale})`,
                    transformOrigin: 'top left',
                    width: contentSize.width,
                    height: contentSize.height,
                    maxWidth: 'none',
                    maxHeight: 'none',
                    border: 'none',
                    display: 'block',
                  }}
                  title="Live Design Preview"
                  sandbox="allow-same-origin allow-forms allow-scripts"
                  scrolling="no"
                />
              </div>
            </div>
          </div>
        ) : (
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
        )}
      </div>
    </div>
  );
}
