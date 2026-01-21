const { createClient } = require('@supabase/supabase-js');
const crypto = require('crypto');

const shouldDelete = process.argv.includes('--delete');

const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
const key = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!url || !key) {
  console.error('Missing Supabase credentials');
  process.exit(1);
}

const client = createClient(url, key);

function getStructureHash(html = '') {
  const normalized = html.replace(/#[0-9a-fA-F]{3,6}/g, 'COLOR');
  const tags = (normalized.match(/<([a-zA-Z0-9-]+)/g) || []).join('');
  const layouts = (normalized.match(/grid-template-columns:[^;]+|flex-direction:[^;]+|display:\s*(?:grid|flex)/g) || []).join('');
  return crypto.createHash('md5').update(tags + layouts).digest('hex');
}

function chunkArray(arr, size) {
  const chunks = [];
  for (let i = 0; i < arr.length; i += size) {
    chunks.push(arr.slice(i, i + size));
  }
  return chunks;
}

(async () => {
  const { data, error } = await client
    .from('designs')
    .select('id,title,created_at,code')
    .order('created_at', { ascending: false });

  if (error) {
    console.error('Supabase error:', error);
    process.exit(1);
  }

  const map = new Map();
  for (const design of data) {
    const hash = getStructureHash(design.code || '');
    if (!map.has(hash)) {
      map.set(hash, []);
    }
    map.get(hash).push({ id: design.id, title: design.title, created_at: design.created_at });
  }

  const duplicates = Array.from(map.entries()).filter(([, list]) => list.length > 1);
  console.log(`Total designs: ${data.length}`);
  console.log(`Duplicate structures: ${duplicates.length}`);
  const idsToDelete = [];

  duplicates.forEach(([hash, list], idx) => {
    console.log(`\n[${idx + 1}] Structure hash ${hash} (${list.length} variants)`);
    list.forEach((d) => {
      console.log(`  - ${d.id} | ${d.title} | ${d.created_at}`);
    });

    const sorted = [...list].sort(
      (a, b) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime(),
    );
    const keep = sorted[0];
    const redundant = sorted.slice(1);
    if (redundant.length) {
      console.log(`  -> Keeping newest ${keep.id}, flagging ${redundant.length} duplicate(s)`);
      idsToDelete.push(...redundant.map((item) => item.id));
    }
  });

  if (!duplicates.length) {
    return;
  }

  if (shouldDelete) {
    if (!idsToDelete.length) {
      console.log('\nNo redundant rows detected for deletion.');
      return;
    }

    console.log(`\n🧹 Deleting ${idsToDelete.length} duplicate design(s)...`);
    const batches = chunkArray(idsToDelete, 50);
    for (const batch of batches) {
      const { error: deleteError } = await client
        .from('designs')
        .delete()
        .in('id', batch)
        .select('id');

      if (deleteError) {
        console.error('Failed to delete duplicates:', deleteError);
        process.exit(1);
      }
    }

    console.log('✅ Duplicate rows deleted successfully.');
  } else {
    console.log('\nRun this script with --delete to remove redundant rows automatically.');
  }
})();
