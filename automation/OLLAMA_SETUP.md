# Ollama 자동화 설정 가이드

## 📋 필수 준비사항

### 1. Ollama 설치 및 실행

#### Windows
1. [Ollama 다운로드](https://ollama.ai/download)
2. 설치 후 자동 실행됨
3. 모델 다운로드:
```powershell
ollama pull llama3
```

#### 확인
```powershell
ollama list
```

### 2. Python 패키지 설치

```powershell
cd automation
pip install -r requirements.txt
playwright install chromium
```

### 3. 환경변수 설정

`automation/.env` 파일에서 `SUPABASE_SERVICE_ROLE_KEY` 설정:

1. Supabase Dashboard → Settings → API
2. **service_role** key 복사 (anon이 아님!)
3. `.env` 파일에 붙여넣기

## 🚀 실행 방법

### 단일 디자인 생성
```powershell
cd automation
python ollama_uploader.py
```

### 2개 생성
```powershell
python ollama_uploader.py --count 2
```

### 특정 카테고리로 생성
```powershell
python ollama_uploader.py --category "Landing Page"
```

## 📝 동작 과정

1. ⚙️ Ollama로 HTML/CSS 코드 생성
2. 📸 Playwright로 렌더링 & 스크린샷
3. ☁️ Supabase Storage 업로드
4. 💾 Database 저장
5. ✅ 메인 페이지에 자동 표시

## ⚠️ 문제 해결

### Ollama 연결 오류
```powershell
# Ollama 실행 확인
ollama serve

# 다른 터미널에서
ollama list
```

### Service Role Key가 필요한 이유
- Storage에 파일 업로드하려면 service_role 권한 필요
- anon key는 읽기만 가능

### Playwright 오류
```powershell
playwright install chromium --with-deps
```

## 🎯 다음 단계: GitHub Actions

설정 완료 후 GitHub Actions로 자동화 예정!
