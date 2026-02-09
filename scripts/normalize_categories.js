#!/usr/bin/env node

const path = require('path');
const fs = require('fs');
const { createClient } = require('@supabase/supabase-js');
const dotenv = require('dotenv');

function loadEnvFiles() {
  const root = path.resolve(__dirname, '..');
  const envFiles = ['.env', '.env.local'];
  for (const filename of envFiles) {
    const fullPath = path.join(root, filename);
    if (fs.existsSync(fullPath)) {
      dotenv.config({ path: fullPath, override: false });
    }
  }
}

loadEnvFiles();

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error('Missing NEXT_PUBLIC_SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY.');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY, {
  auth: {
    persistSession: false,
    autoRefreshToken: false,
  },
});

const CATEGORY_RULES = [
  { canonical: 'Landing Page', aliases: ['landing page', 'landing-page', 'landing'], keyword: /(landing|hero|marketing|homepage|saas)/i },
  { canonical: 'Dashboard', aliases: ['dashboard', 'dashboards'], keyword: /(dashboard|analytics|admin|reporting)/i },
  { canonical: 'E-commerce', aliases: ['e-commerce', 'ecommerce', 'commerce', 'shop', 'store'], keyword: /(commerce|checkout|shop|store|cart|product)/i },
  { canonical: 'Portfolio', aliases: ['portfolio', 'case study'], keyword: /(portfolio|case study|studio|freelance)/i },
  { canonical: 'Blog', aliases: ['blog', 'article', 'posts'], keyword: /(blog|article|news|publication|post|journal)/i },
  { canonical: 'Components', aliases: ['components', 'component', 'library', 'ui kit'], keyword: /(component|library|system|ui kit|widget|module)/i },
];

const aliasLookup = new Map();
CATEGORY_RULES.forEach((rule) => {
  const variants = [rule.canonical, ...(rule.aliases || [])];
  variants.forEach((variant) => {
    if (!variant) return;
    aliasLookup.set(variant.trim().toLowerCase(), rule.canonical);
  });
});

function normalizeCategoryValue(value) {
  if (!value) return null;
  const key = value.trim().toLowerCase();
  if (!key) return null;
  if (aliasLookup.has(key)) {
    return aliasLookup.get(key);
  }
  const withoutHyphen = key.replace(/[-_]/g, ' ');
  if (aliasLookup.has(withoutHyphen)) {
    return aliasLookup.get(withoutHyphen);
  }
  if (key.endsWith('s')) {
    const singular = key.slice(0, -1);
    if (aliasLookup.has(singular)) {
      return aliasLookup.get(singular);
    }
  }
  for (const rule of CATEGORY_RULES) {
    if (rule.keyword && rule.keyword.test(key)) {
      return rule.canonical;
    }
  }
  return null;
}

function inferCategoryFromTitle(title) {
  if (!title) return null;
  const lower = title.toLowerCase();
  for (const rule of CATEGORY_RULES) {
    if (rule.keyword && rule.keyword.test(lower)) {
      return rule.canonical;
    }
  }
  return null;
}

async function main() {
  console.log('Fetching design categories...');
  const { data, error } = await supabase
    .from('designs')
    .select('id, title, category');

  if (error) {
    console.error('Failed to load designs:', error.message);
    process.exit(1);
  }

  const updates = [];
  const unmatched = [];

  for (const design of data) {
    const normalized = normalizeCategoryValue(design.category) || inferCategoryFromTitle(design.title);
    if (!normalized) {
      if (!design.category) {
        unmatched.push({ id: design.id, title: design.title || '(untitled)' });
      }
      continue;
    }

    if (design.category === normalized) {
      continue;
    }

    updates.push({ id: design.id, nextCategory: normalized, previous: design.category || null });
  }

  if (updates.length === 0) {
    console.log('No category updates required.');
  } else {
    console.log(`Preparing to update ${updates.length} design${updates.length > 1 ? 's' : ''}.`);
    const grouped = updates.reduce((acc, item) => {
      acc[item.nextCategory] = acc[item.nextCategory] || [];
      acc[item.nextCategory].push(item.id);
      return acc;
    }, {});

    for (const [category, ids] of Object.entries(grouped)) {
      console.log(`→ Setting ${ids.length} design(s) to "${category}"`);
      const { error: updateError } = await supabase
        .from('designs')
        .update({ category })
        .in('id', ids);
      if (updateError) {
        console.error(`Failed to update category to ${category}:`, updateError.message);
        process.exit(1);
      }
    }

    console.log('Category normalization complete.');
  }

  if (unmatched.length) {
    console.log('\nDesigns still missing a category (needs manual review):');
    unmatched.slice(0, 20).forEach((entry) => {
      console.log(`- ${entry.id} :: ${entry.title}`);
    });
    if (unmatched.length > 20) {
      console.log(`...and ${unmatched.length - 20} more.`);
    }
  }
}

main().catch((err) => {
  console.error('Unexpected error while normalizing categories:', err);
  process.exit(1);
});
