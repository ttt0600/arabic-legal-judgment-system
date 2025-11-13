from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

# User Model
class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(50), default='user')  # admin, judge, lawyer, user
    department = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    created_cases = db.relationship('Case', backref='creator', lazy=True, foreign_keys='Case.created_by')
    created_judgments = db.relationship('Judgment', backref='creator', lazy=True, foreign_keys='Judgment.created_by')
    uploaded_documents = db.relationship('Document', backref='uploader', lazy=True, foreign_keys='Document.uploaded_by')

# Category Model
class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    color = db.Column(db.String(7), default='#007bff')  # Hex color code
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Self-referential relationship for subcategories
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]))
    
    # Relationship with cases
    cases = db.relationship('Case', backref='category', lazy=True)

# Court Model
class Court(db.Model):
    __tablename__ = 'courts'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(200))
    court_type = db.Column(db.String(50))  # محكمة ابتدائية، استئناف، نقض، إدارية
    jurisdiction = db.Column(db.String(100))  # الاختصاص
    address = db.Column(db.Text)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    cases = db.relationship('Case', backref='court', lazy=True)
    judgments = db.relationship('Judgment', backref='court', lazy=True)

# Case Model
class Case(db.Model):
    __tablename__ = 'cases'
    
    id = db.Column(db.Integer, primary_key=True)
    case_number = db.Column(db.String(50), unique=True, nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    
    # Case details
    plaintiff = db.Column(db.String(200))  # المدعي
    defendant = db.Column(db.String(200))  # المدعى عليه
    case_date = db.Column(db.DateTime)
    filing_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Status and priority
    status = db.Column(db.String(50), default='جديدة')  # جديدة، قيد النظر، محكومة، مؤجلة، مغلقة
    priority = db.Column(db.String(20), default='متوسط')  # عاجل، عالي، متوسط، منخفض
    
    # Legal details
    case_type = db.Column(db.String(100))  # نوع القضية
    legal_basis = db.Column(db.Text)  # الأساس القانوني
    claimed_amount = db.Column(db.Decimal(15, 2))  # المبلغ المطالب به
    
    # Administrative
    lawyer_name = db.Column(db.String(150))
    lawyer_license = db.Column(db.String(50))
    fees = db.Column(db.Decimal(10, 2))
    notes = db.Column(db.Text)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    judgments = db.relationship('Judgment', backref='case', lazy=True, cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='case', lazy=True, cascade='all, delete-orphan')
    case_sessions = db.relationship('CaseSession', backref='case', lazy=True, cascade='all, delete-orphan')

# Judgment Model
class Judgment(db.Model):
    __tablename__ = 'judgments'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    
    # Judgment details
    judgment_type = db.Column(db.String(50), nullable=False)  # حكم، قرار، أمر
    judgment_date = db.Column(db.DateTime)
    judge_name = db.Column(db.String(150))
    court_level = db.Column(db.String(50))  # ابتدائية، استئناف، نقض
    
    # Status and appeal
    status = db.Column(db.String(50), default='نهائي')  # نهائي، قابل للاستئناف، مستأنف
    appeal_status = db.Column(db.String(50))  # لم يستأنف، مستأنف، مؤيد، منقوض
    appeal_deadline = db.Column(db.DateTime)
    
    # Financial details
    judgment_amount = db.Column(db.Decimal(15, 2))
    fees_awarded = db.Column(db.Decimal(10, 2))
    execution_status = db.Column(db.String(50))  # لم ينفذ، قيد التنفيذ، منفذ
    
    # Legal citations
    legal_articles = db.Column(db.Text)  # المواد القانونية المستشهد بها
    precedents = db.Column(db.Text)  # السوابق القضائية
    
    # Administrative
    notes = db.Column(db.Text)
    keywords = db.Column(db.Text)  # كلمات مفتاحية للبحث
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # Relationships
    documents = db.relationship('Document', backref='judgment', lazy=True)

# Document Model
class Document(db.Model):
    __tablename__ = 'documents'
    
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer)
    mime_type = db.Column(db.String(100))
    
    # Document metadata
    document_type = db.Column(db.String(50))  # عريضة، حكم، مرافعة، مستند
    description = db.Column(db.Text)
    version = db.Column(db.Integer, default=1)
    is_confidential = db.Column(db.Boolean, default=False)
    
    # OCR and search
    extracted_text = db.Column(db.Text)  # النص المستخرج من المستند
    ocr_confidence = db.Column(db.Float)
    is_searchable = db.Column(db.Boolean, default=False)
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_accessed = db.Column(db.DateTime)
    
    # Foreign Keys
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'))
    judgment_id = db.Column(db.Integer, db.ForeignKey('judgments.id'))
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'))

