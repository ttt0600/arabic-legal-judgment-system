# -*- coding: utf-8 -*-
"""
Automated Project Update Script
سكريبت التحديث التلقائي للمشروع

This script automatically updates all URLs, references, and configurations
to match your actual GitHub repository.
"""

import os
import re
import json
from pathlib import Path

# ============================================
# Configuration / الإعدادات
# ============================================
GITHUB_USERNAME = "ttt0600"
REPO_NAME = "arabic-legal-judgment-system"
GITHUB_URL = f"https://github.com/{GITHUB_USERNAME}/{REPO_NAME}"

def update_all_files():
    """Update all project files with correct URLs and references"""
    
    print("=" * 60)
    print("🔄 تحديث ملفات المشروع تلقائياً")
    print("🔄 Automated Project Update")
    print("=" * 60)
    print()
    
    updates_made = 0
    
    # 1. Update README files
    print("📝 تحديث ملفات README...")
    updates_made += update_readme_files()
    
    # 2. Update package.json
    print("\n📦 تحديث package.json...")
    updates_made += update_package_json()
    
    # 3. Update deployment documentation
    print("\n📚 تحديث وثائق النشر...")
    updates_made += update_deployment_docs()
    
    # 4. Update GitHub badges
    print("\n🏷️  تحديث badges...")
    updates_made += update_badges()
    
    # 5. Create updated .env.example if needed
    print("\n⚙️  فحص .env.example...")
    check_env_example()
    
    # Print summary
    print("\n" + "=" * 60)
    print(f"✅ تم إجراء {updates_made} تحديث")
    print(f"✅ Made {updates_made} updates")
    print("=" * 60)
    print()
    print("🔗 إعدادات المشروع:")
    print(f"   GitHub: {GITHUB_URL}")
    print(f"   Repository: {REPO_NAME}")
    print(f"   Username: {GITHUB_USERNAME}")
    print()

def update_readme_files():
    """Update all README files"""
    count = 0
    
    readme_files = [
        "README.md",
        "README_COMPLETE.md"
    ]
    
    replacements = {
        "YOUR_USERNAME": GITHUB_USERNAME,
        "your-repo": REPO_NAME,
        "username/repo": f"{GITHUB_USERNAME}/{REPO_NAME}",
        "https://github.com/repo": GITHUB_URL,
        "https://github.com/username": f"https://github.com/{GITHUB_USERNAME}",
        "https://github.com/your-repo": GITHUB_URL,
        "<repository-url>": f"{GITHUB_URL}.git",
        "github.com/repo/issues": f"github.com/{GITHUB_USERNAME}/{REPO_NAME}/issues",
        "github.com/repo/discussions": f"github.com/{GITHUB_USERNAME}/{REPO_NAME}/discussions",
        "github.com/repo/wiki": f"github.com/{GITHUB_USERNAME}/{REPO_NAME}/wiki",
    }
    
    for readme_file in readme_files:
        filepath = Path(readme_file)
        if filepath.exists():
            try:
                content = filepath.read_text(encoding='utf-8')
                original_content = content
                
                for old, new in replacements.items():
                    content = content.replace(old, new)
                
                if content != original_content:
                    filepath.write_text(content, encoding='utf-8')
                    print(f"  ✅ {readme_file}")
                    count += 1
                else:
                    print(f"  ✓ {readme_file} (لا تحتاج تحديث)")
            except Exception as e:
                print(f"  ❌ خطأ في {readme_file}: {e}")
    
    return count

