const HEX_COLOR_REGEX = /#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b/g;
const SECTION_REGEX = /<(section|main|header|footer|article|div)[^>]*>/gi;
const BUTTON_REGEX = /<(button|a)[^>]*(class|role|href)[^>]*>/gi;
const TEXT_REGEX = />[^<]+</g;
const IMAGE_REGEX = /<(img|picture|svg)[^>]*>/gi;
const FORM_REGEX = /<(input|textarea|select|form)[^>]*>/gi;
const SEMANTIC_REGEX = /<(article|section|nav|aside|header|footer|main)[^>]*>/gi;
const GRID_REGEX = /grid|grid-cols|grid-rows|display:\s*grid/gi;
const FLEX_REGEX = /flex|flex-row|flex-col|display:\s*flex/gi;
const RESPONSIVE_REGEX = /\b(sm:|md:|lg:|xl:|2xl:|@media)/gi;

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
  imageCount: number;
  formElementCount: number;
  semanticScore: number;
  layoutPattern: 'grid' | 'flex' | 'mixed' | 'basic';
  responsiveBreakpoints: number;
  complexity: number;
};

export function analyzeMarkup(html?: string | null): DesignMetrics | null {
  if (!html) return null;
  const trimmed = html.trim();
  if (!trimmed) return null;

  // Basic metrics
  const sections = trimmed.match(SECTION_REGEX)?.length ?? 0;
  const buttons = trimmed.match(BUTTON_REGEX)?.length ?? 0;
  const colors = Array.from(new Set((trimmed.match(HEX_COLOR_REGEX) || []).map(normalizeHex).filter(Boolean))) as string[];
  const textMatches = trimmed.match(TEXT_REGEX) || [];
  const textLength = textMatches.reduce((sum, chunk) => sum + chunk.replace(/[<>]/g, '').trim().length, 0);

  // Advanced metrics
  const images = trimmed.match(IMAGE_REGEX)?.length ?? 0;
  const formElements = trimmed.match(FORM_REGEX)?.length ?? 0;
  const semanticElements = trimmed.match(SEMANTIC_REGEX)?.length ?? 0;
  const totalElements = (trimmed.match(/<[a-z][^>]*>/gi) || []).length;
  const semanticScore = totalElements > 0 ? Math.min(100, Math.round((semanticElements / totalElements) * 100)) : 0;

  // Layout pattern detection
  const hasGrid = GRID_REGEX.test(trimmed);
  const hasFlex = FLEX_REGEX.test(trimmed);
  let layoutPattern: 'grid' | 'flex' | 'mixed' | 'basic' = 'basic';
  if (hasGrid && hasFlex) layoutPattern = 'mixed';
  else if (hasGrid) layoutPattern = 'grid';
  else if (hasFlex) layoutPattern = 'flex';

  // Responsive breakpoints
  const responsiveMatches = trimmed.match(RESPONSIVE_REGEX) || [];
  const responsiveBreakpoints = new Set(responsiveMatches.map(m => m.toLowerCase())).size;

  // Complexity score (depth + density)
  const depth = sections || (trimmed.split('<div').length - 1) || 1;
  const density = totalElements / Math.max(1, textLength / 100);
  const complexity = Math.round(Math.min(100, (depth * 5 + density * 10 + colors.length * 3)));

  return {
    sectionCount: depth,
    buttonCount: buttons,
    textLength,
    colors,
    imageCount: images,
    formElementCount: formElements,
    semanticScore,
    layoutPattern,
    responsiveBreakpoints,
    complexity,
  };
}

export function similarityScore(a: DesignMetrics, b: DesignMetrics) {
  // Structure similarity
  const sectionDelta = Math.abs(a.sectionCount - b.sectionCount);
  const normalizedSection = Math.max(0, 1 - sectionDelta / 8);

  // Interactive elements similarity
  const buttonDelta = Math.abs(a.buttonCount - b.buttonCount);
  const normalizedButton = Math.max(0, 1 - buttonDelta / 10);

  // Content volume similarity
  const textDelta = Math.abs(a.textLength - b.textLength);
  const normalizedText = Math.max(0, 1 - textDelta / 5000);

  // Color palette overlap
  const colorOverlap = a.colors.filter((color) => b.colors.includes(color)).length;
  const maxColors = Math.max(a.colors.length, b.colors.length, 1);
  const colorScore = colorOverlap / maxColors;

  // Media usage similarity
  const imageDelta = Math.abs(a.imageCount - b.imageCount);
  const normalizedImage = Math.max(0, 1 - imageDelta / 8);

  // Layout pattern match
  const layoutMatch = a.layoutPattern === b.layoutPattern ? 1 : 
                      (a.layoutPattern === 'mixed' || b.layoutPattern === 'mixed') ? 0.5 : 0.3;

  // Complexity similarity
  const complexityDelta = Math.abs(a.complexity - b.complexity);
  const normalizedComplexity = Math.max(0, 1 - complexityDelta / 50);

  // Form elements similarity
  const formDelta = Math.abs(a.formElementCount - b.formElementCount);
  const normalizedForm = a.formElementCount > 0 || b.formElementCount > 0 
    ? Math.max(0, 1 - formDelta / 5)
    : 1; // Both have no forms = perfect match

  // Weighted scoring
  const score = 
    normalizedSection * 0.20 +      // Structure weight
    normalizedButton * 0.15 +       // CTA weight
    normalizedText * 0.15 +         // Content weight
    colorScore * 0.20 +             // Color palette weight
    normalizedImage * 0.10 +        // Media usage weight
    layoutMatch * 0.10 +            // Layout pattern weight
    normalizedComplexity * 0.05 +   // Complexity weight
    normalizedForm * 0.05;          // Form elements weight

  return Number(score.toFixed(3));
}
