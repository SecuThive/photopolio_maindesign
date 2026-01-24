#!/usr/bin/env node
"use strict";

/**
 * Advanced Ollama-powered UI generator
 * - Separates layout structures from aesthetic styles
 * - Enforces structural (DOM) and Tailwind class uniqueness
 * - Produces descriptive metadata via Ollama
 */

const fs = require("fs/promises");
const path = require("path");
const crypto = require("crypto");

const REQUIRED_COMBOS = 10;
const STRUCTURES_PER_CATEGORY = 50;
const HISTORY_PATH = path.join(__dirname, "history.json");
const STRUCTURES_DIR = path.join(__dirname, "structures");
const OUTPUT_PATH = path.join(__dirname, "latest_batch.json");
const OLLAMA_HOST = process.env.OLLAMA_HOST || "http://localhost:11434";
const OLLAMA_MODEL = process.env.OLLAMA_MODEL || "llama3.1";

const CATEGORIES = [
  "Landing Page",
  "Dashboard",
  "E-commerce",
  "Portfolio",
  "Blog",
  "Components",
];

const STYLE_THEMES = [
  {
    name: "Minimal",
    typography: ["font-sans", "tracking-wide", "text-slate-800"],
    palettes: [
      { label: "Ivory", bg: "bg-neutral-50", accent: "text-emerald-600" },
      { label: "Mist", bg: "bg-zinc-100", accent: "text-indigo-500" },
      { label: "Pebble", bg: "bg-stone-100", accent: "text-slate-600" },
    ],
    surfaces: ["border", "border-slate-200", "divide-y", "divide-slate-100"],
    spacing: ["py-16", "px-10", "space-y-6"],
  },
  {
    name: "Luxury",
    typography: ["font-serif", "tracking-tight", "text-zinc-900"],
    palettes: [
      { label: "Aurum", bg: "bg-amber-50", accent: "text-amber-700" },
      { label: "Noir", bg: "bg-[#0b090a]", accent: "text-[#f5c16c]" },
      { label: "Velvet", bg: "bg-rose-50", accent: "text-rose-700" },
    ],
    surfaces: ["border", "border-amber-200", "shadow-2xl", "shadow-amber-200/40"],
    spacing: ["py-20", "px-12", "space-y-8"],
  },
  {
    name: "Cyberpunk",
    typography: ["font-mono", "tracking-[0.2em]", "text-[#f8f9fa]"],
    palettes: [
      { label: "Neon", bg: "bg-[#050816]", accent: "text-[#ff00f5]" },
      { label: "Plasma", bg: "bg-[#010b13]", accent: "text-[#00f7ff]" },
      { label: "Voltage", bg: "bg-[#08011a]", accent: "text-[#ffb703]" },
    ],
    surfaces: ["border", "border-[#1d3557]", "shadow-inner", "shadow-[#00f7ff]/40", "backdrop-blur"],
    spacing: ["py-14", "px-8", "space-y-5"],
  },
  {
    name: "Modern",
    typography: ["font-inter", "text-gray-900", "antialiased"],
    palettes: [
      { label: "Azure", bg: "bg-sky-50", accent: "text-sky-700" },
      { label: "Mint", bg: "bg-emerald-50", accent: "text-emerald-600" },
      { label: "Slate", bg: "bg-slate-50", accent: "text-slate-700" },
    ],
    surfaces: ["shadow-lg", "rounded-3xl", "border", "border-slate-100"],
    spacing: ["py-18", "px-10", "space-y-6"],
  },
  {
    name: "Vintage",
    typography: ["font-serif", "tracking-normal", "text-[#3d2a24]"],
    palettes: [
      { label: "Sepia", bg: "bg-[#f4ecdf]", accent: "text-[#8c5c3e]" },
      { label: "Olive", bg: "bg-[#efe7da]", accent: "text-[#5c6b4f]" },
      { label: "Cocoa", bg: "bg-[#f0e7d8]", accent: "text-[#6f4e37]" },
    ],
    surfaces: ["border", "border-amber-100", "shadow", "shadow-amber-200/60", "rounded-[32px]"],
    spacing: ["py-16", "px-12", "space-y-7"],
  },
];

