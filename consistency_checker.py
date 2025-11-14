# -*- coding: utf-8 -*-
"""
Project Consistency Checker and Updater
نظام فحص وتحديث اتساق المشروع

This script ensures all URLs, references, and configurations are consistent
throughout the entire project.
"""

import os
import re
import json
from pathlib import Path
from typing import List, Dict, Tuple

class ConsistencyChecker:
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root)
        self.github_username = "ttt0600"
        self.repo_name = "arabic-legal-judgment-system"
        self.github_url = f"https://github.com/{self.github_username}/{self.repo_name}"
        
        # Configuration that should be consistent
        self.config = {
            "github_username": self.github_username,
            "repo_name": self.repo_name,
            "github_url": self.github_url,
            "project_name": "Arabic Legal Judgment System",
            "project_name_ar": "نظام إدارة الأحكام القانونية العربية",
            "version": "2.0",
            "license": "MIT",
            "python_version": "3.8+",
            "react_version": "18.2+",
            "api_base_url": "http://localhost:5000/api",
            "frontend_url": "http://localhost:3000",
            "backend_port": "5000",
            "frontend_port": "3000",
        }
        
        self.issues_found = []
        self.files_to_update = []
    
    def check_all(self):
        """Run all consistency checks"""
        print("=" * 60)
        print("🔍 فحص اتساق المشروع / Project Consistency Check")
        print("=" * 60)
        print()
        
        self.check_readme_files()
        self.check_package_json()
        self.check_frontend_config()
        self.check_backend_config()
        self.check_docker_files()
        self.check_github_workflows()
        self.check_deployment_docs()
        
        self.print_report()
        
        if self.files_to_update:
            response = input("\n🔧 هل تريد تطبيق التحديثات؟ (y/n): ")
            if response.lower() == 'y':
                self.apply_updates()
    
    def check_readme_files(self):
        """Check README files for consistency"""
        print("📝 فحص ملفات README...")
        
        readme_files = [
            "README.md",
            "README_COMPLETE.md",
            "GITHUB_DEPLOYMENT.md",
            "QUICK_START_GITHUB.md",
            "DEPLOYMENT_CHECKLIST.md"
        ]
        
        for readme in readme_files:
            filepath = self.project_root / readme
            if filepath.exists():
                content = filepath.read_text(encoding='utf-8')
                
                # Check for placeholder URLs
                if "YOUR_USERNAME" in content or "your-repo" in content:
                    self.issues_found.append(f"❌ {readme}: يحتوي على YOUR_USERNAME")
                    self.files_to_update.append((filepath, self.update_readme))
                
                # Check GitHub URLs
                if "github.com/repo" in content or "github.com/username" in content:
                    self.issues_found.append(f"❌ {readme}: روابط GitHub غير صحيحة")
                    self.files_to_update.append((filepath, self.update_readme))
                
                print(f"  ✓ {readme}")
            else:
                print(f"  ⚠️  {readme} - غير موجود")
    
    def check_package_json(self):
        """Check package.json consistency"""
        print("\n📦 فحص package.json...")
        
        package_json_path = self.project_root / "frontend" / "package.json"
        if package_json_path.exists():
            try:
                with open(package_json_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                # Check repository URL
                if "repository" in data:
                    repo_url = data["repository"].get("url", "")
                    if "YOUR_USERNAME" in repo_url or self.github_url not in repo_url:
                        self.issues_found.append("❌ package.json: رابط repository غير صحيح")
                        self.files_to_update.append((package_json_path, self.update_package_json))
                
                print(f"  ✓ frontend/package.json")
            except Exception as e:
                print(f"  ❌ خطأ في قراءة package.json: {e}")
        else:
            print(f"  ⚠️  package.json غير موجود")
    
    def check_frontend_config(self):
        """Check frontend configuration files"""
        print("\n⚙️  فحص إعدادات Frontend...")
        
        # Check vite.config.js
        vite_config = self.project_root / "frontend" / "vite.config.js"
        if vite_config.exists():
            content = vite_config.read_text(encoding='utf-8')
            
            # Check proxy configuration
            if "localhost:5000" not in content:
                self.issues_found.append("❌ vite.config.js: إعدادات proxy غير صحيحة")
            
            print(f"  ✓ vite.config.js")
        
        # Check API service files
        api_service = self.project_root / "frontend" / "src" / "services" / "api.js"
        if api_service.exists():
            content = api_service.read_text(encoding='utf-8')
            
            if "http://localhost:5000" not in content and "localhost:5000" not in content:
                self.issues_found.append("❌ api.js: API URL غير صحيح")
                self.files_to_update.append((api_service, self.update_api_service))
            
            print(f"  ✓ services/api.js")
    
    def check_backend_config(self):
        """Check backend configuration"""
        print("\n⚙️  فحص إعدادات Backend...")
        
        # Check config.py
        config_py = self.project_root / "config.py"
        if config_py.exists():
            print(f"  ✓ config.py")
        
        # Check .env.example
        env_example = self.project_root / ".env.example"
        if env_example.exists():
            content = env_example.read_text(encoding='utf-8')
            
            # Check for placeholder values
            if "your-secret-key" in content.lower() or "change-me" in content.lower():
                print(f"  ℹ️  .env.example يحتوي على قيم placeholder (هذا طبيعي)")
            
            print(f"  ✓ .env.example")
    
    def check_docker_files(self):
        """Check Docker configuration files"""
        print("\n🐳 فحص ملفات Docker...")
        
        docker_files = [
            "docker-compose.yml",
            "docker-compose.dev.yml"
        ]
        
        for docker_file in docker_files:
            filepath = self.project_root / docker_file
            if filepath.exists():
                content = filepath.read_text(encoding='utf-8')
                
                # Check port configurations
                if "5000:5000" in content or "3000:80" in content or "3000:3000" in content:
                    print(f"  ✓ {docker_file}")
                else:
                    self.issues_found.append(f"❌ {docker_file}: إعدادات المنافذ غير صحيحة")
    
    def check_github_workflows(self):
        """Check GitHub Actions workflows"""
        print("\n🔄 فحص GitHub Actions...")
        
        workflows_dir = self.project_root / ".github" / "workflows"
        if workflows_dir.exists():
            for workflow_file in workflows_dir.glob("*.yml"):
                print(f"  ✓ {workflow_file.name}")
        else:
            print(f"  ⚠️  .github/workflows/ غير موجود")
    
    def check_deployment_docs(self):
        """Check deployment documentation"""
        print("\n📚 فحص وثائق النشر...")
        
        docs_files = [
            "GITHUB_DEPLOYMENT.md",
            "DEPLOYMENT_CHECKLIST.md",
            "QUICK_START_GITHUB.md"
        ]
        
        for doc in docs_files:
            filepath = self.project_root / doc
            if filepath.exists():
                print(f"  ✓ {doc}")
    
    def update_readme(self, filepath: Path):
        """Update README file with correct URLs"""
        content = filepath.read_text(encoding='utf-8')
        
        # Replace placeholder URLs
        replacements = {
            "YOUR_USERNAME": self.github_username,
            "your-repo": self.repo_name,
            "https://github.com/repo": self.github_url,
            "https://github.com/username": f"https://github.com/{self.github_username}",
            "<repository-url>": f"{self.github_url}.git",
        }
        
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        filepath.write_text(content, encoding='utf-8')
        print(f"  ✅ تم تحديث {filepath.name}")
    
    def update_package_json(self, filepath: Path):
        """Update package.json with correct repository URL"""
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Update repository
        data["repository"] = {
            "type": "git",
            "url": f"git+{self.github_url}.git"
        }
        
        # Update bugs URL
        data["bugs"] = {
            "url": f"{self.github_url}/issues"
        }
        
        # Update homepage
        data["homepage"] = f"{self.github_url}#readme"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"  ✅ تم تحديث package.json")
    
    def update_api_service(self, filepath: Path):
        """Update API service with correct base URL"""
        content = filepath.read_text(encoding='utf-8')
        
        # Ensure correct API base URL
        if "baseURL" in content:
            # Update existing baseURL
            content = re.sub(
                r'baseURL:\s*["\'].*?["\']',
                f"baseURL: 'http://localhost:{self.config['backend_port']}/api'",
                content
            )
        
        filepath.write_text(content, encoding='utf-8')
        print(f"  ✅ تم تحديث {filepath.name}")
    
    def apply_updates(self):
        """Apply all pending updates"""
        print("\n🔧 تطبيق التحديثات...")
        print("=" * 60)
        
        for filepath, update_func in self.files_to_update:
            try:
                update_func(filepath)
            except Exception as e:
                print(f"  ❌ خطأ في تحديث {filepath.name}: {e}")
        
        print("\n✅ تم تطبيق جميع التحديثات")
    
    def print_report(self):
        """Print consistency check report"""
        print("\n" + "=" * 60)
        print("📊 تقرير الفحص / Check Report")
        print("=" * 60)
        
        if not self.issues_found:
            print("\n✅ ممتاز! المشروع متسق بالكامل")
            print("✅ Perfect! Project is fully consistent")
        else:
            print(f"\n⚠️  تم العثور على {len(self.issues_found)} مشكلة:")
            for issue in self.issues_found:
                print(f"  {issue}")
        
        print(f"\n📁 ملفات للتحديث: {len(self.files_to_update)}")
        
        print("\n" + "=" * 60)
        print("🔗 إعدادات المشروع الحالية:")
        print("=" * 60)
        for key, value in self.config.items():
            print(f"  {key}: {value}")

def main():
    checker = ConsistencyChecker()
    checker.check_all()
    
    print("\n" + "=" * 60)
    print("✅ انتهى الفحص!")
    print("=" * 60)

if __name__ == "__main__":
    main()
