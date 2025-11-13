from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_cors import CORS
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime, timedelta
import arabic_reshaper
from bidi.algorithm import get_display
import json
import uuid

# Initialize Flask app
app = Flask(__name__)
app.config.from_object('config.Config')

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)
CORS(app)

# Import models after db initialization
from models import User, Case, Judgment, Document, Category, Court

# Arabic text processing helper functions
def process_arabic_text(text):
    """Process Arabic text for proper display"""
    if not text:
        return ""
    reshaped_text = arabic_reshaper.reshape(text)
    bidi_text = get_display(reshaped_text)
    return bidi_text

def normalize_arabic_text(text):
    """Normalize Arabic text for search"""
    if not text:
        return ""
    # Remove diacritics and normalize characters
    normalizations = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا',
        'ة': 'ه',
        'ى': 'ي'
    }
    
    normalized = text
    for old, new in normalizations.items():
        normalized = normalized.replace(old, new)
    
    return normalized.strip()

# Authentication Routes
@app.route('/api/auth/register', methods=['POST'])
def register():
    """User registration"""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['username', 'email', 'password', 'full_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'حقل {field} مطلوب'}), 400
        
        # Check if user already exists
        if User.query.filter_by(username=data['username']).first():
            return jsonify({'error': 'اسم المستخدم موجود بالفعل'}), 400
        
        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'البريد الإلكتروني مسجل بالفعل'}), 400
        
        # Create new user
        user = User(
            username=data['username'],
            email=data['email'],
            password_hash=generate_password_hash(data['password']),
            full_name=data['full_name'],
            role=data.get('role', 'user'),
            phone=data.get('phone'),
            department=data.get('department')
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء الحساب بنجاح',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'full_name': user.full_name,
                'role': user.role
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في النظام'}), 500

@app.route('/api/auth/login', methods=['POST'])
def login():
    """User login"""
    try:
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'error': 'اسم المستخدم وكلمة المرور مطلوبان'}), 400
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            # Update last login
            user.last_login = datetime.utcnow()
            db.session.commit()
            
            # Create access token
            access_token = create_access_token(
                identity=user.id,
                expires_delta=timedelta(days=1)
            )
            
            return jsonify({
                'access_token': access_token,
                'user': {
                    'id': user.id,
                    'username': user.username,
                    'email': user.email,
                    'full_name': user.full_name,
                    'role': user.role,
                    'last_login': user.last_login.isoformat() if user.last_login else None
                }
            }), 200
        
        return jsonify({'error': 'اسم المستخدم أو كلمة المرور غير صحيحة'}), 401
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في النظام'}), 500

