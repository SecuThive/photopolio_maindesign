import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Privacy Policy - Photopolio",
  description: "Privacy Policy for Photopolio - AI Design Gallery",
};

export default function PrivacyPolicyPage() {
  return (
    <div className="min-h-screen bg-white">
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
              and store certain information. You can instruct your browser to refuse all cookies 
              or to indicate when a cookie is being sent.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">5. Data Security</h2>
            <p>
              We take reasonable measures to help protect information about you from loss, theft, 
              misuse, unauthorized access, disclosure, alteration, and destruction.
            </p>
          </section>

          <section>
            <h2 className="text-2xl font-semibold text-gray-900 mt-8 mb-4">6. Contact Us</h2>
            <p>
              If you have any questions about this Privacy Policy, please contact us through our 
              contact page.
            </p>
          </section>

          <section>
            <p className="text-sm text-gray-500 mt-12">
              Last Updated: January 19, 2026
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
