# AI Design Gallery - Photopolio

Photopolio automatically generates AI-driven web designs, uploads them to Supabase, and showcases everything inside a polished Next.js gallery.

## 📋 Project Overview

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Backend**: Supabase (PostgreSQL + Storage)
- **Hosting**: Vercel
- **Automation**: Python + OpenAI DALL·E 3 / Ollama

## 🚀 Quick Start

### 1. Prepare Supabase

Follow [SUPABASE_SETUP.md](SUPABASE_SETUP.md) to create the project, tables, policies, and storage bucket.

Required steps:
- Create the `designs` table
- Create the `designs-bucket` storage bucket
- Enable RLS + policies
- Collect the Project URL, anon key, and service role key

### 2. Run the Next.js app

```bash
npm install
cp .env.local.example .env.local
# Fill .env.local with your Supabase values
npm run dev
```

Visit `http://localhost:3000` to browse the gallery.

### 3. Configure the automation scripts

```bash
cd automation
python -m venv venv
venv\\Scripts\\activate        # Windows
# source venv/bin/activate       # macOS/Linux
pip install -r requirements.txt
cp .env.example .env             # add Supabase + OpenAI keys
python upload_design.py --category "Landing Page"
```

See [automation/README.md](automation/README.md) for every CLI flag and scheduling tip.

## 📁 Project Structure

```
maindesign/
├── app/
│   ├── page.tsx                # Gallery home
│   ├── layout.tsx              # Root layout + metadata
│   ├── globals.css             # Global styles
│   ├── admin/
│   │   ├── page.tsx            # Login screen
│   │   └── dashboard/page.tsx  # Admin dashboard
│   └── api/admin               # Auth + metrics routes
├── components/                 # Shared UI
│   ├── Header.tsx              # Header + filters
│   ├── DesignCard.tsx          # Gallery card
│   └── DesignModal.tsx         # Detail modal
├── lib/supabase                # Client & server helpers
├── types/database.ts           # Generated Supabase types
├── automation/                 # Python + Ollama tooling
├── public/                     # Static assets
├── README.md
└── SUPABASE_SETUP.md
```

## 🎯 Features

### Gallery (`/`)
- Responsive grid of AI-generated designs
- Category filters with optimistic routing
- Modal preview with responsive iframe + code copy
- Command palette (`⌘K`) for instant navigation

### Admin (`/admin` + `/admin/dashboard`)
- Password-protected login
- Upload form (image + metadata + optional source code)
- Realtime metrics (traffic, category counts, weekly views)
- Design management with delete controls

### Automation
- Python pipeline that prompts OpenAI/Ollama
- Playwright screenshots + Supabase uploads
- Ready for cron jobs or GitHub Actions

## 🔒 Environment Variables

### Next.js (`.env.local`)

```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key
ADMIN_PASSWORD=your-secure-password
SUPABASE_SERVICE_ROLE_KEY=service-role-key (server only)
```

### Automation (`automation/.env`)

```env
SUPABASE_URL=https://xxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=service-role-key
OPENAI_API_KEY=sk-xxxx
SITE_BASE_URL=https://ui-syntax.com
INDEXNOW_KEY=your-indexnow-key
INDEXNOW_KEY_LOCATION=https://ui-syntax.com/your-indexnow-key.txt
# Optional override
# INDEXNOW_ENDPOINT=https://indexnow.bing.com/indexnow
```

## 📦 Deployment

### Next.js on Vercel
1. Push the repo to GitHub
2. Import into [Vercel](https://vercel.com)
3. Add the env vars above
4. Deploy

### Automation options
1. **Local cron** — run `run_automation.sh` or `.bat`
2. **Cloud VM** — EC2, Compute Engine, etc. with cron/systemd
3. **Serverless** — Lambda/EventBridge, Cloud Functions/Scheduler, etc.

## 🎨 Usage Examples

```bash
# Generate a landing page design
python automation/upload_design.py --category "Landing Page"

# Generate a custom dashboard concept
python automation/upload_design.py \
  --category "Dashboard" \
  --prompt "Dark analytics dashboard with neon micro charts" \
  --title "Neon Metrics Hub"
```

```ts
import { supabase } from '@/lib/supabase/client';

// Fetch the latest 12 designs
const { data } = await supabase
  .from('designs')
  .select('*')
  .order('created_at', { ascending: false })
  .limit(12);

// Filter by category
await supabase
  .from('designs')
  .select('*')
  .eq('category', 'Landing Page');
```

## 🛠 Development

```bash
npm run dev        # start dev server
npm run lint       # eslint
npm run type-check # tsc --noEmit
npm run build      # production build
```

To add a new category:
1. Update `DESIGN_TEMPLATES` (or similar) in the automation script
2. Add the option to `components/Header.tsx`

## 📊 Database Schema

```sql
CREATE TABLE designs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  description TEXT,
  image_url TEXT NOT NULL,
  category TEXT,
  prompt TEXT,
  code TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🔧 Troubleshooting

- **Images do not load** → ensure the Supabase domain is in `next.config.js` and the storage bucket is public.
- **Admin login fails** → confirm `ADMIN_PASSWORD` in `.env.local`, then clear cookies.
- **Python automation errors** → verify OpenAI credits, service-role key, and rerun `pip install -r requirements.txt`.

## 📝 License

MIT

## 🤝 Contributing

Issues and PRs are always welcome.

## 📧 Support

Open an issue if you need help or have feature requests.
