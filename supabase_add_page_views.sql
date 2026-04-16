-- ── page_views 테이블 ────────────────────────────────────────────
-- UI-Syntax 디자인 조회 이벤트 저장 (일별 트렌드, 카테고리별 분석용)
-- /api/admin/metrics 엔드포인트가 이 테이블을 참조합니다.

CREATE TABLE IF NOT EXISTS public.page_views (
  id          BIGSERIAL PRIMARY KEY,
  design_id   UUID        REFERENCES public.designs(id) ON DELETE SET NULL,
  slug        TEXT,
  category    TEXT,
  created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- 인덱스
CREATE INDEX IF NOT EXISTS idx_page_views_design_id  ON public.page_views (design_id);
CREATE INDEX IF NOT EXISTS idx_page_views_category   ON public.page_views (category);
CREATE INDEX IF NOT EXISTS idx_page_views_created_at ON public.page_views (created_at DESC);

-- RLS
ALTER TABLE public.page_views ENABLE ROW LEVEL SECURITY;

CREATE POLICY "page_views_read_all"
  ON public.page_views FOR SELECT
  USING (true);

CREATE POLICY "page_views_insert_all"
  ON public.page_views FOR INSERT
  WITH CHECK (true);

-- ── designs.quality_score 컬럼 추가 (아직 없는 경우) ─────────────
ALTER TABLE public.designs
  ADD COLUMN IF NOT EXISTS quality_score NUMERIC(4,2);

CREATE INDEX IF NOT EXISTS idx_designs_quality_score
  ON public.designs (quality_score DESC NULLS LAST);
