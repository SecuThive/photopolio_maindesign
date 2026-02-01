#!/usr/bin/env python3
"""
디자인 설명 자동 생성 스크립트
데이터베이스에서 description이 null이거나 짧은 디자인을 찾아 AI로 설명 생성
"""

import os
import sys
from pathlib import Path

# .env 파일 로드
try:
    from dotenv import load_dotenv
    env_path = Path(__file__).parent.parent / '.env'
    load_dotenv(env_path)
    print(f"✅ .env 파일 로드: {env_path}")
except ImportError:
    print("⚠️ python-dotenv 없음")

from supabase import create_client, Client
import google.generativeai as genai
from datetime import datetime
import time

# 환경 변수 로드
SUPABASE_URL = os.getenv("NEXT_PUBLIC_SUPABASE_URL") or os.getenv("SUPABASE_URL")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.0-flash-exp")  # .env에서 모델명 가져오기

print(f"\n=== 환경 변수 확인 ===")
print(f"SUPABASE_URL: {'✅' if SUPABASE_URL else '❌'}")
print(f"SUPABASE_SERVICE_KEY: {'✅' if SUPABASE_SERVICE_KEY else '❌'}")
print(f"GEMINI_API_KEY: {'✅' if GEMINI_API_KEY else '❌'}")
print(f"GEMINI_MODEL: {GEMINI_MODEL}")

if not all([SUPABASE_URL, SUPABASE_SERVICE_KEY, GEMINI_API_KEY]):
    raise ValueError("환경 변수를 확인해주세요.")

# Supabase 클라이언트 초기화
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)

# Gemini 초기화 - .env의 모델 사용
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel(GEMINI_MODEL)
print(f"✅ Gemini 모델 초기화: {GEMINI_MODEL}")

def get_designs_without_description():
    """설명이 없거나 짧은 디자인 조회"""
    print("\n📊 설명이 없는 디자인 조회 중...")
    
    try:
        response = supabase.table('designs').select('*').execute()
        all_designs = response.data
        
        designs_need_desc = []
        for design in all_designs:
            desc = design.get('description')
            if not desc or len(desc.strip()) < 100:
                designs_need_desc.append(design)
        
        print(f"✅ 전체 {len(all_designs)}개 중 {len(designs_need_desc)}개에 설명 추가 필요")
        return designs_need_desc[:50]
        
    except Exception as e:
        print(f"❌ 조회 실패: {e}")
        return []

def generate_description(design):
    """AI로 디자인 설명 생성"""
    title = design.get('title', 'Untitled Design')
    category = design.get('category', 'General')
    colors = design.get('colors', [])
    
    # 타이틀에서 실제 디자인 이름 추출 (예: "Content Calendar - Pixel Harbor 5151F9" -> "Content Calendar")
    clean_title = title.split(' - ')[0] if ' - ' in title else title
    
    prompt = f"""You are a professional web design copywriter. Create a detailed, SEO-friendly description for this {category.lower()} design.

Design Name: {clean_title}
Category: {category}
Color Palette: {', '.join(colors[:3]) if colors else 'Modern color scheme'}

Write a compelling 150-250 word description that:
1. Describes the specific purpose and use case of this {clean_title} {category.lower()}
2. Explains the visual hierarchy, layout structure, and key UI components
3. Highlights what makes this design effective for its target users
4. Mentions modern design principles and best practices demonstrated
5. Uses natural SEO keywords related to {category.lower()} and {clean_title}

Be specific about the design's functionality and benefits. Avoid generic phrases.
Write in a professional, engaging tone. Use plain text only (no markdown, no asterisks)."""

    try:
        response = model.generate_content(prompt)
        description = response.text.strip()
        
        # 마크다운 제거
        description = description.replace('**', '').replace('*', '').replace('#', '')
        
        return description
        
    except Exception as e:
        print(f"⚠️ AI 생성 실패 ({title}): {e}")
        
        # 더 나은 기본 설명 생성
        clean_title = title.split(' - ')[0] if ' - ' in title else title
        color_desc = f" featuring a {colors[0]} color scheme" if colors else ""
        
        return f"This {category.lower()} design showcases a modern {clean_title} interface{color_desc}. Built with contemporary design principles, it demonstrates clean visual hierarchy and intuitive user experience. The layout emphasizes clarity and usability, making it ideal for professionals seeking inspiration for {category.lower()} projects. Each element is carefully crafted to balance aesthetics with functionality, following current web design best practices. Perfect for designers and developers looking to create engaging, user-friendly interfaces that prioritize both form and function in today's digital landscape."

def update_design_description(design_id, description):
    """데이터베이스에 설명 업데이트"""
    try:
        response = supabase.table('designs').update({
            'description': description,
            'updated_at': datetime.utcnow().isoformat()
        }).eq('id', design_id).execute()
        return True
    except Exception as e:
        print(f"❌ 업데이트 실패: {e}")
        return False

def main():
    """메인 실행 함수"""
    print("\n🚀 디자인 설명 자동 생성 시작...")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    designs = get_designs_without_description()
    
    if not designs:
        print("✅ 모든 디자인에 설명이 있습니다!")
        return
    
    print(f"\n📝 {len(designs)}개 디자인 설명 생성 시작...")
    
    success_count = 0
    fail_count = 0
    
    for i, design in enumerate(designs, 1):
        design_id = design['id']
        title = design.get('title', 'Untitled')
        
        print(f"\n[{i}/{len(designs)}] {title}")
        print(f"  ID: {design_id[:8]}...")
        
        description = generate_description(design)
        print(f"  생성: {description[:80]}...")
        
        if update_design_description(design_id, description):
            success_count += 1
            print(f"  ✅ 완료")
        else:
            fail_count += 1
            print(f"  ❌ 실패")
        
        if i < len(designs):
            time.sleep(2)
    
    print(f"\n{'='*50}")
    print(f"🎉 완료!")
    print(f"✅ 성공: {success_count}개")
    print(f"❌ 실패: {fail_count}개")

if __name__ == "__main__":
    main()
