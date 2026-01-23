-- Supabase에서 실행할 SQL
-- designs 테이블에 colors 컬럼 추가

ALTER TABLE designs 
ADD COLUMN IF NOT EXISTS colors TEXT[];

-- 기존 디자인들에 샘플 색상 추가 (예시)
UPDATE designs 
SET colors = ARRAY['#1E293B', '#3B82F6', '#10B981', '#F59E0B', '#EF4444']
WHERE colors IS NULL AND category = 'Dashboard';

UPDATE designs 
SET colors = ARRAY['#000000', '#FFFFFF', '#6366F1', '#EC4899', '#14B8A6']
WHERE colors IS NULL AND category = 'Landing Page';

UPDATE designs 
SET colors = ARRAY['#0F172A', '#F1F5F9', '#8B5CF6', '#F97316', '#06B6D4']
WHERE colors IS NULL AND category = 'E-commerce';

UPDATE designs 
SET colors = ARRAY['#18181B', '#FAFAFA', '#A855F7', '#FB923C', '#22D3EE']
WHERE colors IS NULL AND category = 'Portfolio';

UPDATE designs 
SET colors = ARRAY['#171717', '#F5F5F5', '#7C3AED', '#FBBF24', '#2DD4BF']
WHERE colors IS NULL AND category = 'Blog';

-- 카테고리가 없는 디자인들도 기본 색상 추가
UPDATE designs 
SET colors = ARRAY['#111827', '#F9FAFB', '#4F46E5', '#EF4444', '#10B981']
WHERE colors IS NULL;