# Case Session Model (جلسات المحكمة)
class CaseSession(db.Model):
    __tablename__ = 'case_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_date = db.Column(db.DateTime, nullable=False)
    session_time = db.Column(db.Time)
    session_type = db.Column(db.String(50))  # جلسة نظر، جلسة حكم، جلسة مرافعة
    
    # Session details
    judge_name = db.Column(db.String(150))
    court_room = db.Column(db.String(50))
    agenda = db.Column(db.Text)
    minutes = db.Column(db.Text)  # محضر الجلسة
    
    # Attendance
    plaintiff_present = db.Column(db.Boolean)
    defendant_present = db.Column(db.Boolean)
    plaintiff_lawyer = db.Column(db.String(150))
    defendant_lawyer = db.Column(db.String(150))
    
    # Status
    status = db.Column(db.String(50), default='مجدولة')  # مجدولة، منعقدة، مؤجلة، ملغية
    postponement_reason = db.Column(db.Text)
    next_session_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False)

# Legal Article Model (المواد القانونية)
class LegalArticle(db.Model):
    __tablename__ = 'legal_articles'
    
    id = db.Column(db.Integer, primary_key=True)
    article_number = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(200))
    content = db.Column(db.Text, nullable=False)
    
    # Legal source
    law_name = db.Column(db.String(200), nullable=False)  # اسم القانون
    law_number = db.Column(db.String(50))
    law_year = db.Column(db.Integer)
    chapter = db.Column(db.String(100))  # الباب/الفصل
    section = db.Column(db.String(100))  # القسم
    
    # Status
    is_active = db.Column(db.Boolean, default=True)
    effective_date = db.Column(db.DateTime)
    amendment_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Legal Precedent Model (السوابق القضائية)
class LegalPrecedent(db.Model):
    __tablename__ = 'legal_precedents'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    summary = db.Column(db.Text)
    full_text = db.Column(db.Text)
    
    # Court details
    court_name = db.Column(db.String(150))
    court_level = db.Column(db.String(50))
    decision_date = db.Column(db.DateTime)
    case_reference = db.Column(db.String(100))
    
    # Legal principle
    legal_principle = db.Column(db.Text)  # المبدأ القانوني
    keywords = db.Column(db.Text)
    
    # Citations and references
    cited_articles = db.Column(db.Text)
    citation_count = db.Column(db.Integer, default=0)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# System Settings Model
class SystemSetting(db.Model):
    __tablename__ = 'system_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(100), unique=True, nullable=False)
    value = db.Column(db.Text)
    description = db.Column(db.Text)
    data_type = db.Column(db.String(20), default='string')  # string, integer, boolean, json
    category = db.Column(db.String(50))
    is_public = db.Column(db.Boolean, default=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Audit Log Model
class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    action = db.Column(db.String(100), nullable=False)
    resource_type = db.Column(db.String(50))  # case, judgment, document, user
    resource_id = db.Column(db.Integer)
    old_values = db.Column(db.Text)  # JSON string
    new_values = db.Column(db.Text)  # JSON string
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='audit_logs')

# Notification Model
class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    notification_type = db.Column(db.String(50), default='info')  # info, warning, error, success
    
    # Related resource
    resource_type = db.Column(db.String(50))
    resource_id = db.Column(db.Integer)
    
    # Status
    is_read = db.Column(db.Boolean, default=False)
    read_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationship
    user = db.relationship('User', backref='notifications')

# Search Index Model (for better search performance)
class SearchIndex(db.Model):
    __tablename__ = 'search_indexes'
    
    id = db.Column(db.Integer, primary_key=True)
    resource_type = db.Column(db.String(50), nullable=False)  # case, judgment, document
    resource_id = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)
    normalized_content = db.Column(db.Text)  # Normalized Arabic text
    keywords = db.Column(db.Text)
    
    # Search metadata
    language = db.Column(db.String(10), default='ar')
    last_indexed = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Create composite index for better search performance
    __table_args__ = (
        db.Index('idx_resource_type_id', 'resource_type', 'resource_id'),
        db.Index('idx_content_search', 'normalized_content'),
    )
