import { createClient } from '@supabase/supabase-js';
import type { Database } from '@/types/database';

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const serviceRoleKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

// 🧪 디버깅: 환경 변수 확인 (보안상 앞뒤 5글자만)
console.log('🔍 [Supabase Admin Debug]');
console.log('URL exists:', !!supabaseUrl);
console.log('URL preview:', supabaseUrl ? `${supabaseUrl.slice(0, 15)}...${supabaseUrl.slice(-10)}` : 'MISSING');
console.log('Service Role Key exists:', !!serviceRoleKey);
console.log('Service Role Key preview:', serviceRoleKey ? `${serviceRoleKey.slice(0, 15)}...${serviceRoleKey.slice(-15)}` : 'MISSING');
console.log('Service Role Key length:', serviceRoleKey?.length || 0);

if (!supabaseUrl || !serviceRoleKey) {
  throw new Error('Missing Supabase admin environment variables');
}

export const supabaseAdmin = createClient<Database>(supabaseUrl, serviceRoleKey, {
  auth: {
    persistSession: false,
    autoRefreshToken: false,
  },
});
