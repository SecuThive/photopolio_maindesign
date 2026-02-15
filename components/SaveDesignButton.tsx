"use client";

import { useEffect, useState } from 'react';

const STORAGE_KEY = 'saved_design_ids';

type SaveDesignButtonProps = {
  designId: string;
  className?: string;
  defaultLabel?: string;
  savedLabel?: string;
};

function readSavedIds(): Set<string> {
  if (typeof window === 'undefined') {
    return new Set();
  }

  try {
    const stored = window.localStorage.getItem(STORAGE_KEY);
    if (!stored) return new Set();
    const parsed = JSON.parse(stored) as string[];
    return new Set(parsed);
  } catch (error) {
    console.warn('Failed to read saved designs', error);
    return new Set();
  }
}

function writeSavedIds(ids: Set<string>) {
  if (typeof window === 'undefined') return;
  try {
    window.localStorage.setItem(STORAGE_KEY, JSON.stringify(Array.from(ids)));
  } catch (error) {
    console.warn('Failed to persist saved designs', error);
  }
}

export default function SaveDesignButton({
  designId,
  className,
  defaultLabel = 'Save',
  savedLabel = 'Saved',
}: SaveDesignButtonProps) {
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const ids = readSavedIds();
    setSaved(ids.has(designId));
  }, [designId]);

  const toggleSaved = () => {
    const ids = readSavedIds();
    if (ids.has(designId)) {
      ids.delete(designId);
      setSaved(false);
    } else {
      ids.add(designId);
      setSaved(true);
    }
    writeSavedIds(ids);
  };

  return (
    <button
      type="button"
      onClick={toggleSaved}
      aria-pressed={saved}
      className={className}
    >
      {saved ? savedLabel : defaultLabel}
    </button>
  );
}
