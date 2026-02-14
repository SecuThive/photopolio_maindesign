import type { Metadata } from "next";
import Header from '@/components/Header';
import Footer from '@/components/Footer';
import EzoicPlacements from '@/components/EzoicPlacements';
import { getPlacementIds } from '@/lib/ezoic';

export const metadata: Metadata = {
  title: "Privacy Policy",
  description: "Read UI Syntax's Privacy Policy. Learn about how we collect, use, and protect your information when you visit our AI design gallery.",
  alternates: {
    canonical: 'https://ui-syntax.com/privacy-policy',
  },
  openGraph: {
    title: "Privacy Policy - UI Syntax",
    description: "Read UI Syntax's Privacy Policy. Learn about how we collect, use, and protect your information.",
    url: 'https://ui-syntax.com/privacy-policy',
  },
  robots: {
    index: true,
    follow: true,
  },
};

export default function PrivacyPolicyPage() {
  const placementIds = getPlacementIds('NEXT_PUBLIC_EZOIC_PLACEMENTS_PRIVACY');
  return (
    <div className="min-h-screen bg-luxury-white">
      <Header />

      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Privacy Policy</h1>
        
        <div className="prose prose-lg text-gray-700 space-y-6">
          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">1. Information We Collect</h2>
            <p>
              We collect information that you provide directly to us, including when you create an account, 
              subscribe to our newsletter, or contact us for support.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">2. How We Use Your Information</h2>
            <p>
              We use the information we collect to:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li>Provide, maintain, and improve our services</li>
              <li>Send you technical notices and support messages</li>
              <li>Respond to your comments and questions</li>
              <li>Monitor and analyze trends, usage, and activities</li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">3. Google Analytics</h2>
            <p>
              We use Google Analytics to understand how visitors interact with our website. 
              Google Analytics collects information anonymously and reports website trends without 
              identifying individual visitors.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">4. Cookies</h2>
            <p>
              We use cookies and similar tracking technologies to track activity on our website 
              and store certain information. Cookies are small data files stored on your device 
              that help us improve our services and your experience.
            </p>
            <p className="mt-4">
              <strong>Types of cookies we use:</strong>
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Essential Cookies:</strong> Required for the website to function properly</li>
              <li><strong>Analytics Cookies:</strong> Help us understand how visitors use our website</li>
              <li><strong>Advertising Cookies:</strong> Used to display relevant advertisements</li>
            </ul>
            <p className="mt-4">
              You can instruct your browser to refuse all cookies or to indicate when a cookie is being sent. 
              However, if you do not accept cookies, you may not be able to use some portions of our service.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">5. Data Security</h2>
            <p>
              We take reasonable measures to help protect information about you from loss, theft, 
              misuse, unauthorized access, disclosure, alteration, and destruction. However, no method 
              of transmission over the Internet or electronic storage is 100% secure, and we cannot 
              guarantee absolute security.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">6. GDPR Compliance (European Users)</h2>
            <p>
              If you are located in the European Economic Area (EEA), you have certain data protection rights 
              under the General Data Protection Regulation (GDPR):
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Right to Access:</strong> You can request copies of your personal data</li>
              <li><strong>Right to Rectification:</strong> You can request correction of inaccurate data</li>
              <li><strong>Right to Erasure:</strong> You can request deletion of your personal data</li>
              <li><strong>Right to Restrict Processing:</strong> You can request restriction of data processing</li>
              <li><strong>Right to Data Portability:</strong> You can request transfer of your data</li>
              <li><strong>Right to Object:</strong> You can object to processing of your personal data</li>
            </ul>
            <p className="mt-4">
              To exercise these rights, please contact us at{" "}
              <a href="mailto:thive8564@gmail.com" className="text-blue-600 hover:text-blue-800 underline">
                thive8564@gmail.com
              </a>. We will respond to your request within 30 days.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">7. CCPA Privacy Rights (California Users)</h2>
            <p>
              If you are a California resident, you have specific rights under the California Consumer 
              Privacy Act (CCPA):
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Right to Know:</strong> You can request information about the personal data we collect, 
              use, disclose, or sell</li>
              <li><strong>Right to Delete:</strong> You can request deletion of your personal information</li>
              <li><strong>Right to Opt-Out:</strong> You can opt-out of the sale of your personal information 
              (Note: We do not sell personal information)</li>
              <li><strong>Right to Non-Discrimination:</strong> We will not discriminate against you for 
              exercising your CCPA rights</li>
            </ul>
            <p className="mt-4">
              To submit a CCPA request, please email us at{" "}
              <a href="mailto:thive8564@gmail.com" className="text-blue-600 hover:text-blue-800 underline">
                thive8564@gmail.com
              </a>{" "}
              with the subject line &ldquo;CCPA Request.&rdquo;
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">8. Third-Party Services</h2>
            <p>
              We use third-party services for analytics and advertising, including:
            </p>
            <ul className="list-disc pl-6 space-y-2">
              <li><strong>Google Analytics:</strong> To analyze website traffic and usage patterns</li>
              <li><strong>Google AdSense:</strong> To display advertisements</li>
              <li><strong>Ezoic:</strong> For ad optimization and website performance</li>
            </ul>
            <p className="mt-4">
              These third parties have their own privacy policies. We encourage you to review them:
            </p>
            <ul className="list-disc pl-6 space-y-1 mt-2">
              <li>
                <a href="https://policies.google.com/privacy" target="_blank" rel="noopener noreferrer" 
                   className="text-blue-600 hover:text-blue-800 underline">
                  Google Privacy Policy
                </a>
              </li>
              <li>
                <a href="https://www.ezoic.com/privacy-policy/" target="_blank" rel="noopener noreferrer" 
                   className="text-blue-600 hover:text-blue-800 underline">
                  Ezoic Privacy Policy
                </a>
              </li>
            </ul>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">9. Children&rsquo;s Privacy</h2>
            <p>
              Our service is not intended for children under the age of 13. We do not knowingly collect 
              personally identifiable information from children under 13. If you are a parent or guardian 
              and believe your child has provided us with personal information, please contact us.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">10. International Data Transfers</h2>
            <p>
              Your information may be transferred to and maintained on computers located outside of your 
              state, province, country, or other governmental jurisdiction where data protection laws may 
              differ. By using our service, you consent to such transfers.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">11. Changes to This Privacy Policy</h2>
            <p>
              We may update our Privacy Policy from time to time. We will notify you of any changes by 
              posting the new Privacy Policy on this page and updating the &ldquo;Last Updated&rdquo; date.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">12. Contact Us</h2>
            <p>
              If you have any questions about this Privacy Policy, please contact us:
            </p>
            <ul className="list-none space-y-2 mt-4">
              <li>
                <strong>Email:</strong>{" "}
                <a href="mailto:thive8564@gmail.com" className="text-blue-600 hover:text-blue-800 underline">
                  thive8564@gmail.com
                </a>
              </li>
              <li>
                <strong>Website:</strong>{" "}
                <a href="https://ui-syntax.com/contact" className="text-blue-600 hover:text-blue-800 underline">
                  ui-syntax.com/contact
                </a>
              </li>
            </ul>
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
      <Footer />
    </div>
  );
}
