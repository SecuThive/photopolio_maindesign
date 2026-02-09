import Header from '@/components/Header';
import Footer from '@/components/Footer';
import RecommendationTester from '@/components/RecommendationTester';

export const metadata = {
  title: 'Code Match | UI Syntax',
  description: 'A UI Syntax Labs tool that recommends AI designs based on the markup you paste into it.',
};

export default function CodeMatchPage() {
  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <main className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-16 space-y-16">
        <section className="space-y-6 text-center">
          <p className="text-xs uppercase tracking-[0.45em] text-gray-500">Labs · beta</p>
          <h1 className="text-4xl md:text-5xl font-semibold text-gray-900 tracking-tight">
            A recommendation engine that finds the closest AI designs to your code
          </h1>
          <p className="text-lg text-gray-600 max-w-3xl mx-auto">
            Paste HTML, JSX, or TSX snippets and we&apos;ll analyze layout structure, CTA density, and color palettes across 700+ UI Syntax designs to surface the closest references.
            Use it when you need ideas for refactors, creative direction for prompts, or investor-ready polish grounded in real markup.
          </p>
        </section>

        <RecommendationTester />

        <section className="rounded-[32px] border border-gray-200 bg-white p-8 shadow-[0_25px_70px_rgba(15,23,42,0.08)] grid gap-6 md:grid-cols-3">
          {[
            {
              title: 'Code-aware scoring',
              body: 'We inspect the pasted HTML structure directly rather than guessing from captions, comparing layout depth, CTA count, and copy weight.',
            },
            {
              title: 'Palette matching',
              body: 'HEX palettes are extracted automatically so you see shots with similar tones and can stay close to your brand guidelines.',
            },
            {
              title: 'Instant handoff',
              body: 'Each recommendation links straight to a detail page where you can copy HTML, React code, and color regions without extra tooling.',
            },
          ].map((item) => (
            <article key={item.title} className="space-y-3">
              <h3 className="text-lg font-semibold text-gray-900">{item.title}</h3>
              <p className="text-sm text-gray-600">{item.body}</p>
            </article>
          ))}
        </section>
      </main>

      <Footer />
    </div>
  );
}
