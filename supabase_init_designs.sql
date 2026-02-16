-- Complete initialization script for designs table
-- Run this ONCE in Supabase SQL Editor

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Create designs table with all columns including tags
CREATE TABLE public.designs (
  id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
  title TEXT NOT NULL,
  description TEXT,
  image_url TEXT NOT NULL,
  category TEXT,
  prompt TEXT,
  code TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT TIMEZONE('utc', NOW()),
  likes INTEGER DEFAULT 0,
  views INTEGER DEFAULT 0,
  slug TEXT,
  colors TEXT[],
  tags TEXT[] DEFAULT '{}',
  status TEXT DEFAULT 'published' CHECK (status IN ('published', 'archived')),
  strategy_notes TEXT,
  psychology_notes TEXT,
  usage_notes TEXT,
  performance_notes TEXT,
  accessibility_notes TEXT,
  colorable_regions JSONB
);

-- Create indexes for faster queries
CREATE INDEX idx_designs_created_at ON public.designs(created_at DESC);
CREATE INDEX idx_designs_category ON public.designs(category);
CREATE INDEX idx_designs_slug ON public.designs(slug);
CREATE INDEX idx_designs_status ON public.designs(status);
CREATE INDEX idx_designs_tags ON public.designs USING GIN (tags);

-- Add comments
COMMENT ON COLUMN public.designs.tags IS 'Array of tags for filtering designs within collections (e.g., saas, hero, conversion)';
COMMENT ON COLUMN public.designs.status IS 'Publication status: published (visible) or archived (hidden but keeps slug)';

-- Enable Row Level Security (RLS)
ALTER TABLE public.designs ENABLE ROW LEVEL SECURITY;

-- Create policy to allow public read access (only published)
CREATE POLICY "Allow public read access"
  ON public.designs
  FOR SELECT
  USING (status = 'published');

-- Create policy to allow authenticated insert (admin only)
CREATE POLICY "Allow authenticated insert"
  ON public.designs
  FOR INSERT
  WITH CHECK (auth.role() = 'authenticated');

-- Create policy to allow authenticated update (admin only)
CREATE POLICY "Allow authenticated update"
  ON public.designs
  FOR UPDATE
  USING (auth.role() = 'authenticated');

-- Create policy to allow authenticated delete (admin only)
CREATE POLICY "Allow authenticated delete"
  ON public.designs
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
  BEFORE UPDATE ON public.designs
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- Auto-tag existing designs based on patterns
-- (These will only apply if you're adding designs immediately)

-- SaaS Landing Pages
UPDATE public.designs 
SET tags = ARRAY['saas', 'landing', 'b2b']
WHERE category = 'Landing Page' 
  AND (title ILIKE '%saas%' OR title ILIKE '%b2b%')
  AND tags = '{}';

-- Hero Sections
UPDATE public.designs 
SET tags = ARRAY['hero', 'above-fold', 'conversion']
WHERE category = 'Landing Page' 
  AND (title ILIKE '%hero%' OR description ILIKE '%hero%')
  AND tags = '{}';

-- Dashboards
UPDATE public.designs 
SET tags = ARRAY['dashboard', 'analytics']
WHERE category = 'Dashboard' 
  AND tags = '{}';

-- Minimalist Dashboards
UPDATE public.designs 
SET tags = ARRAY['dashboard', 'minimal', 'clean']
WHERE category = 'Dashboard' 
  AND (title ILIKE '%minimal%' OR description ILIKE '%minimal%' OR description ILIKE '%clean%')
  AND tags = '{}';

-- E-commerce Product Pages
UPDATE public.designs 
SET tags = ARRAY['ecommerce', 'product', 'pdp']
WHERE category = 'E-commerce' 
  AND (title ILIKE '%product%' OR description ILIKE '%product%')
  AND tags = '{}';

-- Checkout/Cart
UPDATE public.designs 
SET tags = ARRAY['ecommerce', 'checkout', 'cart']
WHERE category = 'E-commerce' 
  AND (title ILIKE '%checkout%' OR title ILIKE '%cart%')
  AND tags = '{}';

-- Portfolio/Case Studies
UPDATE public.designs 
SET tags = ARRAY['portfolio', 'case-study']
WHERE category = 'Portfolio' 
  AND tags = '{}';

-- Blog/Articles
UPDATE public.designs 
SET tags = ARRAY['blog', 'content', 'editorial']
WHERE category = 'Blog' 
  AND tags = '{}';

-- Components
UPDATE public.designs 
SET tags = ARRAY['component', 'ui-element']
WHERE category = 'Components' 
  AND tags = '{}';

-- Fintech Trust Screens
UPDATE public.designs 
SET tags = ARRAY['fintech', 'trust', 'security']
WHERE (title ILIKE '%fintech%' OR title ILIKE '%trust%' OR title ILIKE '%security%')
  AND tags = '{}';

-- Pricing Pages
UPDATE public.designs 
SET tags = ARRAY['pricing', 'saas', 'conversion']
WHERE (title ILIKE '%pricing%' OR description ILIKE '%pricing%')
  AND tags = '{}';

-- Onboarding Flows
UPDATE public.designs 
SET tags = ARRAY['onboarding', 'activation', 'signup']
WHERE (title ILIKE '%onboarding%' OR title ILIKE '%signup%')
  AND tags = '{}';