# Case Management Routes
@app.route('/api/cases', methods=['GET'])
@jwt_required()
def get_cases():
    """Get list of cases with pagination and filtering"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        search = request.args.get('search', '')
        category_id = request.args.get('category_id', type=int)
        status = request.args.get('status')
        court_id = request.args.get('court_id', type=int)
        
        # Build query
        query = Case.query
        
        # Apply filters
        if search:
            normalized_search = normalize_arabic_text(search)
            query = query.filter(
                Case.title.contains(search) |
                Case.description.contains(search) |
                Case.case_number.contains(search)
            )
        
        if category_id:
            query = query.filter(Case.category_id == category_id)
        
        if status:
            query = query.filter(Case.status == status)
        
        if court_id:
            query = query.filter(Case.court_id == court_id)
        
        # Order by creation date
        query = query.order_by(Case.created_at.desc())
        
        # Paginate
        cases = query.paginate(
            page=page,
            per_page=per_page,
            error_out=False
        )
        
        return jsonify({
            'cases': [{
                'id': case.id,
                'case_number': case.case_number,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'priority': case.priority,
                'created_at': case.created_at.isoformat(),
                'updated_at': case.updated_at.isoformat(),
                'category': {
                    'id': case.category.id,
                    'name': case.category.name
                } if case.category else None,
                'court': {
                    'id': case.court.id,
                    'name': case.court.name
                } if case.court else None,
                'judgment_count': len(case.judgments)
            } for case in cases.items],
            'pagination': {
                'page': cases.page,
                'pages': cases.pages,
                'per_page': cases.per_page,
                'total': cases.total,
                'has_next': cases.has_next,
                'has_prev': cases.has_prev
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في جلب القضايا'}), 500

@app.route('/api/cases', methods=['POST'])
@jwt_required()
def create_case():
    """Create a new case"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'description', 'category_id']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'حقل {field} مطلوب'}), 400
        
        # Generate case number
        case_number = f"CASE-{datetime.utcnow().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
        
        # Create new case
        case = Case(
            case_number=case_number,
            title=data['title'],
            description=data['description'],
            category_id=data['category_id'],
            court_id=data.get('court_id'),
            status=data.get('status', 'جديدة'),
            priority=data.get('priority', 'متوسط'),
            plaintiff=data.get('plaintiff'),
            defendant=data.get('defendant'),
            case_date=datetime.fromisoformat(data['case_date']) if data.get('case_date') else None,
            created_by=current_user_id
        )
        
        db.session.add(case)
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء القضية بنجاح',
            'case': {
                'id': case.id,
                'case_number': case.case_number,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'priority': case.priority,
                'created_at': case.created_at.isoformat()
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في إنشاء القضية'}), 500

@app.route('/api/cases/<int:case_id>', methods=['GET'])
@jwt_required()
def get_case_details(case_id):
    """Get detailed information about a specific case"""
    try:
        case = Case.query.get_or_404(case_id)
        
        return jsonify({
            'case': {
                'id': case.id,
                'case_number': case.case_number,
                'title': case.title,
                'description': case.description,
                'status': case.status,
                'priority': case.priority,
                'plaintiff': case.plaintiff,
                'defendant': case.defendant,
                'case_date': case.case_date.isoformat() if case.case_date else None,
                'created_at': case.created_at.isoformat(),
                'updated_at': case.updated_at.isoformat(),
                'category': {
                    'id': case.category.id,
                    'name': case.category.name,
                    'description': case.category.description
                } if case.category else None,
                'court': {
                    'id': case.court.id,
                    'name': case.court.name,
                    'location': case.court.location
                } if case.court else None,
                'judgments': [{
                    'id': judgment.id,
                    'title': judgment.title,
                    'judgment_type': judgment.judgment_type,
                    'judgment_date': judgment.judgment_date.isoformat() if judgment.judgment_date else None,
                    'status': judgment.status
                } for judgment in case.judgments],
                'documents': [{
                    'id': doc.id,
                    'filename': doc.filename,
                    'document_type': doc.document_type,
                    'uploaded_at': doc.uploaded_at.isoformat()
                } for doc in case.documents]
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في جلب تفاصيل القضية'}), 500

# Judgment Routes
@app.route('/api/judgments', methods=['POST'])
@jwt_required()
def create_judgment():
    """Create a new judgment"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['case_id', 'title', 'content', 'judgment_type']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'حقل {field} مطلوب'}), 400
        
        # Create new judgment
        judgment = Judgment(
            case_id=data['case_id'],
            title=data['title'],
            content=data['content'],
            judgment_type=data['judgment_type'],
            judgment_date=datetime.fromisoformat(data['judgment_date']) if data.get('judgment_date') else datetime.utcnow(),
            judge_name=data.get('judge_name'),
            court_level=data.get('court_level'),
            status=data.get('status', 'نهائي'),
            appeal_status=data.get('appeal_status'),
            notes=data.get('notes'),
            created_by=current_user_id
        )
        
        db.session.add(judgment)
        db.session.commit()
        
        return jsonify({
            'message': 'تم إنشاء الحكم بنجاح',
            'judgment': {
                'id': judgment.id,
                'title': judgment.title,
                'judgment_type': judgment.judgment_type,
                'judgment_date': judgment.judgment_date.isoformat(),
                'status': judgment.status
            }
        }), 201
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في إنشاء الحكم'}), 500

# Category and Court Management
@app.route('/api/categories', methods=['GET'])
@jwt_required()
def get_categories():
    """Get list of case categories"""
    try:
        categories = Category.query.filter_by(is_active=True).all()
        return jsonify({
            'categories': [{
                'id': cat.id,
                'name': cat.name,
                'description': cat.description,
                'case_count': len(cat.cases)
            } for cat in categories]
        }), 200
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في جلب الفئات'}), 500

@app.route('/api/courts', methods=['GET'])
@jwt_required()
def get_courts():
    """Get list of courts"""
    try:
        courts = Court.query.filter_by(is_active=True).all()
        return jsonify({
            'courts': [{
                'id': court.id,
                'name': court.name,
                'location': court.location,
                'court_type': court.court_type,
                'case_count': len(court.cases)
            } for court in courts]
        }), 200
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في جلب المحاكم'}), 500

# Search functionality
@app.route('/api/search', methods=['GET'])
@jwt_required()
def search_system():
    """Advanced search across cases and judgments"""
    try:
        query = request.args.get('q', '')
        search_type = request.args.get('type', 'all')  # all, cases, judgments
        
        if not query:
            return jsonify({'error': 'استعلام البحث مطلوب'}), 400
        
        normalized_query = normalize_arabic_text(query)
        results = {'cases': [], 'judgments': []}
        
        if search_type in ['all', 'cases']:
            # Search cases
            cases = Case.query.filter(
                Case.title.contains(query) |
                Case.description.contains(query) |
                Case.case_number.contains(query) |
                Case.plaintiff.contains(query) |
                Case.defendant.contains(query)
            ).limit(10).all()
            
            results['cases'] = [{
                'id': case.id,
                'case_number': case.case_number,
                'title': case.title,
                'description': case.description[:200] + '...' if len(case.description) > 200 else case.description,
                'type': 'case'
            } for case in cases]
        
        if search_type in ['all', 'judgments']:
            # Search judgments
            judgments = Judgment.query.filter(
                Judgment.title.contains(query) |
                Judgment.content.contains(query) |
                Judgment.judge_name.contains(query)
            ).limit(10).all()
            
            results['judgments'] = [{
                'id': judgment.id,
                'title': judgment.title,
                'content': judgment.content[:200] + '...' if len(judgment.content) > 200 else judgment.content,
                'judgment_type': judgment.judgment_type,
                'case_id': judgment.case_id,
                'type': 'judgment'
            } for judgment in judgments]
        
        return jsonify(results), 200
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في البحث'}), 500

# Statistics and Analytics
@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_statistics():
    """Get system statistics"""
    try:
        stats = {
            'total_cases': Case.query.count(),
            'total_judgments': Judgment.query.count(),
            'total_documents': Document.query.count(),
            'cases_by_status': {},
            'judgments_by_type': {},
            'recent_cases': []
        }
        
        # Cases by status
        status_counts = db.session.query(
            Case.status, db.func.count(Case.id)
        ).group_by(Case.status).all()
        stats['cases_by_status'] = {status: count for status, count in status_counts}
        
        # Judgments by type
        type_counts = db.session.query(
            Judgment.judgment_type, db.func.count(Judgment.id)
        ).group_by(Judgment.judgment_type).all()
        stats['judgments_by_type'] = {j_type: count for j_type, count in type_counts}
        
        # Recent cases (last 5)
        recent_cases = Case.query.order_by(Case.created_at.desc()).limit(5).all()
        stats['recent_cases'] = [{
            'id': case.id,
            'case_number': case.case_number,
            'title': case.title,
            'status': case.status,
            'created_at': case.created_at.isoformat()
        } for case in recent_cases]
        
        return jsonify(stats), 200
        
    except Exception as e:
        return jsonify({'error': 'حدث خطأ في جلب الإحصائيات'}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    
    app.run(debug=True, host='0.0.0.0', port=5000)
