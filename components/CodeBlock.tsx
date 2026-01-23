"use client";

import { useState } from 'react';

interface CodeBlockProps {
  code: string;
}

export default function CodeBlock({ code }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  return (
    <section className="bg-black text-green-400 border border-gray-900 p-8 relative group">
      <div className="flex items-center justify-between mb-4">
        <h2 className="text-xs uppercase tracking-[0.3em] text-gray-400">Source Code</h2>
        <div className="flex items-center gap-3">
          <span className="text-[11px] uppercase tracking-[0.3em] text-gray-500">Read-only</span>
          <button
            onClick={handleCopy}
            className={`flex items-center gap-2 px-3 py-1.5 rounded text-xs uppercase tracking-[0.2em] transition-all duration-200 ${
              copied
                ? 'bg-green-500 text-black'
                : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white'
            }`}
            title="Copy code to clipboard"
          >
            {copied ? (
              <>
                <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
                </svg>
                Copied!
              </>
            ) : (
              <>
                <svg className="w-3.5 h-3.5" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                  <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
                </svg>
                Copy
              </>
            )}
          </button>
        </div>
      </div>
      <pre className="overflow-x-auto text-sm leading-relaxed font-mono max-h-[480px] overflow-y-auto custom-scrollbar">
        <code>{code}</code>
      </pre>

      <style jsx>{`
        .custom-scrollbar::-webkit-scrollbar {
          width: 8px;
          height: 8px;
        }
        .custom-scrollbar::-webkit-scrollbar-track {
          background: #1a1a1a;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb {
          background: #333;
          border-radius: 4px;
        }
        .custom-scrollbar::-webkit-scrollbar-thumb:hover {
          background: #444;
        }
      `}</style>
    </section>
  );
}
