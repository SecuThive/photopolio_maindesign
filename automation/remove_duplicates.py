#!/usr/bin/env python3
"""
중복된 디자인 찾기 및 삭제
title과 category가 동일한 디자인 중 최신 것만 남기고 삭제
"""

import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Supabase 클라이언트 설정
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not supabase_url or not supabase_key:
    raise ValueError("환경 변수 SUPABASE_URL과 SUPABASE_SERVICE_ROLE_KEY를 설정해주세요.")

supabase = create_client(supabase_url, supabase_key)

def find_duplicates():
    """중복된 디자인 찾기"""
    print("🔍 중복된 디자인을 찾고 있습니다...")
    
    # 모든 디자인 가져오기
    response = supabase.table('designs').select('*').order('created_at', desc=False).execute()
    designs = response.data
    
    print(f"📊 총 {len(designs)}개의 디자인이 있습니다.")
    
    # title과 category로 그룹화
    design_groups = {}
    for design in designs:
        key = f"{design['title']}|{design['category']}"
        if key not in design_groups:
            design_groups[key] = []
        design_groups[key].append(design)
    
    # 중복 찾기
    duplicates = {}
    for key, group in design_groups.items():
        if len(group) > 1:
            duplicates[key] = group
    
    if not duplicates:
        print("✅ 중복된 디자인이 없습니다!")
        return None
    
    print(f"\n⚠️  {len(duplicates)}개의 중복 그룹을 발견했습니다:")
    print("=" * 80)
    
    total_to_delete = 0
    for key, group in duplicates.items():
        title, category = key.split('|')
        print(f"\n📌 {category} - {title}")
        print(f"   중복 개수: {len(group)}개")
        print(f"   삭제할 개수: {len(group) - 1}개")
        
        # 날짜순으로 정렬 (가장 최신 것 유지)
        group.sort(key=lambda x: x['created_at'], reverse=True)
        
        print(f"   유지할 디자인: {group[0]['id']} (생성일: {group[0]['created_at']})")
        for i, design in enumerate(group[1:], 1):
            print(f"   삭제할 디자인 {i}: {design['id']} (생성일: {design['created_at']})")
            total_to_delete += 1
    
    print("\n" + "=" * 80)
    print(f"📊 총 삭제 예정: {total_to_delete}개")
    
    return duplicates

def delete_duplicates(duplicates):
    """중복된 디자인 삭제 (최신 것만 유지)"""
    if not duplicates:
        return
    
    print("\n🗑️  중복 디자인을 삭제합니다...")
    
    deleted_count = 0
    for key, group in duplicates.items():
        # 날짜순으로 정렬 (가장 최신 것 유지)
        group.sort(key=lambda x: x['created_at'], reverse=True)
        
        # 첫 번째(최신)를 제외한 나머지 삭제
        for design in group[1:]:
            try:
                supabase.table('designs').delete().eq('id', design['id']).execute()
                deleted_count += 1
                print(f"   ✓ 삭제됨: {design['id']} ({design['title']})")
            except Exception as e:
                print(f"   ✗ 삭제 실패: {design['id']} - {e}")
    
    print(f"\n✅ 총 {deleted_count}개의 중복 디자인을 삭제했습니다!")

if __name__ == '__main__':
    print("=" * 80)
    print("중복 디자인 삭제 도구")
    print("=" * 80)
    
    # 중복 찾기
    duplicates = find_duplicates()
    
    if duplicates:
        # 사용자 확인
        print("\n⚠️  이 작업은 되돌릴 수 없습니다!")
        confirm = input("정말 삭제하시겠습니까? (yes/no): ").strip().lower()
        
        if confirm == 'yes':
            delete_duplicates(duplicates)
        else:
            print("❌ 취소되었습니다.")
    
    print("\n" + "=" * 80)
