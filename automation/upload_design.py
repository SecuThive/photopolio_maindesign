"""
AI Design Gallery - Automated Upload Script

이 스크립트는 AI를 사용하여 웹 디자인 이미지를 생성하고
Supabase에 자동으로 업로드합니다.

Requirements:
- pip install supabase python-dotenv openai pillow

Usage:
- 크론잡으로 실행: python automation/upload_design.py
- 수동 실행: python automation/upload_design.py --prompt "your custom prompt"
"""

import os
import io
import argparse
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any

from dotenv import load_dotenv
from supabase import create_client, Client
from openai import OpenAI

# Load environment variables
load_dotenv()

# Configuration
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_SERVICE_ROLE_KEY = os.getenv('SUPABASE_SERVICE_ROLE_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Validate environment variables
if not all([SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY, OPENAI_API_KEY]):
    raise ValueError("Missing required environment variables. Check your .env file.")

# Initialize clients
supabase: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)
openai_client = OpenAI(api_key=OPENAI_API_KEY)

# Design templates for different categories
DESIGN_TEMPLATES = {
    "Landing Page": [
        "A modern, minimalist landing page for a SaaS product with hero section, features grid, and call-to-action",
        "Clean landing page design for a mobile app with gradient background and floating UI elements",
        "Professional landing page for a fintech startup with dark mode, glassmorphism effects",
    ],
    "Dashboard": [
        "Analytics dashboard with charts, metrics cards, and data visualization in a clean layout",
        "Admin dashboard with sidebar navigation, data tables, and modern UI components",
        "Project management dashboard with kanban boards and task tracking interface",
    ],
    "E-commerce": [
        "E-commerce product page with image gallery, product details, and shopping cart",
        "Online store homepage with product grid, categories, and promotional banners",
        "Fashion e-commerce website with elegant design and product showcase",
    ],
    "Portfolio": [
        "Creative portfolio website for a designer with project showcase and case studies",
        "Photography portfolio with full-screen images and minimalist navigation",
        "Developer portfolio with project cards and skills section",
    ],
    "Blog": [
        "Modern blog homepage with featured articles and card-based layout",
        "Minimalist blog design with typography focus and reading experience",
        "Tech blog with dark theme and code-friendly design",
    ],
}


class DesignUploader:
    """Handles AI image generation and upload to Supabase"""

    def __init__(self):
        self.supabase = supabase
        self.openai_client = openai_client

    def generate_image(self, prompt: str, size: str = "1792x1024") -> bytes:
        """
        Generate an image using OpenAI DALL-E 3
        
        Args:
            prompt: The text prompt for image generation
            size: Image size (1024x1024, 1792x1024, or 1024x1792)
            
        Returns:
            Image data in bytes
        """
        print(f"🎨 Generating image with prompt: {prompt}")
        
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=f"Website design screenshot: {prompt}. UI/UX design, clean interface, modern aesthetics, high quality mockup",
                size=size,
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Download the image
            import requests
            image_response = requests.get(image_url)
            image_response.raise_for_status()
            
            print("✅ Image generated successfully")
            return image_response.content
            
        except Exception as e:
            print(f"❌ Error generating image: {e}")
            raise

    def upload_to_storage(self, image_data: bytes, filename: str) -> str:
        """
        Upload image to Supabase Storage
        
        Args:
            image_data: Image file in bytes
            filename: Name for the file
            
        Returns:
            Public URL of the uploaded image
        """
        print(f"📤 Uploading image to Supabase Storage: {filename}")
        
        try:
            # Upload to Supabase Storage
            file_path = f"designs/{filename}"
            
            response = self.supabase.storage.from_('designs-bucket').upload(
                file_path,
                image_data,
                file_options={"content-type": "image/png"}
            )
            
            # Get public URL
            public_url = self.supabase.storage.from_('designs-bucket').get_public_url(file_path)
            
            print(f"✅ Image uploaded: {public_url}")
            return public_url
            
        except Exception as e:
            print(f"❌ Error uploading to storage: {e}")
            raise

    def save_to_database(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Save design metadata to Supabase database
        
        Args:
            data: Dictionary containing design information
            
        Returns:
            Inserted row data
        """
        print(f"💾 Saving to database: {data['title']}")
        
        try:
            response = self.supabase.table('designs').insert(data).execute()
            print("✅ Saved to database successfully")
            return response.data[0]
            
        except Exception as e:
            print(f"❌ Error saving to database: {e}")
            raise

    def create_design(
        self,
        category: str,
        custom_prompt: Optional[str] = None,
        title: Optional[str] = None,
        description: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Complete workflow: Generate image, upload to storage, and save to database
        
        Args:
            category: Design category
            custom_prompt: Custom prompt (optional)
            title: Design title (optional)
            description: Design description (optional)
            
        Returns:
            Complete design data
        """
        import random
        
        # Select or use custom prompt
        if custom_prompt:
            prompt = custom_prompt
        else:
            if category not in DESIGN_TEMPLATES:
                raise ValueError(f"Invalid category: {category}")
            prompt = random.choice(DESIGN_TEMPLATES[category])
        
        # Generate title if not provided
        if not title:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            title = f"{category} Design - {timestamp}"
        
        # Generate image
        image_data = self.generate_image(prompt)
        
        # Create filename
        filename = f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
        
        # Upload to storage
        image_url = self.upload_to_storage(image_data, filename)
        
        # Prepare data for database
        design_data = {
            "title": title,
            "description": description or f"AI-generated {category.lower()} design",
            "image_url": image_url,
            "category": category,
            "prompt": prompt,
        }
        
        # Save to database
        result = self.save_to_database(design_data)
        
        print("\n🎉 Design created successfully!")
        print(f"ID: {result['id']}")
        print(f"Title: {result['title']}")
        print(f"URL: {result['image_url']}")
        
        return result


def main():
    """Main function for CLI usage"""
    parser = argparse.ArgumentParser(description="Generate and upload AI design")
    parser.add_argument(
        '--category',
        type=str,
        default='Landing Page',
        choices=list(DESIGN_TEMPLATES.keys()),
        help='Design category'
    )
    parser.add_argument(
        '--prompt',
        type=str,
        help='Custom prompt for image generation'
    )
    parser.add_argument(
        '--title',
        type=str,
        help='Custom title for the design'
    )
    parser.add_argument(
        '--description',
        type=str,
        help='Custom description for the design'
    )
    
    args = parser.parse_args()
    
    # Create uploader instance
    uploader = DesignUploader()
    
    # Create design
    try:
        uploader.create_design(
            category=args.category,
            custom_prompt=args.prompt,
            title=args.title,
            description=args.description,
        )
    except Exception as e:
        print(f"\n❌ Failed to create design: {e}")
        exit(1)


if __name__ == "__main__":
    main()