async function main() {
  const history = await loadHistory();
  const structures = await loadStructures();
  const staged = [];
  const structureUsage = buildStructureUsage(history);
  const { combo: comboHashes, variant: variantHashes } = buildStyleHashSets(history);

  let attempts = 0;
  const maxAttempts = REQUIRED_COMBOS * 12;

  while (staged.length < REQUIRED_COMBOS && attempts < maxAttempts) {
    attempts += 1;
    const category = pickCategory(structures, structureUsage);
    if (!category) break;

    const structure = pickStructure(category, structures, structureUsage);
    if (!structure) continue;

    const structureSignature = structure.signature;
    if (isStructureDuplicate(structureSignature, history, staged)) {
      continue;
    }

    const styleVariant = pickStyleVariant(variantHashes);
    if (!styleVariant) {
      console.warn("⚠️ Exhausted unique style variants. Stopping early.");
      break;
    }

    const tailwindClasses = new Set([
      ...structure.baseClasses,
      ...styleVariant.tailwindClasses,
    ]);
    const styleHash = hashSet(tailwindClasses);
    const styleVariantHash = hashSet(new Set(styleVariant.tailwindClasses));

    if (comboHashes.has(styleHash)) {
      continue;
    }

    const description = await generateDescription({
      category,
      styleName: styleVariant.label,
      structureHtml: structure.html,
      tailwindClasses: Array.from(tailwindClasses),
    });

    const entry = {
      id: crypto.randomUUID(),
      timestamp: new Date().toISOString(),
      category,
      structureId: structure.id,
      structureSignature,
      style: styleVariant,
      tailwindClasses: Array.from(tailwindClasses),
      tailwindHash: styleHash,
      styleVariantHash,
      html: structure.html,
      description,
    };

    staged.push(entry);
    comboHashes.add(styleHash);
    variantHashes.add(styleVariantHash);
    incrementUsage(structureUsage, category, structure.id);
    console.log(`✅ Created combo ${staged.length}/${REQUIRED_COMBOS} → ${category} | ${structure.id} | ${styleVariant.label}`);
  }

  if (!staged.length) {
    console.warn("No valid combinations were produced.");
    return;
  }

  await saveHistory([...history, ...staged]);
  await fs.writeFile(OUTPUT_PATH, JSON.stringify(staged, null, 2), "utf8");
  console.log(`\n📦 Saved ${staged.length} new combo(s) to ${OUTPUT_PATH}`);
}

function buildStructureUsage(history) {
  const usage = {};
  for (const item of history) {
    usage[item.category] = usage[item.category] || {};
    usage[item.category][item.structureId] =
      (usage[item.category][item.structureId] || 0) + 1;
  }
  return usage;
}

function buildStyleHashSets(history) {
  const combo = new Set();
  const variant = new Set();
  for (const item of history) {
    if (item.tailwindHash) {
      combo.add(item.tailwindHash);
    } else if (item.tailwindClasses) {
      combo.add(hashSet(new Set(item.tailwindClasses)));
    }

    const candidateVariant = item.style?.tailwindClasses || item.style?.classes;
    if (candidateVariant) {
      variant.add(hashSet(new Set(candidateVariant)));
    } else if (item.styleVariantHash) {
      variant.add(item.styleVariantHash);
    }
  }
  return { combo, variant };
}

function pickCategory(structures, usage) {
  const prioritized = [];
  const fallback = [];

  for (const category of CATEGORIES) {
    const pool = structures[category] || [];
    if (!pool.length) continue;
    const unused = pool.filter((structure) => {
      const count = usage[category]?.[structure.id] || 0;
      return count === 0;
    });
    if (unused.length) {
      prioritized.push(category);
    } else {
      fallback.push(category);
    }
  }

  if (prioritized.length) {
    return randomFrom(prioritized);
  }
  if (fallback.length) {
    return randomFrom(fallback);
  }
  return null;
}

