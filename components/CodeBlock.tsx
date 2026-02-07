"use client";

import { useEffect, useMemo, useState } from 'react';

interface CodeBlockProps {
  htmlCode: string;
  reactCode?: string | null;
}

type CodeVariant = 'html' | 'react';

const VARIANT_LABEL: Record<CodeVariant, string> = {
  html: 'HTML',
  react: 'React',
};

export default function CodeBlock({ htmlCode, reactCode }: CodeBlockProps) {
  const [copied, setCopied] = useState(false);
  const [variant, setVariant] = useState<CodeVariant>('html');
  const hasReactVariant = Boolean(reactCode && reactCode.trim().length);

  useEffect(() => {
    if (variant === 'react' && !hasReactVariant) {
      setVariant('html');
    }
  }, [variant, hasReactVariant]);

  const currentCode = useMemo(() => {
    if (variant === 'react' && hasReactVariant) {
      return reactCode as string;
    }
    return htmlCode;
  }, [variant, hasReactVariant, reactCode, htmlCode]);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(currentCode);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy code:', err);
    }
  };

  return (
    <section className="rounded-2xl border border-gray-200 bg-gray-950 text-gray-100 shadow-[inset_0_1px_0_rgba(255,255,255,0.04)]">
      <div className="flex flex-col gap-3 border-b border-white/5 px-4 py-3 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div className="flex items-center gap-3 text-sm text-gray-300">
          <span className="font-medium text-white">Source code</span>
          <span className="text-xs text-gray-500">{VARIANT_LABEL[variant]}</span>
          {hasReactVariant && (
            <div className="flex items-center gap-1 rounded-lg bg-white/5 p-1 text-xs">
              {(['html', 'react'] as CodeVariant[]).map((option) => (
                <button
                  key={option}
                  type="button"
                  onClick={() => setVariant(option)}
                  className={`rounded-md px-3 py-1 transition-colors ${
                    variant === option ? 'bg-white text-gray-900' : 'text-gray-500 hover:text-gray-200'
                  }`}
                >
                  {VARIANT_LABEL[option]}
                </button>
              ))}
            </div>
          )}
        </div>
        <button
          onClick={handleCopy}
          className={`inline-flex items-center gap-2 rounded-lg border px-3 py-1.5 text-xs font-medium transition-colors ${
            copied
              ? 'border-emerald-400 bg-emerald-500/20 text-emerald-200'
              : 'border-white/10 bg-white/5 hover:border-white/30 hover:bg-white/10'
          }`}
          title={`Copy ${VARIANT_LABEL[variant]} code to clipboard`}
        >
          {copied ? (
            <>
              <svg className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd" />
              </svg>
              Copied
            </>
          ) : (
            <>
              <svg className="h-3.5 w-3.5" viewBox="0 0 20 20" fill="currentColor">
                <path d="M8 3a1 1 0 011-1h2a1 1 0 110 2H9a1 1 0 01-1-1z" />
                <path d="M6 3a2 2 0 00-2 2v11a2 2 0 002 2h8a2 2 0 002-2V5a2 2 0 00-2-2 3 3 0 01-3 3H9a3 3 0 01-3-3z" />
              </svg>
              Copy
            </>
          )}
        </button>
      </div>

      <pre className="custom-scrollbar max-h-[520px] overflow-auto px-4 py-5 text-sm font-mono leading-relaxed sm:px-6">
        <code>{currentCode}</code>
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
