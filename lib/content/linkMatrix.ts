import { collectionConfigs, type CollectionConfig } from '@/lib/collections';
import { pillarTopics, type PillarTopic } from '@/lib/pillars';

export type PillarLinkCluster = {
  pillar: PillarTopic;
  pillarSlug: string;
  collections: CollectionConfig[];
  supabaseCategories: string[];
};

export type CategoryLinkTargets = {
  pillar: PillarTopic | null;
  collection: CollectionConfig | null;
};

function extractPillarSlug(href: string) {
  const normalized = href.replace(/\/$/, '');
  const parts = normalized.split('/');
  return parts[parts.length - 1];
}

const pillarBySlug = new Map<string, PillarTopic>(pillarTopics.map((topic) => [topic.slug, topic]));

const clusters: PillarLinkCluster[] = pillarTopics.map((topic) => {
  const collections = collectionConfigs.filter((collection) => extractPillarSlug(collection.pillar.href) === topic.slug);
  const categorySet = new Set(collections.map((collection) => collection.supabaseCategory));
  return {
    pillar: topic,
    pillarSlug: topic.slug,
    collections,
    supabaseCategories: Array.from(categorySet),
  };
});

const categoryLookup = new Map<string, CategoryLinkTargets>();

clusters.forEach((cluster) => {
  cluster.collections.forEach((collection) => {
    if (collection.supabaseCategory) {
      categoryLookup.set(collection.supabaseCategory, {
        pillar: cluster.pillar,
        collection,
      });
    }
  });
});

export function listPillarClusters() {
  return clusters;
}

export function getPillarCluster(slug: string): PillarLinkCluster | undefined {
  return clusters.find((cluster) => cluster.pillarSlug === slug);
}

export function getCollectionsForPillar(slug: string) {
  return getPillarCluster(slug)?.collections ?? [];
}

export function getSupabaseCategoriesForPillar(slug: string) {
  return getPillarCluster(slug)?.supabaseCategories ?? [];
}

export function getCategoryLinkTargets(category?: string | null): CategoryLinkTargets | null {
  if (!category) {
    return null;
  }
  const normalized = category.trim();
  if (!normalized) {
    return null;
  }
  return categoryLookup.get(normalized) ?? null;
}

export function getCollectionCluster(slug: string) {
  const collection = collectionConfigs.find((config) => config.slug === slug);
  if (!collection) {
    return null;
  }
  const pillarSlug = extractPillarSlug(collection.pillar.href);
  const pillar = pillarBySlug.get(pillarSlug) ?? null;
  const siblings = getCollectionsForPillar(pillarSlug).filter((item) => item.slug !== slug);

  return {
    collection,
    pillar,
    siblings,
  };
}
