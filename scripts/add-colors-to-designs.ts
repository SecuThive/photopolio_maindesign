import { createClient } from '@supabase/supabase-js';
import * as dotenv from 'dotenv';
import * as path from 'path';

// .env.local 파일 로드
dotenv.config({ path: path.resolve(__dirname, '../.env.local') });

const supabaseUrl = process.env.NEXT_PUBLIC_SUPABASE_URL;
const supabaseKey = process.env.SUPABASE_SERVICE_ROLE_KEY;

if (!supabaseUrl || !supabaseKey) {
  console.error('❌ Missing environment variables!');
  console.error('NEXT_PUBLIC_SUPABASE_URL:', supabaseUrl ? 'OK' : 'MISSING');
  console.error('SUPABASE_SERVICE_ROLE_KEY:', supabaseKey ? 'OK' : 'MISSING');
  process.exit(1);
}

const supabase = createClient(supabaseUrl, supabaseKey);

// 카테고리별 색상 팔레트
const colorPalettes: Record<string, string[]> = {
  'Dashboard': ['#1E293B', '#3B82F6', '#10B981', '#F59E0B', '#EF4444'],
  'Landing Page': ['#000000', '#FFFFFF', '#6366F1', '#EC4899', '#14B8A6'],
  'E-commerce': ['#0F172A', '#F1F5F9', '#8B5CF6', '#F97316', '#06B6D4'],
  'Portfolio': ['#18181B', '#FAFAFA', '#A855F7', '#FB923C', '#22D3EE'],
  'Blog': ['#171717', '#F5F5F5', '#7C3AED', '#FBBF24', '#2DD4BF'],
  'Components': ['#0C4A6E', '#E0F2FE', '#0EA5E9', '#F43F5E', '#84CC16'],
  'default': ['#111827', '#F9FAFB', '#4F46E5', '#EF4444', '#10B981'],
};

async function addColorsToDesigns() {
  try {
    // 모든 디자인 가져오기
    const { data: designs, error: fetchError } = await supabase
      .from('designs')
      .select('id, category, colors');

    if (fetchError) {
      console.error('Error fetching designs:', fetchError);
      return;
    }

    console.log(`Found ${designs?.length || 0} designs`);

    // colors가 없는 디자인들 업데이트
    let updated = 0;
    for (const design of designs || []) {
      if (!design.colors || design.colors.length === 0) {
        const palette = colorPalettes[design.category || 'default'] || colorPalettes.default;
        
        const { error: updateError } = await supabase
          .from('designs')
          .update({ colors: palette })
          .eq('id', design.id);

        if (updateError) {
          console.error(`Error updating design ${design.id}:`, updateError);
        } else {
          updated++;
          console.log(`✓ Updated design ${design.id} (${design.category || 'default'})`);
        }
      }
    }

    console.log(`\n✅ Successfully updated ${updated} designs with color palettes!`);
  } catch (error) {
    console.error('Error:', error);
  }
}

addColorsToDesigns();
