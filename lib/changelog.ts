export type ChangelogType = 'feature' | 'improvement' | 'fix';

export type ChangelogItem = {
  date: string; // YYYY-MM-DD
  type: ChangelogType;
  title: string;
  summary: string;
  links?: Array<{ label: string; href: string }>;
};

export const changelogItems: ChangelogItem[] = [
  {
    date: '2026-02-18',
    type: 'feature',
    title: 'Design Request Queue launched',
    summary: 'Added request submission, live queue, and vote-based prioritization for upcoming designs.',
    links: [
      { label: 'Request Design', href: '/request-design' },
    ],
  },
  {
    date: '2026-02-18',
    type: 'improvement',
    title: 'Generator now supports request-based output',
    summary: 'Gemini generator can process pending requests and auto-link completed designs back to the request queue.',
    links: [
      { label: 'Request Board', href: '/request-design' },
    ],
  },
  {
    date: '2026-02-17',
    type: 'improvement',
    title: 'Component category filtering normalized',
    summary: 'Improved category matching so Component/Components variants are consistently displayed in listing pages.',
    links: [
      { label: 'Components', href: '/category/components' },
    ],
  },
  {
    date: '2026-02-16',
    type: 'feature',
    title: 'Code Match recommendations expanded',
    summary: 'Code Match now returns broader top matches with structure and palette-aware scoring.',
    links: [
      { label: 'Code Match', href: '/code-match' },
    ],
  },
  {
    date: '2026-02-15',
    type: 'feature',
    title: 'Playbook and collection routing enhancements',
    summary: 'Strengthened internal routing between playbooks, collections, and design detail pages.',
    links: [
      { label: 'Playbooks', href: '/playbooks' },
      { label: 'Collections', href: '/collections' },
    ],
  },
];

export function getRecentChangelog(limit = 3): ChangelogItem[] {
  return changelogItems.slice(0, limit);
}