function pickStructure(category, structures, usage) {
  const pool = structures[category] || [];
  if (!pool.length) return null;

  const unused = pool.filter((structure) => {
    const count = usage[category]?.[structure.id] || 0;
    return count === 0;
  });

  const selectionPool = unused.length ? unused : pool;
  return randomFrom(selectionPool);
}

function pickStyleVariant(variantHashes) {
  const guard = 200;
  let attempts = 0;
  while (attempts < guard) {
    attempts += 1;
    const theme = randomFrom(STYLE_THEMES);
    const variant = createStyleVariant(theme);
    const hash = hashSet(new Set(variant.tailwindClasses));
    if (!variantHashes.has(hash)) {
      return variant;
    }
  }
  return null;
}

function createStyleVariant(theme) {
  const palette = randomFrom(theme.palettes);
  const radius = randomFrom([
    "rounded-3xl",
    "rounded-[40px]",
    "rounded-xl",
    "rounded-2xl",
  ]);
  const gradients = randomFrom([
    "bg-gradient-to-br",
    "bg-gradient-to-r",
    "bg-gradient-to-b",
    "bg-gradient-to-t",
  ]);
  const stops = randomFrom([
    "from-opacity-90",
    "from-10%",
    "from-30%",
    "from-0%",
  ]);
  const glow = randomFrom([
    "shadow-emerald-200/70",
    "shadow-indigo-300/50",
    "shadow-cyan-400/40",
    "shadow-rose-200/60",
  ]);
  const layoutTokens = [
    randomFrom(["grid", "flex", "flex-col", "gap-6", "gap-8"]),
    randomFrom(["max-w-6xl", "max-w-5xl", "max-w-7xl"]),
    randomFrom(["mx-auto", "ml-auto", "mr-auto"]),
  ];

  const classes = new Set([
    ...theme.typography,
    ...theme.surfaces,
    ...theme.spacing,
    palette.bg,
    palette.accent,
    radius,
    gradients,
    stops,
    glow,
    ...layoutTokens,
  ]);

  return {
    label: `${theme.name} • ${palette.label}`,
    theme: theme.name,
    palette: palette.label,
    tailwindClasses: Array.from(classes),
  };
}

function isStructureDuplicate(signature, history, staged) {
  const candidates = [...history, ...staged];
  for (const item of candidates) {
    if (!item.structureSignature) continue;
    const ratio = lcsRatio(signature, item.structureSignature);
    if (ratio >= 0.9) {
      return true;
    }
  }
  return false;
}

function lcsRatio(a, b) {
  const lenA = a.length;
  const lenB = b.length;
  if (!lenA || !lenB) return 0;
  const dp = Array.from({ length: lenA + 1 }, () => new Array(lenB + 1).fill(0));
  for (let i = 1; i <= lenA; i += 1) {
    for (let j = 1; j <= lenB; j += 1) {
      if (a[i - 1] === b[j - 1]) {
        dp[i][j] = dp[i - 1][j - 1] + 1;
      } else {
        dp[i][j] = Math.max(dp[i - 1][j], dp[i][j - 1]);
      }
    }
  }
  const lcs = dp[lenA][lenB];
  return lcs / Math.max(lenA, lenB);
}

function hashSet(set) {
  const sorted = Array.from(set).sort().join("|");
  return crypto.createHash("sha1").update(sorted).digest("hex");
}

async function loadHistory() {
  try {
    const raw = await fs.readFile(HISTORY_PATH, "utf8");
    const parsed = JSON.parse(raw);
    if (Array.isArray(parsed)) {
      return parsed;
    }
    return [];
  } catch (error) {
    if (error.code === "ENOENT") {
      await fs.writeFile(HISTORY_PATH, "[]", "utf8");
      return [];
    }
    throw error;
  }
}

