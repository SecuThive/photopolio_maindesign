from dotenv import load_dotenv
import os
from supabase import create_client

load_dotenv()

supabase = create_client(os.getenv('SUPABASE_URL'), os.getenv('SUPABASE_SERVICE_ROLE_KEY'))
designs = supabase.table('designs').select('id, title, description, category').limit(5).execute()

for d in designs.data:
    print(f"Title: {d['title']}")
    print(f"Category: {d['category']}")
    print(f"Description: {d['description']}")
    print("-" * 80)
    print()
