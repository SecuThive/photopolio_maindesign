# Supabase Setup Guide

## 1. Create a Supabase project
1. Sign in to [Supabase](https://supabase.com)
2. Create a new project
3. Choose a name, strong database password, and preferred region

## 2. Create the database tables

Run the following SQL inside the Supabase Dashboard → SQL Editor:

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create designs table
CREATE TABLE designs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  image_url TEXT NOT NULL,
  category TEXT,
  prompt TEXT,
  code TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW())
);

-- Create index for faster queries
CREATE INDEX idx_designs_created_at ON designs(created_at DESC);
CREATE INDEX idx_designs_category ON designs(category);

-- Enable Row Level Security (RLS)
ALTER TABLE designs ENABLE ROW LEVEL SECURITY;

-- Create policy to allow public read access
CREATE POLICY "Allow public read access"
  ON designs
  FOR SELECT
  USING (true);

-- Create policy to allow authenticated insert (admin only)
CREATE POLICY "Allow authenticated insert"
  ON designs
  FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');

-- Create policy to allow authenticated delete (admin only)
CREATE POLICY "Allow authenticated delete"
  ON designs
  FOR DELETE
  USING (auth.role() = 'authenticated');

-- Create updated_at trigger
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_designs_updated_at
  BEFORE UPDATE ON designs
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Track landing page visits for admin analytics
CREATE TABLE page_views (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
  page TEXT,
  referer TEXT,
  user_agent TEXT
);

CREATE INDEX idx_page_views_created_at ON page_views(created_at DESC);
ALTER TABLE page_views ENABLE ROW LEVEL SECURITY;
-- No public policies are created so only the service role can write/read
```

## 3. Create the storage bucket

1. Supabase Dashboard → Storage
2. Click **Create a new bucket**
3. Use the settings below:
  - **Name**: `designs-bucket`
  - **Public bucket**: ✅ enabled (public access)
4. After creating the bucket, add these policies:

### Storage Policies SQL

```sql
-- Allow public read access to all files in designs-bucket
CREATE POLICY "Public Access"
  ON storage.objects FOR SELECT
  USING (bucket_id = 'designs-bucket');

-- Allow authenticated users to upload files
CREATE POLICY "Authenticated users can upload"
  ON storage.objects FOR INSERT
  WITH CHECK (
    bucket_id = 'designs-bucket' 
    AND auth.role() = 'authenticated'
  );

-- Allow authenticated users to delete files
CREATE POLICY "Authenticated users can delete"
  ON storage.objects FOR DELETE
  USING (
    bucket_id = 'designs-bucket' 
    AND auth.role() = 'authenticated'
  );
```

## 4. Collect API keys

Supabase Dashboard → Settings → API:

- **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
- **anon/public key**: used by the frontend
- **service_role key**: used by automation/server scripts (keep secret)

## 5. Configure environment variables

### Next.js (.env.local)
```env
NEXT_PUBLIC_SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
```

### Python (.env)
```env
SUPABASE_URL=https://xxxxxxxxxxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

## 6. Smoke test

Insert sample data via the SQL Editor:

```sql
INSERT INTO designs (title, description, image_url, category, prompt)
VALUES (
  'Sample Landing Page',
  'A beautiful landing page design',
  'https://via.placeholder.com/800x600',
  'Landing Page',
  'Modern landing page with hero section'
);
```

Verify the records:
```sql
SELECT * FROM designs ORDER BY created_at DESC;
```
