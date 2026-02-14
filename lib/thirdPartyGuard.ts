const THIRD_PARTY_BLOCK_KEY = 'ui-syntax:third-party-block';
const DEFAULT_BLOCK_TTL = 30 * 60 * 1000; // 30 minutes
const SLOW_CONNECTION_TYPES = new Set(['slow-2g', '2g']);

type BlockSnapshot = {
  reason: string;
  expiresAt: number;
};

declare global {
  interface Window {
    __THIRD_PARTY_BLOCKED__?: boolean;
  }
}

function markDomState(blocked: boolean) {
  if (typeof document === 'undefined') {
    return;
  }

  const root = document.documentElement;
  if (blocked) {
    root.setAttribute('data-third-party', 'blocked');
  } else {
    root.removeAttribute('data-third-party');
  }
}

function setWindowFlag(blocked: boolean) {
  if (typeof window === 'undefined') {
    return;
  }
  window.__THIRD_PARTY_BLOCKED__ = blocked;
}

function readSnapshot(): BlockSnapshot | null {
  if (typeof window === 'undefined' || typeof window.localStorage === 'undefined') {
    return null;
  }

  try {
    const raw = window.localStorage.getItem(THIRD_PARTY_BLOCK_KEY);
    if (!raw) {
      return null;
    }

    const parsed = JSON.parse(raw) as BlockSnapshot;
    if (!parsed?.expiresAt || parsed.expiresAt <= Date.now()) {
      window.localStorage.removeItem(THIRD_PARTY_BLOCK_KEY);
      setWindowFlag(false);
      markDomState(false);
      return null;
    }

    return parsed;
  } catch (error) {
    if (process.env.NODE_ENV === 'development') {
      console.warn('Failed to read third-party guard snapshot', error);
    }
    return null;
  }
}

export function syncThirdPartyBlockFlag() {
  const snapshot = readSnapshot();
  const blocked = Boolean(snapshot);
  setWindowFlag(blocked);
  markDomState(blocked);
  return snapshot;
}

export function getThirdPartyBlockSnapshot() {
  return readSnapshot();
}

export function isThirdPartyBlocked(): boolean {
  if (typeof window === 'undefined') {
    return false;
  }

  if (window.__THIRD_PARTY_BLOCKED__) {
    return true;
  }

  return Boolean(readSnapshot());
}

export function setThirdPartyBlock(reason: string, ttlMs: number = DEFAULT_BLOCK_TTL) {
  if (typeof window === 'undefined' || typeof window.localStorage === 'undefined') {
    return null;
  }

  const snapshot: BlockSnapshot = {
    reason,
    expiresAt: Date.now() + ttlMs,
  };

  try {
    window.localStorage.setItem(THIRD_PARTY_BLOCK_KEY, JSON.stringify(snapshot));
  } catch (error) {
    if (process.env.NODE_ENV === 'development') {
      console.warn('Failed to persist third-party guard snapshot', error);
    }
  }

  setWindowFlag(true);
  markDomState(true);
  return snapshot;
}

export function clearThirdPartyBlock() {
  if (typeof window === 'undefined' || typeof window.localStorage === 'undefined') {
    return;
  }

  try {
    window.localStorage.removeItem(THIRD_PARTY_BLOCK_KEY);
  } catch (error) {
    if (process.env.NODE_ENV === 'development') {
      console.warn('Failed to clear third-party guard snapshot', error);
    }
  }

  setWindowFlag(false);
  markDomState(false);
}

export function shouldThrottleThirdPartyLoading() {
  if (typeof navigator === 'undefined') {
    return false;
  }

  const connection = (navigator as Navigator & { connection?: { saveData?: boolean; effectiveType?: string } }).connection;
  if (!connection) {
    return false;
  }

  if (connection.saveData) {
    return true;
  }

  if (connection.effectiveType && SLOW_CONNECTION_TYPES.has(connection.effectiveType)) {
    return true;
  }

  return false;
}

export function prefersReducedMotion() {
  if (typeof window === 'undefined' || typeof window.matchMedia !== 'function') {
    return false;
  }
  return window.matchMedia('(prefers-reduced-motion: reduce)').matches;
}

export function getGuardDebugInfo() {
  const snapshot = getThirdPartyBlockSnapshot();
  return {
    blocked: Boolean(snapshot || (typeof window !== 'undefined' && window.__THIRD_PARTY_BLOCKED__)),
    reason: snapshot?.reason ?? null,
    expiresAt: snapshot?.expiresAt ?? null,
  };
}