automation/
# AI Design Gallery Automation

Python scripts generate AI-powered layouts, take screenshots, and push everything to Supabase.

## Installation

1. Create a virtual environment (recommended):
```bash
cd automation
python -m venv venv
venv\\Scripts\\activate      # Windows
# source venv/bin/activate     # macOS/Linux
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure environment variables:
```bash
cp .env.example .env
# then edit .env with SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY
```

## Usage

### Manual runs

```bash
# Generate a landing page with default prompt pool
python upload_design.py --category "Landing Page"

# Provide a custom prompt
python upload_design.py --category "Dashboard" --prompt "Modern analytics dashboard with dark theme"

# Specify every field
python upload_design.py \
  --category "E-commerce" \
  --title "Fashion Store Homepage" \
  --description "Elegant e-commerce layout for a luxury brand" \
  --prompt "Luxury fashion storefront with minimalist hero and featured products"
```

Supported categories: `Landing Page`, `Dashboard`, `E-commerce`, `Portfolio`, `Blog`.

## Scheduling

### Linux / macOS

```bash
crontab -e

# Run every day at 9am
0 9 * * * /path/to/photopolio/maindesign/automation/run_automation.sh

# Run every 3 hours
0 */3 * * * /path/to/photopolio/maindesign/automation/run_automation.sh
```

### Windows Task Scheduler

1. Open **Task Scheduler**
2. Create Basic Task → choose name/time
3. Action: run `run_automation.bat`
4. Finish

PowerShell alternative:
```powershell
$action = New-ScheduledTaskAction -Execute "C:\\Projects\\photopolio\\maindesign\\automation\\run_automation.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "AI Design Upload" -Description "Daily AI design generation"
```

## Directory layout

```
automation/
├── upload_design.py      # Main script
├── requirements.txt      # Python dependencies
├── .env.example          # Template env file
├── run_automation.sh     # Cron helper
├── run_automation.bat    # Windows helper
└── automation.log        # Generated log file
```

## How it works

1. Prompt OpenAI DALL·E (or Ollama) for a layout image
2. Upload the screenshot to the `designs-bucket` storage bucket
3. Store metadata + image URL inside the `designs` table

## IndexNow automation

Set up once and every script run will ping participating search engines:

1. Create an IndexNow key at [indexnow.org](https://www.indexnow.org/keys) and place the `.txt` file in `public/` so it ships with your Next.js app (e.g., `public/your-key.txt`).
2. Add these variables to `automation/.env` (see `.env.example`):
  - `SITE_BASE_URL=https://www.ui-syntax.com`
  - `INDEXNOW_KEY=your-key`
  - `INDEXNOW_KEY_LOCATION=https://www.ui-syntax.com/your-key.txt`
3. Optional: override `INDEXNOW_ENDPOINT` if you need a different region.

When configured, both `design_generator_final.py` and `upload_design.py` automatically call IndexNow with the homepage, the design permalink (`/?design=<id>`), and the relevant category filter URL.

## Troubleshooting

- **ImportError: No module named 'supabase'** → run `pip install -r requirements.txt`
- **OpenAI API errors** → confirm the key, available credits, and region at [OpenAI API Keys](https://platform.openai.com/api-keys)
- **Supabase connection errors** → double-check `SUPABASE_URL`, `SUPABASE_SERVICE_ROLE_KEY`, and that the bucket/table exist

## Cost notes

- DALL·E 3 (1024×1024) ≈ $0.04 per image; 1792×1024 ≈ $0.08
- Daily run (1792×1024) ≈ $2.40/month; three runs per day ≈ $7.20/month
- Supabase free tier includes 500 MB storage + 2 GB bandwidth; upgrade to Pro ($25/mo) if you exceed limits

## Advanced tweaks

```python
# Change image size in upload_design.py
image_data = self.generate_image(prompt, size="1024x1024")
```

```bash
# Batch-generate multiple categories
for category in "Landing Page" "Dashboard" "Portfolio"; do
  python upload_design.py --category "$category"
  sleep 5
done
```

## Logs

```bash
tail -f automation.log
```
