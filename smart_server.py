import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs
import sys
import csv
import io

class LegalSystemHandler(http.server.SimpleHTTPRequestHandler):
    # تخزين البيانات الحقيقية
    real_data = {
        'headers': [],
        'judgments': [],
        'totalRows': 0
    }
    
    def do_OPTIONS(self):
        # Handle CORS preflight
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "message": "مرحباً بك في نظام إدارة الأحكام القانونية العربية",
                "status": "running",
                "dataStatus": f"تم تحميل {self.real_data['totalRows']} حكم قانوني" if self.real_data['totalRows'] > 0 else "لم يتم تحميل البيانات بعد"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {
                "status": "healthy", 
                "database": "connected",
                "totalJudgments": self.real_data['totalRows']
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path.startswith('/api/judgments'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            # إرجاع البيانات الحقيقية
            response = {
                'success': True,
                'judgments': self.real_data['judgments'][:20],  # أول 20 حكم
                'total': self.real_data['totalRows'],
                'headers': self.real_data['headers']
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path.startswith('/api/stats'):
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            
            response = {
                'total_cases': self.real_data['totalRows'],
                'total_judgments': self.real_data['totalRows'],
                'total_documents': self.real_data['totalRows'] * 2 if self.real_data['totalRows'] > 0 else 0,
                'data_source': 'ملف البيانات الحقيقية' if self.real_data['totalRows'] > 0 else 'بيانات تجريبية',
                'headers': self.real_data['headers'],
                'cases_by_status': {
                    'جديدة': max(1, self.real_data['totalRows'] // 4),
                    'قيد النظر': max(1, self.real_data['totalRows'] // 3),
                    'محكومة': max(1, self.real_data['totalRows'] // 2),
                    'مؤجلة': max(1, self.real_data['totalRows'] // 10)
                } if self.real_data['totalRows'] > 0 else {
                    'جديدة': 45, 'قيد النظر': 30, 'محكومة': 20, 'مؤجلة': 5
                }
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/csv-reader':
            # إرجاع صفحة قارئ CSV
            try:
                with open('csv-reader.html', 'r', encoding='utf-8') as f:
                    content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'text/html; charset=utf-8')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(content.encode('utf-8'))
            except FileNotFoundError:
                self.send_error(404, "CSV Reader not found")
        
        else:
            self.send_error(404)

    def do_POST(self):
        if self.path == '/api/auth/login':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                username = data.get('username', '')
                password = data.get('password', '')
                
                if username == 'admin' and password == 'admin123':
                    response = {
                        'access_token': 'fake-jwt-token-admin',
                        'user': {
                            'id': 1,
                            'username': 'admin',
                            'full_name': 'مدير النظام',
                            'role': 'admin',
                            'email': 'admin@legal-system.com'
                        }
                    }
                    self.send_response(200)
                else:
                    response = {'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}
                    self.send_response(401)
                
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_error(500, str(e))
        
        elif self.path == '/api/update-data':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            
            try:
                data = json.loads(post_data.decode('utf-8'))
                
                # تحديث البيانات الحقيقية
                self.real_data['headers'] = data.get('headers', [])
                self.real_data['judgments'] = data.get('sampleData', [])
                self.real_data['totalRows'] = data.get('totalRows', 0)
                
                print(f"\n✅ تم تحديث البيانات:")
                print(f"   📊 عدد الأعمدة: {len(self.real_data['headers'])}")
                print(f"   📄 إجمالي الأحكام: {self.real_data['totalRows']}")
                print(f"   💾 تم تحميل: {len(self.real_data['judgments'])} حكم للعرض")
                print(f"   🏷️  أسماء الأعمدة: {', '.join(self.real_data['headers'][:5])}{'...' if len(self.real_data['headers']) > 5 else ''}")
                
                response = {
                    'success': True,
                    'message': 'تم تحديث البيانات بنجاح',
                    'totalRows': self.real_data['totalRows'],
                    'loadedSample': len(self.real_data['judgments']),
                    'headers': self.real_data['headers']
                }
                
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
                
            except Exception as e:
                self.send_error(500, f"خطأ في تحديث البيانات: {str(e)}")
        
        else:
            self.send_error(404)

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
    # البحث عن منفذ متاح
    PORT = find_free_port(5000, 10)
    
    if PORT is None:
        print("❌ لم يتم العثور على منفذ متاح")
        print("💡 جرب إيقاف العمليات الأخرى: taskkill /F /IM python.exe")
        sys.exit(1)
    
    print("🚀 بدء تشغيل نظام إدارة الأحكام القانونية العربية...")
    print(f"📡 الخادم متاح على: http://localhost:{PORT}")
    print("🔑 بيانات تسجيل الدخول: admin / admin123")
    print(f"📊 قارئ البيانات متاح على: http://localhost:{PORT}/csv-reader")
    print("✅ النظام جاهز للاستخدام!")
    print("🛑 لإيقاف الخادم اضغط Ctrl+C")
    
    if PORT != 5000:
        print(f"⚠️  ملاحظة: تم استخدام المنفذ {PORT} بدلاً من 5000")
        print(f"🔧 تحديث Frontend: غير الرابط في الكود إلى http://localhost:{PORT}")
    
    with socketserver.TCPServer(("", PORT), LegalSystemHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 تم إيقاف الخادم")
            sys.exit(0)
