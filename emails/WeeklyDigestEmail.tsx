import * as React from 'react';

interface WeeklyDigestEmailProps {
  designs: Array<{
    title: string;
    slug: string;
    image_url: string;
    category: string | null;
  }>;
}

export const WeeklyDigestEmail: React.FC<WeeklyDigestEmailProps> = ({ designs }) => (
  <html>
    <head>
      <style>{`
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
          line-height: 1.6;
          color: #333;
          max-width: 600px;
          margin: 0 auto;
          padding: 0;
          background-color: #f5f5f5;
        }
        .container {
          background: white;
          margin: 20px;
          border-radius: 16px;
          overflow: hidden;
          box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .header {
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          padding: 40px 30px;
          text-align: center;
          color: white;
        }
        .logo {
          font-size: 28px;
          font-weight: bold;
          margin-bottom: 10px;
          letter-spacing: 1px;
        }
        .subtitle {
          font-size: 16px;
          opacity: 0.95;
        }
        .content {
          padding: 30px;
        }
        .intro {
          font-size: 16px;
          color: #555;
          margin-bottom: 30px;
        }
        .section-title {
          font-size: 20px;
          font-weight: bold;
          color: #667eea;
          margin-bottom: 20px;
        }
        .design-grid {
          display: grid;
          gap: 20px;
        }
        .design-card {
          border: 1px solid #e5e5e5;
          border-radius: 12px;
          overflow: hidden;
          transition: transform 0.2s;
          text-decoration: none;
          color: inherit;
          display: block;
        }
        .design-card:hover {
          transform: translateY(-2px);
          box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        }
        .design-image {
          width: 100%;
          height: 200px;
          object-fit: cover;
          display: block;
        }
        .design-info {
          padding: 15px;
        }
        .design-category {
          display: inline-block;
          background: #f0f0f0;
          color: #667eea;
          font-size: 11px;
          font-weight: 600;
          text-transform: uppercase;
          padding: 4px 10px;
          border-radius: 4px;
          margin-bottom: 8px;
          letter-spacing: 0.5px;
        }
        .design-title {
          font-size: 16px;
          font-weight: 600;
          color: #333;
          margin: 0;
        }
        .cta-button {
          display: inline-block;
          background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
          color: white;
          padding: 14px 32px;
          border-radius: 8px;
          text-decoration: none;
          font-weight: 600;
          margin: 30px 0 20px;
          text-align: center;
        }
        .footer {
          background: #f9f9f9;
          padding: 30px;
          text-align: center;
          font-size: 14px;
          color: #666;
        }
        .footer-links {
          margin-top: 15px;
        }
        .footer-link {
          color: #667eea;
          text-decoration: none;
          margin: 0 10px;
        }
        .unsubscribe {
          color: #999;
          text-decoration: underline;
          font-size: 12px;
          margin-top: 15px;
          display: inline-block;
        }
      `}</style>
    </head>
    <body>
      <div className="container">
        <div className="header">
          <div className="logo">UI SYNTAX</div>
          <div className="subtitle">Weekly AI Design Digest</div>
        </div>
        
        <div className="content">
          <p className="intro">
            Hi there! 👋<br/><br/>
            Here are this week's most inspiring AI-generated designs. Discover fresh ideas, 
            trending patterns, and creative inspiration for your next project.
          </p>
          
          <h2 className="section-title">✨ This Week's Featured Designs</h2>
          
          <div className="design-grid">
            {designs.map((design, index) => (
              <a 
                key={index} 
                href={`https://uisyntax.com/design/${design.slug}`} 
                className="design-card"
              >
                <img 
                  src={design.image_url} 
                  alt={design.title} 
                  className="design-image"
                />
                <div className="design-info">
                  {design.category && (
                    <span className="design-category">{design.category}</span>
                  )}
                  <h3 className="design-title">{design.title}</h3>
                </div>
              </a>
            ))}
          </div>
          
          <center>
            <a href="https://uisyntax.com" className="cta-button">
              Browse All Designs →
            </a>
          </center>
          
          <p style={{ marginTop: '30px', fontSize: '14px', color: '#666', lineHeight: '1.8' }}>
            <strong>What's next?</strong><br/>
            We're constantly adding new AI-generated designs across landing pages, dashboards, 
            and mobile apps. Check back regularly for fresh inspiration!
          </p>
        </div>
        
        <div className="footer">
          <p>© 2026 UI Syntax. All rights reserved.</p>
          <div className="footer-links">
            <a href="https://uisyntax.com" className="footer-link">Website</a>
            <a href="https://uisyntax.com/about" className="footer-link">About</a>
            <a href="https://uisyntax.com/contact" className="footer-link">Contact</a>
          </div>
          <a href="{{unsubscribe_url}}" className="unsubscribe">
            Unsubscribe from this newsletter
          </a>
        </div>
      </div>
    </body>
  </html>
);
