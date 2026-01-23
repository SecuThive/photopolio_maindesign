# 🎨 색상 팔레트 기능 활성화 가이드

색상 프리뷰 기능이 작동하려면 Supabase 데이터베이스에 `colors` 컬럼을 추가해야 합니다.

## 1단계: Supabase SQL Editor에서 실행

1. **Supabase Dashboard 접속**: https://supabase.com/dashboard
2. 프로젝트 선택
3. 왼쪽 메뉴에서 **SQL Editor** 클릭
4. 아래 SQL을 복사해서 실행:

```sql
-- designs 테이블에 colors 컬럼 추가
ALTER TABLE designs 
ADD COLUMN IF NOT EXISTS colors TEXT[];

-- 인덱스 생성 (선택사항, 성능 향상)
CREATE INDEX IF NOT EXISTS idx_designs_colors ON designs USING GIN(colors);
```

## 2단계: 기존 디자인에 색상 데이터 추가

SQL Editor에서 아래 SQL도 실행:

```sql
-- 카테고리별 샘플 색상 추가
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

UPDATE designs 
SET colors = ARRAY['#0C4A6E', '#E0F2FE', '#0EA5E9', '#F43F5E', '#84CC16']
WHERE colors IS NULL AND category = 'Components';

-- 카테고리가 없는 디자인들도 기본 색상 추가
UPDATE designs 
SET colors = ARRAY['#111827', '#F9FAFB', '#4F46E5', '#EF4444', '#10B981']
WHERE colors IS NULL;
```

## 3단계 (선택): Node.js 스크립트로 업데이트

터미널에서 실행:

```bash
npx tsx scripts/add-colors-to-designs.ts
```

## 확인 방법

1. 사이트에서 아무 디자인 상세 페이지 접속
2. 이미지 아래에 "Color Palette" 섹션이 보임
3. 색상을 클릭하면 프리뷰에 색상이 적용됨

## 색상 팔레트 커스터마이징

개별 디자인의 색상을 변경하려면:

```sql
UPDATE designs 
SET colors = ARRAY['#색상1', '#색상2', '#색상3', '#색상4', '#색상5']
WHERE id = '디자인ID';
```

예시:
```sql
UPDATE designs 
SET colors = ARRAY['#FF0000', '#00FF00', '#0000FF', '#FFFF00', '#FF00FF']
WHERE id = 'abc123';
```
