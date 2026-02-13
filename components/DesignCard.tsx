"use client";

import { CSSProperties, MouseEvent, useMemo, useState } from 'react';
import Image from 'next/image';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { DesignWithSlug } from '@/types/database';
import LikeButton from './LikeButton';

interface DesignCardProps {
  design: DesignWithSlug;
  likes: number;
  liked: boolean;
  onToggleLike: () => void;
  likeDisabled?: boolean;
  priority?: boolean;
  className?: string;
  style?: CSSProperties;
}

const categoryGlyphs: Record<string, string> = {
  'Landing Page': 'LP',
  'Dashboard': 'DB',
  'E-commerce': 'EC',
  'Portfolio': 'PF',
  'Blog': 'BG',
  'Components': 'CP',
};

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
  const router = useRouter();

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
      year: 'numeric',
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
    return preview.length > 160 ? `${preview.slice(0, 160)}…` : preview;
  }, [design.description]);

  const glyph = design.category ? categoryGlyphs[design.category] ?? 'ALL' : 'ALL';
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

  const handleViewDetail = (event: MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    event.stopPropagation();
    router.push(href);
  };

  const cardClassName = ['group block h-full cursor-pointer', className]
    .filter(Boolean)
    .join(' ');

  return (
    <Link
      href={href}
      className={cardClassName}
      style={style}
      aria-label={`${design.title} design details`}
    >
      <article className="flex h-full flex-col overflow-hidden rounded-[32px] border border-gray-100 bg-white/95 shadow-[0_12px_35px_rgba(15,23,42,0.08)] transition-transform duration-500 hover:-translate-y-1 hover:shadow-[0_35px_90px_rgba(15,23,42,0.14)]">
        <div className="relative h-64 w-full overflow-hidden bg-gray-100">
          <Image
            src={design.image_url}
            alt={design.title}
            fill
            priority={priority}
            loading={priority ? 'eager' : 'lazy'}
            className="h-full w-full object-cover object-top transition-transform duration-700 ease-out group-hover:scale-105"
            sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 25vw"
          />
          <div className="absolute inset-x-0 bottom-0 h-20 bg-gradient-to-t from-black/70 to-transparent" aria-hidden />
          <LikeButton likes={likes} liked={liked} onToggle={onToggleLike} disabled={likeDisabled} />
          <button
            type="button"
            onClick={handleCopyHtml}
            disabled={!design.code}
            className={`absolute bottom-4 right-3 inline-flex items-center gap-2 rounded-full border border-white/60 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.3em] text-white transition-colors ${
              copied ? 'bg-emerald-500/90 border-emerald-300 text-white' : 'bg-black/60 hover:bg-black'
            } disabled:opacity-40`}
          >
            {copied ? 'Copied' : 'Copy HTML'}
          </button>
        </div>

        <div className="flex flex-1 flex-col gap-4 p-6">
          <h3 className="font-display text-lg font-semibold text-gray-900 line-clamp-1 tracking-tight">
            {design.title}
          </h3>

          {buildSnippet && (
            <p className="text-sm text-gray-500 leading-relaxed line-clamp-2">
              {buildSnippet}
            </p>
          )}

          <div className="mt-auto flex items-center justify-between text-xs font-medium text-gray-500">
            <div className="flex items-center gap-2">
              <span className="text-xs font-semibold tracking-[0.25em] text-gray-600" aria-hidden>
                {glyph}
              </span>
              <span className="uppercase tracking-[0.25em] text-gray-400">
                {design.category || 'General'}
              </span>
            </div>
            <time className="tracking-wide" dateTime={design.created_at} suppressHydrationWarning>
              {formatDate(design.created_at)}
            </time>
          </div>

          <button
            type="button"
            onClick={handleViewDetail}
            className="inline-flex items-center justify-center rounded-full border border-gray-200 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.35em] text-gray-700 transition-colors hover:border-black hover:text-black"
          >
            View Detail
          </button>
        </div>
      </article>
    </Link>
  );
}
