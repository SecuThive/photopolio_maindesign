#!/usr/bin/env python3
"""
Google Indexing API 자동화 스크립트
sitemap.xml의 모든 URL을 구글에 강제 제출하여 빠른 색인을 요청합니다.

사용법:
    python google_indexing_submit.py                    # sitemap의 모든 URL 제출
    python google_indexing_submit.py --dry-run          # 테스트 (실제 제출 안 함)
    python google_indexing_submit.py --check-status     # URL 색인 상태 확인
    python google_indexing_submit.py --url URL          # 특정 URL만 제출
"""

import argparse
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any
from urllib.parse import urljoin
import xml.etree.ElementTree as ET

try:
    import requests
    from google.oauth2 import service_account
    from googleapiclient.discovery import build
    from googleapiclient.errors import HttpError
except ImportError:
    print("[ERROR] Required packages not installed!")
    print("\nPlease install with:")
    print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client requests")
    sys.exit(1)


# 설정
SCRIPT_DIR = Path(__file__).parent
SERVICE_ACCOUNT_FILE = SCRIPT_DIR / 'service-account-key.json'
SCOPES = ['https://www.googleapis.com/auth/indexing']
SITEMAP_URL = 'https://ui-syntax.com/sitemap.xml'
LOG_FILE = SCRIPT_DIR / 'indexing_log.json'

# API 속도 제한 (안전하게)
BATCH_SIZE = 10  # 한 번에 처리할 URL 개수
DELAY_BETWEEN_BATCHES = 2  # 배치 간 대기 시간 (초)


class GoogleIndexingAPI:
    """Google Indexing API 클라이언트"""
    
    def __init__(self, service_account_file: str):
        """
        Args:
            service_account_file: 서비스 계정 JSON 키 파일 경로
        """
        self.service_account_file = service_account_file
        self.service = None
        self._authenticate()
    
    def _authenticate(self):
        """서비스 계정으로 인증"""
        try:
            credentials = service_account.Credentials.from_service_account_file(
                self.service_account_file,
                scopes=SCOPES
            )
            self.service = build('indexing', 'v3', credentials=credentials)
            print("[OK] Google authentication successful!")
        except FileNotFoundError:
            print(f"[ERROR] Service account key file not found: {self.service_account_file}")
            print("\nGOOGLE_INDEXING_API_SETUP.md 파일을 참고하여 설정하세요!")
            sys.exit(1)
        except Exception as e:
            print(f"❌ 인증 실패: {str(e)}")
            sys.exit(1)
    
    def submit_url(self, url: str, action: str = "URL_UPDATED") -> Dict[str, Any]:
        """
        URL을 구글에 제출
        
        Args:
            url: 제출할 URL
            action: URL_UPDATED (업데이트) 또는 URL_DELETED (삭제)
        
        Returns:
            API 응답 딕셔너리
        """
        body = {
            "url": url,
            "type": action
        }
        
        try:
            response = self.service.urlNotifications().publish(body=body).execute()
            return {"success": True, "data": response}
        except HttpError as e:
            error_content = json.loads(e.content.decode('utf-8'))
            return {"success": False, "error": error_content}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_status(self, url: str) -> Dict[str, Any]:
        """
        URL의 색인 상태 확인
        
        Args:
            url: 확인할 URL
        
        Returns:
            상태 정보 딕셔너리
        """
        try:
            response = self.service.urlNotifications().getMetadata(url=url).execute()
            return {"success": True, "data": response}
        except HttpError as e:
            error_content = json.loads(e.content.decode('utf-8'))
            return {"success": False, "error": error_content}
        except Exception as e:
            return {"success": False, "error": str(e)}


def fetch_sitemap_urls(sitemap_url: str) -> List[str]:
    """
    sitemap.xml에서 모든 URL 추출
    
    Args:
        sitemap_url: sitemap.xml URL
    
    Returns:
        URL 리스트
    """
    try:
        print(f"📡 Sitemap 다운로드 중: {sitemap_url}")
        response = requests.get(sitemap_url, timeout=10)
        response.raise_for_status()
        
        # XML 파싱
        root = ET.fromstring(response.content)
        
        # XML 네임스페이스 처리
        namespaces = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
        
        # <loc> 태그에서 모든 URL 추출
        urls = [
            loc.text
            for loc in root.findall('.//ns:loc', namespaces)
            if loc.text
        ]
        
        print(f"✅ {len(urls)}개의 URL을 찾았습니다!")
        return urls
    
    except requests.exceptions.RequestException as e:
        print(f"❌ Sitemap 다운로드 실패: {str(e)}")
        print("\n💡 SITEMAP_URL 변수를 실제 사이트 주소로 변경했는지 확인하세요!")
        return []
    except ET.ParseError as e:
        print(f"❌ Sitemap XML 파싱 실패: {str(e)}")
        return []


def load_log() -> Dict[str, Any]:
    """이전 제출 로그 불러오기"""
    log_path = Path(LOG_FILE)
    if log_path.exists():
        with open(log_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {"submissions": [], "last_run": None}


def save_log(log_data: Dict[str, Any]):
    """제출 로그 저장"""
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, indent=2, ensure_ascii=False)


