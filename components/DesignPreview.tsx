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

  // 컨테이너 크기에 맞춰 스케일 계산
  useEffect(() => {
    const updateScale = () => {
      if (containerRef.current) {
        const containerWidth = containerRef.current.offsetWidth;
        const designWidth = 1920; // HTML 디자인의 기본 너비
        const newScale = containerWidth / designWidth;
        setScale(newScale);
      }
    };

    updateScale();
    window.addEventListener('resize', updateScale);
    return () => window.removeEventListener('resize', updateScale);
  }, []);

  // iframe에 HTML 주입
  useEffect(() => {
    if (iframeRef.current && htmlCode) {
      const iframeDoc = iframeRef.current.contentDocument;
      if (!iframeDoc) return;

      const htmlContent = `
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
          ${htmlCode}
        </body>
        </html>
      `;

      iframeDoc.open();
      iframeDoc.write(htmlContent);
      iframeDoc.close();
    }
  }, [htmlCode]);

  const hasLivePreview = htmlCode && htmlCode.trim().length > 0;

  return (
    <div className="space-y-6">
      {/* Preview Container */}
      <div 
        ref={containerRef}
        className="relative overflow-hidden rounded-[32px] border border-gray-200 shadow-[0_25px_70px_rgba(0,0,0,0.12)] bg-white"
      >
        {hasLivePreview ? (
          <div className="relative w-full" style={{ paddingBottom: '66.67%' }}>
            <div className="absolute inset-0">
              <iframe
                ref={iframeRef}
                className="border-0 origin-top-left"
                style={{
                  transform: `scale(${scale})`,
                  width: `${100 / scale}%`,
                  height: `${100 / scale}%`,
                }}
                title="Live Design Preview"
                sandbox="allow-same-origin"
              />
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
