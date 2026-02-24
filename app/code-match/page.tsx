import Header from '@/components/Header';
import Footer from '@/components/Footer';
import RecommendationTester from '@/components/RecommendationTester';
import PopularSearchesGallery from '@/components/PopularSearchesGallery';
import { buildSoftwareApplicationSchema, buildHowToSchema, buildBreadcrumbSchema } from '@/lib/richSnippets';
import { getPublishedDesignCount } from '@/lib/siteStats';

export async function generateMetadata() {
  const publishedDesignCount = await getPublishedDesignCount();
  const countLabel = publishedDesignCount > 0 ? publishedDesignCount.toLocaleString('en-US') : 'published';
  return {
    title: 'Free Code Match Tool - Find Similar UI Designs Instantly',
    description: `Paste your HTML/React code and discover matching UI designs from ${countLabel} templates in the published gallery.`,
    openGraph: {
      title: 'Free Code Match Tool - Find Similar UI Designs Instantly',
      description: `Paste your code and find matching UI designs from ${countLabel} templates.`,
    },
  };
}

export default async function CodeMatchPage() {
  const publishedDesignCount = await getPublishedDesignCount();
  const countLabel = publishedDesignCount > 0 ? `${publishedDesignCount.toLocaleString('en-US')} published` : 'published';
  // Rich Snippets for better CTR
  const softwareSchema = buildSoftwareApplicationSchema({
    name: 'UI Syntax Code Match',
    description: `Free tool that analyzes your HTML/React code and finds matching UI designs from the ${countLabel} design gallery.`,
    url: 'https://ui-syntax.com/code-match',
    applicationCategory: 'DeveloperApplication',
    operatingSystem: 'Web Browser',
    offers: {
      price: '0',
      priceCurrency: 'USD',
    },
  });

  const howToSchema = buildHowToSchema({
    name: 'How to Use Code Match to Find UI Design Inspiration',
    description: 'Find matching UI designs by analyzing your code in 3 simple steps',
    totalTime: 'PT2M',
    steps: [
      {
        name: 'Paste Your Code',
        text: 'Copy and paste your HTML, JSX, or TSX code snippet into the code input field. Minimum 50 characters required.',
        url: 'https://ui-syntax.com/code-match',
      },
      {
        name: 'Analyze Structure',
        text: 'Our AI analyzer automatically detects layout patterns, color palettes, button count, and semantic structure.',
        url: 'https://ui-syntax.com/code-match',
      },
      {
        name: 'Get Matches',
        text: 'Receive 9 personalized design recommendations ranked by similarity score. View match percentage and quality metrics.',
        url: 'https://ui-syntax.com/code-match',
      },
    ],
  });

  const breadcrumbSchema = buildBreadcrumbSchema([
    { name: 'Home', url: 'https://ui-syntax.com' },
    { name: 'Code Match', url: 'https://ui-syntax.com/code-match' },
  ]);

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-white">
      {/* Structured Data for Rich Snippets */}
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(softwareSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(howToSchema) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(breadcrumbSchema) }}
      />

      <Header />

      <main className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-20 space-y-20">
        {/* Hero Section */}
        <section className="relative space-y-8 text-center">
          {/* Background decoration */}
          <div className="absolute -top-40 left-1/2 -translate-x-1/2 h-96 w-96 rounded-full bg-gradient-to-r from-emerald-100 to-cyan-100 blur-[120px] opacity-60" aria-hidden />
          
          <div className="relative space-y-5">
            <div className="inline-flex items-center gap-2 rounded-full bg-gradient-to-r from-emerald-50 to-cyan-50 border border-emerald-200 px-5 py-2">
              <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
              <p className="text-xs uppercase tracking-[0.35em] text-emerald-900 font-semibold">Labs · beta</p>
            </div>
            
            <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold text-gray-900 tracking-tight leading-[1.1]">
              Find Your Perfect
              <br />
              <span className="bg-gradient-to-r from-emerald-600 to-cyan-600 bg-clip-text text-transparent">
                Design Match
              </span>
            </h1>
            
            <p className="text-xl md:text-2xl text-gray-600 max-w-4xl mx-auto leading-relaxed font-light">
              Paste your HTML, JSX, or TSX code and discover the closest matching designs from our 
              <span className="font-semibold text-gray-900"> {countLabel} design collection</span>.
              Analyze structure, colors, and patterns instantly.
            </p>
          </div>
        </section>

        <RecommendationTester />

        <PopularSearchesGallery />

        {/* Features Section */}
        <section className="rounded-[40px] border border-gray-200 bg-white p-10 shadow-[0_25px_70px_rgba(15,23,42,0.08)] grid gap-8 md:grid-cols-3">
          {[
            {
              title: 'Code-aware scoring',
              body: 'We inspect the pasted HTML structure directly rather than guessing from captions, comparing layout depth, CTA count, and copy weight.',
              icon: '🎯',
              gradient: 'from-emerald-500 to-teal-500',
            },
            {
              title: 'Palette matching',
              body: 'HEX palettes are extracted automatically so you see shots with similar tones and can stay close to your brand guidelines.',
              icon: '🎨',
              gradient: 'from-cyan-500 to-blue-500',
            },
            {
              title: 'Instant handoff',
              body: 'Each recommendation links straight to a detail page where you can copy HTML, React code, and color regions without extra tooling.',
              icon: '⚡',
              gradient: 'from-purple-500 to-pink-500',
            },
          ].map((item) => (
            <article key={item.title} className="relative group space-y-4">
              <div className={`inline-flex items-center justify-center h-14 w-14 rounded-2xl bg-gradient-to-br ${item.gradient} text-3xl shadow-lg group-hover:scale-110 transition-transform duration-300`}>
                {item.icon}
              </div>
              <h3 className="text-xl font-bold text-gray-900">{item.title}</h3>
              <p className="text-base text-gray-600 leading-relaxed">{item.body}</p>
            </article>
          ))}
        </section>
      </main>

      <Footer />
    </div>
  );
}