async function saveHistory(entries) {
  await fs.writeFile(HISTORY_PATH, JSON.stringify(entries, null, 2), "utf8");
}

async function loadStructures() {
  const map = {};
  await fs.mkdir(STRUCTURES_DIR, { recursive: true });

  for (const category of CATEGORIES) {
    const filePath = path.join(STRUCTURES_DIR, `${slugify(category)}.json`);
    let list = [];
    try {
      const raw = await fs.readFile(filePath, "utf8");
      const parsed = JSON.parse(raw);
      if (Array.isArray(parsed)) {
        list = parsed;
      }
    } catch (error) {
      if (error.code !== "ENOENT") {
        throw error;
      }
    }

    if (!list.length) {
      list = generateSyntheticStructures(category, STRUCTURES_PER_CATEGORY);
      await fs.writeFile(filePath, JSON.stringify(list, null, 2), "utf8");
      console.log(`ℹ️ Generated synthetic structures for ${category}`);
    }

    map[category] = list.map((structure) => {
      const html = structure.html || "";
      const id = structure.id || crypto.randomUUID();
      const signature = serializeStructure(html);
      const baseClasses = extractTailwindClasses(html);
      return { id, html, signature, baseClasses };
    });
  }

  return map;
}

function generateSyntheticStructures(category, count) {
  const blocks = getStructuralBlocks();
  const list = [];
  for (let i = 0; i < count; i += 1) {
    const picked = shuffle([...blocks]).slice(0, 4 + (i % 3));
    const layout = picked
      .map((block) =>
        block
          .replaceAll("{{CATEGORY}}", category)
          .replaceAll("{{INDEX}}", String(i + 1))
      )
      .join("\n");
    list.push({ id: `${slugify(category)}-${i + 1}`, html: wrapHtml(layout) });
  }
  return list;
}

