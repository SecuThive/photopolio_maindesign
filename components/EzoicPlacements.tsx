"use client";

import { useEffect } from 'react';

interface EzoicPlacementsProps {
  placementIds: number[];
  wrapperClassName?: string;
}

declare global {
  interface Window {
    ezstandalone?: {
      cmd?: Array<() => void>;
      showAds?: (...ids: number[]) => void;
    };
  }
}

export default function EzoicPlacements({ placementIds, wrapperClassName }: EzoicPlacementsProps) {
  useEffect(() => {
    if (typeof window === 'undefined' || placementIds.length === 0) {
      return;
    }

    const ez = window.ezstandalone = window.ezstandalone || {};
    ez.cmd = ez.cmd || [];
    const uniqueIds = Array.from(new Set(placementIds));

    const enqueueShowAds = () => {
      try {
        if (typeof ez.showAds === 'function') {
          ez.showAds(...uniqueIds);
        }
      } catch (error) {
        // Ignore transient Ezoic script loading errors
        console.debug('Ezoic ads not ready:', error);
      }
    };

    // Run after a short delay so the SDK can initialize
    const timer = setTimeout(() => {
      if (ez.cmd) {
        ez.cmd.push(enqueueShowAds);
      }
    }, 100);

    return () => clearTimeout(timer);
  }, [placementIds]);

  if (placementIds.length === 0) {
    return null;
  }

  return (
    <div className={wrapperClassName} aria-label="Sponsored placements">
      {placementIds.map((id) => (
        <div key={id} className="py-8">
          <div id={`ezoic-pub-ad-placeholder-${id}`} />
        </div>
      ))}
    </div>
  );
}
