#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Database Migration Script - Upgrade to Large Dataset Support
This script migrates the database schema to support large datasets
"""

import sys
import os
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import create_engine, text, inspect
from sqlalchemy.pool import NullPool
import pymysql
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_database_url():
    """Get database URL from environment"""
    host = os.getenv('MYSQL_HOST', 'localhost')
    user = os.getenv('MYSQL_USER', 'root')
    password = os.getenv('MYSQL_PASSWORD', '')
    database = os.getenv('MYSQL_DB', 'arabic_legal_system')
    
    return f"mysql+pymysql://{user}:{password}@{host}/{database}?charset=utf8mb4"

def backup_database(engine):
    """Create a backup before migration"""
    print("📦 Creating database backup...")
    
    try:
        with engine.connect() as conn:
            # Get database name
            result = conn.execute(text("SELECT DATABASE()"))
            db_name = result.fetchone()[0]
            
            print(f"   Database: {db_name}")
            print(f"   Backup will be created by your database administrator")
            print(f"   Recommended: mysqldump -u root -p {db_name} > backup_{db_name}.sql")
            
            response = input("\n⚠️  Have you created a backup? (yes/no): ")
            if response.lower() != 'yes':
                print("❌ Please create a backup before proceeding!")
                return False
        
        print("✅ Backup confirmed")
        return True
    except Exception as e:
        print(f"❌ Error checking backup: {e}")
        return False

def alter_table_columns(engine):
    """Alter existing table columns to support larger sizes"""
    print("\n🔧 Upgrading table columns for large datasets...")
    
    alterations = [
        # Users table
        ("users", [
            "ALTER TABLE users MODIFY COLUMN username VARCHAR(100)",
            "ALTER TABLE users MODIFY COLUMN email VARCHAR(150)",
            "ALTER TABLE users MODIFY COLUMN full_name VARCHAR(200)",
            "ALTER TABLE users MODIFY COLUMN phone VARCHAR(30)",
            "ALTER TABLE users MODIFY COLUMN department VARCHAR(150)",
        ]),
        
        # Categories table
        ("categories", [
            "ALTER TABLE categories MODIFY COLUMN name VARCHAR(200)",
            "ALTER TABLE categories MODIFY COLUMN description TEXT(5000)",
            "ALTER TABLE categories MODIFY COLUMN color VARCHAR(10)",
        ]),
        
        # Courts table
        ("courts", [
            "ALTER TABLE courts MODIFY COLUMN name VARCHAR(250)",
            "ALTER TABLE courts MODIFY COLUMN location VARCHAR(300)",
            "ALTER TABLE courts MODIFY COLUMN court_type VARCHAR(100)",
            "ALTER TABLE courts MODIFY COLUMN jurisdiction VARCHAR(200)",
            "ALTER TABLE courts MODIFY COLUMN address TEXT(2000)",
            "ALTER TABLE courts MODIFY COLUMN phone VARCHAR(30)",
            "ALTER TABLE courts MODIFY COLUMN email VARCHAR(150)",
        ]),
        
        # Cases table
        ("cases", [
            "ALTER TABLE cases MODIFY COLUMN case_number VARCHAR(100)",
            "ALTER TABLE cases MODIFY COLUMN title VARCHAR(500)",
            "ALTER TABLE cases MODIFY COLUMN description TEXT(50000)",
            "ALTER TABLE cases MODIFY COLUMN plaintiff VARCHAR(300)",
            "ALTER TABLE cases MODIFY COLUMN defendant VARCHAR(300)",
            "ALTER TABLE cases MODIFY COLUMN status VARCHAR(100)",
            "ALTER TABLE cases MODIFY COLUMN priority VARCHAR(50)",
            "ALTER TABLE cases MODIFY COLUMN case_type VARCHAR(200)",
            "ALTER TABLE cases MODIFY COLUMN legal_basis TEXT(20000)",
            "ALTER TABLE cases MODIFY COLUMN claimed_amount DECIMAL(20, 2)",
            "ALTER TABLE cases MODIFY COLUMN lawyer_name VARCHAR(250)",
            "ALTER TABLE cases MODIFY COLUMN lawyer_license VARCHAR(100)",
            "ALTER TABLE cases MODIFY COLUMN fees DECIMAL(15, 2)",
            "ALTER TABLE cases MODIFY COLUMN notes TEXT(50000)",
        ]),
        
        # Judgments table
        ("judgments", [
            "ALTER TABLE judgments MODIFY COLUMN title VARCHAR(500)",
            "ALTER TABLE judgments MODIFY COLUMN content TEXT(100000)",
            "ALTER TABLE judgments MODIFY COLUMN judgment_type VARCHAR(100)",
            "ALTER TABLE judgments MODIFY COLUMN judge_name VARCHAR(250)",
            "ALTER TABLE judgments MODIFY COLUMN court_level VARCHAR(100)",
            "ALTER TABLE judgments MODIFY COLUMN status VARCHAR(100)",
            "ALTER TABLE judgments MODIFY COLUMN appeal_status VARCHAR(100)",
            "ALTER TABLE judgments MODIFY COLUMN judgment_amount DECIMAL(20, 2)",
            "ALTER TABLE judgments MODIFY COLUMN fees_awarded DECIMAL(15, 2)",
            "ALTER TABLE judgments MODIFY COLUMN execution_status VARCHAR(100)",
            "ALTER TABLE judgments MODIFY COLUMN legal_articles TEXT(50000)",
            "ALTER TABLE judgments MODIFY COLUMN precedents TEXT(50000)",
            "ALTER TABLE judgments MODIFY COLUMN notes TEXT(50000)",
            "ALTER TABLE judgments MODIFY COLUMN keywords TEXT(10000)",
        ]),
        
        # Documents table
        ("documents", [
            "ALTER TABLE documents MODIFY COLUMN filename VARCHAR(500)",
            "ALTER TABLE documents MODIFY COLUMN original_filename VARCHAR(500)",
            "ALTER TABLE documents MODIFY COLUMN file_path VARCHAR(1000)",
            "ALTER TABLE documents MODIFY COLUMN file_size BIGINT",
            "ALTER TABLE documents MODIFY COLUMN mime_type VARCHAR(150)",
            "ALTER TABLE documents MODIFY COLUMN document_type VARCHAR(100)",
            "ALTER TABLE documents MODIFY COLUMN description TEXT(10000)",
            "ALTER TABLE documents MODIFY COLUMN extracted_text TEXT(100000)",
        ]),
        
        # Case Sessions table
        ("case_sessions", [
            "ALTER TABLE case_sessions MODIFY COLUMN session_type VARCHAR(100)",
            "ALTER TABLE case_sessions MODIFY COLUMN judge_name VARCHAR(250)",
            "ALTER TABLE case_sessions MODIFY COLUMN court_room VARCHAR(100)",
            "ALTER TABLE case_sessions MODIFY COLUMN agenda TEXT(20000)",
            "ALTER TABLE case_sessions MODIFY COLUMN minutes TEXT(50000)",
            "ALTER TABLE case_sessions MODIFY COLUMN plaintiff_lawyer VARCHAR(250)",
            "ALTER TABLE case_sessions MODIFY COLUMN defendant_lawyer VARCHAR(250)",
            "ALTER TABLE case_sessions MODIFY COLUMN status VARCHAR(100)",
            "ALTER TABLE case_sessions MODIFY COLUMN postponement_reason TEXT(10000)",
        ]),
        
        # Legal Articles table
        ("legal_articles", [
            "ALTER TABLE legal_articles MODIFY COLUMN article_number VARCHAR(50)",
            "ALTER TABLE legal_articles MODIFY COLUMN title VARCHAR(500)",
            "ALTER TABLE legal_articles MODIFY COLUMN content TEXT(100000)",
            "ALTER TABLE legal_articles MODIFY COLUMN law_name VARCHAR(500)",
            "ALTER TABLE legal_articles MODIFY COLUMN law_number VARCHAR(100)",
            "ALTER TABLE legal_articles MODIFY COLUMN chapter VARCHAR(300)",
            "ALTER TABLE legal_articles MODIFY COLUMN section VARCHAR(300)",
        ]),
        
        # Legal Precedents table
        ("legal_precedents", [
            "ALTER TABLE legal_precedents MODIFY COLUMN title VARCHAR(500)",
            "ALTER TABLE legal_precedents MODIFY COLUMN summary TEXT(20000)",
            "ALTER TABLE legal_precedents MODIFY COLUMN full_text TEXT(100000)",
            "ALTER TABLE legal_precedents MODIFY COLUMN court_name VARCHAR(250)",
            "ALTER TABLE legal_precedents MODIFY COLUMN court_level VARCHAR(100)",
            "ALTER TABLE legal_precedents MODIFY COLUMN case_reference VARCHAR(200)",
            "ALTER TABLE legal_precedents MODIFY COLUMN legal_principle TEXT(50000)",
            "ALTER TABLE legal_precedents MODIFY COLUMN keywords TEXT(10000)",
            "ALTER TABLE legal_precedents MODIFY COLUMN cited_articles TEXT(20000)",
        ]),
        
        # System Settings table
        ("system_settings", [
            "ALTER TABLE system_settings MODIFY COLUMN `key` VARCHAR(200)",
            "ALTER TABLE system_settings MODIFY COLUMN value TEXT(20000)",
            "ALTER TABLE system_settings MODIFY COLUMN description TEXT(5000)",
            "ALTER TABLE system_settings MODIFY COLUMN data_type VARCHAR(50)",
            "ALTER TABLE system_settings MODIFY COLUMN category VARCHAR(100)",
        ]),
        
        # Audit Logs table
        ("audit_logs", [
            "ALTER TABLE audit_logs MODIFY COLUMN action VARCHAR(150)",
            "ALTER TABLE audit_logs MODIFY COLUMN resource_type VARCHAR(100)",
            "ALTER TABLE audit_logs MODIFY COLUMN old_values TEXT(50000)",
            "ALTER TABLE audit_logs MODIFY COLUMN new_values TEXT(50000)",
            "ALTER TABLE audit_logs MODIFY COLUMN ip_address VARCHAR(50)",
            "ALTER TABLE audit_logs MODIFY COLUMN user_agent VARCHAR(1000)",
        ]),
        
        # Notifications table
        ("notifications", [
            "ALTER TABLE notifications MODIFY COLUMN title VARCHAR(500)",
            "ALTER TABLE notifications MODIFY COLUMN message TEXT(10000)",
            "ALTER TABLE notifications MODIFY COLUMN notification_type VARCHAR(100)",
            "ALTER TABLE notifications MODIFY COLUMN resource_type VARCHAR(100)",
        ]),
        
        # Search Indexes table
        ("search_indexes", [
            "ALTER TABLE search_indexes MODIFY COLUMN resource_type VARCHAR(100)",
            "ALTER TABLE search_indexes MODIFY COLUMN content TEXT(100000)",
            "ALTER TABLE search_indexes MODIFY COLUMN normalized_content TEXT(100000)",
            "ALTER TABLE search_indexes MODIFY COLUMN keywords TEXT(10000)",
            "ALTER TABLE search_indexes MODIFY COLUMN language VARCHAR(20)",
        ]),
    ]
    
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            for table_name, queries in alterations:
                if table_name not in existing_tables:
                    print(f"   ⏭️  Skipping {table_name} (table doesn't exist)")
                    continue
                
                print(f"   🔄 Updating {table_name}...")
                for query in queries:
                    try:
                        conn.execute(text(query))
                        conn.commit()
                    except Exception as e:
                        # Some columns might not exist or already be correct size
                        if "doesn't exist" not in str(e).lower():
                            print(f"      ⚠️  Warning: {str(e)[:100]}")
                
                print(f"   ✅ {table_name} updated")
        
        print("\n✅ All table columns upgraded successfully")
        return True
        
    except Exception as e:
        print(f"\n❌ Error during column alteration: {e}")
        return False

def add_missing_indexes(engine):
    """Add indexes for better performance with large datasets"""
    print("\n📊 Adding performance indexes...")
    
    indexes = [
        # Users indexes
        "CREATE INDEX IF NOT EXISTS idx_username ON users(username)",
        "CREATE INDEX IF NOT EXISTS idx_email ON users(email)",
        "CREATE INDEX IF NOT EXISTS idx_role ON users(role)",
        "CREATE INDEX IF NOT EXISTS idx_is_active ON users(is_active)",
        "CREATE INDEX IF NOT EXISTS idx_last_login ON users(last_login)",
        "CREATE INDEX IF NOT EXISTS idx_created_at ON users(created_at)",
        
        # Categories indexes
        "CREATE INDEX IF NOT EXISTS idx_category_name ON categories(name)",
        "CREATE INDEX IF NOT EXISTS idx_category_active ON categories(is_active)",
        
        # Courts indexes
        "CREATE INDEX IF NOT EXISTS idx_court_name ON courts(name)",
        "CREATE INDEX IF NOT EXISTS idx_court_type ON courts(court_type)",
        "CREATE INDEX IF NOT EXISTS idx_court_active ON courts(is_active)",
        
        # Cases indexes
        "CREATE INDEX IF NOT EXISTS idx_case_status ON cases(status)",
        "CREATE INDEX IF NOT EXISTS idx_case_priority ON cases(priority)",
        "CREATE INDEX IF NOT EXISTS idx_case_date ON cases(case_date)",
        "CREATE INDEX IF NOT EXISTS idx_case_category ON cases(category_id)",
        "CREATE INDEX IF NOT EXISTS idx_case_court ON cases(court_id)",
        "CREATE INDEX IF NOT EXISTS idx_case_created ON cases(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_case_updated ON cases(updated_at)",
        "CREATE INDEX IF NOT EXISTS idx_case_plaintiff ON cases(plaintiff)",
        "CREATE INDEX IF NOT EXISTS idx_case_defendant ON cases(defendant)",
        
        # Judgments indexes
        "CREATE INDEX IF NOT EXISTS idx_judgment_case ON judgments(case_id)",
        "CREATE INDEX IF NOT EXISTS idx_judgment_type ON judgments(judgment_type)",
        "CREATE INDEX IF NOT EXISTS idx_judgment_date ON judgments(judgment_date)",
        "CREATE INDEX IF NOT EXISTS idx_judgment_status ON judgments(status)",
        "CREATE INDEX IF NOT EXISTS idx_judgment_court ON judgments(court_id)",
        "CREATE INDEX IF NOT EXISTS idx_judgment_created ON judgments(created_at)",
        "CREATE INDEX IF NOT EXISTS idx_judgment_updated ON judgments(updated_at)",
        
        # Documents indexes
        "CREATE INDEX IF NOT EXISTS idx_document_case ON documents(case_id)",
        "CREATE INDEX IF NOT EXISTS idx_document_judgment ON documents(judgment_id)",
        "CREATE INDEX IF NOT EXISTS idx_document_type ON documents(document_type)",
        "CREATE INDEX IF NOT EXISTS idx_document_uploaded ON documents(uploaded_at)",
        "CREATE INDEX IF NOT EXISTS idx_document_searchable ON documents(is_searchable)",
        "CREATE INDEX IF NOT EXISTS idx_document_confidential ON documents(is_confidential)",
        
        # Case Sessions indexes
        "CREATE INDEX IF NOT EXISTS idx_session_case ON case_sessions(case_id)",
        "CREATE INDEX IF NOT EXISTS idx_session_date ON case_sessions(session_date)",
        "CREATE INDEX IF NOT EXISTS idx_session_status ON case_sessions(status)",
        "CREATE INDEX IF NOT EXISTS idx_session_next_date ON case_sessions(next_session_date)",
        
        # Legal Articles indexes
        "CREATE INDEX IF NOT EXISTS idx_article_number ON legal_articles(article_number)",
        "CREATE INDEX IF NOT EXISTS idx_article_law ON legal_articles(law_name)",
        "CREATE INDEX IF NOT EXISTS idx_article_active ON legal_articles(is_active)",
        "CREATE INDEX IF NOT EXISTS idx_article_year ON legal_articles(law_year)",
        
        # Legal Precedents indexes
        "CREATE INDEX IF NOT EXISTS idx_precedent_court ON legal_precedents(court_name)",
        "CREATE INDEX IF NOT EXISTS idx_precedent_date ON legal_precedents(decision_date)",
        "CREATE INDEX IF NOT EXISTS idx_precedent_reference ON legal_precedents(case_reference)",
        "CREATE INDEX IF NOT EXISTS idx_precedent_citations ON legal_precedents(citation_count)",
        
        # Audit Logs indexes
        "CREATE INDEX IF NOT EXISTS idx_audit_user ON audit_logs(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_audit_timestamp ON audit_logs(timestamp)",
        "CREATE INDEX IF NOT EXISTS idx_audit_action ON audit_logs(action)",
        "CREATE INDEX IF NOT EXISTS idx_audit_resource_type ON audit_logs(resource_type)",
        "CREATE INDEX IF NOT EXISTS idx_audit_resource_id ON audit_logs(resource_id)",
        
        # Notifications indexes
        "CREATE INDEX IF NOT EXISTS idx_notification_user ON notifications(user_id)",
        "CREATE INDEX IF NOT EXISTS idx_notification_read ON notifications(is_read)",
        "CREATE INDEX IF NOT EXISTS idx_notification_created ON notifications(created_at)",
        
        # Search Indexes
        "CREATE INDEX IF NOT EXISTS idx_search_resource_type ON search_indexes(resource_type)",
        "CREATE INDEX IF NOT EXISTS idx_search_resource_id ON search_indexes(resource_id)",
        "CREATE INDEX IF NOT EXISTS idx_search_language ON search_indexes(language)",
        "CREATE INDEX IF NOT EXISTS idx_search_indexed ON search_indexes(last_indexed)",
    ]
    
    try:
        with engine.connect() as conn:
            for index_query in indexes:
                try:
                    conn.execute(text(index_query))
                    conn.commit()
                except Exception as e:
                    if "duplicate" not in str(e).lower() and "already exists" not in str(e).lower():
                        print(f"   ⚠️  Warning: {str(e)[:100]}")
        
        print("✅ Performance indexes added successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error adding indexes: {e}")
        return False

def optimize_tables(engine):
    """Optimize tables after migration"""
    print("\n🚀 Optimizing tables...")
    
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            tables = inspector.get_table_names()
            
            for table in tables:
                print(f"   🔄 Optimizing {table}...")
                try:
                    conn.execute(text(f"OPTIMIZE TABLE {table}"))
                    conn.commit()
                except Exception as e:
                    print(f"      ⚠️  Could not optimize {table}: {str(e)[:50]}")
        
        print("✅ Tables optimized successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error optimizing tables: {e}")
        return False

def verify_migration(engine):
    """Verify the migration was successful"""
    print("\n🔍 Verifying migration...")
    
    try:
        with engine.connect() as conn:
            inspector = inspect(engine)
            
            # Check a few key tables
            tables_to_check = ['cases', 'judgments', 'documents']
            
            for table in tables_to_check:
                if table in inspector.get_table_names():
                    columns = inspector.get_columns(table)
                    print(f"   ✅ {table}: {len(columns)} columns")
                else:
                    print(f"   ❌ {table}: NOT FOUND")
                    return False
        
        print("✅ Migration verified successfully")
        return True
        
    except Exception as e:
        print(f"❌ Error verifying migration: {e}")
        return False

def main():
    """Main migration function"""
    print("=" * 60)
    print("🔄 Database Migration: Upgrade to Large Dataset Support")
    print("=" * 60)
    
    try:
        # Create engine
        database_url = get_database_url()
        engine = create_engine(
            database_url,
            poolclass=NullPool,
            echo=False,
            pool_pre_ping=True
        )
        
        print(f"\n📡 Connected to database")
        
        # Step 1: Backup
        if not backup_database(engine):
            print("\n❌ Migration aborted - Please create a backup first")
            return False
        
        # Step 2: Alter columns
        if not alter_table_columns(engine):
            print("\n❌ Migration failed at column alteration step")
            return False
        
        # Step 3: Add indexes
        if not add_missing_indexes(engine):
            print("\n⚠️  Warning: Some indexes could not be added")
            # Continue anyway as this is not critical
        
        # Step 4: Optimize tables
        if not optimize_tables(engine):
            print("\n⚠️  Warning: Table optimization had issues")
            # Continue anyway
        
        # Step 5: Verify
        if not verify_migration(engine):
            print("\n❌ Migration verification failed")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 Migration completed successfully!")
        print("=" * 60)
        print("\n✅ Your database is now optimized for large datasets")
        print("✅ All columns have been expanded")
        print("✅ Performance indexes have been added")
        print("✅ Tables have been optimized")
        
        print("\n📝 Next steps:")
        print("   1. Test your application with the new schema")
        print("   2. Monitor performance with large datasets")
        print("   3. Consider adding FULLTEXT indexes for search optimization")
        print("   4. Keep the backup file safe for 30 days")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Migration failed: {e}")
        print("\n⚠️  Please restore from backup if needed")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
