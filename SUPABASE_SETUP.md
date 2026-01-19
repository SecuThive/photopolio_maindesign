# Supabase 설정 가이드

## 1. Supabase 프로젝트 생성
1. [Supabase](https://supabase.com)에 로그인
2. 새 프로젝트 생성
3. 프로젝트 이름, 데이터베이스 비밀번호, 리전 설정

## 2. 데이터베이스 테이블 생성

Supabase Dashboard → SQL Editor에서 다음 SQL을 실행하세요:

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

## 3. Storage Bucket 생성

1. Supabase Dashboard → Storage
2. "Create a new bucket" 클릭
3. 버킷 설정:
   - **Name**: `designs-bucket`
   - **Public bucket**: ✅ 체크 (공개 액세스 허용)
4. 생성 후 Policies 설정:

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

## 4. API Keys 확인

Supabase Dashboard → Settings → API에서 다음 정보를 확인하세요:

- **Project URL**: `https://xxxxxxxxxxxxx.supabase.co`
- **anon/public key**: 프론트엔드에서 사용
- **service_role key**: Python 스크립트에서 사용 (보안 주의!)

## 5. 환경변수 설정

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

## 6. 테스트

SQL Editor에서 테스트 데이터 삽입:

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

데이터 확인:
```sql
SELECT * FROM designs ORDER BY created_at DESC;
```
