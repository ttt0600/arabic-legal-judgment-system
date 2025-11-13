#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database initialization script for Arabic Legal Judgment System
This script creates the database, tables, and populates initial data
"""

import sys
import os
from datetime import datetime
from werkzeug.security import generate_password_hash

# Add the parent directory to the path to import our modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import (User, Category, Court, Case, Judgment, Document, 
                   LegalArticle, SystemSetting, CaseSession)

def create_database():
    """Create all database tables"""
    print("Creating database tables...")
    with app.app_context():
        db.create_all()
        print("✓ Database tables created successfully")

def create_admin_user():
    """Create default admin user"""
    print("Creating admin user...")
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        if admin_user:
            print("! Admin user already exists")
            return
        
        admin = User(
            username='admin',
            email='admin@legal-system.com',
            password_hash=generate_password_hash('admin123'),
            full_name='مدير النظام',
            role='admin',
            department='إدارة النظام',
            is_active=True
        )
        
        db.session.add(admin)
        db.session.commit()
        print("✓ Admin user created successfully")
        print("  Username: admin")
        print("  Password: admin123")

def create_sample_categories():
    """Create sample legal categories"""
    print("Creating sample categories...")
    with app.app_context():
        categories = [
            {
                'name': 'القضايا المدنية',
                'description': 'القضايا المتعلقة بالحقوق المدنية والشخصية',
                'color': '#007bff'
            },
            {
                'name': 'القضايا التجارية',
                'description': 'القضايا المتعلقة بالأنشطة التجارية والشركات',
                'color': '#28a745'
            },
            {
                'name': 'القضايا الجنائية',
                'description': 'القضايا المتعلقة بالجرائم والعقوبات',
                'color': '#dc3545'
            },
            {
                'name': 'القضايا الإدارية',
                'description': 'القضايا المتعلقة بالإدارة الحكومية',
                'color': '#ffc107'
            },
            {
                'name': 'قضايا الأحوال الشخصية',
                'description': 'قضايا الزواج والطلاق والميراث',
                'color': '#17a2b8'
            },
            {
                'name': 'القضايا العمالية',
                'description': 'القضايا المتعلقة بحقوق العمال وأصحاب العمل',
                'color': '#6c757d'
            },
            {
                'name': 'القضايا العقارية',
                'description': 'القضايا المتعلقة بالعقارات والملكية',
                'color': '#fd7e14'
            },
            {
                'name': 'قضايا الملكية الفكرية',
                'description': 'القضايا المتعلقة بحقوق الملكية الفكرية',
                'color': '#6f42c1'
            }
        ]
        
        for cat_data in categories:
            # Check if category already exists
            existing_cat = Category.query.filter_by(name=cat_data['name']).first()
            if existing_cat:
                continue
                
            category = Category(
                name=cat_data['name'],
                description=cat_data['description'],
                color=cat_data['color'],
                is_active=True
            )
            db.session.add(category)
        
        db.session.commit()
        print(f"✓ Created {len(categories)} sample categories")

def create_sample_courts():
    """Create sample courts"""
    print("Creating sample courts...")
    with app.app_context():
        courts = [
            {
                'name': 'المحكمة العامة بالرياض',
                'location': 'الرياض',
                'court_type': 'محكمة عامة',
                'jurisdiction': 'القضايا العامة',
                'address': 'الرياض، المملكة العربية السعودية',
                'phone': '+966112345678'
            },
            {
                'name': 'محكمة الاستئناف بالرياض',
                'location': 'الرياض',
                'court_type': 'محكمة استئناف',
                'jurisdiction': 'الاستئناف',
                'address': 'الرياض، المملكة العربية السعودية',
                'phone': '+966112345679'
            },
            {
                'name': 'المحكمة التجارية بالرياض',
                'location': 'الرياض',
                'court_type': 'محكمة متخصصة',
                'jurisdiction': 'القضايا التجارية',
                'address': 'الرياض، المملكة العربية السعودية',
                'phone': '+966112345680'
            },
            {
                'name': 'المحكمة الإدارية بالرياض',
                'location': 'الرياض',
                'court_type': 'محكمة إدارية',
                'jurisdiction': 'القضايا الإدارية',
                'address': 'الرياض، المملكة العربية السعودية',
                'phone': '+966112345681'
            },
            {
                'name': 'محكمة الأحوال الشخصية بالرياض',
                'location': 'الرياض',
                'court_type': 'محكمة متخصصة',
                'jurisdiction': 'الأحوال الشخصية',
                'address': 'الرياض، المملكة العربية السعودية',
                'phone': '+966112345682'
            }
        ]
        
        for court_data in courts:
            # Check if court already exists
            existing_court = Court.query.filter_by(name=court_data['name']).first()
            if existing_court:
                continue
                
            court = Court(
                name=court_data['name'],
                location=court_data['location'],
                court_type=court_data['court_type'],
                jurisdiction=court_data['jurisdiction'],
                address=court_data['address'],
                phone=court_data['phone'],
                is_active=True
            )
            db.session.add(court)
        
        db.session.commit()
        print(f"✓ Created {len(courts)} sample courts")

def create_sample_legal_articles():
    """Create sample legal articles"""
    print("Creating sample legal articles...")
    with app.app_context():
        articles = [
            {
                'article_number': '1',
                'law_name': 'نظام المرافعات الشرعية',
                'law_number': 'م/1',
                'law_year': 1435,
                'title': 'تطبيق أحكام الشريعة الإسلامية',
                'content': 'تطبق المحاكم على القضايا المعروضة عليها أحكام الشريعة الإسلامية، وفقاً لما دل عليه الكتاب والسنة، وما يصدره ولي الأمر من أنظمة لا تتعارض مع الكتاب والسنة.',
                'chapter': 'الباب الأول - أحكام عامة'
            },
            {
                'article_number': '25',
                'law_name': 'نظام المرافعات الشرعية',
                'law_number': 'م/1',
                'law_year': 1435,
                'title': 'اختصاص المحاكم',
                'content': 'تختص المحاكم العامة بالفصل في جميع الخصومات والجرائم والقضايا الداخلة في اختصاص القضاء الشرعي.',
                'chapter': 'الباب الثاني - الاختصاص'
            },
            {
                'article_number': '1',
                'law_name': 'نظام الشركات',
                'law_number': 'م/3',
                'law_year': 1437,
                'title': 'تعريف الشركة',
                'content': 'الشركة عقد يلتزم بموجبه شخصان أو أكثر بأن يساهم كل منهم في مشروع يستهدف الربح بتقديم حصة من مال أو عمل، لاقتسام ما قد ينشأ عن المشروع من ربح أو خسارة.',
                'chapter': 'الباب الأول - أحكام عامة'
            },
            {
                'article_number': '76',
                'law_name': 'نظام العمل',
                'law_number': 'م/51',
                'law_year': 1426,
                'title': 'ساعات العمل',
                'content': 'ساعات العمل الفعلية للعامل ثماني ساعات يومياً، أو ثماني وأربعون ساعة أسبوعياً.',
                'chapter': 'الباب السادس - ساعات العمل والراحة الأسبوعية والإجازات'
            }
        ]
        
        for article_data in articles:
            # Check if article already exists
            existing_article = LegalArticle.query.filter_by(
                article_number=article_data['article_number'],
                law_name=article_data['law_name']
            ).first()
            if existing_article:
                continue
                
            article = LegalArticle(
                article_number=article_data['article_number'],
                law_name=article_data['law_name'],
                law_number=article_data['law_number'],
                law_year=article_data['law_year'],
                title=article_data['title'],
                content=article_data['content'],
                chapter=article_data['chapter'],
                is_active=True,
                effective_date=datetime(article_data['law_year'], 1, 1)
            )
            db.session.add(article)
        
        db.session.commit()
        print(f"✓ Created {len(articles)} sample legal articles")

def create_system_settings():
    """Create default system settings"""
    print("Creating system settings...")
    with app.app_context():
        settings = [
            {
                'key': 'system_name',
                'value': 'نظام إدارة الأحكام القانونية العربية',
                'description': 'اسم النظام',
                'category': 'general',
                'is_public': True
            },
            {
                'key': 'system_version',
                'value': '1.0.0',
                'description': 'إصدار النظام',
                'category': 'general',
                'is_public': True
            },
            {
                'key': 'default_language',
                'value': 'ar',
                'description': 'اللغة الافتراضية للنظام',
                'category': 'localization',
                'is_public': True
            },
            {
                'key': 'cases_per_page',
                'value': '20',
                'description': 'عدد القضايا في الصفحة الواحدة',
                'data_type': 'integer',
                'category': 'pagination',
                'is_public': False
            },
            {
                'key': 'max_file_size',
                'value': '16777216',  # 16MB
                'description': 'الحد الأقصى لحجم الملف بالبايت',
                'data_type': 'integer',
                'category': 'upload',
                'is_public': False
            },
            {
                'key': 'allowed_file_types',
                'value': '["pdf", "doc", "docx", "txt", "jpg", "jpeg", "png"]',
                'description': 'أنواع الملفات المسموحة',
                'data_type': 'json',
                'category': 'upload',
                'is_public': False
            },
            {
                'key': 'backup_enabled',
                'value': 'true',
                'description': 'تفعيل النسخ الاحتياطي التلقائي',
                'data_type': 'boolean',
                'category': 'backup',
                'is_public': False
            },
            {
                'key': 'notification_enabled',
                'value': 'true',
                'description': 'تفعيل الإشعارات',
                'data_type': 'boolean',
                'category': 'notification',
                'is_public': False
            }
        ]
        
        for setting_data in settings:
            # Check if setting already exists
            existing_setting = SystemSetting.query.filter_by(key=setting_data['key']).first()
            if existing_setting:
                continue
                
            setting = SystemSetting(
                key=setting_data['key'],
                value=setting_data['value'],
                description=setting_data['description'],
                data_type=setting_data.get('data_type', 'string'),
                category=setting_data['category'],
                is_public=setting_data['is_public']
            )
            db.session.add(setting)
        
        db.session.commit()
        print(f"✓ Created {len(settings)} system settings")

def create_sample_data():
    """Create sample cases and judgments for testing"""
    print("Creating sample data...")
    with app.app_context():
        # Get admin user, first category, and first court
        admin_user = User.query.filter_by(username='admin').first()
        first_category = Category.query.first()
        first_court = Court.query.first()
        
        if not admin_user or not first_category or not first_court:
            print("! Cannot create sample data - missing admin user, category, or court")
            return
        
        # Create sample cases
        sample_cases = [
            {
                'case_number': 'CASE-20240101-ABC12345',
                'title': 'قضية تعويض أضرار حادث مروري',
                'description': 'دعوى تعويض عن الأضرار الناتجة عن حادث مروري وقع بتاريخ 15/12/2023 بمدينة الرياض',
                'plaintiff': 'أحمد محمد العبدالله',
                'defendant': 'شركة التأمين الوطنية',
                'status': 'قيد النظر',
                'priority': 'عالي',
                'case_type': 'تعويضات',
                'claimed_amount': 50000.00,
                'lawyer_name': 'المحامي سعد العتيبي',
                'case_date': datetime(2024, 1, 15)
            },
            {
                'case_number': 'CASE-20240102-DEF67890',
                'title': 'نزاع تجاري حول عقد توريد',
                'description': 'نزاع بين شركة المقاولات والشركة الموردة حول تنفيذ عقد توريد مواد البناء',
                'plaintiff': 'شركة البناء المتقدم المحدودة',
                'defendant': 'مؤسسة التوريد الشامل',
                'status': 'جديدة',
                'priority': 'متوسط',
                'case_type': 'عقود تجارية',
                'claimed_amount': 250000.00,
                'lawyer_name': 'المحاميه فاطمة الزهراني',
                'case_date': datetime(2024, 2, 1)
            }
        ]
        
        created_cases = []
        for case_data in sample_cases:
            case = Case(
                case_number=case_data['case_number'],
                title=case_data['title'],
                description=case_data['description'],
                plaintiff=case_data['plaintiff'],
                defendant=case_data['defendant'],
                status=case_data['status'],
                priority=case_data['priority'],
                case_type=case_data['case_type'],
                claimed_amount=case_data['claimed_amount'],
                lawyer_name=case_data['lawyer_name'],
                case_date=case_data['case_date'],
                category_id=first_category.id,
                court_id=first_court.id,
                created_by=admin_user.id
            )
            db.session.add(case)
            created_cases.append(case)
        
        db.session.commit()
        
        # Create sample judgments for the first case
        if created_cases:
            first_case = created_cases[0]
            sample_judgment = Judgment(
                case_id=first_case.id,
                title='حكم ابتدائي في قضية التعويض',
                content='بعد الاطلاع على أوراق الدعوى والمرافعات المقدمة من الطرفين، وبناءً على ما ثبت لدى المحكمة من أدلة ووثائق، تقرر المحكمة الحكم للمدعي بمبلغ 35000 ريال سعودي كتعويض عن الأضرار المادية والمعنوية الناتجة عن الحادث المروري.',
                judgment_type='حكم ابتدائي',
                judgment_date=datetime(2024, 3, 15),
                judge_name='القاضي محمد السعيد',
                court_level='ابتدائية',
                status='نهائي',
                judgment_amount=35000.00,
                legal_articles='المادة 76 من نظام المرور، المادة 163 من نظام المرافعات الشرعية',
                created_by=admin_user.id,
                court_id=first_court.id
            )
            db.session.add(sample_judgment)
            db.session.commit()
        
        print(f"✓ Created {len(sample_cases)} sample cases and 1 sample judgment")

def initialize_database():
    """Main function to initialize the database"""
    print("=== Arabic Legal Judgment System - Database Initialization ===")
    print()
    
    try:
        create_database()
        create_admin_user()
        create_sample_categories()
        create_sample_courts()
        create_sample_legal_articles()
        create_system_settings()
        create_sample_data()
        
        print()
        print("✅ Database initialization completed successfully!")
        print()
        print("You can now:")
        print("1. Start the Flask application: python app.py")
        print("2. Login with username: admin, password: admin123")
        print("3. Begin using the Arabic Legal Judgment System")
        print()
        
    except Exception as e:
        print(f"❌ Error during database initialization: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    initialize_database()
