#!/usr/bin/env node
/*
  Populates/updates the `slug` column in the `designs` table so we can serve
  clean URLs like /design/modern-animated-login-form. Run with:

    node scripts/sync-slugs.js

  Ensure .env.local contains NEXT_PUBLIC_SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY.
*/

const path = require('path');
const fs = require('fs');
const { createClient } = require('@supabase/supabase-js');

const envPath = path.resolve(process.cwd(), '.env.local');
if (fs.existsSync(envPath)) {
  require('dotenv').config({ path: envPath });
}

const SUPABASE_URL = process.env.NEXT_PUBLIC_SUPABASE_URL;
const SERVICE_ROLE_KEY = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!SUPABASE_URL || !SERVICE_ROLE_KEY) {
  console.error('Missing NEXT_PUBLIC_SUPABASE_URL or SUPABASE_SERVICE_ROLE_KEY.');
  process.exit(1);
}

const supabase = createClient(SUPABASE_URL, SERVICE_ROLE_KEY);

const MAX_SLUG_LENGTH = 80;
const DEFAULT_SLUG = 'design';

const slugify = (title) => {
  return (
    (title || DEFAULT_SLUG)
      .toLowerCase()
      .replace(/&/g, ' and ')
      .replace(/[^a-z0-9\s-]/g, '')
      .replace(/\s+/g, '-')
      .replace(/-+/g, '-')
      .replace(/^-|-$/g, '')
      .slice(0, MAX_SLUG_LENGTH)
      .replace(/-+$/g, '') || DEFAULT_SLUG
  );
};

async function main() {
  const { data, error } = await supabase
    .from('designs')
    .select('id,title,slug')
    .order('created_at', { ascending: true });

  if (error) {
    console.error('Failed to read designs:', error);
    process.exit(1);
  }

  const taken = new Set();
  data.forEach((design) => {
    if (design.slug) {
      taken.add(design.slug);
    }
  });

  const updates = [];

  for (const design of data) {
    if (design.slug && design.slug.trim().length > 0) {
      continue;
    }
    const base = slugify(design.title);
    let candidate = base;
    let suffix = 2;
    while (taken.has(candidate)) {
      candidate = `${base}-${suffix}`;
      suffix += 1;
    }
    taken.add(candidate);
    updates.push({ id: design.id, slug: candidate });
  }

  if (!updates.length) {
    console.log('All designs already have slugs. Nothing to do.');
    return;
  }

  for (const batch of chunk(updates, 10)) {
    const results = await Promise.all(
      batch.map(({ id, slug }) =>
        supabase
          .from('designs')
          .update({ slug })
          .eq('id', id)
      ),
    );

    const failed = results.find((result) => result.error);
    if (failed?.error) {
      console.error('Failed to update slug batch:', failed.error);
      process.exit(1);
    }
  }

  console.log(`Updated ${updates.length} designs with new slugs.`);
}

function chunk(arr, size) {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
}

main().catch((err) => {
  console.error('Unexpected error while syncing slugs:', err);
  process.exit(1);
});
