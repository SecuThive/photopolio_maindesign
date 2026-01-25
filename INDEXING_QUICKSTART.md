# Google Indexing API - 빠른 시작 가이드 🚀

구글 색인을 강제로 요청하는 3단계 설정!

## Step 1: Python 패키지 설치

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

## Step 2: Google Cloud 설정

1. https://console.cloud.google.com/ 접속
2. "Web Search Indexing API" 활성화
3. 서비스 계정 생성 및 JSON 키 다운로드
4. JSON 키를 `service-account-key.json` 이름으로 프로젝트 루트에 저장

**자세한 설정 방법**: `GOOGLE_INDEXING_API_SETUP.md` 참고

## Step 3: 스크립트 실행

### 첫 실행 (테스트)
```bash
# 스크립트 파일 수정 필요: SITEMAP_URL 변수를 실제 사이트 주소로 변경
# scripts/google_indexing_submit.py 파일 열어서:
# SITEMAP_URL = 'https://yoursite.com/sitemap.xml'  # ← 여기 수정!

# 테스트 실행 (실제 제출 안 함)
python scripts/google_indexing_submit.py --dry-run
```

### 실제 제출
```bash
# 모든 URL 제출
python scripts/google_indexing_submit.py

# 특정 URL만 제출
python scripts/google_indexing_submit.py --url https://yoursite.com/page

# URL 상태 확인
python scripts/google_indexing_submit.py --check-status
```

## 📊 기대 효과

- ✅ 1~2시간 이내 색인 (운 좋으면)
- ✅ 하루 200개 URL 무료
- ✅ 자동화로 시간 절약

## ⚠️ 중요 체크리스트

- [ ] `service-account-key.json` 파일 다운로드
- [ ] Search Console에 서비스 계정 이메일 추가 (소유자 권한)
- [ ] 스크립트에서 `SITEMAP_URL` 변수 수정
- [ ] `.gitignore`에 `service-account-key.json` 추가됨 확인

## 💡 문제 해결

**"403 Permission denied"** → Search Console에 서비스 계정 추가 안 함
**"404 Not found"** → Web Search Indexing API 활성화 안 함  
**"파일을 찾을 수 없음"** → `service-account-key.json` 위치 확인

---

더 자세한 설명은 `GOOGLE_INDEXING_API_SETUP.md` 참고!
