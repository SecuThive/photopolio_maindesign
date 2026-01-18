import os
from supabase import create_client
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

# Supabase 클라이언트 초기화
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(supabase_url, supabase_key)

def delete_all_designs():
    """모든 디자인 삭제"""
    try:
        # 모든 디자인 조회
        response = supabase.table('designs').select('*').execute()
        
        designs = response.data
        
        if not designs:
            print("❌ 삭제할 디자인이 없습니다.")
            return
        
        print(f"🔍 {len(designs)}개의 디자인을 찾았습니다.")
        
        # 각 디자인 삭제
        for design in designs:
            design_id = design['id']
            image_url = design['image_url']
            
            # Storage에서 이미지 삭제
            if image_url:
                # URL에서 파일 경로 추출
                file_path = image_url.split('/designs-bucket/')[-1].split('?')[0]
                try:
                    supabase.storage.from_('designs-bucket').remove([file_path])
                    print(f"🗑️  이미지 삭제: {file_path}")
                except Exception as e:
                    print(f"⚠️  이미지 삭제 실패: {e}")
            
            # 데이터베이스에서 디자인 삭제
            supabase.table('designs').delete().eq('id', design_id).execute()
        
        print(f"\n🎉 총 {len(designs)}개의 디자인이 삭제되었습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    delete_all_designs()
