"use client";

import { useEffect, useMemo, useState } from 'react';
import Link from 'next/link';

type RequestStatus = 'pending' | 'in_progress' | 'completed';

type RequestItem = {
  id: string;
  title: string;
  description: string;
  category: string | null;
  status: RequestStatus;
  voteCount: number;
  createdAt: string;
  linkedDesign: { slug: string | null; title: string } | null;
};

const VOTE_TOKEN_KEY = 'design_request_vote_token';
const VOTED_IDS_KEY = 'design_request_voted_ids';

function generateToken() {
  if (typeof crypto !== 'undefined' && typeof crypto.randomUUID === 'function') {
    return crypto.randomUUID();
  }
  return `dr-${Date.now()}-${Math.random().toString(16).slice(2)}`;
}

export default function DesignRequestBoard() {
  const [items, setItems] = useState<RequestItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [voteToken, setVoteToken] = useState<string | null>(null);
  const [votedIds, setVotedIds] = useState<Set<string>>(new Set());
  const [votingMap, setVotingMap] = useState<Record<string, boolean>>({});

  useEffect(() => {
    let mounted = true;

    const initLocalState = () => {
      try {
        const existingToken = localStorage.getItem(VOTE_TOKEN_KEY);
        if (existingToken) {
          setVoteToken(existingToken);
        } else {
          const freshToken = generateToken();
          localStorage.setItem(VOTE_TOKEN_KEY, freshToken);
          setVoteToken(freshToken);
        }

        const rawVoted = localStorage.getItem(VOTED_IDS_KEY);
        if (rawVoted) {
          const parsed = JSON.parse(rawVoted) as string[];
          setVotedIds(new Set(parsed));
        }
      } catch (_error) {
        setVoteToken(generateToken());
      }
    };

    const fetchRequests = async () => {
      setLoading(true);
      setError(null);
      try {
        const response = await fetch('/api/design-requests');
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data?.error || 'Failed to load requests.');
        }
        if (!mounted) return;
        setItems(Array.isArray(data.requests) ? data.requests : []);
      } catch (fetchError) {
        if (!mounted) return;
        setError(fetchError instanceof Error ? fetchError.message : 'Failed to load requests.');
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    initLocalState();
    fetchRequests();

    return () => {
      mounted = false;
    };
  }, []);

  const statusStyle = useMemo(() => ({
    pending: 'bg-amber-50 text-amber-700 border-amber-200',
    in_progress: 'bg-blue-50 text-blue-700 border-blue-200',
    completed: 'bg-emerald-50 text-emerald-700 border-emerald-200',
  }), []);

  const persistVotedIds = (next: Set<string>) => {
    setVotedIds(next);
    try {
      localStorage.setItem(VOTED_IDS_KEY, JSON.stringify(Array.from(next)));
    } catch (_error) {
      // no-op
    }
  };

  const handleVote = async (id: string) => {
    if (!voteToken || votedIds.has(id) || votingMap[id]) return;

    setVotingMap((prev) => ({ ...prev, [id]: true }));

    try {
      const response = await fetch(`/api/design-requests/${id}/vote`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ token: voteToken }),
      });
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.error || 'Failed to vote.');
      }

      setItems((prev) =>
        prev.map((item) =>
          item.id === id
            ? { ...item, voteCount: typeof data.voteCount === 'number' ? data.voteCount : item.voteCount }
            : item
        )
      );

      const next = new Set(votedIds);
      next.add(id);
      persistVotedIds(next);
    } catch (_error) {
      // no-op
    } finally {
      setVotingMap((prev) => {
        const next = { ...prev };
        delete next[id];
        return next;
      });
    }
  };

  return (
    <section className="space-y-5">
      <div>
        <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Live Queue</p>
        <h2 className="mt-2 text-2xl font-semibold text-gray-900">Top requested designs</h2>
      </div>

      {loading && (
        <div className="rounded-2xl border border-gray-200 bg-white p-6 space-y-4">
          <p className="text-sm text-gray-700 leading-relaxed">
            The live request queue appears after hydration. In the meantime, submit your request above with project
            context, target audience, and required constraints.
          </p>
          <div className="flex flex-wrap gap-3">
            <Link
              href="#request-form"
              className="inline-flex items-center rounded-full border border-gray-900 bg-gray-900 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-white transition hover:bg-black"
            >
              Submit Request
            </Link>
            <Link
              href="/collections"
              className="inline-flex items-center rounded-full border border-gray-300 bg-white px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-gray-700 transition hover:border-gray-900 hover:text-gray-900"
            >
              View Examples
            </Link>
          </div>
        </div>
      )}
      {error && <div className="rounded-2xl border border-red-200 bg-red-50 p-6 text-sm text-red-700">{error}</div>}

      {!loading && !error && items.length === 0 && (
        <div className="rounded-2xl border border-dashed border-gray-300 bg-white p-6 space-y-4">
          <p className="text-sm text-gray-700">
            No requests are in the queue yet. Start with a focused brief so other builders can vote it up.
          </p>
          <Link
            href="#request-form"
            className="inline-flex items-center rounded-full border border-gray-900 px-4 py-2 text-[11px] font-semibold uppercase tracking-[0.25em] text-gray-900 transition hover:bg-gray-900 hover:text-white"
          >
            Add First Request
          </Link>
        </div>
      )}

      {!loading && !error && items.length > 0 && (
        <div className="space-y-4">
          {items.map((item) => (
            <article key={item.id} className="rounded-2xl border border-gray-200 bg-white p-5 shadow-sm">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <h3 className="text-lg font-semibold text-gray-900">{item.title}</h3>
                <div className="flex items-center gap-2">
                  <span className={`rounded-full border px-3 py-1 text-[11px] font-semibold uppercase tracking-[0.2em] ${statusStyle[item.status]}`}>
                    {item.status.replace('_', ' ')}
                  </span>
                  <button
                    type="button"
                    onClick={() => handleVote(item.id)}
                    disabled={votedIds.has(item.id) || !!votingMap[item.id]}
                    className="rounded-full border border-gray-300 px-3 py-1 text-xs font-semibold uppercase tracking-[0.2em] text-gray-700 hover:border-gray-900 hover:text-gray-900 disabled:opacity-50"
                  >
                    ▲ {item.voteCount}
                  </button>
                </div>
              </div>

              <p className="mt-3 text-sm text-gray-600 leading-relaxed">{item.description}</p>

              <div className="mt-4 flex flex-wrap items-center gap-3 text-xs text-gray-500">
                {item.category && <span>{item.category}</span>}
                <span>{new Date(item.createdAt).toLocaleDateString('en-US')}</span>
                {item.linkedDesign?.slug && (
                  <Link
                    href={`/design/${item.linkedDesign.slug}`}
                    className="font-semibold uppercase tracking-[0.2em] text-emerald-700 hover:text-emerald-800"
                  >
                    View generated design
                  </Link>
                )}
              </div>
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
