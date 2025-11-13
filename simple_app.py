from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime

# إنشاء تطبيق Flask بسيط
app = Flask(__name__)
CORS(app)

# بيانات تجريبية
users = {
    "admin": {
        "id": 1,
        "username": "admin",
        "password": "admin123",  # في التطبيق الحقيقي، يجب تشفير كلمة المرور
        "full_name": "مدير النظام",
        "role": "admin",
        "email": "admin@legal-system.com"
    }
}

cases_data = [
    {
        "id": 1,
        "case_number": "CASE-20240101-ABC12345",
        "title": "قضية تعويض أضرار حادث مروري",
        "description": "دعوى تعويض عن الأضرار الناتجة عن حادث مروري",
        "status": "قيد النظر",
        "priority": "عالي",
        "plaintiff": "أحمد محمد العبدالله",
        "defendant": "شركة التأمين الوطنية",
        "created_at": "2024-01-01T10:00:00Z"
    },
    {
        "id": 2,
        "case_number": "CASE-20240102-DEF67890", 
        "title": "نزاع تجاري حول عقد توريد",
        "description": "نزاع بين شركة المقاولات والشركة الموردة",
        "status": "جديدة",
        "priority": "متوسط",
        "plaintiff": "شركة البناء المتقدم المحدودة",
        "defendant": "مؤسسة التوريد الشامل",
        "created_at": "2024-01-02T09:30:00Z"
    }
]

@app.route('/')
def home():
    return jsonify({
        "message": "مرحباً بك في نظام إدارة الأحكام القانونية العربية",
        "status": "running",
        "version": "1.0.0"
    })

@app.route('/api/health')
def health_check():
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "database": "connected",
        "arabic_support": "enabled"
    })

@app.route('/api/auth/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
        
        user = users.get(username)
        if user and user['password'] == password:
            # في التطبيق الحقيقي، نستخدم JWT token
            return jsonify({
                'access_token': 'fake-jwt-token-' + username,
                'user': {
                    'id': user['id'],
                    'username': user['username'],
                    'full_name': user['full_name'],
                    'role': user['role'],
                    'email': user['email']
                }
            }), 200
        
        return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في النظام'}), 500

@app.route('/api/cases', methods=['GET'])
def get_cases():
    try:
        # في التطبيق الحقيقي، نجلب البيانات من قاعدة البيانات
        return jsonify({
            'success': True,
            'cases': cases_data,
            'pagination': {
                'page': 1,
                'pages': 1,
                'per_page': 20,
                'total': len(cases_data)
            }
        }), 200
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في جلب القضايا'}), 500

@app.route('/api/stats', methods=['GET'])
def get_stats():
    try:
        return jsonify({
            'total_cases': len(cases_data),
            'total_judgments': 89,
            'total_documents': 156,
            'cases_by_status': {
                'جديدة': 45,
                'قيد النظر': 30,
                'محكومة': 20,
                'مؤجلة': 5
            },
            'recent_cases': cases_data[:3]
        }), 200
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في جلب الإحصائيات'}), 500

@app.route('/api/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q', '')
        if not query:
            return jsonify({'error': 'استعلام البحث مطلوب'}), 400
        
        # بحث بسيط في البيانات التجريبية
        results = []
        for case in cases_data:
            if (query.lower() in case['title'].lower() or 
                query.lower() in case['description'].lower()):
                results.append(case)
        
        return jsonify({
            'success': True,
            'cases': results,
            'judgments': []
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في البحث'}), 500

if __name__ == '__main__':
    print("🚀 بدء تشغيل نظام إدارة الأحكام القانونية العربية...")
    print("📡 الخادم متاح على: http://localhost:5000")
    print("🔑 بيانات تسجيل الدخول: admin / admin123")
    print("✅ النظام جاهز للاستخدام!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
