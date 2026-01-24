'use client';

import { useEffect } from 'react';

interface ViewTrackerProps {
  designId: string;
}

export default function ViewTracker({ designId }: ViewTrackerProps) {
  useEffect(() => {
    if (!designId) {
      return;
    }

    const storageKey = `ui-syntax:viewed:${designId}`;
    const hasTracked = () => {
      try {
        return typeof window !== 'undefined' && sessionStorage.getItem(storageKey);
      } catch (error) {
        return false;
      }
    };

    const markTracked = () => {
      try {
        if (typeof window !== 'undefined') {
          sessionStorage.setItem(storageKey, '1');
        }
      } catch (error) {
        /* no-op */
      }
    };

    if (hasTracked()) {
      return;
    }

    void fetch('/api/metrics/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ designId }),
      keepalive: true,
    })
      .then((response) => {
        if (response.ok) {
          markTracked();
        }
      })
      .catch((error) => {
        if (process.env.NODE_ENV === 'development') {
          console.warn('Failed to record page view', error);
        }
      });
  }, [designId]);

  return null;
}