def submit_urls_batch(api: GoogleIndexingAPI, urls: List[str], dry_run: bool = False):
    """
    URL들을 배치로 나눠서 제출
    
    Args:
        api: GoogleIndexingAPI 인스턴스
        urls: 제출할 URL 리스트
        dry_run: True면 실제 제출 안 하고 시뮬레이션만
    """
    total = len(urls)
    success_count = 0
    error_count = 0
    
    log_data = load_log()
    log_data["last_run"] = datetime.now().isoformat()
    current_submissions = []
    
    print(f"\n🚀 총 {total}개 URL 제출 시작!")
    print("=" * 60)
    
    for i in range(0, total, BATCH_SIZE):
        batch = urls[i:i + BATCH_SIZE]
        batch_num = (i // BATCH_SIZE) + 1
        total_batches = (total + BATCH_SIZE - 1) // BATCH_SIZE
        
        print(f"\n📦 배치 {batch_num}/{total_batches} 처리 중...")
        
        for url in batch:
            if dry_run:
                print(f"  [DRY-RUN] {url}")
                success_count += 1
                continue
            
            result = api.submit_url(url)
            
            submission_log = {
                "url": url,
                "timestamp": datetime.now().isoformat(),
                "success": result["success"]
            }
            
            if result["success"]:
                print(f"  ✅ {url}")
                success_count += 1
                submission_log["response"] = result["data"]
            else:
                print(f"  ❌ {url}")
                print(f"     오류: {result['error']}")
                error_count += 1
                submission_log["error"] = result["error"]
            
            current_submissions.append(submission_log)
            time.sleep(0.2)  # API 속도 제한 방지
        
        # 배치 간 대기
        if i + BATCH_SIZE < total:
            print(f"  ⏳ {DELAY_BETWEEN_BATCHES}초 대기 중...")
            time.sleep(DELAY_BETWEEN_BATCHES)
    
    # 로그 저장
    if not dry_run:
        log_data["submissions"].extend(current_submissions)
        save_log(log_data)
    
    # 결과 요약
    print("\n" + "=" * 60)
    print("📊 결과 요약")
    print("=" * 60)
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {error_count}개")
    print(f"📝 총 처리: {total}개")
    
    if not dry_run:
        print(f"\n💾 로그 저장됨: {LOG_FILE}")
    
    if error_count > 0:
        print("\n⚠️  일부 URL 제출에 실패했습니다.")
        print("   자세한 내용은 위의 오류 메시지를 확인하세요.")


def check_urls_status(api: GoogleIndexingAPI, urls: List[str]):
    """URL들의 색인 상태 확인"""
    print(f"\n🔍 {len(urls)}개 URL 상태 확인 중...")
    print("=" * 60)
    
    for url in urls:
        result = api.get_status(url)
        
        if result["success"]:
            data = result["data"]
            latest = data.get("latestUpdate", {})
            url_type = latest.get("type", "알 수 없음")
            notify_time = latest.get("notifyTime", "없음")
            
            print(f"\n📄 {url}")
            print(f"   상태: {url_type}")
            print(f"   마지막 알림: {notify_time}")
        else:
            print(f"\n📄 {url}")
            print(f"   ⚠️  상태 확인 실패: {result['error']}")
        
        time.sleep(0.5)


def main():
    parser = argparse.ArgumentParser(
        description="Google Indexing API로 URL을 구글에 강제 제출합니다."
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='실제 제출 없이 시뮬레이션만 실행'
    )
    parser.add_argument(
        '--check-status',
        action='store_true',
        help='URL들의 색인 상태 확인'
    )
    parser.add_argument(
        '--url',
        type=str,
        help='특정 URL만 제출 (sitemap 대신)'
    )
    parser.add_argument(
        '--sitemap',
        type=str,
        default=SITEMAP_URL,
        help=f'Sitemap URL (기본값: {SITEMAP_URL})'
    )
    
    args = parser.parse_args()
    
    print("🚀 Google Indexing API 자동화 도구")
    print("=" * 60)
    
    # API 클라이언트 초기화
    api = GoogleIndexingAPI(SERVICE_ACCOUNT_FILE)
    
    # URL 가져오기
    if args.url:
        urls = [args.url]
        print(f"📌 특정 URL 모드: {args.url}")
    else:
        urls = fetch_sitemap_urls(args.sitemap)
        if not urls:
            print("❌ 처리할 URL이 없습니다.")
            sys.exit(1)
    
    # 동작 실행
    if args.check_status:
        check_urls_status(api, urls)
    else:
        submit_urls_batch(api, urls, dry_run=args.dry_run)
        
        if args.dry_run:
            print("\n💡 실제로 제출하려면 --dry-run 옵션 없이 다시 실행하세요!")
        else:
            print("\n🎉 완료! 구글이 곧 크롤링을 시작할 겁니다!")
            print("   Search Console에서 색인 상태를 확인하세요:")
            print("   https://search.google.com/search-console")


if __name__ == "__main__":
    main()
