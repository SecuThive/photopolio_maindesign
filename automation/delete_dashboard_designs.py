import os
from supabase import create_client

SUPABASE_URL = "https://vswzoulerodrphbsfkjq.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InZzd3pvdWxlcm9kcnBoYnNma2pxIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MzY5NjA0NjksImV4cCI6MjA1MjUzNjQ2OX0.UqGjEXKJ6RfM_Q5SMcG0Y54Ld7LDQxXmyHLEEbwfhbE"

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

def delete_dashboard_designs():
    try:
        # Get all Dashboard designs
        response = supabase.table("designs").select("*").eq("category", "Dashboard").execute()
        designs = response.data
        
        print(f"📊 Dashboard 디자인 {len(designs)}개 발견")
        
        deleted_count = 0
        
        for design in designs:
            # Delete from storage
            if design['image_url']:
                file_path = design['image_url'].split('/designs/')[-1]
                try:
                    supabase.storage.from_("designs-bucket").remove([f"designs/{file_path}"])
                    print(f"🗑️  Storage에서 삭제: {file_path}")
                except Exception as e:
                    print(f"⚠️  Storage 삭제 오류 (계속 진행): {e}")
            
            # Delete from database
            supabase.table("designs").delete().eq("id", design['id']).execute()
            print(f"💾 DB에서 삭제: {design['title']}")
            deleted_count += 1
        
        print(f"\n🎉 총 {deleted_count}개의 Dashboard 디자인이 삭제되었습니다!")
        
    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    delete_dashboard_designs()
