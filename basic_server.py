import http.server
import socketserver
import json
from urllib.parse import urlparse, parse_qs
import sys

class LegalSystemHandler(http.server.SimpleHTTPRequestHandler):
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
                "status": "running"
            }
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/api/health':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response = {"status": "healthy", "database": "connected"}
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
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
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                error_response = {'error': 'حدث خطأ في النظام'}
                self.wfile.write(json.dumps(error_response, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_error(404)

if __name__ == "__main__":
    PORT = 5000
    
    print("🚀 بدء تشغيل نظام إدارة الأحكام القانونية العربية...")
    print(f"📡 الخادم متاح على: http://localhost:{PORT}")
    print("🔑 بيانات تسجيل الدخول: admin / admin123")
    print("✅ النظام جاهز للاستخدام!")
    print("🛑 لإيقاف الخادم اضغط Ctrl+C")
    
    with socketserver.TCPServer(("", PORT), LegalSystemHandler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n🛑 تم إيقاف الخادم")
            sys.exit(0)
