import htmlToJsx from 'html-to-jsx';

const BODY_REGEX = /<body[^>]*>([\s\S]*?)<\/body>/i;
const DOCTYPE_REGEX = /<!DOCTYPE[\s\S]*?>/gi;
const HTML_TAG_REGEX = /<\/?html[^>]*>/gi;
const HEAD_TAG_REGEX = /<head[^>]*>[\s\S]*?<\/head>/gi;
const BODY_TAG_REGEX = /<\/?body[^>]*>/gi;

function indentBlock(value: string, spaces: number) {
  const pad = ' '.repeat(spaces);
  return value
    .split('\n')
    .map((line) => (line.trim().length ? pad + line : pad))
    .join('\n');
}

function extractBody(html: string) {
  const bodyMatch = html.match(BODY_REGEX);
  if (bodyMatch) {
    return bodyMatch[1];
  }
  return html;
}

function sanitizeMarkup(html: string) {
  return html
    .replace(DOCTYPE_REGEX, '')
    .replace(HEAD_TAG_REGEX, '')
    .replace(HTML_TAG_REGEX, '')
    .replace(BODY_TAG_REGEX, '')
    .trim();
}

export function buildReactComponentFromHtml(html?: string | null) {
  if (!html) {
    return null;
  }

  try {
    const trimmed = html.trim();
    if (!trimmed) {
      return null;
    }

    const bodyMarkup = extractBody(trimmed);
    const sanitized = sanitizeMarkup(bodyMarkup);

    if (!sanitized) {
      return null;
    }

    const jsxMarkup = htmlToJsx(sanitized).trim();
    if (!jsxMarkup) {
      return null;
    }

    const indentedJsx = indentBlock(jsxMarkup, 4);
      return [
        'import React from "react";',
      '',
      'export default function DesignComponent() {',
      '  return (',
      indentedJsx,
      '  );',
      '}',
      '',
    ].join('\n');
  } catch (error) {
    console.error('Failed to build React code from HTML snippet', error);
    return null;
  }
}
