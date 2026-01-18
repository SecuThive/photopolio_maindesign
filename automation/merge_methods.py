"""
Merge generated stub methods into design_generator_enhanced.py
"""
import re

print("🚀 Starting method merge...")

# Read generated methods
print("📖 Reading generated_stub_methods.txt...")
with open('generated_stub_methods.txt', 'r', encoding='utf-8') as f:
    generated = f.read()

# Read current file
print("📖 Reading design_generator_enhanced.py...")
with open('design_generator_enhanced.py', 'r', encoding='utf-8') as f:
    current = f.read()

# Extract method blocks
print("🔍 Extracting method blocks...")

# Find where to insert each category
dashboard_insert_point = current.find("    # ===== E-commerce")
ecommerce_insert_point = current.find("    # ===== Portfolio")
portfolio_insert_point = current.find("    # ===== Blog")
blog_insert_point = current.find("    # ===== Components")
components_insert_point = current.find("    def get_structure_hash(self, html: str)")

# Extract methods from generated file
dashboard_start = generated.find("# DASHBOARD METHODS")
dashboard_end = generated.find("# E-COMMERCE METHODS")
dashboard_methods = generated[dashboard_start:dashboard_end].strip()

ecommerce_start = generated.find("# E-COMMERCE METHODS")
ecommerce_end = generated.find("# PORTFOLIO METHODS")
ecommerce_methods = generated[ecommerce_start:ecommerce_end].strip()

portfolio_start = generated.find("# PORTFOLIO METHODS")
portfolio_end = generated.find("# BLOG METHODS")
portfolio_methods = generated[portfolio_start:portfolio_end].strip()

blog_start = generated.find("# BLOG METHODS")
blog_end = generated.find("# COMPONENTS METHODS")
blog_methods = generated[blog_start:blog_end].strip()

components_start = generated.find("# COMPONENTS METHODS")
components_methods = generated[components_start:].strip()

# Clean up the method blocks (remove the comment headers)
dashboard_methods = dashboard_methods.split('\n', 4)[-1].strip() if dashboard_methods else ""
ecommerce_methods = ecommerce_methods.split('\n', 4)[-1].strip() if ecommerce_methods else ""
portfolio_methods = portfolio_methods.split('\n', 4)[-1].strip() if portfolio_methods else ""
blog_methods = blog_methods.split('\n', 4)[-1].strip() if blog_methods else ""
components_methods = components_methods.split('\n', 4)[-1].strip() if components_methods else ""

print(f"📊 Extracted methods:")
print(f"  Dashboard: {len(dashboard_methods)} chars")
print(f"  E-commerce: {len(ecommerce_methods)} chars")
print(f"  Portfolio: {len(portfolio_methods)} chars")
print(f"  Blog: {len(blog_methods)} chars")
print(f"  Components: {len(components_methods)} chars")

# Build new file
print("🔧 Building new file...")
new_content = current[:dashboard_insert_point]
new_content += "\n" + dashboard_methods + "\n\n    "
new_content += current[dashboard_insert_point:ecommerce_insert_point]
new_content += "\n" + ecommerce_methods + "\n\n    "
new_content += current[ecommerce_insert_point:portfolio_insert_point]
new_content += "\n" + portfolio_methods + "\n\n    "
new_content += current[portfolio_insert_point:blog_insert_point]
new_content += "\n" + blog_methods + "\n\n    "
new_content += current[blog_insert_point:components_insert_point]
new_content += "\n" + components_methods + "\n\n    "
new_content += current[components_insert_point:]

# Write new file
print("💾 Writing updated file...")
with open('design_generator_enhanced_v2.py', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"✅ Success! Created design_generator_enhanced_v2.py")
print(f"📏 Original file: {len(current)} chars")
print(f"📏 New file: {len(new_content)} chars")
print(f"📈 Added: {len(new_content) - len(current)} chars")

# Backup original
import shutil
shutil.copy('design_generator_enhanced.py', 'design_generator_enhanced_backup.py')
print("💾 Backup created: design_generator_enhanced_backup.py")

# Replace original
shutil.copy('design_generator_enhanced_v2.py', 'design_generator_enhanced.py')
print("✨ Replaced original file with new version")

print("\n🎉 Merge complete!")