function getStructuralBlocks() {
  return [
    `<section class="grid gap-8 md:grid-cols-2 bg-white/70 p-10 rounded-[32px]">
      <div class="space-y-4">
        <p class="text-sm uppercase tracking-[0.3em] text-slate-500">{{CATEGORY}}</p>
        <h1 class="text-5xl font-black">Structure {{INDEX}}</h1>
        <p class="text-lg text-slate-600">Hero narrative tailored for {{CATEGORY}} experiences.</p>
        <div class="flex gap-4">
          <button class="px-6 py-3 bg-black text-white rounded-full">Primary</button>
          <button class="px-6 py-3 border rounded-full">Secondary</button>
        </div>
      </div>
      <div class="grid gap-4">
        <div class="rounded-3xl border p-6">
          <p class="text-sm text-slate-500">Metric A</p>
          <p class="text-4xl font-semibold">87%</p>
        </div>
        <div class="rounded-3xl border p-6">
          <p class="text-sm text-slate-500">Metric B</p>
          <p class="text-4xl font-semibold">2.3M</p>
        </div>
      </div>
    </section>`,
    `<section class="rounded-[36px] border bg-white p-12 space-y-6">
      <header class="flex flex-col gap-3">
        <p class="text-xs uppercase tracking-widest">{{CATEGORY}} Insights</p>
        <h2 class="text-4xl font-bold">Customer psyche split layout</h2>
      </header>
      <div class="grid gap-6 md:grid-cols-3">
        <article class="rounded-2xl border p-5 shadow-sm">
          <p class="text-sm text-slate-500">Segment</p>
          <p class="text-2xl font-semibold">Explorers</p>
        </article>
        <article class="rounded-2xl border p-5 shadow-sm">
          <p class="text-sm text-slate-500">Segment</p>
          <p class="text-2xl font-semibold">Creators</p>
        </article>
        <article class="rounded-2xl border p-5 shadow-sm">
          <p class="text-sm text-slate-500">Segment</p>
          <p class="text-2xl font-semibold">Operators</p>
        </article>
      </div>
    </section>`,
    `<section class="rounded-[40px] border bg-white/80 p-10">
      <div class="grid gap-8 lg:grid-cols-[1.3fr_1fr] items-center">
        <div class="space-y-6">
          <h3 class="text-3xl font-semibold">Story-driven narrative</h3>
          <p class="text-base text-slate-600">Explain how {{CATEGORY}} users move from discovery to conversion.</p>
          <ul class="space-y-3 text-sm text-slate-500">
            <li class="flex items-center gap-3"><span class="size-2 rounded-full bg-emerald-500"></span>Clarity-first message</li>
            <li class="flex items-center gap-3"><span class="size-2 rounded-full bg-sky-500"></span>Modular grid</li>
            <li class="flex items-center gap-3"><span class="size-2 rounded-full bg-amber-500"></span>Social proof rail</li>
          </ul>
        </div>
        <div class="rounded-[32px] border p-6 space-y-4">
          <p class="text-lg font-semibold">Layered CTA stack</p>
          <div class="grid gap-3">
            <button class="rounded-full bg-black py-3 text-white">Start free trial</button>
            <button class="rounded-full border py-3">Schedule demo</button>
          </div>
        </div>
      </div>
    </section>`,
    `<section class="rounded-[36px] border bg-white/60 p-10">
      <div class="flex flex-wrap items-center justify-between gap-4">
        <div>
          <p class="text-xs tracking-[0.4em] uppercase">Signals</p>
          <h4 class="text-2xl font-semibold">Operational Pulse</h4>
        </div>
        <div class="flex gap-3">
          <button class="px-4 py-2 border rounded-full">Week</button>
          <button class="px-4 py-2 border rounded-full">Month</button>
          <button class="px-4 py-2 border rounded-full">Quarter</button>
        </div>
      </div>
      <div class="mt-6 grid gap-6 md:grid-cols-4">
        <article class="rounded-3xl border p-4 text-center">
          <p class="text-sm text-slate-500">Velocity</p>
          <p class="text-3xl font-semibold">72%</p>
        </article>
        <article class="rounded-3xl border p-4 text-center">
          <p class="text-sm text-slate-500">Confidence</p>
          <p class="text-3xl font-semibold">91%</p>
        </article>
        <article class="rounded-3xl border p-4 text-center">
          <p class="text-sm text-slate-500">NPS</p>
          <p class="text-3xl font-semibold">64</p>
        </article>
        <article class="rounded-3xl border p-4 text-center">
          <p class="text-sm text-slate-500">Latency</p>
          <p class="text-3xl font-semibold">212ms</p>
        </article>
      </div>
    </section>`,
    `<section class="rounded-[38px] border bg-white/70 p-12">
      <div class="grid gap-6 md:grid-cols-2">
        <div class="space-y-5">
          <h5 class="text-3xl font-semibold">Editorial rail</h5>
          <p class="text-base text-slate-600">Highlight curated knowledge boards for {{CATEGORY}} decision-makers.</p>
          <div class="space-y-4">
            <div class="rounded-2xl border p-4">
              <p class="text-sm text-slate-500">Playlist</p>
              <p class="text-xl font-semibold">Deep dives</p>
            </div>
            <div class="rounded-2xl border p-4">
              <p class="text-sm text-slate-500">Playlist</p>
              <p class="text-xl font-semibold">Fast takes</p>
            </div>
          </div>
        </div>
        <div class="space-y-4">
          <div class="rounded-[32px] border p-5">
            <p class="text-sm text-slate-500">Trusted by</p>
            <div class="grid grid-cols-3 gap-3 text-sm font-semibold">
              <span>Nova</span>
              <span>Helix</span>
              <span>Flux</span>
            </div>
          </div>
          <div class="rounded-[32px] border p-5">
            <p class="text-sm text-slate-500">Escalation</p>
            <p class="text-3xl font-semibold">Priority lanes</p>
          </div>
        </div>
      </div>
    </section>`,
  ];
}