def update_package_json():
    """Update frontend package.json"""
    count = 0
    package_json_path = Path("frontend/package.json")
    
    if package_json_path.exists():
        try:
            with open(package_json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            # Update repository
            data["repository"] = {
                "type": "git",
                "url": f"git+{GITHUB_URL}.git"
            }
            
            # Update bugs URL
            data["bugs"] = {
                "url": f"{GITHUB_URL}/issues"
            }
            
            # Update homepage
            data["homepage"] = f"{GITHUB_URL}#readme"
            
            # Update author if not set
            if "author" not in data:
                data["author"] = GITHUB_USERNAME
            
            with open(package_json_path, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
                f.write('\n')  # Add newline at end
            
            print(f"  ✅ package.json")
            count += 1
        except Exception as e:
            print(f"  ❌ خطأ في package.json: {e}")
    else:
        print(f"  ⚠️  package.json غير موجود")
    
    return count

def update_deployment_docs():
    """Update deployment documentation"""
    count = 0
    
    doc_files = [
        "GITHUB_DEPLOYMENT.md",
        "DEPLOYMENT_CHECKLIST.md",
        "QUICK_START_GITHUB.md"
    ]
    
    for doc_file in doc_files:
        filepath = Path(doc_file)
        if filepath.exists():
            try:
                content = filepath.read_text(encoding='utf-8')
                original_content = content
                
                # Replace placeholders
                content = content.replace("YOUR_USERNAME", GITHUB_USERNAME)
                content = content.replace("your-repo", REPO_NAME)
                content = re.sub(
                    r'https://github\.com/[a-zA-Z0-9_-]+/arabic-legal-judgment-system',
                    GITHUB_URL,
                    content
                )
                
                if content != original_content:
                    filepath.write_text(content, encoding='utf-8')
                    print(f"  ✅ {doc_file}")
                    count += 1
                else:
                    print(f"  ✓ {doc_file} (لا يحتاج تحديث)")
            except Exception as e:
                print(f"  ❌ خطأ في {doc_file}: {e}")
    
    return count

def update_badges():
    """Update GitHub badges in README"""
    count = 0
    
    readme_path = Path("README.md")
    if readme_path.exists():
        try:
            content = readme_path.read_text(encoding='utf-8')
            
            # Update badge URLs
            badge_patterns = [
                (r'github\.com/workflow/status/[^/]+/[^/)]+', f'github.com/workflow/status/{GITHUB_USERNAME}/{REPO_NAME}'),
                (r'github\.com/license/[^/]+/[^)]+', f'github.com/license/{GITHUB_USERNAME}/{REPO_NAME}'),
                (r'github\.com/v/release/[^/]+/[^)]+', f'github.com/v/release/{GITHUB_USERNAME}/{REPO_NAME}'),
                (r'github\.com/stars/[^/]+/[^?]+', f'github.com/stars/{GITHUB_USERNAME}/{REPO_NAME}'),
            ]
            
            original_content = content
            for pattern, replacement in badge_patterns:
                content = re.sub(pattern, replacement, content)
            
            if content != original_content:
                readme_path.write_text(content, encoding='utf-8')
                print(f"  ✅ GitHub badges updated")
                count += 1
        except Exception as e:
            print(f"  ❌ خطأ في تحديث badges: {e}")
    
    return count

def check_env_example():
    """Check .env.example file"""
    env_example = Path(".env.example")
    
    if env_example.exists():
        print(f"  ✓ .env.example موجود")
        
        # Check if it has the right structure
        content = env_example.read_text(encoding='utf-8')
        
        required_keys = [
            "SECRET_KEY",
            "MYSQL_HOST",
            "MYSQL_USER",
            "MYSQL_PASSWORD",
            "MYSQL_DB",
            "JWT_SECRET_KEY"
        ]
        
        missing_keys = []
        for key in required_keys:
            if key not in content:
                missing_keys.append(key)
        
        if missing_keys:
            print(f"  ⚠️  مفاتيح ناقصة في .env.example: {', '.join(missing_keys)}")
        else:
            print(f"  ✓ .env.example يحتوي على جميع المفاتيح المطلوبة")
    else:
        print(f"  ⚠️  .env.example غير موجود")

def create_project_config():
    """Create a project configuration file"""
    config = {
        "github": {
            "username": GITHUB_USERNAME,
            "repository": REPO_NAME,
            "url": GITHUB_URL
        },
        "project": {
            "name": "Arabic Legal Judgment System",
            "name_ar": "نظام إدارة الأحكام القانونية العربية",
            "version": "2.0",
            "license": "MIT"
        },
        "urls": {
            "frontend": "http://localhost:3000",
            "backend": "http://localhost:5000",
            "api": "http://localhost:5000/api"
        },
        "ports": {
            "frontend": 3000,
            "backend": 5000
        }
    }
    
    config_path = Path("project_config.json")
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write('\n')
    
    print(f"\n📝 تم إنشاء project_config.json")

if __name__ == "__main__":
    print()
    print("⚠️  هذا السكريبت سيقوم بتحديث:")
    print("   - ملفات README")
    print("   - package.json")
    print("   - وثائق النشر")
    print("   - GitHub badges")
    print()
    
    response = input("هل تريد المتابعة? (y/n): ")
    
    if response.lower() in ['y', 'yes', 'نعم']:
        update_all_files()
        create_project_config()
        
        print("\n" + "=" * 60)
        print("🎉 تم التحديث بنجاح!")
        print("🎉 Update Complete!")
        print("=" * 60)
        print()
        print("💡 الخطوات التالية:")
        print("   1. راجع التغييرات: git diff")
        print("   2. أضف التغييرات: git add .")
        print("   3. Commit: git commit -m 'Update project URLs and references'")
        print("   4. Push: git push")
        print()
    else:
        print("\n❌ تم الإلغاء")
