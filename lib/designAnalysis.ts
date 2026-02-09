const HEX_COLOR_REGEX = /#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b/g;
const SECTION_REGEX = /<(section|main|header|footer|article|div)[^>]*>/gi;
const BUTTON_REGEX = /<(button|a)[^>]*(class|role|href)[^>]*>/gi;
const TEXT_REGEX = />[^<]+</g;

const normalizeHex = (value: string) => {
  const match = value.match(/^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/);
  if (!match) return null;
  let hex = match[1];
  if (hex.length === 3) {
    hex = hex
      .split('')
      .map((char) => char + char)
      .join('');
  }
  return `#${hex.toLowerCase()}`;
};

export type DesignMetrics = {
  sectionCount: number;
  buttonCount: number;
  textLength: number;
  colors: string[];
};

export function analyzeMarkup(html?: string | null): DesignMetrics | null {
  if (!html) return null;
  const trimmed = html.trim();
  if (!trimmed) return null;

  const sections = trimmed.match(SECTION_REGEX)?.length ?? 0;
  const buttons = trimmed.match(BUTTON_REGEX)?.length ?? 0;
  const colors = Array.from(new Set((trimmed.match(HEX_COLOR_REGEX) || []).map(normalizeHex).filter(Boolean))) as string[];
  const textMatches = trimmed.match(TEXT_REGEX) || [];
  const textLength = textMatches.reduce((sum, chunk) => sum + chunk.replace(/[<>]/g, '').trim().length, 0);

  return {
    sectionCount: sections || (trimmed.split('<div').length - 1) || 1,
    buttonCount: buttons,
    textLength,
    colors,
  };
}

export function similarityScore(a: DesignMetrics, b: DesignMetrics) {
  const sectionDelta = Math.abs(a.sectionCount - b.sectionCount);
  const buttonDelta = Math.abs(a.buttonCount - b.buttonCount);
  const textDelta = Math.abs(a.textLength - b.textLength);
  const colorOverlap = a.colors.filter((color) => b.colors.includes(color)).length;

  const normalizedSection = Math.max(0, 1 - sectionDelta / 6);
  const normalizedButton = Math.max(0, 1 - buttonDelta / 8);
  const normalizedText = Math.max(0, 1 - textDelta / 4000);
  const colorBoost = Math.min(1, colorOverlap / 3);

  return Number(((normalizedSection * 0.3) + (normalizedButton * 0.2) + (normalizedText * 0.3) + (colorBoost * 0.2)).toFixed(3));
}
