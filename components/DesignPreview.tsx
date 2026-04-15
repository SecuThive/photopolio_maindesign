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
const PREVIEW_MAX_HEIGHT = 2400;

function injectHeadMarkup(html: string) {
  const hasTailwind = /cdn\.tailwindcss\.com/.test(html);
  const hasHead = /<head[^>]*>/i.test(html);
  const hasHtml = /<html[^>]*>/i.test(html);
  const hasBody = /<body[^>]*>/i.test(html);

  // Tailwind CDN은 반드시 다른 스크립트보다 먼저 로드되어야 함
  const tailwindScript = !hasTailwind ? `<script src="${TAILWIND_CDN}"></script>` : '';

  // 프리뷰 안정화 CSS — 디자인 자체의 배경색/폰트는 건드리지 않음
  const previewFixes = `<style data-preview-fixes>
    *,*::before,*::after{box-sizing:border-box;}
    html{margin:0;padding:0;width:${PREVIEW_BASE_WIDTH}px;overflow-x:hidden;}
    body{margin:0;padding:0;width:${PREVIEW_BASE_WIDTH}px;min-height:auto;height:auto;overflow-x:hidden;}
    .min-h-screen,.min-h-\\[100vh\\]{min-height:auto!important;}
    .h-screen,.h-\\[100vh\\]{height:auto!important;}
    [class*="h-screen"]{height:auto!important;}
    [style*="100vh"]{min-height:auto!important;height:auto!important;}
    [style*="position: fixed"],[style*="position:fixed"]{position:sticky!important;}
    .fixed{position:sticky!important;}
  </style>`;

  const baseHead = [tailwindScript, previewFixes].filter(Boolean).join('\n');

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
  const iframeRef = useRef<HTMLIFrameElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const [scale, setScale] = useState(0.5);
  const DESIGN_WIDTH = PREVIEW_BASE_WIDTH;
  const DESIGN_HEIGHT = PREVIEW_BASE_HEIGHT;
  const [contentSize, setContentSize] = useState({ width: DESIGN_WIDTH, height: DESIGN_HEIGHT });
  const [iframeLoaded, setIframeLoaded] = useState(false);

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

  useEffect(() => {
    if (iframeRef.current && htmlCode) {
      const iframeDoc = iframeRef.current.contentDocument;
      if (!iframeDoc) return;

      setIframeLoaded(false);

      const trimmed = htmlCode.trim();
      const htmlContent = injectHeadMarkup(trimmed);

      iframeDoc.open();
      iframeDoc.write(htmlContent);
      iframeDoc.close();

      const measure = () => {
        const body = iframeRef.current?.contentDocument?.body;
        if (!body) return;
        const docEl = iframeRef.current?.contentDocument?.documentElement;
        // scrollHeight를 body와 documentElement 양쪽에서 측정하여 더 큰 값 사용
        const bodyH = body.scrollHeight;
        const docH = docEl?.scrollHeight ?? bodyH;
        const width = Math.max(body.scrollWidth, DESIGN_WIDTH);
        const height = Math.max(bodyH, docH, DESIGN_HEIGHT);
        setContentSize({ width, height });
        setIframeLoaded(true);
      };

      iframeRef.current.onload = measure;
      const timeouts = [100, 500, 1200, 2500, 4000].map((delay) => window.setTimeout(measure, delay));
      return () => {
        timeouts.forEach((id) => window.clearTimeout(id));
      };
    }
  }, [htmlCode, DESIGN_HEIGHT, DESIGN_WIDTH]);

  const hasLivePreview = htmlCode && htmlCode.trim().length > 0;
  const previewHeight = Math.min(contentSize.height * scale, PREVIEW_MAX_HEIGHT);

  return (
    <div
      ref={containerRef}
      className="relative w-full max-w-full overflow-hidden rounded-[32px] border border-gray-200 shadow-[0_25px_70px_rgba(0,0,0,0.12)]"
    >
      {hasLivePreview ? (
        <div className="relative w-full bg-gray-100" style={{ height: previewHeight }}>
          {/* 로딩 스켈레톤 — iframe이 로드되기 전까지 표시 */}
          {!iframeLoaded && (
            <div className="absolute inset-0 flex items-center justify-center bg-gray-100 z-10">
              <div className="flex items-center gap-3 text-xs text-gray-400">
                <span className="inline-flex h-6 w-6 items-center justify-center rounded-full border-2 border-gray-300 border-t-gray-600 animate-spin" />
                Loading preview
              </div>
            </div>
          )}
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
