import type { NextWebVitalsMetric } from 'next/app';
import { isThirdPartyBlocked, setThirdPartyBlock, syncThirdPartyBlockFlag } from '@/lib/thirdPartyGuard';

type MetricName = 'CLS' | 'FCP' | 'FID' | 'INP' | 'LCP' | 'TTFB';

type Rating = 'good' | 'needs-improvement' | 'poor';

type Threshold = {
  good: number;
  poor: number;
};

const WEB_VITAL_THRESHOLDS: Record<MetricName, Threshold> = {
  CLS: { good: 0.1, poor: 0.25 },
  FCP: { good: 1800, poor: 3000 },
  FID: { good: 100, poor: 300 },
  INP: { good: 200, poor: 500 },
  LCP: { good: 2500, poor: 4000 },
  TTFB: { good: 800, poor: 1800 },
};

const BLOCK_GUARD_METRICS = new Set<MetricName>(['CLS', 'INP', 'LCP']);
const METRIC_ENDPOINT = process.env.NEXT_PUBLIC_VITALS_ENDPOINT || '/api/metrics/web-vitals';

const connectionInfo = () => {
  if (typeof navigator === 'undefined') {
    return null;
  }
  const connection = (navigator as Navigator & { connection?: { effectiveType?: string; saveData?: boolean } }).connection;
  if (!connection) {
    return null;
  }
  return {
    effectiveType: connection.effectiveType ?? null,
    saveData: connection.saveData ?? null,
  };
};

function getMetricRating(metric: NextWebVitalsMetric): Rating {
  const thresholds = WEB_VITAL_THRESHOLDS[metric.name as MetricName];
  if (!thresholds) {
    return 'good';
  }

  if (metric.value <= thresholds.good) {
    return 'good';
  }

  if (metric.value <= thresholds.poor) {
    return 'needs-improvement';
  }

  return 'poor';
}

function sendMetric(metric: NextWebVitalsMetric, rating: Rating, blockedThirdParty: boolean) {
  if (typeof window === 'undefined') {
    return;
  }

  const withDelta = metric as NextWebVitalsMetric & { delta?: number };
  const deltaValue = typeof withDelta.delta === 'number'
    ? Number(withDelta.delta.toFixed(4))
    : null;

  const body = {
    metric: metric.name,
    value: Number(metric.value.toFixed(4)),
    delta: deltaValue,
    rating,
    label: metric.label,
    id: metric.id,
    page: (metric as NextWebVitalsMetric & { path?: string }).path ?? window.location.pathname,
    navigationType: (metric as NextWebVitalsMetric & { navigationType?: string }).navigationType ?? null,
    blockedThirdParty,
    connection: connectionInfo(),
  };

  const payload = JSON.stringify(body);

  try {
    if (typeof navigator !== 'undefined' && 'sendBeacon' in navigator && typeof Blob !== 'undefined') {
      const blob = new Blob([payload], { type: 'application/json' });
      navigator.sendBeacon(METRIC_ENDPOINT, blob);
    } else {
      void fetch(METRIC_ENDPOINT, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: payload,
        keepalive: true,
      }).catch(() => undefined);
    }
  } catch (error) {
    if (process.env.NODE_ENV === 'development') {
      console.warn('Failed to send web vitals metric', error);
    }
  }
}

if (typeof window !== 'undefined') {
  syncThirdPartyBlockFlag();
}

export function reportWebVitals(metric: NextWebVitalsMetric) {
  const rating = getMetricRating(metric);
  const shouldBlock = rating === 'poor' && BLOCK_GUARD_METRICS.has(metric.name as MetricName) && !isThirdPartyBlocked();

  if (shouldBlock) {
    setThirdPartyBlock(`poor-${metric.name}`);
  }

  sendMetric(metric, rating, shouldBlock || isThirdPartyBlocked());
}
