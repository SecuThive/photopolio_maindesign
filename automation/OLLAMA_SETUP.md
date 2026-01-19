# Ollama Automation Setup Guide

## 📋 Prerequisites

### 1. Install and run Ollama

#### Windows
1. [Download Ollama](https://ollama.ai/download)
2. Finish the installer (Ollama starts automatically)
3. Pull a model:
```powershell
ollama pull llama3
```

#### Verify
```powershell
ollama list
```

### 2. Install Python dependencies

```powershell
cd automation
pip install -r requirements.txt
playwright install chromium
```

### 3. 환경변수 설정

Edit `automation/.env` and add `SUPABASE_SERVICE_ROLE_KEY`:

1. Supabase Dashboard → Settings → API
2. Copy the **service_role** key (not the anon key)
3. Paste it into `.env`

## 🚀 Run the script

### Generate one design
```powershell
cd automation
python ollama_uploader.py
```

### Generate two designs
```powershell
python ollama_uploader.py --count 2
```

### Target a specific category
```powershell
python ollama_uploader.py --category "Landing Page"
```

## 📝 Workflow

1. ⚙️ Generate HTML/CSS via Ollama
2. 📸 Render with Playwright and capture a screenshot
3. ☁️ Upload the image to Supabase Storage
4. 💾 Save metadata to the Supabase database
5. ✅ The gallery consumes the new record automatically

## ⚠️ Troubleshooting

### Ollama connection issues
```powershell
# Start/verify Ollama
ollama serve

# In another terminal
ollama list
```

### Why the service-role key is required
- Storage uploads require elevated permissions
- The anon key is read-only

### Playwright issues
```powershell
playwright install chromium --with-deps
```

## 🎯 Next step: GitHub Actions

After validating local runs, wire this script into your preferred CI/CD workflow.
