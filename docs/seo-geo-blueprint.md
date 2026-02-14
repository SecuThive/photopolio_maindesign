# UI Syntax SEO & GEO Blueprint

## 1. 정보 구조 리뷰
- **현재 구조**: `/` → `/collections/[slug]` → `/design/[slug]`, `/blog/[slug]`. 블로그는 컬렉션/디자인과 연결이 거의 없고, 컬렉션 페이지는 얕은 소개만 제공.
- **문제점**
  - 카테고리 허브 콘텐츠 부족(400단어 내외)으로 랭킹 경쟁력이 떨어짐.
  - 필러 페이지 부재로 토픽 권위가 분산.
  - 내부 링크가 홈·컬렉션 사이에만 있어 클러스터 구조가 모호.
  - 모든 디자인이 동일 빈도로 sitemap에 노출되어 크롤링 비효율.
- **신규 계층 제안**
  1. `Pillar (playbooks/[slug])` – 전략·프레임워크·FAQ 중심의 2,500+ 단어 권위 페이지.
  2. `Collection Hub (collections/[slug])` – 800~1,000 단어 설명 + ItemList/FAQ.
  3. `Design Detail (design/[slug])` – 실사용 패턴 분석, 전략 메모, 성능/접근성 섹션.

## 2. 필러 페이지 시스템
| 토픽 | URL | H1/H2 구조 | 추천 스키마 | 링크 전략 |
| --- | --- | --- | --- | --- |
| SaaS Landing Page UX Strategy | `/playbooks/saas-landing-page-ux` | H1: Strategy → H2: Value Prop Matrix / Hero Experiments / CTA Ladder / Case Studies / FAQ | `Article`, `BreadcrumbList`, 섹션별 `HowTo` | 각 H2에서 관련 디자인 2~3개, 해당 컬렉션 1개, 블로그 심화글 1개 링크 |
| Dashboard UX Design Principles | `/playbooks/dashboard-ux-principles` | 정보 구조, 데이터 밀도, 다크모드 지침, QA 체크리스트 | `Article`, `FAQPage` | Dashboard 컬렉션 + 핵심 디자인 10개 |
| E-Commerce UI Conversion Patterns | `/playbooks/ecommerce-conversion-patterns` | 구매 여정, 신뢰 요소, 장바구니 UX, CRO 실험 | `Article`, `ItemList` | 전자상거래 디자인, 관련 블로그 |
| UX Psychology in Modern Interfaces | `/playbooks/ux-psychology` | 인지 편향, 사회적 증거, 감성 톤, 실험 결과 | `Article`, `Dataset`(선택) | 패턴별 디자인/블로그 교차 링크 |
| UI Optimization for Core Web Vitals | `/playbooks/ui-core-web-vitals` | LCP/CLS/INP 요약, 컴포넌트 가이드, 코드 스니펫 | `Article`, `TechArticle`, `FAQPage` | 성능 관련 디자인, 개발 문서 링크 |

## 3. 디자인 상세 리팩터링 (/design/[slug])
- **섹션**
  - H1: 기존 타이틀 유지.
  - H2 `UX Strategy Behind This Layout`: 2~3문단 + 전략 bullet.
  - H2 `Psychological Triggers Used`: 인지 편향/사회적 증거 설명.
  - H2 `When To Use This Pattern`: 3가지 시나리오.
  - H2 `Performance Considerations`: 이미지, 폰트, LCP 팁.
  - H2 `Accessibility Considerations`: 대비, 키보드 포커스, aria.
- **메타/데이터**
  - `generateMetadata`에서 canonical 유지.
  - JSON-LD `CreativeWork` 확장: `audience`, `isPartOf` (컬렉션/필러), `about`, `material`, `timeRequired`.
  - `BreadcrumbList`: Home → Pillar → Collection → Design.
- **구현**
  - `/components/design/StrategySections.tsx` 컴포넌트 생성.
  - Supabase `designs` 테이블에 `strategy_notes`, `psychology_notes`, `performance_notes`, `accessibility_notes` 컬럼 추가 또는 `jsonb` 필드 사용.

## 4. 컬렉션 페이지 업그레이드
- 목표: 각 `/collections/[slug]`에 500~1,000 단어 설명 + 체크리스트 + FAQ.
- **구성**
  1. Hero 정의 단락 + 요약 리스트.
  2. `Best Practices` 섹션(불릿 5~7개).
  3. `Implementation Checklist` (번호 리스트).
  4. `FAQ` 4~6문항 (`FAQ schema`).
  5. `ItemList schema`: 포함 디자인 8~12개.
  6. `Related Pillar` 섹션.
