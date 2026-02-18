import type { Metadata } from 'next';
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import DesignRequestForm from '@/components/DesignRequestForm';
import DesignRequestBoard from '@/components/DesignRequestBoard';
import { createPageMetadata } from '@/lib/seo';

export const metadata: Metadata = createPageMetadata({
  title: 'Request a Design',
  description: 'Submit the exact UI design you want. We review requests and generate selected designs for the gallery.',
  path: '/request-design',
});

export default function RequestDesignPage() {
  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-8">
        <header className="space-y-4">
          <p className="text-xs uppercase tracking-[0.35em] text-gray-500">Community Requests</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 tracking-tight">Request a design</h1>
          <p className="text-lg text-gray-600 max-w-3xl">
            Tell us exactly what you need. Clear requests with practical constraints are prioritized.
          </p>
        </header>

        <DesignRequestForm />
        <DesignRequestBoard />
      </main>

      <Footer />
    </div>
  );
}
