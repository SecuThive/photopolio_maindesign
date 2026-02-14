import type { ReactNode } from 'react';
import Header from '@/components/Header';
import Footer from '@/components/Footer';

export default function CollectionsLayout({ children }: { children: ReactNode }) {
  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />
      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-12">
        {children}
      </main>
      <Footer />
    </div>
  );
}