function wrapHtml(inner) {
  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="min-h-screen bg-slate-100 flex items-center justify-center p-10">
  <main class="w-full max-w-6xl space-y-8">${inner}</main>
</body>
</html>`;
}

function serializeStructure(html) {
  const tokens = [];
  const regex = /<\/?([a-zA-Z0-9-]+)([^>]*)>/g;
  let depth = 0;
  let match;
  while ((match = regex.exec(html))) {
    const full = match[0];
    const tag = match[1].toLowerCase();
    const isClosing = full.startsWith("</");
    const selfClosing = full.endsWith("/>");
    if (isClosing) {
      depth = Math.max(0, depth - 1);
      continue;
    }
    tokens.push(`${depth}:${tag}`);
    if (!selfClosing) {
      depth += 1;
    }
  }
  return tokens;
}

function extractTailwindClasses(html) {
  const regex = /class\s*=\s*"([^"]+)"/g;
  const classes = new Set();
  let match;
  while ((match = regex.exec(html))) {
    match[1]
      .split(/\s+/)
      .filter(Boolean)
      .forEach((cls) => classes.add(cls));
  }
  return classes;
}

function randomFrom(array) {
  return array[Math.floor(Math.random() * array.length)];
}

function shuffle(array) {
  for (let i = array.length - 1; i > 0; i -= 1) {
    const j = Math.floor(Math.random() * (i + 1));
    [array[i], array[j]] = [array[j], array[i]];
  }
  return array;
}

function slugify(value) {
  return value
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/(^-|-$)/g, "");
}

function incrementUsage(usage, category, id) {
  usage[category] = usage[category] || {};
  usage[category][id] = (usage[category][id] || 0) + 1;
}

async function generateDescription({
  category,
  styleName,
  structureHtml,
  tailwindClasses,
}) {
  const prompt = buildPrompt({ category, styleName, structureHtml, tailwindClasses });
  try {
    const response = await fetch(`${OLLAMA_HOST}/api/generate`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        model: OLLAMA_MODEL,
        prompt,
        stream: false,
      }),
    });
    if (!response.ok) {
      throw new Error(`Ollama request failed: ${response.status}`);
    }
    const payload = await response.json();
    return payload.response?.trim() || fallbackDescription(styleName, category);
  } catch (error) {
    console.warn("⚠️ Ollama generation failed, using fallback.", error.message);
    return fallbackDescription(styleName, category);
  }
}

function buildPrompt({ category, styleName, structureHtml, tailwindClasses }) {
  const truncatedHtml = structureHtml.slice(0, 2400);
  const classes = tailwindClasses.slice(0, 60).join(", ");
  return `You are an enterprise UX copywriter.
The layout below belongs to the category "${category}" and should be described in four distinct English sentences.
Each sentence must cover the following in order:
1. Design Concept – explain how the ${styleName} mood reshapes the ${category} skeleton.
2. Tech Detail – mention notable Tailwind CSS decisions referencing the following class tokens: ${classes}.
3. Accessibility – describe ARIA roles, contrast, motion safety, or keyboard focus choices.
4. Engineering Tip – provide a secure UX or defensive engineering insight referencing session integrity or safe defaults.
Ensure the summary references concrete UI behaviors.
Layout HTML:
${truncatedHtml}`;
}

function fallbackDescription(styleName, category) {
  return [
    `The ${styleName} direction reframes this ${category} flow with layered sections and deliberate pacing for conversion.`,
    "Tailwind utility orchestration balances radius tokens, gradient overlays, and responsive grids to keep density predictable.",
    "Semantic landmarks, aria-label reinforcement, and 4.5:1 contrast pairs keep the interface screen-reader ready.",
    "Ship with CSP headers, strict form validation, and short-lived tokens to ensure the experience resists session hijacking.",
  ].join(" ");
}

main().catch((error) => {
  console.error("❌ Advanced generator failed", error);
  process.exit(1);
});
