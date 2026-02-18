import * as React from 'react';

interface DesignRequestReadyEmailProps {
  requestTitle: string;
  designTitle: string;
  designUrl: string;
}

export const DesignRequestReadyEmail: React.FC<DesignRequestReadyEmailProps> = ({
  requestTitle,
  designTitle,
  designUrl,
}) => (
  <html>
    <head>
      <style>{`
        body {
          font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', 'Helvetica Neue', Arial, sans-serif;
          background: #f5f7fb;
          color: #1f2937;
          margin: 0;
          padding: 24px;
        }
        .card {
          max-width: 620px;
          margin: 0 auto;
          background: #ffffff;
          border: 1px solid #e5e7eb;
          border-radius: 14px;
          overflow: hidden;
        }
        .header {
          background: #0b1220;
          color: #ffffff;
          padding: 22px 24px;
          font-size: 18px;
          font-weight: 700;
          letter-spacing: 0.04em;
          text-transform: uppercase;
        }
        .content {
          padding: 24px;
          line-height: 1.7;
          font-size: 15px;
        }
        .label {
          display: inline-block;
          font-size: 11px;
          text-transform: uppercase;
          letter-spacing: 0.18em;
          color: #6b7280;
          margin-bottom: 8px;
        }
        .title {
          font-size: 20px;
          font-weight: 700;
          margin: 0 0 18px;
          color: #111827;
        }
        .button {
          display: inline-block;
          background: #111827;
          color: #ffffff !important;
          text-decoration: none;
          padding: 12px 20px;
          border-radius: 9999px;
          font-size: 12px;
          font-weight: 700;
          text-transform: uppercase;
          letter-spacing: 0.18em;
          margin-top: 10px;
        }
        .footer {
          border-top: 1px solid #e5e7eb;
          padding: 16px 24px;
          font-size: 12px;
          color: #6b7280;
        }
      `}</style>
    </head>
    <body>
      <div className="card">
        <div className="header">UI Syntax Update</div>
        <div className="content">
          <div className="label">Your request is ready</div>
          <h1 className="title">{designTitle}</h1>
          <p>
            We generated a design for your request:
            <br />
            <strong>{requestTitle}</strong>
          </p>
          <a href={designUrl} className="button">View Design</a>
          <p style={{ marginTop: '16px', fontSize: '13px', color: '#6b7280' }}>
            If the button does not work, open this URL:
            <br />
            {designUrl}
          </p>
        </div>
        <div className="footer">UI Syntax · Request Queue</div>
      </div>
    </body>
  </html>
);
