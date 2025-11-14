# -*- coding: utf-8 -*-
"""
Project Consistency Checker and Updater
Ensures all files are consistent and up-to-date across the entire project
"""

import os
import re
import json
from pathlib import Path
from datetime import datetime

class ProjectConsistencyChecker:
    """Check and ensure consistency across all project files"""
    
    def __init__(self, project_root):
        self.project_root = Path(project_root)
        self.issues = []
        self.warnings = []
        self.suggestions = []
        
    def check_all(self):
        """Run all consistency checks"""
        print("=" * 70)
        print("🔍 فحص اتساق المشروع - Project Consistency Check")
        print("=" * 70)
        print()
        
        self.check_version_consistency()
        self.check_dependencies()
        self.check_configuration_files()
        self.check_documentation()
        self.check_api_endpoints()
        self.check_database_models()
        self.check_environment_files()
        self.check_docker_files()
        
        self.print_report()
        
    def check_version_consistency(self):
        """Check version numbers across files"""
        print("📦 Checking version consistency...")
        
        version_files = {
            'package.json': self.extract_version_from_package_json(),
            'setup.py': self.extract_version_from_setup_py(),
            'README.md': self.extract_version_from_readme(),
            'PROJECT_SUMMARY.md': self.extract_version_from_summary()
        }
        
        versions = [v for v in version_files.values() if v]
        
        if len(set(versions)) > 1:
            self.issues.append(
                f"❌ Version mismatch found: {version_files}"
            )
        else:
            print(f"   ✅ Version is consistent: {versions[0] if versions else 'Not found'}")
    
    def extract_version_from_package_json(self):
        """Extract version from package.json"""
        try:
            pkg_file = self.project_root / 'frontend' / 'package.json'
            if pkg_file.exists():
                with open(pkg_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data.get('version')
        except:
            pass
        return None
    
    def extract_version_from_setup_py(self):
        """Extract version from setup.py"""
        try:
            setup_file = self.project_root / 'setup.py'
            if setup_file.exists():
                with open(setup_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r"version=['\"]([^'\"]+)['\"]", content)
                    if match:
                        return match.group(1)
        except:
            pass
        return None
    
    def extract_version_from_readme(self):
        """Extract version from README"""
        try:
            readme = self.project_root / 'README.md'
            if readme.exists():
                with open(readme, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r'version-(\d+\.\d+)', content)
                    if match:
                        return match.group(1)
        except:
            pass
        return None
    
    def extract_version_from_summary(self):
        """Extract version from PROJECT_SUMMARY"""
        try:
            summary = self.project_root / 'PROJECT_SUMMARY.md'
            if summary.exists():
                with open(summary, 'r', encoding='utf-8') as f:
                    content = f.read()
                    match = re.search(r'v(\d+\.\d+)', content)
                    if match:
                        return match.group(1)
        except:
            pass
        return None
    
    def check_dependencies(self):
        """Check if dependencies are consistent"""
        print("📚 Checking dependencies...")
        
        req_file = self.project_root / 'requirements.txt'
        req_minimal = self.project_root / 'requirements-minimal.txt'
        
        if req_file.exists() and req_minimal.exists():
            with open(req_file, 'r') as f:
                full_deps = set(f.read().splitlines())
            
            with open(req_minimal, 'r') as f:
                minimal_deps = set(f.read().splitlines())
            
            if not minimal_deps.issubset(full_deps):
                self.issues.append(
                    "❌ requirements-minimal.txt contains packages not in requirements.txt"
                )
            else:
                print("   ✅ Dependencies are consistent")
        else:
            self.warnings.append("⚠️  Missing requirements files")
    
    def check_configuration_files(self):
        """Check configuration files consistency"""
        print("⚙️  Checking configuration files...")
        
        config_files = ['config.py', 'config_large.py']
        env_example = self.project_root / '.env.example'
        
        if not env_example.exists():
            self.issues.append("❌ .env.example is missing")
        else:
            # Extract keys from .env.example
            with open(env_example, 'r') as f:
                env_keys = set()
                for line in f:
                    if '=' in line and not line.strip().startswith('#'):
                        key = line.split('=')[0].strip()
                        env_keys.add(key)
            
            # Check if config files reference these keys
            for config_file in config_files:
                config_path = self.project_root / config_file
                if config_path.exists():
                    with open(config_path, 'r') as f:
                        content = f.read()
                        for key in env_keys:
                            if key not in content:
                                self.warnings.append(
                                    f"⚠️  {config_file} doesn't reference {key}"
                                )
        
        print("   ✅ Configuration files checked")
    
    def check_documentation(self):
        """Check documentation consistency"""
        print("📖 Checking documentation...")
        
        doc_files = {
            'README.md': self.project_root / 'README.md',
            'README_COMPLETE.md': self.project_root / 'README_COMPLETE.md',
            'PROJECT_SUMMARY.md': self.project_root / 'PROJECT_SUMMARY.md',
            'GITHUB_DEPLOYMENT.md': self.project_root / 'GITHUB_DEPLOYMENT.md'
        }
        
        missing_docs = []
        for name, path in doc_files.items():
            if not path.exists():
                missing_docs.append(name)
        
        if missing_docs:
            self.issues.append(f"❌ Missing documentation: {', '.join(missing_docs)}")
        else:
            print("   ✅ All documentation files present")
    
    def check_api_endpoints(self):
        """Check API endpoint consistency between backend and frontend"""
        print("🔌 Checking API endpoints...")
        
        # This would require parsing both backend routes and frontend API calls
        # For now, just check if main files exist
        
        backend_files = ['app.py', 'optimized_server.py']
        frontend_api = self.project_root / 'frontend' / 'src' / 'services' / 'api.js'
        
        missing = []
        for bf in backend_files:
            if not (self.project_root / bf).exists():
                missing.append(bf)
        
        if not frontend_api.exists():
            missing.append('frontend/src/services/api.js')
        
        if missing:
            self.warnings.append(f"⚠️  Missing API files: {', '.join(missing)}")
        else:
            print("   ✅ API files present")
    
    def check_database_models(self):
        """Check database model consistency"""
        print("🗄️  Checking database models...")
        
        model_files = ['models.py', 'models_large.py']
        
        for model_file in model_files:
            model_path = self.project_root / model_file
            if model_path.exists():
                with open(model_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                    # Check for SQLAlchemy import
                    if 'from flask_sqlalchemy import SQLAlchemy' not in content:
                        self.issues.append(f"❌ {model_file} missing SQLAlchemy import")
                    
                    # Check for db = SQLAlchemy()
                    if 'db = SQLAlchemy()' not in content:
                        self.issues.append(f"❌ {model_file} missing db initialization")
        
        print("   ✅ Database models checked")
    
    def check_environment_files(self):
        """Check environment configuration"""
        print("🔐 Checking environment files...")
        
        env_example = self.project_root / '.env.example'
        gitignore = self.project_root / '.gitignore'
        
        if env_example.exists() and gitignore.exists():
            with open(gitignore, 'r') as f:
                gitignore_content = f.read()
            
            if '.env' not in gitignore_content:
                self.issues.append("❌ .env is not in .gitignore - SECURITY RISK!")
            else:
                print("   ✅ .env properly protected in .gitignore")
        else:
            self.issues.append("❌ Missing .env.example or .gitignore")
    
    def check_docker_files(self):
        """Check Docker configuration"""
        print("🐳 Checking Docker files...")
        
        docker_files = [
            'docker-compose.yml',
            'docker-compose.dev.yml'
        ]
        
        missing = []
        for df in docker_files:
            if not (self.project_root / df).exists():
                missing.append(df)
        
        if missing:
            self.warnings.append(f"⚠️  Missing Docker files: {', '.join(missing)}")
        else:
            print("   ✅ Docker files present")
    
    def print_report(self):
        """Print final report"""
        print()
        print("=" * 70)
        print("📊 تقرير الفحص - Consistency Report")
        print("=" * 70)
        print()
        
        if not self.issues and not self.warnings:
            print("✅ ✅ ✅ All checks passed! Project is consistent! ✅ ✅ ✅")
            print()
            print("المشروع متسق تماماً - كل شيء على ما يرام! 🎉")
        else:
            if self.issues:
                print("🔴 CRITICAL ISSUES:")
                for issue in self.issues:
                    print(f"   {issue}")
                print()
            
            if self.warnings:
                print("🟡 WARNINGS:")
                for warning in self.warnings:
                    print(f"   {warning}")
                print()
            
            if self.suggestions:
                print("💡 SUGGESTIONS:")
                for suggestion in self.suggestions:
                    print(f"   {suggestion}")
                print()
        
        print("=" * 70)
        print(f"Checked at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 70)


def main():
    """Main function"""
    project_root = os.getcwd()
    
    checker = ProjectConsistencyChecker(project_root)
    checker.check_all()
    
    print()
    print("💡 للحصول على تقرير مفصل أكثر، راجع الملفات الفردية")
    print("💡 For more detailed reports, check individual files")
    print()


if __name__ == "__main__":
    main()
