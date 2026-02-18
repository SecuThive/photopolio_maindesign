"use client";

import { FormEvent, useState } from 'react';

type Status = 'idle' | 'loading' | 'success' | 'error';

const CATEGORY_OPTIONS = [
  'Landing Page',
  'Dashboard',
  'E-commerce',
  'Portfolio',
  'Blog',
  'Components',
  'Other',
] as const;

export default function DesignRequestForm() {
  const [status, setStatus] = useState<Status>('idle');
  const [message, setMessage] = useState('');

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setStatus('loading');
    setMessage('');

    const form = event.currentTarget;
    const formData = new FormData(form);
    const payload = {
      title: String(formData.get('title') || '').trim(),
      description: String(formData.get('description') || '').trim(),
      category: String(formData.get('category') || '').trim(),
      target_audience: String(formData.get('target_audience') || '').trim(),
      reference_notes: String(formData.get('reference_notes') || '').trim(),
      requester_email: String(formData.get('requester_email') || '').trim(),
      homepage_url: String(formData.get('homepage_url') || '').trim(),
    };

    try {
      const response = await fetch('/api/design-requests', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data?.error || 'Failed to submit request.');
      }

      setStatus('success');
      setMessage('Request submitted. We will review it and generate it if selected.');
      form.reset();
    } catch (error) {
      setStatus('error');
      setMessage(error instanceof Error ? error.message : 'Failed to submit request.');
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-6 rounded-3xl border border-gray-200 bg-white p-6 sm:p-8 shadow-sm">
      <div className="grid gap-6 md:grid-cols-2">
        <div className="md:col-span-2">
          <label htmlFor="title" className="block text-sm font-semibold text-gray-900">Request title</label>
          <input
            id="title"
            name="title"
            required
            minLength={6}
            maxLength={120}
            placeholder="Ex: Cybersecurity SaaS pricing page with trust badges"
            className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
          />
        </div>

        <div className="md:col-span-2">
          <label htmlFor="description" className="block text-sm font-semibold text-gray-900">What should it include?</label>
          <textarea
            id="description"
            name="description"
            required
            minLength={30}
            maxLength={4000}
            rows={7}
            placeholder="Describe layout sections, tone, color direction, key UI blocks, and any constraints."
            className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
          />
        </div>

        <div>
          <label htmlFor="category" className="block text-sm font-semibold text-gray-900">Category</label>
          <select
            id="category"
            name="category"
            defaultValue="Landing Page"
            className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
          >
            {CATEGORY_OPTIONS.map((option) => (
              <option key={option} value={option}>{option}</option>
            ))}
          </select>
        </div>

        <div>
          <label htmlFor="target_audience" className="block text-sm font-semibold text-gray-900">Target audience (optional)</label>
          <input
            id="target_audience"
            name="target_audience"
            maxLength={160}
            placeholder="Ex: US B2B founders"
            className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
          />
        </div>

        <div className="md:col-span-2">
          <label htmlFor="reference_notes" className="block text-sm font-semibold text-gray-900">Reference notes (optional)</label>
          <textarea
            id="reference_notes"
            name="reference_notes"
            rows={3}
            maxLength={1000}
            placeholder="Mention reference sites, patterns, or style directions."
            className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
          />
        </div>

        <div>
          <label htmlFor="requester_email" className="block text-sm font-semibold text-gray-900">Email (optional)</label>
          <input
            id="requester_email"
            name="requester_email"
            type="email"
            maxLength={254}
            placeholder="you@company.com"
            className="mt-2 w-full rounded-xl border border-gray-300 px-4 py-3 text-sm text-gray-900 outline-none focus:border-gray-900"
          />
        </div>

        <div className="hidden" aria-hidden>
          <label htmlFor="homepage_url">Homepage URL</label>
          <input id="homepage_url" name="homepage_url" tabIndex={-1} autoComplete="off" />
        </div>
      </div>

      <button
        type="submit"
        disabled={status === 'loading'}
        className="inline-flex items-center rounded-full bg-gray-900 px-6 py-3 text-xs font-semibold uppercase tracking-[0.25em] text-white transition hover:bg-black disabled:opacity-60"
      >
        {status === 'loading' ? 'Submitting...' : 'Submit request'}
      </button>

      {message && (
        <p className={`text-sm ${status === 'success' ? 'text-emerald-700' : 'text-red-600'}`}>
          {message}
        </p>
      )}
    </form>
  );
}
