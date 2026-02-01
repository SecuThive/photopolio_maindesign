import os
from supabase import create_client
import requests
import json
import time
from dotenv import load_dotenv

load_dotenv()

# Supabase 설정
supabase_url = os.getenv('SUPABASE_URL')
supabase_key = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
supabase = create_client(supabase_url, supabase_key)

# Ollama 설정
ollama_url = os.getenv('OLLAMA_API_URL', 'http://localhost:11434')
ollama_model = os.getenv('OLLAMA_MODEL', 'llama3')

def get_designs_without_description():
    response = supabase.table('designs').select('*').execute()
    
    designs_need_desc = []
    for design in response.data:
        desc = design.get('description', '')
        if not desc or len(desc) < 100:
            designs_need_desc.append(design)
    
    return designs_need_desc

def extract_clean_title(title):
    if ' - ' in title:
        parts = title.split(' - ')
        return parts[0].strip()
    return title

def generate_description_with_ollama(design):
    title = design.get('title', 'Untitled')
    clean_title = extract_clean_title(title)
    category = design.get('category', 'general')
    colors = design.get('colors', [])
    
    color_list = ', '.join(colors) if colors else 'Not specified'
    
    prompt = f"Generate a detailed, SEO-optimized description for this UI design:\n\nDesign Name: {clean_title}\nCategory: {category}\nColors: {color_list}\n\nWrite a 150-250 word description that:\n1. Describes what type of interface this is\n2. Highlights key visual and functional features\n3. Explains the design approach and style\n4. Mentions the color scheme and its effect\n5. Describes who would benefit from this design\n6. Uses keywords naturally for SEO\n\nWrite in a professional, engaging tone. DO NOT include markdown formatting. Write plain text only."

    try:
        response = requests.post(
            f"{ollama_url}/api/generate",
            json={
                "model": ollama_model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            timeout=60
        )
        
        if response.status_code == 200:
            result = response.json()
            description = result.get('response', '').strip()
            description = description.replace('**', '').replace('##', '').replace('*', '')
            return description if len(description) > 100 else None
        else:
            print(f"  ⚠️ Ollama API 오류: {response.status_code}")
            return None
            
    except Exception as e:
        print(f"  ⚠️ Ollama 생성 실패: {str(e)}")
        return None

def create_fallback_description(design):
    title = design.get('title', 'Untitled')
    clean_title = extract_clean_title(title)
    category = design.get('category', 'interface')
    colors = design.get('colors', [])
    
    primary_color = colors[0] if colors else '#000000'
    
    descriptions = {
        'dashboard': f"A comprehensive {clean_title} featuring an intuitive dashboard interface designed for data visualization and monitoring. The design utilizes a {primary_color} color scheme to create a professional and focused user experience. Perfect for analytics platforms, admin panels, and business intelligence tools that require clear data presentation and efficient workflow management.",
        
        'e-commerce': f"An elegant {clean_title} showcasing a modern e-commerce interface optimized for online shopping experiences. Built with a {primary_color} color palette, this design emphasizes product discovery, seamless navigation, and conversion-focused layouts. Ideal for online stores, marketplaces, and retail platforms seeking to enhance their digital shopping experience.",
        
        'portfolio': f"A striking {clean_title} presenting a creative portfolio interface designed to showcase work beautifully. The {primary_color} color foundation creates visual impact while maintaining professional presentation. Perfect for designers, photographers, artists, and creative professionals who want to display their work in an engaging, memorable format.",
        
        'blog': f"A clean {clean_title} offering a reader-friendly blog interface focused on content readability and engagement. The {primary_color} color scheme enhances the reading experience while maintaining visual interest. Ideal for content creators, publishers, and bloggers who prioritize typography, layout, and user engagement in their digital publications.",
        
        'components': f"A versatile {clean_title} providing a comprehensive component library interface for design systems. Featuring a {primary_color} base color, this design demonstrates UI patterns, interactive elements, and reusable components. Essential for developers and designers building consistent, scalable user interfaces across digital products."
    }
    
    default_desc = f"A professional {clean_title} interface designed with attention to user experience and visual hierarchy. The {primary_color} color palette creates a cohesive visual language throughout the design. This interface combines functional clarity with aesthetic appeal, making it suitable for modern web applications that require both usability and engaging visual design."
    
    return descriptions.get(category, default_desc)

def update_design_description(design_id, description):
    try:
        supabase.table('designs').update({
            'description': description
        }).eq('id', design_id).execute()
        return True
    except Exception as e:
        print(f"  ❌ 업데이트 실패: {str(e)}")
        return False

def main():
    print("🚀 Ollama로 디자인 설명 생성 시작...")
    print(f"📡 Ollama URL: {ollama_url}")
    print(f"🤖 Model: {ollama_model}")
    print()
    
    designs = get_designs_without_description()
    total = len(designs)
    print(f"📊 총 {total}개의 디자인이 설명이 필요합니다.")
    print()
    
    success_count = 0
    fallback_count = 0
    fail_count = 0
    
    for i, design in enumerate(designs, 1):
        title = design.get('title', 'Untitled')
        design_id = design.get('id')
        
        print(f"[{i}/{total}] {title}")
        print(f"  ID: {design_id[:8]}...")
        
        description = generate_description_with_ollama(design)
        
        if description:
            print("  ✅ Ollama 생성 성공")
            if update_design_description(design_id, description):
                success_count += 1
                print("  ✅ 완료")
                print()
            else:
                fail_count += 1
        else:
            print("  ⚠️ Ollama 실패, fallback 설명 사용")
            fallback_desc = create_fallback_description(design)
            if update_design_description(design_id, fallback_desc):
                fallback_count += 1
                print("  ✅ 완료 (fallback)")
                print()
            else:
                fail_count += 1
        
        if i < total:
            time.sleep(2)
    
    print()
    print("=" * 50)
    print("✅ 작업 완료!")
    print("📊 결과:")
    print(f"  - AI 생성 성공: {success_count}개")
    print(f"  - Fallback 사용: {fallback_count}개")
    print(f"  - 실패: {fail_count}개")
    print("=" * 50)

if __name__ == "__main__":
    main()
