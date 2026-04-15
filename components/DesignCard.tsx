"use client";

import { CSSProperties, MouseEvent, useMemo, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { DesignWithSlug } from '@/types/database';
import LikeButton from './LikeButton';

interface DesignCardProps {
  design: DesignWithSlug;
  likes: number;
  liked: boolean;
  onToggleLike?: () => void;
  likeDisabled?: boolean;
  priority?: boolean;
  className?: string;
  style?: CSSProperties;
}

export default function DesignCard({
  design,
  likes,
  liked,
  onToggleLike,
  likeDisabled,
  priority = false,
  className,
  style,
}: DesignCardProps) {
  const [copied, setCopied] = useState(false);

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
    });
  };

  const buildSnippet = useMemo(() => {
    if (!design.description) return null;
    const trimmed = design.description.trim();
    if (!trimmed) return null;
    const sentences = trimmed
      .split(/(?<=[.!?])\s+/)
      .map((segment) => segment.trim())
      .filter(Boolean);
    const preview = sentences.slice(0, 2).join(' ') || trimmed;
    return preview.length > 120 ? `${preview.slice(0, 120)}...` : preview;
  }, [design.description]);

  const href = `/design/${design.slug}`;

  const handleCopyHtml = async (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    event.stopPropagation();
    if (!design.code) return;

    try {
      await navigator.clipboard.writeText(design.code);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch (error) {
      console.error('Failed to copy HTML code', error);
    }
  };

  const cardClassName = ['group block h-full', className].filter(Boolean).join(' ');

  return (
    <Link href={href} className={cardClassName} style={style} aria-label={`${design.title} — view details`}>
      <article className="flex h-full flex-col overflow-hidden rounded-xl border border-gray-200 bg-white transition-all duration-300 hover:border-gray-300 hover:shadow-lg">
        {/* Image */}
        <div className="relative aspect-[16/10] w-full overflow-hidden bg-gray-100">
          <Image
            src={design.image_url}
            alt={design.title}
            fill
            priority={priority}
            loading={priority ? 'eager' : 'lazy'}
            className="object-cover object-top transition-transform duration-500 ease-out group-hover:scale-[1.03]"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
          />
          {/* Overlay on hover */}
          <div className="absolute inset-0 bg-gradient-to-t from-black/60 via-transparent to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300" />

          {/* Copy button — visible on hover */}
          <div className="absolute bottom-3 right-3 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
            <button
              type="button"
              onClick={handleCopyHtml}
              disabled={!design.code}
              className={`inline-flex items-center gap-1.5 rounded-lg px-3 py-1.5 text-xs font-medium transition-colors backdrop-blur-sm ${
                copied
                  ? 'bg-emerald-500 text-white'
                  : 'bg-white/90 text-gray-900 hover:bg-white'
              } disabled:opacity-40`}
            >
              {copied ? (
                <>
                  <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M20 6 9 17l-5-5" /></svg>
                  Copied
                </>
              ) : (
                <>
                  <svg className="h-3.5 w-3.5" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><rect width="14" height="14" x="8" y="8" rx="2" /><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2" /></svg>
                  Copy HTML
                </>
              )}
            </button>
          </div>
        </div>

        {/* Content */}
        <div className="flex flex-1 flex-col gap-2 p-4">
          <h3 className="text-sm font-semibold text-gray-900 leading-snug line-clamp-1">
            {design.title}
          </h3>

          {buildSnippet && (
            <p className="text-xs text-gray-500 leading-relaxed line-clamp-2">
              {buildSnippet}
            </p>
          )}

          <div className="mt-auto flex items-center justify-between pt-2">
            <span className="inline-flex items-center rounded-md bg-gray-100 px-2 py-0.5 text-[11px] font-medium text-gray-600">
              {design.category || 'General'}
            </span>
            <div className="flex items-center gap-2">
              <time className="text-[11px] text-gray-400" dateTime={design.created_at} suppressHydrationWarning>
                {formatDate(design.created_at)}
              </time>
              <LikeButton
                likes={likes}
                liked={liked}
                onToggle={onToggleLike}
                disabled={likeDisabled || !onToggleLike}
                variant="card"
              />
            </div>
          </div>
        </div>
      </article>
    </Link>
  );
}
