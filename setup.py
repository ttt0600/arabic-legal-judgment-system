#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Setup script for Arabic Legal Judgment System
This script automates the complete setup process
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def print_step(step_number, description):
    """Print a formatted step description"""
    print(f"\n{'='*60}")
    print(f"الخطوة {step_number}: {description}")
    print('='*60)

def run_command(command, cwd=None):
    """Run a system command and return success status"""
    try:
        result = subprocess.run(command, shell=True, cwd=cwd, check=True, 
                              capture_output=True, text=True)
        return True, result.stdout
    except subprocess.CalledProcessError as e:
        return False, e.stderr

def check_prerequisites():
    """Check if required software is installed"""
    print_step(1, "فحص المتطلبات الأساسية")
    
    requirements = {
        'python': 'python --version',
        'pip': 'pip --version',
        'node': 'node --version',
        'npm': 'npm --version',
        'mysql': 'mysql --version'
    }
    
    missing_requirements = []
    
    for name, command in requirements.items():
        success, output = run_command(command)
        if success:
            print(f"✓ {name}: {output.strip().split()[0] if output else 'موجود'}")
        else:
            print(f"✗ {name}: غير موجود")
            missing_requirements.append(name)
    
    if missing_requirements:
        print(f"\nيرجى تثبيت المتطلبات المفقودة: {', '.join(missing_requirements)}")
        return False
    
    print("\n✓ جميع المتطلبات الأساسية متوفرة")
    return True

def setup_python_environment():
    """Setup Python virtual environment and install dependencies"""
    print_step(2, "إعداد بيئة Python")
    
    project_root = Path(__file__).parent
    
    # Create virtual environment
    print("إنشاء البيئة الافتراضية...")
    success, output = run_command('python -m venv venv', cwd=project_root)
    if not success:
        print(f"فشل في إنشاء البيئة الافتراضية: {output}")
        return False
    
    # Activate virtual environment
    if platform.system() == 'Windows':
        activate_script = project_root / 'venv' / 'Scripts' / 'activate.bat'
        pip_command = str(project_root / 'venv' / 'Scripts' / 'pip.exe')
    else:
        activate_script = project_root / 'venv' / 'bin' / 'activate'
        pip_command = str(project_root / 'venv' / 'bin' / 'pip')
    
    # Install Python dependencies
    print("تثبيت مكتبات Python...")
    success, output = run_command(f'"{pip_command}" install -r requirements.txt', cwd=project_root)
    if not success:
        print(f"فشل في تثبيت مكتبات Python: {output}")
        return False
    
    print("✓ تم إعداد بيئة Python بنجاح")
    return True

def setup_database():
    """Setup database and run migrations"""
    print_step(3, "إعداد قاعدة البيانات")
    
    project_root = Path(__file__).parent
    
    # Check if .env file exists
    env_file = project_root / '.env'
    if not env_file.exists():
        print("إنشاء ملف البيئة (.env)...")
        env_example = project_root / '.env.example'
        if env_example.exists():
            import shutil
            shutil.copy(env_example, env_file)
            print("تم إنشاء ملف .env من .env.example")
            print("يرجى تحديث إعدادات قاعدة البيانات في ملف .env")
        else:
            print("ملف .env.example غير موجود")
            return False
    
    # Run database initialization
    print("تهيئة قاعدة البيانات...")
    if platform.system() == 'Windows':
        python_command = str(project_root / 'venv' / 'Scripts' / 'python.exe')
    else:
        python_command = str(project_root / 'venv' / 'bin' / 'python')
    
    success, output = run_command(f'"{python_command}" database/init_db.py', cwd=project_root)
    if not success:
        print(f"فشل في تهيئة قاعدة البيانات: {output}")
        print("يرجى التأكد من إعدادات قاعدة البيانات في ملف .env")
        return False
    
    print("✓ تم إعداد قاعدة البيانات بنجاح")
    return True

def setup_frontend():
    """Setup frontend dependencies"""
    print_step(4, "إعداد الواجهة الأمامية")
    
    frontend_path = Path(__file__).parent / 'frontend'
    
    # Install npm dependencies
    print("تثبيت مكتبات Node.js...")
    success, output = run_command('npm install', cwd=frontend_path)
    if not success:
        print(f"فشل في تثبيت مكتبات Node.js: {output}")
        return False
    
    print("✓ تم إعداد الواجهة الأمامية بنجاح")
    return True

def create_startup_scripts():
    """Create startup scripts for easy development"""
    print_step(5, "إنشاء ملفات التشغيل")
    
    project_root = Path(__file__).parent
    
    # Backend startup script
    if platform.system() == 'Windows':
        backend_script = """@echo off
echo Starting Arabic Legal Judgment System Backend...
call venv\\Scripts\\activate.bat
python app.py
pause
"""
        script_path = project_root / 'start_backend.bat'
    else:
        backend_script = """#!/bin/bash
echo "Starting Arabic Legal Judgment System Backend..."
source venv/bin/activate
python app.py
"""
        script_path = project_root / 'start_backend.sh'
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(backend_script)
    
    if not platform.system() == 'Windows':
        os.chmod(script_path, 0o755)
    
    # Frontend startup script
    if platform.system() == 'Windows':
        frontend_script = """@echo off
echo Starting Arabic Legal Judgment System Frontend...
cd frontend
npm run dev
pause
"""
        script_path = project_root / 'start_frontend.bat'
    else:
        frontend_script = """#!/bin/bash
echo "Starting Arabic Legal Judgment System Frontend..."
cd frontend
npm run dev
"""
        script_path = project_root / 'start_frontend.sh'
    
    with open(script_path, 'w', encoding='utf-8') as f:
        f.write(frontend_script)
    
    if not platform.system() == 'Windows':
        os.chmod(script_path, 0o755)
    
    print("✓ تم إنشاء ملفات التشغيل بنجاح")
    return True

def main():
    """Main setup function"""
    print("=" * 60)
    print("مرحباً بك في نظام إعداد الأحكام القانونية العربية")
    print("=" * 60)
    
    steps = [
        ("فحص المتطلبات", check_prerequisites),
        ("إعداد Python", setup_python_environment),
        ("إعداد قاعدة البيانات", setup_database),
        ("إعداد الواجهة الأمامية", setup_frontend),
        ("إنشاء ملفات التشغيل", create_startup_scripts),
    ]
    
    for step_name, step_function in steps:
        if not step_function():
            print(f"\n❌ فشل في {step_name}")
            print("يرجى مراجعة الأخطاء أعلاه وإعادة المحاولة")
            sys.exit(1)
    
    print("\n" + "=" * 60)
    print("🎉 تم إعداد النظام بنجاح!")
    print("=" * 60)
    
    print("\nلتشغيل النظام:")
    print("1. تشغيل الخادم الخلفي:")
    if platform.system() == 'Windows':
        print("   start_backend.bat")
    else:
        print("   ./start_backend.sh")
    
    print("2. تشغيل الواجهة الأمامية (في نافذة طرفية جديدة):")
    if platform.system() == 'Windows':
        print("   start_frontend.bat")
    else:
        print("   ./start_frontend.sh")
    
    print("\n3. افتح المتصفح واذهب إلى: http://localhost:3000")
    print("4. استخدم بيانات تسجيل الدخول التجريبية:")
    print("   اسم المستخدم: admin")
    print("   كلمة المرور: admin123")
    
    print("\nاستمتع باستخدام نظام إدارة الأحكام القانونية العربية! 🚀")

if __name__ == "__main__":
    main()
