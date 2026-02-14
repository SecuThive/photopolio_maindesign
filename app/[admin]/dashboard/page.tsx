'use client';

import { useState, useEffect, useCallback, useRef } from 'react';
import { useRouter, useParams } from 'next/navigation';
import { notFound } from 'next/navigation';
import { supabase } from '@/lib/supabase/client';
import { Design } from '@/types/database';
import Image from 'next/image';

interface MetricsSummary {
  totalDesigns: number;
  totalViews: number;
  todayViews: number;
  categoryCounts: { category: string; count: number }[];
  dailyViews: { date: string; count: number }[];
}

const NOTE_FIELD_CONFIG = [
  {
    name: 'strategy_notes',
    label: 'Strategy Notes',
    helper: 'Value prop structure, ICP, conversion promise.',
    placeholder: 'Hero promise, CTA framing, laddered narrative…',
  },
  {
    name: 'psychology_notes',
    label: 'Psychology Notes',
    helper: 'Behavioral cues, trust signals, bias levers.',
    placeholder: 'Social proof orbit, urgency pattern, reciprocity cues…',
  },
  {
    name: 'usage_notes',
    label: 'Usage Notes',
    helper: 'Interaction model, density, navigation guidance.',
    placeholder: 'Primary flows, command palette behavior, responsive states…',
  },
  {
    name: 'performance_notes',
    label: 'Performance Notes',
    helper: 'Core Web Vitals guardrails, rendering strategy.',
    placeholder: 'LCP budget, streaming/lazy load plan, asset compression…',
  },
  {
    name: 'accessibility_notes',
    label: 'Accessibility Notes',
    helper: 'Contrast, focus, motion, language considerations.',
    placeholder: 'ARIA hooks, focus outlines, reduced motion handling…',
  },
] as const;

const normalizeOptionalText = (value: FormDataEntryValue | null) => {
  if (typeof value !== 'string') {
    return null;
  }
  const trimmed = value.trim();
  return trimmed.length ? trimmed : null;
};

