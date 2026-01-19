# AI Design Gallery - Photopolio

AI가 생성한 웹페이지 디자인을 자동으로 업로드하고 갤러리로 보여주는 풀스택 웹 애플리케이션입니다.

## 📋 프로젝트 개요

- **Frontend**: Next.js 14 (App Router), TypeScript, Tailwind CSS
- **Backend**: Supabase (PostgreSQL + Storage)
- **Deployment**: Vercel
- **Automation**: Python + OpenAI DALL-E 3

## 🚀 빠른 시작

### 1. Supabase 설정

[SUPABASE_SETUP.md](SUPABASE_SETUP.md) 파일을 참고하여 Supabase 프로젝트를 생성하고 설정하세요.

필수 작업:
- 테이블 생성 (`designs`)
- Storage 버킷 생성 (`designs-bucket`)
- RLS 정책 설정
- API Keys 확인

### 2. Next.js 프로젝트 설정

```bash
# 의존성 설치
npm install

# 환경변수 설정
cp .env.local.example .env.local
# .env.local 파일을 열어서 Supabase 정보 입력

# 개발 서버 실행
npm run dev
```

브라우저에서 `http://localhost:3000` 접속

### 3. Python 자동화 설정

```bash
cd automation

# 가상환경 생성 및 활성화
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 패키지 설치
pip install -r requirements.txt

# 환경변수 설정
cp .env.example .env
# .env 파일을 열어서 API Keys 입력

# 테스트 실행
python upload_design.py --category "Landing Page"
```

자세한 내용은 [automation/README.md](automation/README.md) 참고

## 📁 프로젝트 구조

```
maindesign/
├── app/                          # Next.js App Router
│   ├── page.tsx                 # 메인 갤러리 페이지
│   ├── layout.tsx               # 루트 레이아웃
│   ├── globals.css              # 글로벌 스타일
│   ├── admin/                   # Admin 페이지
│   │   ├── page.tsx            # 로그인 페이지
│   │   └── dashboard/          
│   │       └── page.tsx        # 관리자 대시보드
│   └── api/                     # API Routes
│       └── admin/               # Admin 인증 API
├── components/                   # React 컴포넌트
│   ├── Header.tsx               # 헤더 & 카테고리 필터
│   ├── DesignCard.tsx           # 디자인 카드
│   └── DesignModal.tsx          # 디자인 상세 모달
├── lib/                         # 유틸리티
│   └── supabase/
│       ├── client.ts            # 클라이언트 Supabase
│       └── server.ts            # 서버 Supabase
├── types/                       # TypeScript 타입
│   └── database.ts              # Database 타입 정의
├── automation/                  # Python 자동화 스크립트
│   ├── upload_design.py         # 메인 업로드 스크립트
│   ├── requirements.txt         # Python 의존성
│   ├── run_automation.sh        # Linux/Mac 자동화
│   ├── run_automation.bat       # Windows 자동화
│   └── README.md                # 자동화 가이드
├── package.json
├── tsconfig.json
├── tailwind.config.ts
├── next.config.js
├── .env.local.example           # 환경변수 템플릿
├── SUPABASE_SETUP.md           # Supabase 설정 가이드
└── README.md                    # 이 파일
```

## 🎯 주요 기능

### Frontend (Next.js)

#### 메인 갤러리 페이지 (`/`)
- Grid 레이아웃으로 디자인 카드 표시
- 카테고리별 필터링
- 무한 스크롤 (페이지네이션)
- 반응형 디자인
- 이미지 클릭 시 모달로 상세보기

#### Admin 페이지 (`/admin`)
- 비밀번호 기반 간단 인증
- 디자인 수동 업로드
- 등록된 디자인 목록 조회
- 디자인 삭제 기능
- 실시간 사이트 통계(일일 방문자, 총 방문자, 카테고리별 디자인 수)

### Backend (Supabase)

- **Database**: PostgreSQL로 디자인 메타데이터 저장
- **Storage**: 이미지 파일 저장 및 Public URL 제공
- **Row Level Security**: 읽기는 공개, 쓰기/삭제는 인증된 사용자만 가능

