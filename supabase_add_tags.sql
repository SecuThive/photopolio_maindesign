-- Add tags column to designs table for better collection filtering
ALTER TABLE public.designs ADD COLUMN IF NOT EXISTS tags text[] DEFAULT '{}';

-- Create GIN index for efficient tag searches
CREATE INDEX IF NOT EXISTS idx_designs_tags ON public.designs USING GIN (tags);

-- Add comment
COMMENT ON COLUMN public.designs.tags IS 'Array of tags for filtering designs within collections (e.g., saas, hero, conversion)';

-- Example: Update existing designs with initial tags based on category and title
-- These are examples - adjust based on your actual data

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
