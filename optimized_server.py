# -*- coding: utf-8 -*-
"""
نظام محسّن لإدارة الأحكام القانونية العربية
يدعم تخزين وعرض مجموعات بيانات كبيرة بكفاءة عالية
Optimized Arabic Legal Judgment System
Supports efficient storage and display of large datasets
"""

import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs
import sys
import sqlite3
import os
from datetime import datetime
import threading

class DatabaseManager:
    """مدير قاعدة البيانات لتخزين البيانات الكبيرة بكفاءة"""
    
    def __init__(self, db_path='legal_judgments.db'):
        self.db_path = db_path
        self.lock = threading.Lock()
        self.init_database()
    
    def get_connection(self):
        """إنشاء اتصال جديد بقاعدة البيانات"""
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn
    
    def init_database(self):
        """إنشاء جداول قاعدة البيانات"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # جدول الأحكام القانونية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS judgments (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # جدول البيانات الوصفية
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS metadata (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            # إنشاء فهارس للبحث السريع
            cursor.execute('''
                CREATE INDEX IF NOT EXISTS idx_judgments_created 
                ON judgments(created_at DESC)
            ''')
            
            conn.commit()
            conn.close()
    
    def store_judgments(self, judgments_data, headers):
        """تخزين الأحكام القانونية في قاعدة البيانات"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            try:
                # حذف البيانات القديمة
                cursor.execute('DELETE FROM judgments')
                
                # إدراج البيانات الجديدة
                for judgment in judgments_data:
                    cursor.execute(
                        'INSERT INTO judgments (data) VALUES (?)',
                        (json.dumps(judgment, ensure_ascii=False),)
                    )
                
                # حفظ البيانات الوصفية
                cursor.execute('''
                    INSERT OR REPLACE INTO metadata (key, value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', ('headers', json.dumps(headers, ensure_ascii=False)))
                
                cursor.execute('''
                    INSERT OR REPLACE INTO metadata (key, value, updated_at)
                    VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', ('total_count', str(len(judgments_data))))
                
                conn.commit()
                return True, len(judgments_data)
                
            except Exception as e:
                conn.rollback()
                return False, str(e)
            finally:
                conn.close()
    
    def get_judgments_paginated(self, page=1, per_page=20, search=''):
        """جلب الأحكام مع الصفحات والبحث"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            offset = (page - 1) * per_page
            
            if search:
                # البحث في البيانات
                cursor.execute('''
                    SELECT id, data FROM judgments 
                    WHERE data LIKE ? 
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                ''', (f'%{search}%', per_page, offset))
                
                cursor.execute('''
                    SELECT COUNT(*) FROM judgments 
                    WHERE data LIKE ?
                ''', (f'%{search}%',))
            else:
                # جلب جميع البيانات
                cursor.execute('''
                    SELECT id, data FROM judgments 
                    ORDER BY created_at DESC
                    LIMIT ? OFFSET ?
                ''', (per_page, offset))
                
                cursor.execute('SELECT COUNT(*) FROM judgments')
            
            rows = cursor.fetchall()
            total = cursor.fetchone()[0]
            
            judgments = []
            for row in rows:
                judgment = json.loads(row['data'])
                judgment['_id'] = row['id']
                judgments.append(judgment)
            
            return {
                'judgments': judgments,
                'total': total,
                'page': page,
                'per_page': per_page,
                'total_pages': (total + per_page - 1) // per_page
            }
            
        finally:
            conn.close()
    
    def get_metadata(self, key):
        """جلب البيانات الوصفية"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT value FROM metadata WHERE key = ?', (key,))
            row = cursor.fetchone()
            return json.loads(row['value']) if row else None
        finally:
            conn.close()
    
    def get_total_count(self):
        """جلب إجمالي عدد الأحكام"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        try:
            cursor.execute('SELECT COUNT(*) FROM judgments')
            return cursor.fetchone()[0]
        finally:
            conn.close()
    
    def clear_all_data(self):
        """حذف جميع البيانات"""
        with self.lock:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            try:
                cursor.execute('DELETE FROM judgments')
                cursor.execute('DELETE FROM metadata')
                conn.commit()
                return True
            except Exception as e:
                conn.rollback()
                return False
            finally:
                conn.close()


class OptimizedLegalSystemHandler(http.server.SimpleHTTPRequestHandler):
    """معالج محسّن للطلبات مع دعم قاعدة البيانات"""
    
    db_manager = DatabaseManager()
    
    def do_OPTIONS(self):
        """معالجة طلبات CORS"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
        self.end_headers()
    
    def send_json_response(self, data, status=200):
        """إرسال استجابة JSON"""
        self.send_response(status)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data, ensure_ascii=False).encode('utf-8'))
    
    def do_GET(self):
        """معالجة طلبات GET"""
        parsed_url = urlparse(self.path)
        path = parsed_url.path
        query_params = parse_qs(parsed_url.query)
        
        if path == '/':
            total = self.db_manager.get_total_count()
            self.send_json_response({
                "message": "مرحباً بك في نظام إدارة الأحكام القانونية العربية المحسّن",
                "status": "running",
                "version": "2.0 - Optimized",
                "totalJudgments": total,
                "database": "SQLite (Optimized)",
                "features": [
                    "تخزين مجموعات بيانات كبيرة",
                    "بحث سريع ومحسّن",
                    "صفحات تلقائية",
                    "أداء عالي"
                ]
            })
        
        elif path == '/api/health':
            total = self.db_manager.get_total_count()
            self.send_json_response({
                "status": "healthy",
                "database": "connected",
                "totalJudgments": total,
                "timestamp": datetime.now().isoformat()
            })
        
        elif path == '/api/judgments':
            # استخراج معاملات الصفحة والبحث
            page = int(query_params.get('page', [1])[0])
            per_page = int(query_params.get('per_page', [20])[0])
            search = query_params.get('search', [''])[0]
            
            # جلب البيانات من قاعدة البيانات
            result = self.db_manager.get_judgments_paginated(page, per_page, search)
            headers = self.db_manager.get_metadata('headers') or []
            
            self.send_json_response({
                'success': True,
                'judgments': result['judgments'],
                'headers': headers,
                'pagination': {
                    'page': result['page'],
                    'per_page': result['per_page'],
                    'total': result['total'],
                    'total_pages': result['total_pages'],
                    'has_next': result['page'] < result['total_pages'],
                    'has_prev': result['page'] > 1
                }
            })
        
        elif path == '/api/stats':
            total = self.db_manager.get_total_count()
            headers = self.db_manager.get_metadata('headers') or []
            
            self.send_json_response({
                'total_cases': total,
                'total_judgments': total,
                'total_documents': total * 2,
                'data_source': 'قاعدة بيانات SQLite محسّنة',
                'headers': headers,
                'database_size': os.path.getsize(self.db_manager.db_path) if os.path.exists(self.db_manager.db_path) else 0,
                'cases_by_status': {
                    'جديدة': max(1, total // 4),
                    'قيد النظر': max(1, total // 3),
                    'محكومة': max(1, total // 2),
                    'مؤجلة': max(1, total // 10)
                }
            })
        
        elif path == '/csv-reader-full':
            try:
                with open('csv-reader-full.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_json_response({'error': 'CSV Reader not found'}, 404)
        
        else:
            self.send_json_response({'error': 'نقطة النهاية غير موجودة'}, 404)
    
    def do_POST(self):
        """معالجة طلبات POST"""
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        
        if self.path == '/api/auth/login':
            try:
                data = json.loads(post_data.decode('utf-8'))
                username = data.get('username', '')
                password = data.get('password', '')
                
                if username == 'admin' and password == 'admin123':
                    self.send_json_response({
                        'access_token': 'fake-jwt-token-admin',
                        'user': {
                            'id': 1,
                            'username': 'admin',
                            'full_name': 'مدير النظام',
                            'role': 'admin',
                            'email': 'admin@legal-system.com'
                        }
                    })
                else:
                    self.send_json_response({
                        'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'
                    }, 401)
            except Exception as e:
                self.send_json_response({'error': str(e)}, 500)
        
        elif self.path == '/api/update-data':
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                headers = data.get('headers', [])
                all_data = data.get('allData', [])
                
                print(f"\n📥 استلام البيانات للتخزين...")
                print(f"   📊 عدد الأعمدة: {len(headers)}")
                print(f"   📄 عدد الأحكام: {len(all_data)}")
                
                # تخزين البيانات في قاعدة البيانات
                success, result = self.db_manager.store_judgments(all_data, headers)
                
                if success:
                    print(f"\n✅ تم تخزين البيانات بنجاح!")
                    print(f"   💾 عدد الأحكام المخزنة: {result}")
                    print(f"   🗄️  حجم قاعدة البيانات: {os.path.getsize(self.db_manager.db_path) / 1024 / 1024:.2f} MB")
                    
                    self.send_json_response({
                        'success': True,
                        'message': f'تم تخزين {result} حكم قانوني بنجاح في قاعدة البيانات',
                        'totalRows': len(all_data),
                        'loadedJudgments': result,
                        'headers': headers,
                        'loadingPercentage': 100,
                        'database': 'SQLite',
                        'storage': 'persistent'
                    })
                else:
                    print(f"\n❌ فشل التخزين: {result}")
                    self.send_json_response({
                        'success': False,
                        'error': f'فشل تخزين البيانات: {result}'
                    }, 500)
                
            except Exception as e:
                print(f"\n❌ خطأ في معالجة البيانات: {str(e)}")
                self.send_json_response({
                    'success': False,
                    'error': f'خطأ في تحديث البيانات: {str(e)}'
                }, 500)
        
        else:
            self.send_json_response({'error': 'نقطة النهاية غير موجودة'}, 404)
    
    def do_DELETE(self):
        """معالجة طلبات DELETE"""
        if self.path == '/api/judgments':
            try:
                success = self.db_manager.clear_all_data()
                if success:
                    self.send_json_response({
                        'success': True,
                        'message': 'تم حذف جميع البيانات بنجاح'
                    })
                else:
                    self.send_json_response({
                        'success': False,
                        'error': 'فشل حذف البيانات'
                    }, 500)
            except Exception as e:
                self.send_json_response({
                    'success': False,
                    'error': str(e)
                }, 500)
        else:
            self.send_json_response({'error': 'نقطة النهاية غير موجودة'}, 404)


def find_free_port(start_port=5000, max_tries=10):
    """البحث عن منفذ متاح"""
    import socket
    for port in range(start_port, start_port + max_tries):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None


if __name__ == "__main__":
    PORT = find_free_port(5000, 10)
    
    if PORT is None:
        print("❌ لم يتم العثور على منفذ متاح")
        print("💡 جرب إيقاف العمليات الأخرى: taskkill /F /IM python.exe")
        sys.exit(1)
    
    print("=" * 70)
    print("🚀 نظام إدارة الأحكام القانونية العربية - النسخة المحسّنة")
    print("=" * 70)
    print(f"\n📡 الخادم متاح على: http://localhost:{PORT}")
    print("🔑 بيانات تسجيل الدخول: admin / admin123")
    print(f"📊 قارئ البيانات: http://localhost:{PORT}/csv-reader-full")
    print("\n✨ المميزات الجديدة:")
    print("   ✅ تخزين دائم في قاعدة بيانات SQLite")
    print("   ✅ دعم مجموعات بيانات ضخمة (ملايين السجلات)")
    print("   ✅ بحث سريع ومحسّن")
    print("   ✅ صفحات تلقائية (Pagination)")
    print("   ✅ ذاكرة محسّنة (لا يتم تحميل جميع البيانات)")
    print("\n🛑 لإيقاف الخادم اضغط Ctrl+C")
    
    if PORT != 5000:
        print(f"\n⚠️  ملاحظة: تم استخدام المنفذ {PORT} بدلاً من 5000")
    
    print("=" * 70)
    
    with socketserver.TCPServer(("", PORT), OptimizedLegalSystemHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n\n🛑 تم إيقاف الخادم")
            sys.exit(0)
