"use client";

import { useMemo, useState } from 'react';
import Link from 'next/link';
import ShareLinkButton from '@/components/ShareLinkButton';
import SaveDesignButton from '@/components/SaveDesignButton';

type RelatedLink = {
  title: string;
  href: string;
};

type DesignQuickActionsProps = {
  shareUrl: string;
  title: string;
  description?: string | null;
  imageUrl: string;
  designId: string;
  relatedPlaybooks: RelatedLink[];
  relatedCollections: RelatedLink[];
};

export default function DesignQuickActions({
  shareUrl,
  title,
  description,
  imageUrl,
  designId,
  relatedPlaybooks,
  relatedCollections,
}: DesignQuickActionsProps) {
  const [embedCopied, setEmbedCopied] = useState(false);

  const embedCode = useMemo(() => {
    const safeTitle = title || 'UI Syntax design';
    const altText = safeTitle.replace(/"/g, '&quot;');
    return `<a href="${shareUrl}" target="_blank" rel="noopener noreferrer"><img src="${imageUrl}" alt="${altText}" style="width:100%;max-width:1200px;height:auto;border-radius:16px;border:1px solid #e5e7eb" /></a>`;
  }, [imageUrl, shareUrl, title]);

  const handleCopyEmbed = async () => {
    try {
      await navigator.clipboard.writeText(embedCode);
      setEmbedCopied(true);
      window.setTimeout(() => setEmbedCopied(false), 2000);
    } catch (error) {
      console.error('Failed to copy embed code', error);
      setEmbedCopied(false);
    }
  };

  return (
    <div className="rounded-2xl border border-gray-200 bg-white/90 p-5 shadow-sm space-y-4">
      <div className="flex items-center justify-between">
        <div>
          <p className="text-[10px] uppercase tracking-[0.3em] text-gray-400">Quick actions</p>
          <h3 className="mt-1 text-lg font-semibold text-gray-900">Related · Share · Embed</h3>
        </div>
        <SaveDesignButton
          designId={designId}
          className="rounded-full border border-gray-900 px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.3em] text-gray-900 hover:bg-gray-900 hover:text-white transition"
          defaultLabel="Save"
          savedLabel="Saved"
        />
      </div>

      <div className="space-y-3 text-sm text-gray-700">
        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Related</p>
          <div className="mt-2 flex flex-wrap gap-2">
            {relatedPlaybooks.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-[11px] font-semibold text-gray-700 transition hover:border-gray-900 hover:text-gray-900"
              >
                {item.title}
              </Link>
            ))}
            {relatedCollections.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                className="rounded-full border border-gray-200 bg-gray-50 px-3 py-1 text-[11px] font-semibold text-gray-700 transition hover:border-gray-900 hover:text-gray-900"
              >
                {item.title}
              </Link>
            ))}
            {relatedPlaybooks.length === 0 && relatedCollections.length === 0 && (
              <span className="text-xs text-gray-500">No related links available.</span>
            )}
          </div>
        </div>

        <div className="flex flex-wrap items-center gap-2">
          <ShareLinkButton
            url={shareUrl}
            shareData={{ title: title, text: description || undefined }}
            className="rounded-full border border-gray-200 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.3em] text-gray-700 hover:border-gray-900 hover:text-gray-900"
            defaultLabel="Share"
            successLabel="Shared"
            copiedLabel="Copied"
          />
          <Link
            href="/saved"
            className="rounded-full border border-gray-200 px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.3em] text-gray-700 hover:border-gray-900 hover:text-gray-900"
          >
            View Saved
          </Link>
        </div>

        <div>
          <p className="text-xs uppercase tracking-[0.3em] text-gray-400">Embed</p>
          <div className="mt-2 flex items-center justify-between gap-2 rounded-xl border border-gray-100 bg-gray-50 px-3 py-2">
            <span className="text-[11px] text-gray-600 line-clamp-1">{embedCode}</span>
            <button
              type="button"
              onClick={handleCopyEmbed}
              className="rounded-full border border-gray-300 bg-white px-3 py-1 text-[10px] font-semibold uppercase tracking-[0.3em] text-gray-700 hover:border-gray-900 hover:text-gray-900"
            >
              {embedCopied ? 'Copied' : 'Copy'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
