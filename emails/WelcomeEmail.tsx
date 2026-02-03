import * as React from 'react';

interface WelcomeEmailProps {
  email: string;
}

export const WelcomeEmail: React.FC<WelcomeEmailProps> = ({ email }) => (
  <html>
    <head>
      <style>{`
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
          line-height: 1.6;
          color: #333;
          max-width: 600px;
          margin: 0 auto;
          padding: 20px;
        }
        .container {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          border-radius: 16px;
          padding: 40px;
          color: white;
        }
        .logo {
          font-size: 28px;
          font-weight: bold;
          margin-bottom: 20px;
          letter-spacing: 1px;
        }
        .content {
          background: white;
          color: #333;
          border-radius: 12px;
          padding: 30px;
          margin-top: 20px;
        }
        h1 {
          color: #667eea;
          font-size: 24px;
          margin-bottom: 16px;
        }
        .cta-button {
          display: inline-block;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 14px 32px;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 600;
          margin: 20px 0;
        }
        .footer {
          text-align: center;
          margin-top: 30px;
          padding-top: 20px;
          border-top: 1px solid rgba(255,255,255,0.3);
          font-size: 14px;
          opacity: 0.9;
        }
        .unsubscribe {
          color: rgba(255,255,255,0.8);
          text-decoration: underline;
        }
      `}</style>
    </head>
    <body>
      <div className="container">
        <div className="logo">UI SYNTAX</div>
        
        <div className="content">
          <h1>🎉 Welcome to UI Syntax!</h1>
          
          <p>Hi there,</p>
          
          <p>
            Thank you for subscribing to our weekly newsletter! You've just joined a community of designers, 
            developers, and founders who are passionate about AI-generated design.
          </p>
          
          <p><strong>Here's what you'll receive every week:</strong></p>
          <ul>
            <li>🎨 Latest AI-generated design inspiration</li>
            <li>📊 Trending design patterns and UI components</li>
            <li>🎯 Exclusive tips and insights</li>
            <li>🌈 Curated color palettes</li>
          </ul>
          
          <p>
            Your first newsletter will arrive next week. In the meantime, explore our collection 
            of cutting-edge designs.
          </p>
          
          <a href="https://uisyntax.com" className="cta-button">
            Explore Designs →
          </a>
          
          <p style={{ marginTop: '30px', fontSize: '14px', color: '#666' }}>
            Questions? Just reply to this email – we'd love to hear from you!
          </p>
        </div>
        
        <div className="footer">
          <p>© 2026 UI Syntax. All rights reserved.</p>
          <p>
            Don't want to receive these emails? 
            <a href="{{unsubscribe_url}}" className="unsubscribe">Unsubscribe</a>
          </p>
        </div>
      </div>
    </body>
  </html>
);
