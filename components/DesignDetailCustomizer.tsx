"use client";

import DesignPreview from './DesignPreview';
import CodeBlock from './CodeBlock';

interface DesignDetailCustomizerProps {
  title: string;
  imageUrl: string;
  htmlCode?: string | null;
  reactCode?: string | null;
  colors?: string[] | null;
}

/*
 * NOTE: Color swapping helpers are temporarily disabled because palette-based
 * replacements were producing broken previews. When we revisit the feature,
 * restore the utilities below and the stateful logic that used them.
 *
 * const HEX_COLOR_REGEX = /#(?:[0-9a-fA-F]{3}|[0-9a-fA-F]{6})\b/g;
 * type PaletteColor = { raw: string; hex: string };
 * const normalizeHex = ...
 * const replaceColorToken = ...
 */

export default function DesignDetailCustomizer({
  title,
  imageUrl,
  htmlCode,
  reactCode,
  colors,
}: DesignDetailCustomizerProps) {
  const safeHtml = htmlCode && htmlCode.trim().length ? htmlCode : null;

  // Color swapping is temporarily disabled to avoid visual glitches.
  // const palette = useMemo<PaletteColor[]>(() => ...);
  // const [selectedColor, setSelectedColor] = useState<string | null>(...);
  // const detectedAccent = useMemo(...);
  // useEffect(...);
  // const transformedHtml = useMemo(...);
  // const transformedReact = useMemo(...);

  const previewHtml = safeHtml ?? undefined;
  const codeForBlock = safeHtml ?? '';

  return (
    <section className="space-y-6 sm:space-y-8">
      {/* Color selection UI temporarily disabled; revisit once preview stability is resolved. */}
      <DesignPreview imageUrl={imageUrl} title={title} colors={colors ?? undefined} htmlCode={previewHtml} />

      {safeHtml && (
        <CodeBlock htmlCode={codeForBlock} reactCode={reactCode ?? undefined} />
      )}
    </section>
  );
}
