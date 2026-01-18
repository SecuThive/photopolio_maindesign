# AI Design Gallery Automation

Python 스크립트를 사용하여 AI 이미지를 생성하고 자동으로 Supabase에 업로드합니다.

## 설치

1. Python 가상환경 생성 (권장):
```bash
cd automation
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

2. 필요한 패키지 설치:
```bash
pip install -r requirements.txt
```

3. 환경변수 설정:
```bash
# .env.example을 .env로 복사
cp .env.example .env

# .env 파일을 열어서 실제 값으로 수정
# - SUPABASE_URL
# - SUPABASE_SERVICE_ROLE_KEY
# - OPENAI_API_KEY
```

## 사용법

### 수동 실행

1. 기본 실행 (랜덤 프롬프트):
```bash
python upload_design.py --category "Landing Page"
```

2. 커스텀 프롬프트로 실행:
```bash
python upload_design.py --category "Dashboard" --prompt "Modern analytics dashboard with dark theme"
```

3. 모든 옵션 지정:
```bash
python upload_design.py \
  --category "E-commerce" \
  --title "Fashion Store Homepage" \
  --description "Elegant e-commerce design for fashion brand" \
  --prompt "Luxury fashion e-commerce homepage with minimalist design"
```

### 카테고리 옵션

- `Landing Page`
- `Dashboard`
- `E-commerce`
- `Portfolio`
- `Blog`

## 자동화 (Cron Job)

### Linux/Mac

1. 크론탭 편집:
```bash
crontab -e
```

2. 크론잡 추가 (매일 오전 9시 실행):
```
0 9 * * * /path/to/photopolio/maindesign/automation/run_automation.sh
```

3. 크론잡 추가 (3시간마다 실행):
```
0 */3 * * * /path/to/photopolio/maindesign/automation/run_automation.sh
```

### Windows

1. 작업 스케줄러 열기
2. "기본 작업 만들기" 클릭
3. 트리거: 원하는 시간 설정
4. 작업: `run_automation.bat` 파일 실행
5. 완료

또는 PowerShell로 작업 스케줄러 등록:
```powershell
$action = New-ScheduledTaskAction -Execute "C:\Users\PC\photopolio\maindesign\automation\run_automation.bat"
$trigger = New-ScheduledTaskTrigger -Daily -At 9am
Register-ScheduledTask -Action $action -Trigger $trigger -TaskName "AI Design Upload" -Description "Daily AI design generation and upload"
```

## 스크립트 구조

```
automation/
├── upload_design.py      # 메인 스크립트
├── requirements.txt      # Python 패키지 의존성
├── .env.example         # 환경변수 템플릿
├── .env                 # 실제 환경변수 (생성 필요, git에서 제외됨)
├── run_automation.sh    # Linux/Mac 자동화 스크립트
├── run_automation.bat   # Windows 자동화 스크립트
└── automation.log       # 실행 로그 (자동 생성)
```

## 동작 방식

1. **이미지 생성**: OpenAI DALL-E 3 API를 사용하여 웹 디자인 이미지 생성
2. **스토리지 업로드**: 생성된 이미지를 Supabase Storage의 `designs-bucket`에 업로드
3. **데이터베이스 저장**: 이미지 URL과 메타데이터를 `designs` 테이블에 저장

## 문제 해결

### ImportError: No module named 'supabase'
```bash
pip install -r requirements.txt
```

### OpenAI API Error
- API 키가 올바른지 확인
- OpenAI 계정에 충분한 크레딧이 있는지 확인
- [OpenAI API Keys](https://platform.openai.com/api-keys)에서 키 확인

### Supabase Connection Error
- SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY가 올바른지 확인
- Supabase 프로젝트가 활성화되어 있는지 확인
- Storage bucket과 테이블이 생성되었는지 확인

## 비용 안내

### OpenAI DALL-E 3 비용 (2024년 기준)
- Standard quality (1024x1024): $0.040 per image
- Standard quality (1792x1024 or 1024x1792): $0.080 per image

### 예상 비용
- 하루 1회 자동 실행: 월 약 $2.40 (1792x1024 기준)
- 하루 3회 자동 실행: 월 약 $7.20

### Supabase
- Free tier: 500MB storage, 2GB bandwidth/month
- 초과 시 Pro plan ($25/month) 필요

## 고급 설정

### 다양한 크기로 생성

스크립트 수정:
```python
# upload_design.py에서
image_data = self.generate_image(prompt, size="1024x1024")  # 정사각형
```

### 여러 디자인 한 번에 생성

```bash
# 여러 카테고리 순차 실행
for category in "Landing Page" "Dashboard" "Portfolio"; do
  python upload_design.py --category "$category"
  sleep 5
done
```

## 로그 확인

```bash
# 최근 실행 로그 확인
tail -f automation.log
```
