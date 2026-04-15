"use client";

import { useState, useRef, useEffect } from 'react';
import Image from 'next/image';

interface DesignPreviewProps {
  imageUrl: string;
  title: string;
  colors?: string[];
  htmlCode?: string | null;
}

const TAILWIND_CDN = 'https://cdn.tailwindcss.com';
const PREVIEW_BASE_WIDTH = 1400;
const PREVIEW_BASE_HEIGHT = Math.round((PREVIEW_BASE_WIDTH * 2) / 3);
// 컨테이너 최대 높이 — 길이가 긴 디자인도 잘리지 않도록 충분히 크게 설정
const PREVIEW_MAX_HEIGHT = 2400;

function injectHeadMarkup(html: string) {
  const hasTailwind = /cdn\.tailwindcss\.com/.test(html);
  const hasHead = /<head[^>]*>/i.test(html);
  const hasHtml = /<html[^>]*>/i.test(html);
  const hasBody = /<body[^>]*>/i.test(html);

  const baseHead = [
    '<meta charset="UTF-8" />',
    `<meta name="viewport" content="width=${PREVIEW_BASE_WIDTH}" />`,
    !hasTailwind ? `<script src="${TAILWIND_CDN}"></script>` : null,
    `<style>
      *,*::before,*::after{box-sizing:border-box;}
      html,body{margin:0;padding:0;width:${PREVIEW_BASE_WIDTH}px;background:white;min-height:auto;height:auto;overflow-x:hidden;}
      .min-h-screen,.h-screen,.min-h-\\[100vh\\],.h-\\[100vh\\]{min-height:auto!important;height:auto!important;}
      [class*="h-screen"]{height:auto!important;}
      [style*="100vh"]{min-height:auto!important;height:auto!important;}
      [style*="position: fixed"],[style*="position:fixed"]{position:sticky!important;}
      .fixed{position:sticky!important;}
    </style>`,
  ]
    .filter(Boolean)
    .join('\n');

  if (hasHead) {
    return html.replace(/<head[^>]*>/i, (match) => `${match}\n${baseHead}`);
  }

  if (hasHtml) {
    if (hasBody) {
      return html.replace(/<body[^>]*>/i, (match) => `<head>${baseHead}</head>\n${match}`);
    }
    return html.replace(/<html[^>]*>/i, (match) => `${match}\n<head>${baseHead}</head>`);
  }

  return `<!DOCTYPE html><html lang="en"><head>${baseHead}</head><body>${html}</body></html>`;
}

export default function DesignPreview({ imageUrl, title, colors, htmlCode }: DesignPreviewProps) {
  const [selectedColor, setSelectedColor] = useState<string | null>(null);
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(0.5);
  const DESIGN_WIDTH = PREVIEW_BASE_WIDTH;
  const DESIGN_HEIGHT = PREVIEW_BASE_HEIGHT; // keep 3:2 aspect
  const [contentSize, setContentSize] = useState({ width: DESIGN_WIDTH, height: DESIGN_HEIGHT });

  // Calculate the scale based on the current container width only
  // (height-based constraint is removed — tall pages should not be shrunk further)
  useEffect(() => {
    const updateScale = () => {
      if (containerRef.current) {
        const safeWidth = containerRef.current.clientWidth - 2;
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
      const htmlContent = injectHeadMarkup(trimmed);

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
      // Tailwind CDN + Google Fonts 로딩 대기를 위한 측정 간격 확대
      const timeouts = [100, 500, 1200, 2500, 4000].map((delay) => window.setTimeout(measure, delay));
      return () => {
        timeouts.forEach((id) => window.clearTimeout(id));
      };
    }
  }, [htmlCode, DESIGN_HEIGHT, DESIGN_WIDTH]);

  const hasLivePreview = htmlCode && htmlCode.trim().length > 0;
  const previewHeight = Math.min(contentSize.height * scale, PREVIEW_MAX_HEIGHT);
  // PREVIEW_MAX_HEIGHT는 2400으로 설정되어 있어 대부분의 디자인이 잘리지 않음

  return (
    <div
      ref={containerRef}
      className="relative w-full max-w-full overflow-hidden rounded-[32px] border border-gray-200 bg-white shadow-[0_25px_70px_rgba(0,0,0,0.12)]"
    >
      {hasLivePreview ? (
        <div className="relative w-full" style={{ height: previewHeight }}>
          <div className="absolute inset-0 overflow-hidden">
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
              scrolling="yes"
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
  );
}