export default function AdminDashboardPage() {
  const [designs, setDesigns] = useState<Design[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploading, setUploading] = useState(false);
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [metricsLoading, setMetricsLoading] = useState(true);
  const [isValidPath, setIsValidPath] = useState(false);
  const [selectedIds, setSelectedIds] = useState<string[]>([]);
  const [bulkDeleting, setBulkDeleting] = useState(false);
  const selectAllCheckboxRef = useRef<HTMLInputElement | null>(null);
  const router = useRouter();
  const params = useParams();
  const hasSelection = selectedIds.length > 0;
  const isSelectAllChecked = designs.length > 0 && selectedIds.length === designs.length;
  const formatNumber = (value: number) => new Intl.NumberFormat('en-US').format(value);
  const formatDayLabel = (date: string) =>
    new Date(date).toLocaleDateString('en-US', { month: 'numeric', day: 'numeric' });
  const dailyViews = metrics?.dailyViews ?? [];
  const maxDailyValue = dailyViews.reduce((max, day) => Math.max(max, day.count), 0);
  const normalizedDailyMax = Math.max(maxDailyValue, 1);

  useEffect(() => {
    // Validate the secret path before allowing dashboard access
    const checkPath = async () => {
      const response = await fetch('/api/admin/verify', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ path: params.admin }),
      });
      
      if (response.ok) {
        setIsValidPath(true);
      } else {
        notFound();
      }
    };
    
    checkPath();
  }, [params.admin]);

  const checkAuth = useCallback(async () => {
    try {
      const response = await fetch('/api/admin/verify');
      if (!response.ok) {
        router.push(`/${params.admin}`);
      }
    } catch (err) {
      router.push(`/${params.admin}`);
    }
  }, [router, params.admin]);

  const loadDesigns = useCallback(async () => {
    setLoading(true);
    try {
      const { data, error } = await supabase
        .from('designs')
        .select('*')
        .eq('status', 'published')
        .order('created_at', { ascending: false });

      if (error) throw error;
      if (data) setDesigns(data);
    } catch (error) {
      console.error('Error loading designs:', error);
    } finally {
      setLoading(false);
    }
  }, []);

  const loadMetrics = useCallback(async () => {
    setMetricsLoading(true);
    try {
      const response = await fetch('/api/admin/metrics');
      if (!response.ok) {
        throw new Error('Failed to load metrics');
      }
      const data = await response.json();
      setMetrics(data);
    } catch (error) {
      console.error('Error loading metrics:', error);
    } finally {
      setMetricsLoading(false);
    }
  }, []);

  useEffect(() => {
    if (isValidPath) {
      checkAuth();
      loadDesigns();
      loadMetrics();
    }
  }, [isValidPath, checkAuth, loadDesigns, loadMetrics]);

  useEffect(() => {
    const validIdSet = new Set(designs.map((design) => design.id));
    setSelectedIds((prev) => {
      const next = prev.filter((id) => validIdSet.has(id));
      return next.length === prev.length ? prev : next;
    });
  }, [designs]);

  useEffect(() => {
    if (selectAllCheckboxRef.current) {
      selectAllCheckboxRef.current.indeterminate = hasSelection && !isSelectAllChecked;
    }
  }, [hasSelection, isSelectAllChecked]);

  if (!isValidPath) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
          <p className="mt-4 text-gray-600">Verifying...</p>
        </div>
      </div>
    );
  }

  const toggleSelectAll = () => {
    if (isSelectAllChecked) {
      setSelectedIds([]);
    } else {
      setSelectedIds(designs.map((design) => design.id));
    }
  };

  const toggleSelect = (id: string) => {
    setSelectedIds((prev) =>
      prev.includes(id) ? prev.filter((existing) => existing !== id) : [...prev, id]
    );
  };

  const handleBulkDelete = async () => {
    const idsToDelete = [...selectedIds];
    if (!idsToDelete.length) return;

    if (
      !confirm(
        `Are you sure you want to delete ${idsToDelete.length} selected design${
          idsToDelete.length > 1 ? 's' : ''
        }?`
      )
    ) {
      return;
    }

    setBulkDeleting(true);

    try {
      const response = await fetch('/api/admin/designs/bulk-delete', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ ids: idsToDelete }),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData?.error || 'Failed to delete designs');
      }

      setSelectedIds([]);
      loadDesigns();
      loadMetrics();
    } catch (error) {
      console.error('Error deleting designs:', error);
      alert('An error occurred while deleting the selected designs.');
    } finally {
      setBulkDeleting(false);
    }
  };
  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this design?')) return;

    try {
      const response = await fetch(`/api/admin/designs/${id}`, {
        method: 'DELETE',
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData?.error || 'Failed to delete design');
      }

      setSelectedIds((prev) => prev.filter((selectedId) => selectedId !== id));
      // Reload designs
      loadDesigns();
      loadMetrics();
    } catch (error) {
      console.error('Error deleting design:', error);
      alert('An error occurred while deleting.');
    }
  };

  const handleUpload = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setUploading(true);

    const formData = new FormData(e.currentTarget);
    const file = formData.get('file') as File;
    const titleValue = formData.get('title');
    const description = normalizeOptionalText(formData.get('description'));
    const category = normalizeOptionalText(formData.get('category'));
    const code = normalizeOptionalText(formData.get('code'));
    const notePayload: Record<string, string | null> = {};

    NOTE_FIELD_CONFIG.forEach((field) => {
      notePayload[field.name] = normalizeOptionalText(formData.get(field.name));
    });

    const title = typeof titleValue === 'string' ? titleValue.trim() : '';

    if (!title) {
      alert('Title is required.');
      setUploading(false);
      return;
    }

    try {
      // Upload to Supabase Storage
      const fileName = `${Date.now()}_${file.name}`;
      const { data: uploadData, error: uploadError } = await supabase.storage
        .from('designs-bucket')
        .upload(`designs/${fileName}`, file);

      if (uploadError) throw uploadError;

      // Get public URL
      const { data: { publicUrl } } = supabase.storage
        .from('designs-bucket')
        .getPublicUrl(`designs/${fileName}`);

      // Insert into database
      const designData = {
        title,
        description,
        category,
        code,
        image_url: publicUrl,
        ...notePayload,
      };

      const { error: dbError } = await (supabase as any)
        .from('designs')
        .insert(designData);

      if (dbError) throw dbError;

      // Reset form and reload
      (e.target as HTMLFormElement).reset();
      loadDesigns();
      loadMetrics();
      alert('Upload complete!');
    } catch (error) {
      console.error('Error uploading:', error);
      alert('An error occurred during upload.');
    } finally {
      setUploading(false);
    }
  };

  const handleLogout = async () => {
    await fetch('/api/admin/logout', { method: 'POST' });
    router.push('/admin');
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4 flex justify-between items-center">
          <h1 className="text-2xl font-bold text-gray-900">Admin Dashboard</h1>
          <div className="flex gap-4">
            <a href="/" className="text-blue-600 hover:text-blue-700">
              Main Site
            </a>
            <button onClick={handleLogout} className="text-red-600 hover:text-red-700">
              Log out
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Site Insights</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { label: "Today's visitors", value: metrics?.todayViews ?? 0 },
              { label: 'Total visitors', value: metrics?.totalViews ?? 0 },
              { label: 'Published designs', value: metrics?.totalDesigns ?? designs.length },
            ].map(({ label, value }) => (
              <div key={label} className="bg-white rounded-lg shadow p-6 border border-gray-100">
                <p className="text-sm text-gray-500">{label}</p>
                {metricsLoading ? (
                  <div className="mt-4 h-8 bg-gray-100 animate-pulse rounded" />
                ) : (
                  <p className="mt-2 text-3xl font-bold text-gray-900">{formatNumber(value)}</p>
                )}
              </div>
            ))}
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 mt-6">
            <div className="bg-white rounded-lg shadow p-6 border border-gray-100 lg:col-span-2">
              <div className="flex justify-between items-center mb-4">
                <div>
                  <p className="text-sm text-gray-500">Last 7 days trend</p>
                  <p className="text-lg font-semibold text-gray-900">Daily page views</p>
                </div>
              </div>
              {metricsLoading ? (
                <div className="h-48 bg-gray-50 rounded animate-pulse" />
              ) : (
                <div className="h-48 flex items-end gap-4">
                  {dailyViews.map((day) => {
                    const height = (day.count / normalizedDailyMax) * 100;
                    return (
                      <div key={day.date} className="flex-1">
                        <div
                          className="bg-blue-500 rounded-t"
                          style={{ height: `${height}%` }}
                        ></div>
                        <div className="mt-2 text-xs text-gray-500 text-center">
                          <div>{formatDayLabel(day.date)}</div>
                          <div className="font-semibold text-gray-900">{day.count}</div>
                        </div>
                      </div>
                    );
                  })}
                </div>
              )}
            </div>

            <div className="bg-white rounded-lg shadow p-6 border border-gray-100">
              <p className="text-sm text-gray-500">Designs per category</p>
              {metricsLoading ? (
                <div className="mt-4 space-y-3">
                  {Array.from({ length: 5 }).map((_, idx) => (
                    <div key={idx} className="h-6 bg-gray-100 rounded animate-pulse" />
                  ))}
                </div>
              ) : (
                <div className="mt-4 space-y-3">
                  {(metrics?.categoryCounts ?? []).map((item) => (
                    <div key={item.category} className="flex items-center justify-between">
                      <span className="text-sm text-gray-700">{item.category}</span>
                      <span className="text-sm font-semibold text-gray-900">
                        {formatNumber(item.count)}
                      </span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Upload Form */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold text-gray-900 mb-4">Upload a new design</h2>
          <form onSubmit={handleUpload} className="space-y-4">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Image file
                </label>
                <input
                  type="file"
                  name="file"
                  accept="image/*"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>
              
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Title
                </label>
                <input
                  type="text"
                  name="title"
                  required
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Category
                </label>
                <select
                  name="category"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                >
                  <option value="">No selection</option>
                  <option value="Landing Page">Landing Page</option>
                  <option value="Dashboard">Dashboard</option>
                  <option value="E-commerce">E-commerce</option>
                  <option value="Portfolio">Portfolio</option>
                  <option value="Blog">Blog</option>
                  <option value="Components">Components</option>
                </select>
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Description
                </label>
                <textarea
                  name="description"
                  rows={3}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md"
                />
              </div>

              <div className="md:col-span-2 border border-gray-200 rounded-xl p-4">
                <div className="flex flex-col gap-1 sm:flex-row sm:items-center sm:justify-between">
                  <div>
                    <p className="text-[11px] font-semibold uppercase tracking-[0.3em] text-gray-400">
                      Strategy fields
                    </p>
                    <h3 className="text-lg font-semibold text-gray-900">Execution notes</h3>
                  </div>
                  <p className="text-xs text-gray-500">Shown on the public detail page</p>
                </div>
                <div className="mt-4 grid gap-4 md:grid-cols-2">
                  {NOTE_FIELD_CONFIG.map((field) => (
                    <label key={field.name} className="flex flex-col gap-2">
                      <div>
                        <span className="text-sm font-medium text-gray-700">{field.label}</span>
                        <p className="text-xs text-gray-500">{field.helper}</p>
                      </div>
                      <textarea
                        name={field.name}
                        rows={4}
                        placeholder={field.placeholder}
                        className="w-full rounded-md border border-gray-300 px-3 py-2 text-sm"
                      />
                    </label>
                  ))}
                </div>
              </div>

              <div className="md:col-span-2">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Source code (HTML/CSS/JavaScript)
                </label>
                <textarea
                  name="code"
                  rows={8}
                  placeholder="<!DOCTYPE html>&#10;<html>&#10;<head>&#10;  <title>Design</title>&#10;</head>&#10;<body>&#10;  <!-- Your code here -->&#10;</body>&#10;</html>"
                  className="w-full px-3 py-2 border border-gray-300 rounded-md font-mono text-sm"
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={uploading}
              className="w-full px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {uploading ? 'Uploading...' : 'Upload'}
            </button>
          </form>
        </div>

        {/* Designs List */}
        <div className="bg-white rounded-lg shadow">
          <div className="px-6 py-4 border-b border-gray-200 flex flex-col gap-3 md:flex-row md:items-center md:justify-between">
            <div>
              <h2 className="text-xl font-bold text-gray-900">
                Published designs ({designs.length})
              </h2>
              <p className="text-sm text-gray-500">
                {hasSelection ? `${selectedIds.length} selected` : 'Select rows to enable bulk actions'}
              </p>
            </div>
            <button
              type="button"
              onClick={handleBulkDelete}
              disabled={!hasSelection || bulkDeleting}
              className="inline-flex items-center justify-center rounded-md bg-red-600 px-4 py-2 text-sm font-medium text-white hover:bg-red-700 disabled:cursor-not-allowed disabled:opacity-50"
            >
              {bulkDeleting ? 'Deleting...' : 'Delete selected'}
            </button>
          </div>
          
          {loading ? (
            <div className="p-12 text-center">
              <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-gray-900 mx-auto"></div>
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="min-w-full divide-y divide-gray-200">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider w-12">
                      <span className="sr-only">Select all</span>
                      <input
                        ref={selectAllCheckboxRef}
                        type="checkbox"
                        className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                        checked={isSelectAllChecked}
                        onChange={toggleSelectAll}
                        disabled={designs.length === 0}
                      />
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Image
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Title
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Category
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Created
                    </th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody className="bg-white divide-y divide-gray-200">
                  {designs.map((design) => (
                    <tr key={design.id}>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <input
                          type="checkbox"
                          className="h-4 w-4 rounded border-gray-300 text-blue-600 focus:ring-blue-500"
                          checked={selectedIds.includes(design.id)}
                          onChange={() => toggleSelect(design.id)}
                        />
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="relative h-16 w-24">
                          <Image
                            src={design.image_url}
                            alt={design.title}
                            fill
                            className="object-cover rounded"
                            sizes="96px"
                          />
                        </div>
                      </td>
                      <td className="px-6 py-4">
                        <div className="text-sm font-medium text-gray-900">
                          {design.title}
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-2 py-1 text-xs rounded-full bg-blue-100 text-blue-700">
                          {design.category || '-'}
                        </span>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                        {new Date(design.created_at).toLocaleDateString('en-US')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm">
                        <button
                          onClick={() => handleDelete(design.id)}
                          className="text-red-600 hover:text-red-900"
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </main>
    </div>
  );
}