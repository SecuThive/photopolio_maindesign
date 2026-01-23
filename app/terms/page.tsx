import type { Metadata } from "next";
import Link from 'next/link';
import SimpleHeader from '@/components/SimpleHeader';
import EzoicPlacements from '@/components/EzoicPlacements';
import { getPlacementIds } from '@/lib/ezoic';

export const metadata: Metadata = {
  title: "Terms and Conditions",
  description: "Read UI Syntax's Terms and Conditions. Learn about the rules and regulations for using our AI design gallery and services.",
  alternates: {
    canonical: 'https://www.ui-syntax.com/terms',
  },
  openGraph: {
    title: "Terms and Conditions - UI Syntax",
    description: "Read UI Syntax's Terms and Conditions. Learn about the rules and regulations for using our services.",
    url: 'https://www.ui-syntax.com/terms',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function TermsPage() {
  const placementIds = getPlacementIds('NEXT_PUBLIC_EZOIC_PLACEMENTS_TERMS');
  return (
    <div className="min-h-screen bg-white">
      <SimpleHeader />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Terms and Conditions</h1>
        
        <div className="prose prose-lg text-gray-700 space-y-6">
          <section>
            <p className="text-lg">
              Welcome to UI Syntax. By accessing and using this website, you accept and agree to be bound by 
              the terms and provision of this agreement.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">1. Use of Service</h2>
            <p>
              UI Syntax provides a curated gallery of AI-generated web design inspiration for professional use. 
              By accessing our service, you agree to:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li>Use the designs for inspiration and reference purposes</li>
              <li>Not reproduce or redistribute designs without proper attribution</li>
              <li>Respect intellectual property rights of AI-generated content</li>
              <li>Use the service in compliance with all applicable laws and regulations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">2. Intellectual Property</h2>
            <p>
              All designs, content, and materials available on UI Syntax are provided for inspiration purposes. 
              While the designs are AI-generated, the curation, presentation, and accompanying content are 
              proprietary to UI Syntax.
            </p>
            <p className="mt-4">
              You may use the design concepts for your own projects, but you may not claim ownership of the 
              AI-generated designs themselves or redistribute them as your own original work.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">3. User Conduct</h2>
            <p>
              You agree not to:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li>Attempt to gain unauthorized access to any portion of the website</li>
              <li>Use automated systems (bots, scrapers) without written permission</li>
              <li>Interfere with or disrupt the service or servers</li>
              <li>Violate any applicable local, state, national, or international law</li>
              <li>Transmit any harmful or malicious code</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">4. Disclaimer of Warranties</h2>
            <p>
              UI Syntax is provided on an "AS IS" and "AS AVAILABLE" basis. We make no warranties, expressed 
              or implied, and hereby disclaim all warranties including, without limitation:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li>Implied warranties of merchantability or fitness for a particular purpose</li>
              <li>That the service will be uninterrupted, timely, secure, or error-free</li>
              <li>That the results obtained from the use of the service will be accurate or reliable</li>
              <li>That the quality of any designs, information, or materials will meet your expectations</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">5. Limitation of Liability</h2>
            <p>
              In no event shall UI Syntax, its officers, directors, employees, or agents be liable for any 
              indirect, incidental, special, consequential, or punitive damages, including without limitation, 
              loss of profits, data, use, goodwill, or other intangible losses, resulting from:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li>Your access to or use of or inability to access or use the service</li>
              <li>Any conduct or content of any third party on the service</li>
              <li>Unauthorized access, use, or alteration of your transmissions or content</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">6. Third-Party Links</h2>
            <p>
              Our service may contain links to third-party websites or services that are not owned or 
              controlled by UI Syntax. We have no control over and assume no responsibility for the content, 
              privacy policies, or practices of any third-party websites or services.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">7. Advertising and Analytics</h2>
            <p>
              We use third-party advertising partners (including Google AdSense and Ezoic) and analytics 
              services to serve advertisements and analyze site usage. These partners may use cookies and 
              similar technologies to collect information about your use of our services.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">8. Changes to Terms</h2>
            <p>
              We reserve the right to modify or replace these Terms at any time. If a revision is material, 
              we will provide at least 30 days' notice prior to any new terms taking effect. What constitutes 
              a material change will be determined at our sole discretion.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">9. Governing Law</h2>
            <p>
              These Terms shall be governed and construed in accordance with the laws of California, 
              United States, without regard to its conflict of law provisions.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">10. Contact Information</h2>
            <p>
              If you have any questions about these Terms, please contact us at{" "}
              <a href="mailto:thive8564@gmail.com" className="text-blue-600 hover:text-blue-800 underline">
                thive8564@gmail.com
              </a>
            </p>
          </section>

          <section>
            <p className="text-sm text-gray-500 mt-12">
              Last Updated: January 23, 2026
            </p>
          </section>
        </div>
      </div>

      {placementIds.length > 0 && (
        <EzoicPlacements placementIds={placementIds} wrapperClassName="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 my-16" />
      )}

      {/* Footer */}
      <footer className="bg-black border-t border-gray-900 mt-auto">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div>
              <h2 className="text-xl font-display font-semibold text-white mb-4">UI SYNTAX</h2>
              <p className="text-gray-400 text-sm">AI-generated web design gallery showcasing creative and innovative designs.</p>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Quick Links</h3>
              <ul className="space-y-2">
                <li><Link href="/" className="text-gray-400 hover:text-white text-sm transition-colors">Home</Link></li>
                <li><Link href="/about" className="text-gray-400 hover:text-white text-sm transition-colors">About</Link></li>
              </ul>
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white mb-4 uppercase tracking-wider">Legal</h3>
              <ul className="space-y-2">
                <li><Link href="/privacy-policy" className="text-gray-400 hover:text-white text-sm transition-colors">Privacy Policy</Link></li>
                <li><Link href="/terms" className="text-gray-400 hover:text-white text-sm transition-colors">Terms of Service</Link></li>
                <li><Link href="/contact" className="text-gray-400 hover:text-white text-sm transition-colors">Contact</Link></li>
                <li><a href="/feed.xml" className="text-gray-400 hover:text-white text-sm transition-colors">RSS Feed</a></li>
              </ul>
            </div>
          </div>
          <div className="mt-8 pt-8 border-t border-gray-900">
            <p className="text-center text-gray-500 text-sm">© {new Date().getFullYear()} UI Syntax. All rights reserved.</p>
          </div>
        </div>
      </footer>
    </div>
  );
}
