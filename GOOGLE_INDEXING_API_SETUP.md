# 🚀 Google Indexing API 자동화 설정 가이드

구글 크롤러를 기다리지 말고, **직접 구글한테 "여기 새 글 있으니까 긁어가"** 라고 요청하세요!

## 📋 사전 준비

### 1. Google Cloud Console 설정

1. **Google Cloud Console 접속**
   - https://console.cloud.google.com/ 이동
   - 프로젝트 생성 (또는 기존 프로젝트 선택)

2. **Indexing API 활성화**
   - 좌측 메뉴 → "API 및 서비스" → "라이브러리"
   - "Web Search Indexing API" 검색
   - **사용 설정** 클릭

3. **서비스 계정 생성**
   - "API 및 서비스" → "사용자 인증 정보"
   - 상단 "사용자 인증 정보 만들기" → "서비스 계정" 선택
   - 서비스 계정 이름 입력 (예: `indexing-api-bot`)
   - 역할: **소유자** (Owner) 선택
   - "완료" 클릭

4. **JSON 키 다운로드**
   - 생성된 서비스 계정 클릭
   - "키" 탭 → "키 추가" → "새 키 만들기"
   - 형식: **JSON** 선택
   - 자동으로 JSON 파일 다운로드됨
   - 이 파일을 `service-account-key.json` 이름으로 프로젝트 루트에 저장

### 2. Google Search Console 권한 부여

**중요**: 서비스 계정에 Search Console 권한을 줘야 합니다!

1. **Search Console 접속**
   - https://search.google.com/search-console 이동
   - 본인 사이트 선택

2. **서비스 계정 이메일 복사**
   - JSON 키 파일 열어서 `client_email` 값 복사
   - 형식: `indexing-api-bot@프로젝트명.iam.gserviceaccount.com`

3. **Search Console에 사용자 추가**
   - Search Console 좌측 메뉴 → "설정" (톱니바퀴)
   - "사용자 및 권한" 클릭
   - "사용자 추가" 버튼
   - 복사한 서비스 계정 이메일 붙여넣기
   - 권한: **소유자** 선택
   - "추가" 클릭

## 📦 파이썬 패키지 설치

```bash
pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests
```

## 🔐 보안 설정

**.gitignore에 추가** (절대 커밋하지 마세요!)

```
service-account-key.json
```

## 🎯 사용 방법

### 1. 기본 사용 (sitemap.xml 자동 추출)

```bash
python scripts/google_indexing_submit.py
```

### 2. 특정 URL만 제출

```bash
python scripts/google_indexing_submit.py --url https://yoursite.com/specific-page
```

### 3. 드라이런 (실제 제출 없이 테스트)

```bash
python scripts/google_indexing_submit.py --dry-run
```

### 4. URL 상태 확인

```bash
python scripts/google_indexing_submit.py --check-status
```

## ⚡ 효과

- **요청 후 1~2시간 이내** 색인 가능 (운 좋으면)
- 하루 **200개 URL 무료** 쿼터
- 새 글 작성 → 스크립트 실행 → 빠른 색인!

## 📊 할당량 제한

- **일일**: 200 요청
- **분당**: 600 요청
- **초당**: 제한 없음

→ 125개 URL이면 충분히 여유 있습니다!

## 🔍 트러블슈팅

### "Error 403: The caller does not have permission"
→ Search Console에 서비스 계정 추가 안 한 경우. 위 2번 단계 다시 확인!

### "Error 429: Rate limit exceeded"
→ 하루 200개 넘게 요청한 경우. 내일 다시 시도하세요.

### "Error 404: Not found"
→ Web Search Indexing API 활성화 안 한 경우. 위 1-2번 단계 확인!

## 💡 Pro Tips

1. **GitHub Actions 자동화**: 새 글 푸시할 때마다 자동으로 실행되게 설정 가능
2. **cron job**: 매일 새벽에 자동으로 실행 (혹시 누락된 URL 대비)
3. **로그 확인**: 스크립트가 어떤 URL을 제출했는지 로그 저장됨

## 🎉 완료!

이제 구글 크롤러를 **강제 소환**할 수 있습니다! 🚀
