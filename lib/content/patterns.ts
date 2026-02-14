type HtmlProps = Record<string, string | number | boolean>;

export type DefinitionPattern = {
  text: string;
  props: HtmlProps;
};

export type SummaryPattern = {
  text: string;
  containerProps: HtmlProps;
  textProps: HtmlProps;
};

export type ChecklistItemPattern = {
  text: string;
  position: number;
  itemProps: HtmlProps;
};

export type ChecklistPattern = {
  listProps: HtmlProps;
  items: ChecklistItemPattern[];
};

function sanitizeText(input?: string | null) {
  return (input ?? '').trim();
}

export function buildDefinition(content: string): DefinitionPattern {
  const text = sanitizeText(content);
  return {
    text,
    props: {
      role: 'definition',
      itemProp: 'description',
    },
  };
}

export function buildSummary(content: string): SummaryPattern {
  const text = sanitizeText(content);
  return {
    text,
    containerProps: {
      role: 'doc-abstract',
      itemScope: true,
      itemType: 'https://schema.org/CreativeWork',
      itemProp: 'abstract',
    },
    textProps: {
      itemProp: 'description',
    },
  };
}

export function buildChecklist(items: string[]): ChecklistPattern {
  const normalized = items
    .map((item) => sanitizeText(item))
    .filter((item): item is string => Boolean(item));

  return {
    listProps: {
      role: 'list',
      itemScope: true,
      itemType: 'https://schema.org/ItemList',
    },
    items: normalized.map((text, index) => ({
      text,
      position: index + 1,
      itemProps: {
        itemProp: 'itemListElement',
        itemScope: true,
        itemType: 'https://schema.org/ListItem',
      },
    })),
  };
}
