# -*- coding: utf-8 -*-
"""
Database service layer for the Arabic Legal Judgment System
"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import or_, and_, func
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from utils.text_processing import ArabicTextProcessor, SearchUtils

class DatabaseService:
    """Database operations service"""
    
    def __init__(self, db):
        self.db = db
        self.text_processor = ArabicTextProcessor()
        self.search_utils = SearchUtils()

class CaseService(DatabaseService):
    """Case management service"""
    
    def create_case(self, case_data: Dict, created_by: int) -> Dict:
        """Create a new case"""
        from models import Case
        
        try:
            case = Case(
                case_number=case_data['case_number'],
                title=case_data['title'],
                description=case_data.get('description', ''),
                plaintiff=case_data.get('plaintiff'),
                defendant=case_data.get('defendant'),
                case_date=case_data.get('case_date'),
                status=case_data.get('status', 'جديدة'),
                priority=case_data.get('priority', 'متوسط'),
                case_type=case_data.get('case_type'),
                legal_basis=case_data.get('legal_basis'),
                claimed_amount=case_data.get('claimed_amount'),
                lawyer_name=case_data.get('lawyer_name'),
                lawyer_license=case_data.get('lawyer_license'),
                category_id=case_data['category_id'],
                court_id=case_data.get('court_id'),
                created_by=created_by
            )
            
            self.db.session.add(case)
            self.db.session.commit()
            
            return {
                'success': True,
                'case_id': case.id,
                'message': 'تم إنشاء القضية بنجاح'
            }
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'success': False,
                'error': f'حدث خطأ في إنشاء القضية: {str(e)}'
            }
    
    def update_case(self, case_id: int, case_data: Dict) -> Dict:
        """Update an existing case"""
        from models import Case
        
        try:
            case = Case.query.get(case_id)
            if not case:
                return {
                    'success': False,
                    'error': 'القضية غير موجودة'
                }
            
            # Update fields
            for field, value in case_data.items():
                if hasattr(case, field) and value is not None:
                    setattr(case, field, value)
            
            case.updated_at = datetime.utcnow()
            self.db.session.commit()
            
            return {
                'success': True,
                'message': 'تم تحديث القضية بنجاح'
            }
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'success': False,
                'error': f'حدث خطأ في تحديث القضية: {str(e)}'
            }
    
    def search_cases(self, query: str, filters: Dict = None, page: int = 1, per_page: int = 20) -> Dict:
        """Search cases with filters"""
        from models import Case, Category, Court
        
        try:
            # Base query
            base_query = Case.query.join(Category, Case.category_id == Category.id, isouter=True)\
                                 .join(Court, Case.court_id == Court.id, isouter=True)
            
            # Apply search query
            if query:
                normalized_query = self.text_processor.normalize_arabic(query)
                query_words = normalized_query.split()
                
                search_conditions = []
                for word in query_words:
                    if word:
                        search_conditions.append(
                            or_(
                                Case.title.contains(word),
                                Case.description.contains(word),
                                Case.case_number.contains(word),
                                Case.plaintiff.contains(word),
                                Case.defendant.contains(word),
                                Case.legal_basis.contains(word)
                            )
                        )
                
                if search_conditions:
                    base_query = base_query.filter(and_(*search_conditions))
            
            # Apply filters
            if filters:
                if filters.get('category_id'):
                    base_query = base_query.filter(Case.category_id == filters['category_id'])
                
                if filters.get('court_id'):
                    base_query = base_query.filter(Case.court_id == filters['court_id'])
                
                if filters.get('status'):
                    base_query = base_query.filter(Case.status == filters['status'])
                
                if filters.get('priority'):
                    base_query = base_query.filter(Case.priority == filters['priority'])
                
                if filters.get('date_from'):
                    base_query = base_query.filter(Case.case_date >= filters['date_from'])
                
                if filters.get('date_to'):
                    base_query = base_query.filter(Case.case_date <= filters['date_to'])
            
            # Order by relevance and date
            base_query = base_query.order_by(Case.created_at.desc())
            
            # Paginate
            cases = base_query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'success': True,
                'cases': [{
                    'id': case.id,
                    'case_number': case.case_number,
                    'title': case.title,
                    'description': case.description,
                    'plaintiff': case.plaintiff,
                    'defendant': case.defendant,
                    'status': case.status,
                    'priority': case.priority,
                    'case_date': case.case_date.isoformat() if case.case_date else None,
                    'created_at': case.created_at.isoformat(),
                    'category': {
                        'id': case.category.id,
                        'name': case.category.name
                    } if case.category else None,
                    'court': {
                        'id': case.court.id,
                        'name': case.court.name
                    } if case.court else None
                } for case in cases.items],
                'pagination': {
                    'page': cases.page,
                    'pages': cases.pages,
                    'per_page': cases.per_page,
                    'total': cases.total,
                    'has_next': cases.has_next,
                    'has_prev': cases.has_prev
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'حدث خطأ في البحث: {str(e)}'
            }
    
    def get_case_statistics(self, filters: Dict = None) -> Dict:
        """Get case statistics"""
        from models import Case, Category, Court
        
        try:
            # Base query
            base_query = Case.query
            
            # Apply filters
            if filters:
                if filters.get('category_id'):
                    base_query = base_query.filter(Case.category_id == filters['category_id'])
                
                if filters.get('court_id'):
                    base_query = base_query.filter(Case.court_id == filters['court_id'])
                
                if filters.get('date_from'):
                    base_query = base_query.filter(Case.created_at >= filters['date_from'])
                
                if filters.get('date_to'):
                    base_query = base_query.filter(Case.created_at <= filters['date_to'])
            
            # Total cases
            total_cases = base_query.count()
            
            # Cases by status
            status_stats = self.db.session.query(
                Case.status, func.count(Case.id)
            ).group_by(Case.status).all()
            
            # Cases by priority
            priority_stats = self.db.session.query(
                Case.priority, func.count(Case.id)
            ).group_by(Case.priority).all()
            
            # Cases by category
            category_stats = self.db.session.query(
                Category.name, func.count(Case.id)
            ).join(Case, Category.id == Case.category_id)\
             .group_by(Category.name).all()
            
            # Monthly case creation trend (last 12 months)
            twelve_months_ago = datetime.now() - timedelta(days=365)
            monthly_stats = self.db.session.query(
                func.extract('year', Case.created_at).label('year'),
                func.extract('month', Case.created_at).label('month'),
                func.count(Case.id).label('count')
            ).filter(Case.created_at >= twelve_months_ago)\
             .group_by('year', 'month')\
             .order_by('year', 'month').all()
            
            return {
                'success': True,
                'statistics': {
                    'total_cases': total_cases,
                    'by_status': dict(status_stats),
                    'by_priority': dict(priority_stats),
                    'by_category': dict(category_stats),
                    'monthly_trend': [
                        {
                            'year': int(stat.year),
                            'month': int(stat.month),
                            'count': stat.count
                        } for stat in monthly_stats
                    ]
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'حدث خطأ في جلب الإحصائيات: {str(e)}'
            }

class JudgmentService(DatabaseService):
    """Judgment management service"""
    
    def create_judgment(self, judgment_data: Dict, created_by: int) -> Dict:
        """Create a new judgment"""
        from models import Judgment
        
        try:
            judgment = Judgment(
                case_id=judgment_data['case_id'],
                title=judgment_data['title'],
                content=judgment_data['content'],
                judgment_type=judgment_data['judgment_type'],
                judgment_date=judgment_data.get('judgment_date', datetime.utcnow()),
                judge_name=judgment_data.get('judge_name'),
                court_level=judgment_data.get('court_level'),
                status=judgment_data.get('status', 'نهائي'),
                appeal_status=judgment_data.get('appeal_status'),
                judgment_amount=judgment_data.get('judgment_amount'),
                fees_awarded=judgment_data.get('fees_awarded'),
                legal_articles=judgment_data.get('legal_articles'),
                precedents=judgment_data.get('precedents'),
                keywords=judgment_data.get('keywords'),
                notes=judgment_data.get('notes'),
                court_id=judgment_data.get('court_id'),
                created_by=created_by
            )
            
            # Extract keywords from content if not provided
            if not judgment.keywords and judgment.content:
                extracted_keywords = self.text_processor.extract_keywords(judgment.content)
                judgment.keywords = ', '.join(extracted_keywords)
            
            self.db.session.add(judgment)
            self.db.session.commit()
            
            return {
                'success': True,
                'judgment_id': judgment.id,
                'message': 'تم إنشاء الحكم بنجاح'
            }
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'success': False,
                'error': f'حدث خطأ في إنشاء الحكم: {str(e)}'
            }
    
    def search_judgments(self, query: str, filters: Dict = None, page: int = 1, per_page: int = 20) -> Dict:
        """Search judgments with filters"""
        from models import Judgment, Case, Court
        
        try:
            # Base query
            base_query = Judgment.query.join(Case, Judgment.case_id == Case.id)\
                                     .join(Court, Judgment.court_id == Court.id, isouter=True)
            
            # Apply search query
            if query:
                normalized_query = self.text_processor.normalize_arabic(query)
                query_words = normalized_query.split()
                
                search_conditions = []
                for word in query_words:
                    if word:
                        search_conditions.append(
                            or_(
                                Judgment.title.contains(word),
                                Judgment.content.contains(word),
                                Judgment.judge_name.contains(word),
                                Judgment.legal_articles.contains(word),
                                Judgment.keywords.contains(word),
                                Case.case_number.contains(word)
                            )
                        )
                
                if search_conditions:
                    base_query = base_query.filter(and_(*search_conditions))
            
            # Apply filters
            if filters:
                if filters.get('judgment_type'):
                    base_query = base_query.filter(Judgment.judgment_type == filters['judgment_type'])
                
                if filters.get('status'):
                    base_query = base_query.filter(Judgment.status == filters['status'])
                
                if filters.get('court_level'):
                    base_query = base_query.filter(Judgment.court_level == filters['court_level'])
                
                if filters.get('date_from'):
                    base_query = base_query.filter(Judgment.judgment_date >= filters['date_from'])
                
                if filters.get('date_to'):
                    base_query = base_query.filter(Judgment.judgment_date <= filters['date_to'])
            
            # Order by relevance and date
            base_query = base_query.order_by(Judgment.judgment_date.desc())
            
            # Paginate
            judgments = base_query.paginate(
                page=page,
                per_page=per_page,
                error_out=False
            )
            
            return {
                'success': True,
                'judgments': [{
                    'id': judgment.id,
                    'title': judgment.title,
                    'content': judgment.content[:500] + '...' if len(judgment.content) > 500 else judgment.content,
                    'judgment_type': judgment.judgment_type,
                    'judgment_date': judgment.judgment_date.isoformat() if judgment.judgment_date else None,
                    'judge_name': judgment.judge_name,
                    'court_level': judgment.court_level,
                    'status': judgment.status,
                    'case': {
                        'id': judgment.case.id,
                        'case_number': judgment.case.case_number,
                        'title': judgment.case.title
                    } if judgment.case else None,
                    'court': {
                        'id': judgment.court.id,
                        'name': judgment.court.name
                    } if judgment.court else None
                } for judgment in judgments.items],
                'pagination': {
                    'page': judgments.page,
                    'pages': judgments.pages,
                    'per_page': judgments.per_page,
                    'total': judgments.total,
                    'has_next': judgments.has_next,
                    'has_prev': judgments.has_prev
                }
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'حدث خطأ في البحث: {str(e)}'
            }

class DocumentService(DatabaseService):
    """Document management service"""
    
    def upload_document(self, document_data: Dict, uploaded_by: int) -> Dict:
        """Upload a new document"""
        from models import Document
        from utils.text_processing import FileUtils
        
        try:
            # Validate file
            if not FileUtils.allowed_file(document_data['filename']):
                return {
                    'success': False,
                    'error': 'نوع الملف غير مدعوم'
                }
            
            # Generate secure filename
            secure_filename = FileUtils.secure_filename(document_data['filename'])
            
            document = Document(
                filename=secure_filename,
                original_filename=document_data['filename'],
                file_path=document_data['file_path'],
                file_size=document_data.get('file_size', 0),
                mime_type=document_data.get('mime_type'),
                document_type=document_data.get('document_type'),
                description=document_data.get('description'),
                is_confidential=document_data.get('is_confidential', False),
                case_id=document_data.get('case_id'),
                judgment_id=document_data.get('judgment_id'),
                uploaded_by=uploaded_by
            )
            
            self.db.session.add(document)
            self.db.session.commit()
            
            return {
                'success': True,
                'document_id': document.id,
                'message': 'تم رفع المستند بنجاح'
            }
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'success': False,
                'error': f'حدث خطأ في رفع المستند: {str(e)}'
            }

class UserService(DatabaseService):
    """User management service"""
    
    def create_user(self, user_data: Dict) -> Dict:
        """Create a new user"""
        from models import User
        from werkzeug.security import generate_password_hash
        from utils.text_processing import ValidationUtils
        
        try:
            # Validate data
            if not ValidationUtils.validate_email(user_data.get('email')):
                return {
                    'success': False,
                    'error': 'البريد الإلكتروني غير صحيح'
                }
            
            phone = user_data.get('phone')
            if phone and not ValidationUtils.validate_phone_number(phone):
                return {
                    'success': False,
                    'error': 'رقم الهاتف غير صحيح'
                }
            
            # Check if user already exists
            if User.query.filter_by(username=user_data['username']).first():
                return {
                    'success': False,
                    'error': 'اسم المستخدم موجود بالفعل'
                }
            
            if User.query.filter_by(email=user_data['email']).first():
                return {
                    'success': False,
                    'error': 'البريد الإلكتروني مسجل بالفعل'
                }
            
            user = User(
                username=user_data['username'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                full_name=user_data['full_name'],
                phone=phone,
                role=user_data.get('role', 'user'),
                department=user_data.get('department'),
                is_active=True
            )
            
            self.db.session.add(user)
            self.db.session.commit()
            
            return {
                'success': True,
                'user_id': user.id,
                'message': 'تم إنشاء الحساب بنجاح'
            }
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'success': False,
                'error': f'حدث خطأ في إنشاء الحساب: {str(e)}'
            }
    
    def get_user_activity_log(self, user_id: int, limit: int = 50) -> Dict:
        """Get user activity log"""
        from models import AuditLog, User
        
        try:
            logs = AuditLog.query.filter_by(user_id=user_id)\
                                .order_by(AuditLog.timestamp.desc())\
                                .limit(limit).all()
            
            return {
                'success': True,
                'activities': [{
                    'action': log.action,
                    'resource_type': log.resource_type,
                    'resource_id': log.resource_id,
                    'timestamp': log.timestamp.isoformat(),
                    'ip_address': log.ip_address
                } for log in logs]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'حدث خطأ في جلب سجل النشاط: {str(e)}'
            }

class NotificationService(DatabaseService):
    """Notification service"""
    
    def create_notification(self, user_id: int, title: str, message: str, 
                          notification_type: str = 'info', resource_type: str = None, 
                          resource_id: int = None) -> Dict:
        """Create a new notification"""
        from models import Notification
        
        try:
            notification = Notification(
                user_id=user_id,
                title=title,
                message=message,
                notification_type=notification_type,
                resource_type=resource_type,
                resource_id=resource_id
            )
            
            self.db.session.add(notification)
            self.db.session.commit()
            
            return {
                'success': True,
                'notification_id': notification.id
            }
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'success': False,
                'error': f'حدث خطأ في إنشاء الإشعار: {str(e)}'
            }
    
    def get_user_notifications(self, user_id: int, unread_only: bool = False) -> Dict:
        """Get user notifications"""
        from models import Notification
        
        try:
            query = Notification.query.filter_by(user_id=user_id)
            
            if unread_only:
                query = query.filter_by(is_read=False)
            
            notifications = query.order_by(Notification.created_at.desc()).all()
            
            return {
                'success': True,
                'notifications': [{
                    'id': notif.id,
                    'title': notif.title,
                    'message': notif.message,
                    'type': notif.notification_type,
                    'is_read': notif.is_read,
                    'created_at': notif.created_at.isoformat(),
                    'resource_type': notif.resource_type,
                    'resource_id': notif.resource_id
                } for notif in notifications]
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': f'حدث خطأ في جلب الإشعارات: {str(e)}'
            }
    
    def mark_notification_read(self, notification_id: int) -> Dict:
        """Mark notification as read"""
        from models import Notification
        
        try:
            notification = Notification.query.get(notification_id)
            if not notification:
                return {
                    'success': False,
                    'error': 'الإشعار غير موجود'
                }
            
            notification.is_read = True
            notification.read_at = datetime.utcnow()
            self.db.session.commit()
            
            return {
                'success': True,
                'message': 'تم تحديث الإشعار'
            }
            
        except Exception as e:
            self.db.session.rollback()
            return {
                'success': False,
                'error': f'حدث خطأ في تحديث الإشعار: {str(e)}'
            }

# Export all services
__all__ = [
    'CaseService',
    'JudgmentService', 
    'DocumentService',
    'UserService',
    'NotificationService'
]