- 재사용 컴포넌트: `CollectionOverview`, `BestPracticeList`, `FAQList`, `SchemaInjector`.

## 5. 내부 링크 클러스터
```
Home
 ├─ Pillar (playbooks)
 │    ├─ Collection A
 │    │    ├─ Design 1 ↔ Collection A / Pillar
 │    │    ├─ Design 2 ↔ Collection A / Pillar
 │    │    └─ ...
 │    └─ Collection B ...
 └─ Blog posts → Pillar 섹션 앵커 ↔ Design
```
- 홈 hero/feature 섹션에서 상위 3개 필러 바로가기 버튼.
- 필러: `Featured Designs` 컴포넌트로 10~20개 디자인 리스트 + `Related Collections`.
- 컬렉션: 본문 중간에 필러 CTA, 디자인 카드 아래 “전략 읽기” 링크.
- 디자인: 사이드바에 `Part of` 배지 (컬렉션, 필러). 본문 끝 `Further Reading`으로 블로그/필러 링크.

## 6. 크롤링/사이트맵 전략
- `sitemap.ts` 분리: `base`, `playbooks`, `collections`, `designs-a`, `designs-b`, `blog`.
- `changefreq`: Pillar/Collection weekly, Blog weekly, Design monthly (최근 업데이트 시만 daily).
- 디자인 ID 파티셔닝(예: a-m, n-z)으로 sitemap 분할.
- 컬렉션 페이지네이션: `/collections/[slug]/page/[n]` 라우트 추가, `rel="next"/"prev"`, canonical은 페이지별 유지.
- `robots`: 새로운 `/playbooks` 포함, 불필요한 API 경로는 `Disallow` 유지.

## 7. GEO 최적화 레이어
- 텍스트 패턴
  - 정의형 문단: “A SaaS landing page is …”.
  - 구조화 요약 `<section role="doc-abstract">`.
  - 리스트 기반 섹션 최소 3개.
  - 인용/출처 톤: “According to usability heuristics…”.
- 코드 제언
  - `lib/content/patterns.ts`: `buildDefinition`, `buildSummary`, `buildChecklist` 헬퍼.
  - `PillarSection` 컴포넌트에서 `props`로 정의/요약/리스트 조합하도록 강제.
  - `generateMetadata`에서 `other: { 'citation_title': title }` 등 추가.

## 8. 이슈 및 개선 요약
- **Critical**
  - 필러 페이지 부재 → 토픽 권위 낮음.
  - 컬렉션 허브 콘텐츠/FAQ 부족.
  - 디자인 상세에 전략/성능/접근성 정보 미노출.
- **Medium**
  - 내부 링크 체계 미비.
  - JSON-LD 범위 제한(FAQ, ItemList, Breadcrumb 없음).
  - Sitemap 단일 + changefreq 과다.
- **Structural Improvements**
  - `/playbooks` 디렉터리 추가, 컬렉션/디자인 전용 컴포넌트 분리.
  - Supabase 스키마 확장(전략 메모 필드).
  - 콘텐츠 헬퍼/스키마 빌더 모듈화.

## 9. 추천 디렉터리 구조
```
app/
  playbooks/
    layout.tsx
    [slug]/
      page.tsx
      sections.tsx
  collections/
    layout.tsx
    [slug]/page.tsx
  design/
    [slug]/
      StrategySections.tsx
components/
  content/
    PillarHero.tsx
    DefinitionBlock.tsx
    FAQList.tsx
    ItemListSchema.tsx
lib/
  content/
    patterns.ts
    linkMatrix.ts
  seo/
    schemaBuilders.ts
    sitemapConfig.ts
```

## 10. 4주 구현 로드맵
- **Week 1**: IA 확정, `/playbooks` 레이아웃/템플릿 구축, sitemap 다중 파일 지원.
- **Week 2**: 컬렉션 템플릿 리팩터링, 콘텐츠 컴포넌트/FAQ/ItemList 스키마 적용.
- **Week 3**: 디자인 상세 섹션 + Supabase 필드 추가, Breadcrumb/JSON-LD 확장.
- **Week 4**: GEO 패턴 헬퍼 도입, 내부 링크 매트릭스 자동화, QA (Lighthouse + 구조화 데이터 테스트), 문서화.
