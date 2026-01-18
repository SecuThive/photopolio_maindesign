"""Dashboard 디자인만 삭제하는 스크립트"""
import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')

if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY]):
    raise ValueError("Missing required environment variables. Please check .env file.")

supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def delete_dashboard_only():
    """Dashboard 카테고리 디자인만 삭제"""
    try:
        # Dashboard 디자인만 조회
        response = supabase.table('designs').select('*').eq('category', 'Dashboard').execute()
        
        designs = response.data
        
        if not designs:
            print("❌ 삭제할 Dashboard 디자인이 없습니다.")
            return
        
        print(f"🔍 {len(designs)}개의 Dashboard 디자인을 찾았습니다.")
        print(f"\n현재 Dashboard 디자인:")
        for design in designs:
            print(f"  - {design['title']}")
        
        # 각 디자인 삭제
        deleted_count = 0
        for design in designs:
            design_id = design['id']
            image_url = design['image_url']
            
            # Storage에서 이미지 삭제
            if image_url:
                # URL에서 파일 경로 추출
                file_path = image_url.split('/designs-bucket/')[-1].split('?')[0]
                try:
                    supabase.storage.from_('designs-bucket').remove([file_path])
                    print(f"  🗑️  이미지 삭제: {file_path}")
                except Exception as e:
                    print(f"  ⚠️  이미지 삭제 실패: {e}")
            
            # 데이터베이스에서 디자인 삭제
            supabase.table('designs').delete().eq('id', design_id).execute()
            deleted_count += 1
        
        print(f"\n🎉 총 {deleted_count}개의 Dashboard 디자인이 삭제되었습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    delete_dashboard_only()
