import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Contact Us - Photopolio",
  description: "Get in touch with Photopolio - AI Design Gallery",
};

export default function ContactPage() {
  return (
    <div className="min-h-screen bg-white">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
        <h1 className="text-4xl font-bold text-gray-900 mb-8">Contact Us</h1>
        
        <div className="prose prose-lg text-gray-700 space-y-6">
          <section>
            <p className="text-lg">
              We'd love to hear from you! Whether you have a question, feedback, or just want to say hello, 
              feel free to reach out.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Get in Touch</h2>
            
            <div className="bg-gray-50 border border-gray-200 rounded-lg p-8 space-y-6">
              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Email</h3>
                <p className="text-gray-700">
                  <a href="mailto:contact@ui-syntax.com" className="text-blue-600 hover:text-blue-800 underline">
                    contact@ui-syntax.com
                  </a>
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Business Hours</h3>
                <p className="text-gray-700">
                  Monday - Friday: 9:00 AM - 6:00 PM (KST)<br />
                  Saturday - Sunday: Closed
                </p>
              </div>

              <div>
                <h3 className="text-lg font-semibold text-gray-900 mb-2">Response Time</h3>
                <p className="text-gray-700">
                  We typically respond within 24-48 hours on business days.
                </p>
              </div>
            </div>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">Feedback & Suggestions</h2>
            <p>
              Your feedback helps us improve! If you have any suggestions for new features, 
              design categories, or improvements to our gallery, we'd love to hear them.
            </p>
          </section>

          <section className="mt-12">
            <h2 className="text-2xl font-semibold text-gray-900 mb-4">For Designers</h2>
            <p>
              Interested in contributing your AI-generated designs to our gallery? 
              Please reach out to us via email with your portfolio and we'll get back to you.
            </p>
          </section>

          <section className="mt-12 pt-8 border-t border-gray-200">
            <p className="text-sm text-gray-500">
              Note: We do not provide technical support for third-party tools or services. 
              For general inquiries only.
            </p>
          </section>
        </div>
      </div>
    </div>
  );
}