### Automation (Python)

- OpenAI DALL-E 3로 AI 이미지 생성
- Supabase Storage에 자동 업로드
- 메타데이터 자동 저장
- 크론잡으로 주기적 실행 가능
- 카테고리별 템플릿 프롬프트 제공

## 🔒 환경변수 설정

### Next.js (`.env.local`)

```env
# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://xxxxx.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key

# Admin
ADMIN_PASSWORD=your-secure-password

# Service Role (서버 사이드 전용)
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
```

### Python (`automation/.env`)

```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_SERVICE_ROLE_KEY=your-service-role-key
OPENAI_API_KEY=sk-xxxxx
```

## 📦 배포

### Vercel 배포

1. GitHub 저장소에 코드 푸시
2. [Vercel](https://vercel.com)에서 프로젝트 import
3. 환경변수 설정:
   - `NEXT_PUBLIC_SUPABASE_URL`
   - `NEXT_PUBLIC_SUPABASE_ANON_KEY`
   - `ADMIN_PASSWORD`
   - `SUPABASE_SERVICE_ROLE_KEY`
4. 배포

### Python 자동화 배포

**옵션 1: 로컬 서버/컴퓨터**
- 크론잡 설정 (Linux/Mac)
- 작업 스케줄러 설정 (Windows)

**옵션 2: 클라우드 서버**
- AWS EC2, Google Cloud Compute Engine 등
- 크론잡으로 정기 실행

**옵션 3: Serverless**
- AWS Lambda + EventBridge
- Google Cloud Functions + Cloud Scheduler
- Azure Functions + Timer Trigger

## 🎨 사용 예시

### 디자인 자동 생성 및 업로드

```bash
# 랜딩 페이지 생성
python automation/upload_design.py --category "Landing Page"

# 커스텀 프롬프트로 대시보드 생성
python automation/upload_design.py \
  --category "Dashboard" \
  --prompt "Analytics dashboard with dark theme and neon accents" \
  --title "Dark Analytics Dashboard"
```

### API 사용 (서버 컴포넌트)

```typescript
import { supabase } from '@/lib/supabase/client';

// 모든 디자인 가져오기
const { data, error } = await supabase
  .from('designs')
  .select('*')
  .order('created_at', { ascending: false })
  .limit(12);

// 카테고리별 필터링
const { data, error } = await supabase
  .from('designs')
  .select('*')
  .eq('category', 'Landing Page');
```

## 🛠️ 개발 가이드

### 로컬 개발 환경

```bash
# 개발 서버 시작
npm run dev

# 타입 체크
npm run type-check

# 린트
npm run lint

# 빌드
npm run build
```

### 새로운 카테고리 추가

1. `automation/upload_design.py`의 `DESIGN_TEMPLATES`에 추가
2. `components/Header.tsx`의 `categories` 배열에 추가

### 커스터마이징

- **색상**: `tailwind.config.ts` 수정
- **레이아웃**: `app/page.tsx` 수정
- **카드 디자인**: `components/DesignCard.tsx` 수정

## 📊 데이터베이스 스키마

```sql
CREATE TABLE designs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  title TEXT NOT NULL,
  description TEXT,
  image_url TEXT NOT NULL,
  category TEXT,
  prompt TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

## 🔧 문제 해결

### 이미지가 로드되지 않음
- `next.config.js`에 Supabase 도메인이 추가되었는지 확인
- Supabase Storage 버킷이 Public으로 설정되었는지 확인

### Admin 페이지 로그인 실패
- `.env.local`의 `ADMIN_PASSWORD` 확인
- 브라우저 쿠키 삭제 후 재시도

### Python 스크립트 오류
- OpenAI API 키가 유효한지 확인
- Supabase Service Role Key가 올바른지 확인
- `pip install -r requirements.txt` 재실행

## 📝 라이선스

MIT License

## 🤝 기여

이슈와 PR은 언제나 환영합니다!

## 📧 문의

프로젝트 관련 문의사항이 있으시면 이슈를 남겨주세요.
