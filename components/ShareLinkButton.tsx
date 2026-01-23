"use client";

import { useRef, useState } from 'react';

export type SharePayload = {
  title?: string;
  text?: string;
};

interface ShareLinkButtonProps {
  url: string;
  shareData?: SharePayload;
  className?: string;
  icon?: React.ReactNode;
  defaultLabel?: string;
  successLabel?: string;
  copiedLabel?: string;
}

export default function ShareLinkButton({
  url,
  shareData,
  className = '',
  icon,
  defaultLabel = 'Share',
  successLabel = 'Shared successfully',
  copiedLabel = 'Link copied',
}: ShareLinkButtonProps) {
  const [message, setMessage] = useState<string | null>(null);
  const timeoutRef = useRef<number | null>(null);

  const clearExistingTimeout = () => {
    if (timeoutRef.current && typeof window !== 'undefined') {
      window.clearTimeout(timeoutRef.current);
      timeoutRef.current = null;
    }
  };

  const showMessage = (text: string) => {
    setMessage(text);
    if (typeof window !== 'undefined') {
      clearExistingTimeout();
      timeoutRef.current = window.setTimeout(() => setMessage(null), 2500);
    }
  };

  const handleShare = async () => {
    try {
      if (navigator.share && typeof navigator.share === 'function') {
        await navigator.share({ url, ...(shareData || {}) });
        showMessage(successLabel);
        return;
      }

      await navigator.clipboard.writeText(url);
      showMessage(copiedLabel);
    } catch (error) {
      console.warn('Share failed, attempting copy fallback', error);
      try {
        await navigator.clipboard.writeText(url);
        showMessage(copiedLabel);
      } catch (clipboardError) {
        console.error('Clipboard write failed', clipboardError);
        showMessage('Unable to share link');
      }
    }
  };

  return (
    <button
      type="button"
      onClick={handleShare}
      className={`flex items-center gap-2 transition-colors ${className}`}
    >
      {icon}
      <span>{message ?? defaultLabel}</span>
    </button>
  );
}
