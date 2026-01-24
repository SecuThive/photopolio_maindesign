'use client';

import { useEffect, useState } from 'react';

interface ViewCountBadgeProps {
  designId: string;
  initialViews: number;
}

export default function ViewCountBadge({ designId, initialViews }: ViewCountBadgeProps) {
  const [views, setViews] = useState(() => Math.max(0, initialViews));

  useEffect(() => {
    if (!designId) {
      return;
    }

    const storageKey = `ui-syntax:viewed:${designId}`;

    const hasTracked = () => {
      try {
        if (typeof window === 'undefined') {
          return false;
        }
        const value = sessionStorage.getItem(storageKey);
        return value === 'recorded' || value === 'pending';
      } catch (error) {
        return false;
      }
    };

    const markPending = () => {
      try {
        if (typeof window !== 'undefined') {
            sessionStorage.setItem(storageKey, 'pending');
        }
      } catch (error) {
        /* no-op */
      }
    };

    const markRecorded = () => {
      try {
        if (typeof window !== 'undefined') {
          sessionStorage.setItem(storageKey, 'recorded');
        }
      } catch (error) {
        /* no-op */
      }
    };

    const clearPending = () => {
      try {
        if (typeof window !== 'undefined') {
          sessionStorage.removeItem(storageKey);
        }
      } catch (error) {
        /* no-op */
      }
    };

    if (hasTracked()) {
      return;
    }

    markPending();

    void fetch('/api/metrics/track', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ designId }),
      keepalive: true,
    })
      .then(async (response) => {
        if (!response.ok) {
          return;
        }
        const payload = await response.json().catch(() => null);
        if (payload && typeof payload.views === 'number') {
          setViews(payload.views);
        } else {
          setViews((prev) => prev + 1);
        }
        markRecorded();
      })
      .catch((error) => {
        clearPending();
        if (process.env.NODE_ENV === 'development') {
          console.warn('Failed to record page view', error);
        }
      });
  }, [designId]);

  return <span>{views.toLocaleString()}</span>;
}
