# GitHub Actions 자동 디자인 생성 설정

## 📋 개요
매일 자동으로 10개의 새로운 디자인을 생성하는 GitHub Actions workflow가 설정되었습니다.

## ⚙️ GitHub Secrets 설정

GitHub Repository에서 다음 환경 변수를 설정해야 합니다:

1. **GitHub 저장소로 이동**
2. **Settings** → **Secrets and variables** → **Actions** 클릭
3. **New repository secret** 버튼 클릭
4. 다음 2개의 Secret 추가:

### Required Secrets

| Name | Value | 설명 |
|------|-------|------|
| `SUPABASE_URL` | `https://vswzoulerodrphbsfkjq.supabase.co` | Supabase 프로젝트 URL |
| `SUPABASE_SERVICE_ROLE_KEY` | `your-service-role-key` | Supabase Service Role Key |

### Supabase Service Role Key 찾기

1. [Supabase Dashboard](https://supabase.com/dashboard) 접속
2. 프로젝트 선택
3. **Settings** → **API** 메뉴
4. **Project API keys** 섹션에서 **service_role** key 복사
5. GitHub Secret에 추가

## 🕐 실행 스케줄

- **자동 실행**: 매일 UTC 00:00 (한국시간 오전 9시)
- **수동 실행**: GitHub Actions 탭에서 "Run workflow" 버튼으로 언제든 실행 가능

## 🎨 생성 설정

- **카테고리별 생성 개수**: 10개씩
- **총 생성 개수**: 60개 (Landing Page 10, Dashboard 10, E-commerce 9, Portfolio 10, Blog 10, Components 10)
- **생성 시간**: 약 5-10분 소요 (GitHub Actions 환경에서)

## 📝 수동 실행 방법

1. GitHub 저장소의 **Actions** 탭으로 이동
2. 왼쪽에서 **Auto Generate Designs** workflow 선택
3. 오른쪽 상단의 **Run workflow** 버튼 클릭
4. **Run workflow** 확인 버튼 클릭

## 🔍 실행 결과 확인

1. GitHub **Actions** 탭에서 실행 중인 workflow 확인
2. workflow 클릭하여 상세 로그 확인
3. 각 단계별 진행 상황 모니터링 가능
4. 완료 후 Supabase 데이터베이스에서 새로운 디자인 확인

## ⚠️ 주의사항

### 중복 방지
- 각 카테고리는 최대 10개의 고유 구조를 가지고 있음
- 이미 10개 디자인이 생성된 경우, 추가 생성 시 실패할 수 있음
- 새로운 디자인을 계속 생성하려면 기존 디자인 삭제 필요

### GitHub Actions 무료 사용 한도
- Public 저장소: 무제한
- Private 저장소: 월 2,000분 무료
- Playwright 브라우저 설치 및 스크린샷 캡처로 인해 실행 시간이 길 수 있음

### 비용 관리
매일 자동 생성이 과도한 경우, cron 스케줄 조정:
- 주 1회: `'0 0 * * 1'` (매주 월요일)
- 월 1회: `'0 0 1 * *'` (매월 1일)
- 주 2회: `'0 0 * * 1,4'` (월요일, 목요일)

## 🛠️ 문제 해결

### Workflow 실패 시
1. Actions 탭에서 실패한 workflow 클릭
2. 에러 로그 확인
3. 주요 원인:
   - Secret 설정 누락
   - Supabase 연결 실패
   - 이미 모든 구조가 생성됨

### Secret 업데이트
1. Settings → Secrets and variables → Actions
2. 해당 Secret 클릭
3. Update secret으로 값 변경

## 📊 현재 설정

```yaml
Schedule: 매일 UTC 00:00 (한국 09:00)
Python: 3.12
Browser: Chromium (Playwright)
Designs per run: 10 per category
Total: ~59 designs per run (E-commerce는 9개)
```

## 🚀 최적화 옵션

### 생성 개수 조정
workflow 파일의 마지막 명령어 수정:
```yaml
python design_generator_final.py --total 5  # 6개 카테고리를 합쳐 총 5개만 생성
```

### 특정 카테고리만 생성
```yaml
python design_generator_final.py --category "Landing Page" --count 10
```

### 실행 빈도 조정
`.github/workflows/generate-designs.yml` 파일의 cron 수정:
```yaml
schedule:
  - cron: '0 0 * * 1'  # 매주 월요일만
```
