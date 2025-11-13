from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

# User Model - Optimized for large datasets
class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        db.Index('idx_username', 'username'),
        db.Index('idx_email', 'email'),
        db.Index('idx_role', 'role'),
        db.Index('idx_is_active', 'is_active'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    full_name = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(30))
    role = db.Column(db.String(50), default='user', index=True)
    department = db.Column(db.String(150))
    is_active = db.Column(db.Boolean, default=True, index=True)
    last_login = db.Column(db.DateTime, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships with lazy loading
    created_cases = db.relationship('Case', backref='creator', lazy='dynamic', foreign_keys='Case.created_by')
    created_judgments = db.relationship('Judgment', backref='creator', lazy='dynamic', foreign_keys='Judgment.created_by')
    uploaded_documents = db.relationship('Document', backref='uploader', lazy='dynamic', foreign_keys='Document.uploaded_by')

# Category Model - Optimized
class Category(db.Model):
    __tablename__ = 'categories'
    __table_args__ = (
        db.Index('idx_category_name', 'name'),
        db.Index('idx_category_active', 'is_active'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text(5000))  # Increased size
    parent_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True)
    color = db.Column(db.String(10), default='#007bff')
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    children = db.relationship('Category', backref=db.backref('parent', remote_side=[id]), lazy='dynamic')
    cases = db.relationship('Case', backref='category', lazy='dynamic')

# Court Model - Optimized
class Court(db.Model):
    __tablename__ = 'courts'
    __table_args__ = (
        db.Index('idx_court_name', 'name'),
        db.Index('idx_court_type', 'court_type'),
        db.Index('idx_court_active', 'is_active'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(250), nullable=False)
    location = db.Column(db.String(300))
    court_type = db.Column(db.String(100), index=True)
    jurisdiction = db.Column(db.String(200))
    address = db.Column(db.Text(2000))
    phone = db.Column(db.String(30))
    email = db.Column(db.String(150))
    is_active = db.Column(db.Boolean, default=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    cases = db.relationship('Case', backref='court', lazy='dynamic')
    judgments = db.relationship('Judgment', backref='court', lazy='dynamic')

# Case Model - Optimized for large datasets
class Case(db.Model):
    __tablename__ = 'cases'
    __table_args__ = (
        db.Index('idx_case_number', 'case_number'),
        db.Index('idx_case_status', 'status'),
        db.Index('idx_case_priority', 'priority'),
        db.Index('idx_case_date', 'case_date'),
        db.Index('idx_case_category', 'category_id'),
        db.Index('idx_case_court', 'court_id'),
        db.Index('idx_case_created', 'created_at'),
        db.Index('idx_case_plaintiff', 'plaintiff'),
        db.Index('idx_case_defendant', 'defendant'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    case_number = db.Column(db.String(100), unique=True, nullable=False, index=True)
    title = db.Column(db.String(500), nullable=False)
    description = db.Column(db.Text(50000))  # Increased for large content
    
    # Case details - Increased sizes
    plaintiff = db.Column(db.String(300), index=True)
    defendant = db.Column(db.String(300), index=True)
    case_date = db.Column(db.DateTime, index=True)
    filing_date = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    # Status and priority with indexes
    status = db.Column(db.String(100), default='جديدة', index=True)
    priority = db.Column(db.String(50), default='متوسط', index=True)
    
    # Legal details - Increased sizes
    case_type = db.Column(db.String(200))
    legal_basis = db.Column(db.Text(20000))
    claimed_amount = db.Column(db.Decimal(20, 2))  # Increased precision
    
    # Administrative - Increased sizes
    lawyer_name = db.Column(db.String(250))
    lawyer_license = db.Column(db.String(100))
    fees = db.Column(db.Decimal(15, 2))
    notes = db.Column(db.Text(50000))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    
    # Foreign Keys
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), index=True)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    
    # Relationships with dynamic loading
    judgments = db.relationship('Judgment', backref='case', lazy='dynamic', cascade='all, delete-orphan')
    documents = db.relationship('Document', backref='case', lazy='dynamic', cascade='all, delete-orphan')
    case_sessions = db.relationship('CaseSession', backref='case', lazy='dynamic', cascade='all, delete-orphan')

# Judgment Model - Optimized for large datasets
class Judgment(db.Model):
    __tablename__ = 'judgments'
    __table_args__ = (
        db.Index('idx_judgment_case', 'case_id'),
        db.Index('idx_judgment_type', 'judgment_type'),
        db.Index('idx_judgment_date', 'judgment_date'),
        db.Index('idx_judgment_status', 'status'),
        db.Index('idx_judgment_court', 'court_id'),
        db.Index('idx_judgment_created', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    content = db.Column(db.Text(100000), nullable=False)  # Large content support
    
    # Judgment details - Increased sizes
    judgment_type = db.Column(db.String(100), nullable=False, index=True)
    judgment_date = db.Column(db.DateTime, index=True)
    judge_name = db.Column(db.String(250))
    court_level = db.Column(db.String(100))
    
    # Status and appeal
    status = db.Column(db.String(100), default='نهائي', index=True)
    appeal_status = db.Column(db.String(100))
    appeal_deadline = db.Column(db.DateTime)
    
    # Financial details - Increased precision
    judgment_amount = db.Column(db.Decimal(20, 2))
    fees_awarded = db.Column(db.Decimal(15, 2))
    execution_status = db.Column(db.String(100))
    
    # Legal citations - Increased sizes
    legal_articles = db.Column(db.Text(50000))
    precedents = db.Column(db.Text(50000))
    
    # Administrative - Increased sizes
    notes = db.Column(db.Text(50000))
    keywords = db.Column(db.Text(10000))
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, index=True)
    
    # Foreign Keys
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False, index=True)
    court_id = db.Column(db.Integer, db.ForeignKey('courts.id'), index=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    
    # Relationships
    documents = db.relationship('Document', backref='judgment', lazy='dynamic')

# Document Model - Optimized for large files
class Document(db.Model):
    __tablename__ = 'documents'
    __table_args__ = (
        db.Index('idx_document_case', 'case_id'),
        db.Index('idx_document_judgment', 'judgment_id'),
        db.Index('idx_document_type', 'document_type'),
        db.Index('idx_document_uploaded', 'uploaded_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(500), nullable=False)
    original_filename = db.Column(db.String(500), nullable=False)
    file_path = db.Column(db.String(1000), nullable=False)
    file_size = db.Column(db.BigInteger)  # Changed to BigInteger for large files
    mime_type = db.Column(db.String(150))
    
    # Document metadata
    document_type = db.Column(db.String(100), index=True)
    description = db.Column(db.Text(10000))
    version = db.Column(db.Integer, default=1)
    is_confidential = db.Column(db.Boolean, default=False, index=True)
    
    # OCR and search - Increased sizes
    extracted_text = db.Column(db.Text(100000))
    ocr_confidence = db.Column(db.Float)
    is_searchable = db.Column(db.Boolean, default=False, index=True)
    
    # Timestamps
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    last_accessed = db.Column(db.DateTime, index=True)
    
    # Foreign Keys
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), index=True)
    judgment_id = db.Column(db.Integer, db.ForeignKey('judgments.id'), index=True)
    uploaded_by = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)

# Case Session Model - Optimized
class CaseSession(db.Model):
    __tablename__ = 'case_sessions'
    __table_args__ = (
        db.Index('idx_session_case', 'case_id'),
        db.Index('idx_session_date', 'session_date'),
        db.Index('idx_session_status', 'status'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_date = db.Column(db.DateTime, nullable=False, index=True)
    session_time = db.Column(db.Time)
    session_type = db.Column(db.String(100))
    
    # Session details - Increased sizes
    judge_name = db.Column(db.String(250))
    court_room = db.Column(db.String(100))
    agenda = db.Column(db.Text(20000))
    minutes = db.Column(db.Text(50000))
    
    # Attendance
    plaintiff_present = db.Column(db.Boolean)
    defendant_present = db.Column(db.Boolean)
    plaintiff_lawyer = db.Column(db.String(250))
    defendant_lawyer = db.Column(db.String(250))
    
    # Status
    status = db.Column(db.String(100), default='مجدولة', index=True)
    postponement_reason = db.Column(db.Text(10000))
    next_session_date = db.Column(db.DateTime, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Foreign Keys
    case_id = db.Column(db.Integer, db.ForeignKey('cases.id'), nullable=False, index=True)

# Legal Article Model - Optimized
class LegalArticle(db.Model):
    __tablename__ = 'legal_articles'
    __table_args__ = (
        db.Index('idx_article_number', 'article_number'),
        db.Index('idx_article_law', 'law_name'),
        db.Index('idx_article_active', 'is_active'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    article_number = db.Column(db.String(50), nullable=False, index=True)
    title = db.Column(db.String(500))
    content = db.Column(db.Text(100000), nullable=False)
    
    # Legal source - Increased sizes
    law_name = db.Column(db.String(500), nullable=False, index=True)
    law_number = db.Column(db.String(100))
    law_year = db.Column(db.Integer, index=True)
    chapter = db.Column(db.String(300))
    section = db.Column(db.String(300))
    
    # Status
    is_active = db.Column(db.Boolean, default=True, index=True)
    effective_date = db.Column(db.DateTime, index=True)
    amendment_date = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Legal Precedent Model - Optimized
class LegalPrecedent(db.Model):
    __tablename__ = 'legal_precedents'
    __table_args__ = (
        db.Index('idx_precedent_court', 'court_name'),
        db.Index('idx_precedent_date', 'decision_date'),
        db.Index('idx_precedent_reference', 'case_reference'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(500), nullable=False)
    summary = db.Column(db.Text(20000))
    full_text = db.Column(db.Text(100000))
    
    # Court details - Increased sizes
    court_name = db.Column(db.String(250), index=True)
    court_level = db.Column(db.String(100))
    decision_date = db.Column(db.DateTime, index=True)
    case_reference = db.Column(db.String(200), index=True)
    
    # Legal principle - Increased sizes
    legal_principle = db.Column(db.Text(50000))
    keywords = db.Column(db.Text(10000))
    
    # Citations and references
    cited_articles = db.Column(db.Text(20000))
    citation_count = db.Column(db.Integer, default=0, index=True)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# System Settings Model
class SystemSetting(db.Model):
    __tablename__ = 'system_settings'
    __table_args__ = (
        db.Index('idx_setting_key', 'key'),
        db.Index('idx_setting_category', 'category'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    key = db.Column(db.String(200), unique=True, nullable=False, index=True)
    value = db.Column(db.Text(20000))
    description = db.Column(db.Text(5000))
    data_type = db.Column(db.String(50), default='string')
    category = db.Column(db.String(100), index=True)
    is_public = db.Column(db.Boolean, default=False, index=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Audit Log Model - Optimized
class AuditLog(db.Model):
    __tablename__ = 'audit_logs'
    __table_args__ = (
        db.Index('idx_audit_user', 'user_id'),
        db.Index('idx_audit_resource', 'resource_type', 'resource_id'),
        db.Index('idx_audit_timestamp', 'timestamp'),
        db.Index('idx_audit_action', 'action'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    action = db.Column(db.String(150), nullable=False, index=True)
    resource_type = db.Column(db.String(100), index=True)
    resource_id = db.Column(db.Integer, index=True)
    old_values = db.Column(db.Text(50000))
    new_values = db.Column(db.Text(50000))
    ip_address = db.Column(db.String(50))
    user_agent = db.Column(db.String(1000))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    user = db.relationship('User', backref=db.backref('audit_logs', lazy='dynamic'))

# Notification Model
class Notification(db.Model):
    __tablename__ = 'notifications'
    __table_args__ = (
        db.Index('idx_notification_user', 'user_id'),
        db.Index('idx_notification_read', 'is_read'),
        db.Index('idx_notification_created', 'created_at'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    title = db.Column(db.String(500), nullable=False)
    message = db.Column(db.Text(10000), nullable=False)
    notification_type = db.Column(db.String(100), default='info')
    
    # Related resource
    resource_type = db.Column(db.String(100))
    resource_id = db.Column(db.Integer)
    
    # Status
    is_read = db.Column(db.Boolean, default=False, index=True)
    read_at = db.Column(db.DateTime)
    
    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    user = db.relationship('User', backref=db.backref('notifications', lazy='dynamic'))

# Search Index Model - Optimized for large datasets
class SearchIndex(db.Model):
    __tablename__ = 'search_indexes'
    __table_args__ = (
        db.Index('idx_search_resource', 'resource_type', 'resource_id'),
        db.Index('idx_search_language', 'language'),
        db.Index('idx_search_indexed', 'last_indexed'),
        # FULLTEXT indexes for MySQL (add manually in production)
        # db.Index('idx_search_content_fulltext', 'normalized_content', mysql_prefix='FULLTEXT'),
    )
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    resource_type = db.Column(db.String(100), nullable=False, index=True)
    resource_id = db.Column(db.Integer, nullable=False, index=True)
    content = db.Column(db.Text(100000), nullable=False)
    normalized_content = db.Column(db.Text(100000))  # Increased size
    keywords = db.Column(db.Text(10000))
    
    # Search metadata
    language = db.Column(db.String(20), default='ar', index=True)
    last_indexed = db.Column(db.DateTime, default=datetime.utcnow, index=True)
