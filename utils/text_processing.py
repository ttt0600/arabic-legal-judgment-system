# -*- coding: utf-8 -*-
"""
Utility functions for Arabic text processing and search functionality
"""

import re
import arabic_reshaper
from bidi.algorithm import get_display
from fuzzywuzzy import fuzz, process
import string
from datetime import datetime, timedelta
import hashlib
import os
import uuid

class ArabicTextProcessor:
    """Arabic text processing utilities"""
    
    # Arabic diacritics for removal
    ARABIC_DIACRITICS = re.compile(r'[\u064B-\u0652\u0670\u0640]')
    
    # Character normalization map
    NORMALIZE_MAP = {
        'أ': 'ا', 'إ': 'ا', 'آ': 'ا', 'ٱ': 'ا',
        'ة': 'ه',
        'ى': 'ي',
        'ي': 'ي', 'ئ': 'ي', 'ؤ': 'و'
    }
    
    @staticmethod
    def reshape_arabic(text):
        """Reshape Arabic text for proper display"""
        if not text:
            return ""
        try:
            reshaped = arabic_reshaper.reshape(text)
            return get_display(reshaped)
        except Exception:
            return text
    
    @staticmethod
    def normalize_arabic(text):
        """Normalize Arabic text for search and comparison"""
        if not text:
            return ""
        
        # Convert to lowercase (for mixed content)
        text = text.lower()
        
        # Remove diacritics
        text = ArabicTextProcessor.ARABIC_DIACRITICS.sub('', text)
        
        # Normalize characters
        for old, new in ArabicTextProcessor.NORMALIZE_MAP.items():
            text = text.replace(old, new)
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text).strip()
        
        return text
    
    @staticmethod
    def remove_punctuation(text):
        """Remove punctuation from Arabic text"""
        if not text:
            return ""
        
        # Arabic and English punctuation
        arabic_punctuation = '،؛؟!""''()[]{}«»'
        english_punctuation = string.punctuation
        
        all_punctuation = arabic_punctuation + english_punctuation
        
        # Remove punctuation
        translator = str.maketrans('', '', all_punctuation)
        return text.translate(translator)
    
    @staticmethod
    def extract_keywords(text, min_length=3, max_keywords=10):
        """Extract keywords from Arabic text"""
        if not text:
            return []
        
        # Normalize text
        normalized = ArabicTextProcessor.normalize_arabic(text)
        normalized = ArabicTextProcessor.remove_punctuation(normalized)
        
        # Split into words
        words = normalized.split()
        
        # Filter words by length and remove common stop words
        arabic_stopwords = {
            'في', 'من', 'إلى', 'على', 'عن', 'مع', 'بعد', 'قبل', 'تحت', 'فوق',
            'هذا', 'هذه', 'ذلك', 'تلك', 'التي', 'الذي', 'التي', 'الذين', 'اللذان',
            'هو', 'هي', 'أنت', 'أنتم', 'أنتن', 'نحن', 'أنا',
            'كان', 'كانت', 'يكون', 'تكون', 'أكون', 'نكون',
            'قد', 'لقد', 'قال', 'قالت', 'يقول', 'تقول',
            'كل', 'بعض', 'جميع', 'معظم', 'أغلب'
        }
        
        keywords = []
        for word in words:
            if (len(word) >= min_length and 
                word not in arabic_stopwords and
                word not in keywords):
                keywords.append(word)
        
        return keywords[:max_keywords]
    
    @staticmethod
    def similarity_score(text1, text2):
        """Calculate similarity score between two Arabic texts"""
        if not text1 or not text2:
            return 0
        
        # Normalize both texts
        norm1 = ArabicTextProcessor.normalize_arabic(text1)
        norm2 = ArabicTextProcessor.normalize_arabic(text2)
        
        # Calculate fuzzy similarity
        return fuzz.ratio(norm1, norm2)
    
    @staticmethod
    def fuzzy_search(query, text_list, threshold=60):
        """Perform fuzzy search on a list of Arabic texts"""
        if not query or not text_list:
            return []
        
        # Normalize query
        normalized_query = ArabicTextProcessor.normalize_arabic(query)
        
        # Normalize text list
        normalized_texts = [ArabicTextProcessor.normalize_arabic(text) for text in text_list]
        
        # Perform fuzzy matching
        matches = process.extract(normalized_query, normalized_texts, limit=len(text_list))
        
        # Filter by threshold and return with original indices
        results = []
        for match, score in matches:
            if score >= threshold:
                # Find original index
                original_index = normalized_texts.index(match)
                results.append({
                    'text': text_list[original_index],
                    'score': score,
                    'index': original_index
                })
        
        return results

class SearchUtils:
    """Search utility functions"""
    
    @staticmethod
    def build_search_query(terms, fields=None):
        """Build a search query from search terms"""
        if not terms:
            return ""
        
        # Default fields to search in
        if fields is None:
            fields = ['title', 'description', 'content']
        
        # Normalize search terms
        normalized_terms = [ArabicTextProcessor.normalize_arabic(term) for term in terms]
        
        # Build query conditions
        conditions = []
        for field in fields:
            for term in normalized_terms:
                if term:
                    conditions.append(f"{field} LIKE '%{term}%'")
        
        return " OR ".join(conditions) if conditions else ""
    
    @staticmethod
    def highlight_matches(text, query, tag='mark'):
        """Highlight search matches in text"""
        if not text or not query:
            return text
        
        # Normalize query
        normalized_query = ArabicTextProcessor.normalize_arabic(query)
        query_words = normalized_query.split()
        
        highlighted_text = text
        for word in query_words:
            if word:
                # Case-insensitive replacement
                pattern = re.compile(re.escape(word), re.IGNORECASE)
                highlighted_text = pattern.sub(
                    f'<{tag}>\\g<0></{tag}>', 
                    highlighted_text
                )
        
        return highlighted_text

class FileUtils:
    """File handling utilities"""
    
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png'}
    MAX_FILE_SIZE = 16 * 1024 * 1024  # 16MB
    
    @staticmethod
    def allowed_file(filename):
        """Check if file extension is allowed"""
        return ('.' in filename and 
                filename.rsplit('.', 1)[1].lower() in FileUtils.ALLOWED_EXTENSIONS)
    
    @staticmethod
    def secure_filename(filename):
        """Generate a secure filename"""
        # Get file extension
        if '.' in filename:
            name, ext = filename.rsplit('.', 1)
            ext = ext.lower()
        else:
            name, ext = filename, ''
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        
        # Clean the original name (keep Arabic characters)
        clean_name = re.sub(r'[^\w\u0600-\u06FF\s-]', '', name)
        clean_name = re.sub(r'\s+', '_', clean_name)
        
        if clean_name:
            secure_name = f"{clean_name}_{timestamp}_{unique_id}"
        else:
            secure_name = f"file_{timestamp}_{unique_id}"
        
        return f"{secure_name}.{ext}" if ext else secure_name
    
    @staticmethod
    def get_file_hash(filepath):
        """Calculate file hash for duplicate detection"""
        hasher = hashlib.md5()
        try:
            with open(filepath, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None
    
    @staticmethod
    def get_file_size_mb(filepath):
        """Get file size in MB"""
        try:
            size_bytes = os.path.getsize(filepath)
            return round(size_bytes / (1024 * 1024), 2)
        except Exception:
            return 0

class DateUtils:
    """Date and time utilities"""
    
    @staticmethod
    def hijri_to_gregorian(hijri_year, hijri_month, hijri_day):
        """Convert Hijri date to Gregorian (approximation)"""
        # Simple approximation - for accurate conversion, use a proper library
        # This is just a basic implementation
        gregorian_year = int(hijri_year * 0.97 + 622)
        return datetime(gregorian_year, hijri_month, hijri_day)
    
    @staticmethod
    def format_arabic_date(date_obj):
        """Format date in Arabic"""
        if not date_obj:
            return ""
        
        arabic_months = [
            'يناير', 'فبراير', 'مارس', 'أبريل', 'مايو', 'يونيو',
            'يوليو', 'أغسطس', 'سبتمبر', 'أكتوبر', 'نوفمبر', 'ديسمبر'
        ]
        
        arabic_days = [
            'الاثنين', 'الثلاثاء', 'الأربعاء', 'الخميس', 
            'الجمعة', 'السبت', 'الأحد'
        ]
        
        day_name = arabic_days[date_obj.weekday()]
        month_name = arabic_months[date_obj.month - 1]
        
        return f"{day_name}، {date_obj.day} {month_name} {date_obj.year}"
    
    @staticmethod
    def parse_arabic_date(date_string):
        """Parse Arabic date string to datetime object"""
        # This would need proper implementation based on expected format
        # For now, return current date
        return datetime.now()
    
    @staticmethod
    def get_relative_time_arabic(date_obj):
        """Get relative time in Arabic"""
        if not date_obj:
            return ""
        
        now = datetime.now()
        diff = now - date_obj
        
        if diff.days == 0:
            if diff.seconds < 3600:  # Less than 1 hour
                minutes = diff.seconds // 60
                return f"منذ {minutes} دقيقة"
            else:  # Less than 24 hours
                hours = diff.seconds // 3600
                return f"منذ {hours} ساعة"
        elif diff.days == 1:
            return "أمس"
        elif diff.days < 7:
            return f"منذ {diff.days} أيام"
        elif diff.days < 30:
            weeks = diff.days // 7
            return f"منذ {weeks} أسابيع"
        elif diff.days < 365:
            months = diff.days // 30
            return f"منذ {months} شهور"
        else:
            years = diff.days // 365
            return f"منذ {years} سنوات"

class ValidationUtils:
    """Data validation utilities"""
    
    @staticmethod
    def validate_saudi_id(national_id):
        """Validate Saudi national ID"""
        if not national_id or len(national_id) != 10:
            return False
        
        if not national_id.isdigit():
            return False
        
        # Check if starts with 1 or 2
        if not national_id.startswith(('1', '2')):
            return False
        
        # Luhn algorithm check
        digits = [int(d) for d in national_id]
        checksum = 0
        
        for i in range(9):
            digit = digits[i]
            if i % 2 == 0:
                digit *= 2
                if digit > 9:
                    digit = digit // 10 + digit % 10
            checksum += digit
        
        return (checksum % 10) == (10 - digits[9]) % 10
    
    @staticmethod
    def validate_phone_number(phone):
        """Validate Saudi phone number"""
        if not phone:
            return False
        
        # Remove spaces and special characters
        clean_phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        # Check for Saudi mobile patterns
        patterns = [
            r'^(\+966|966|0)?5[0-9]{8}$',  # Mobile
            r'^(\+966|966|0)?1[1-9][0-9]{7}$',  # Landline
        ]
        
        for pattern in patterns:
            if re.match(pattern, clean_phone):
                return True
        
        return False
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        if not email:
            return False
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email))

class ReportUtils:
    """Report generation utilities"""
    
    @staticmethod
    def generate_case_summary(case):
        """Generate a summary for a case"""
        if not case:
            return ""
        
        summary_parts = []
        
        # Basic info
        summary_parts.append(f"رقم القضية: {case.case_number}")
        summary_parts.append(f"العنوان: {case.title}")
        
        if case.plaintiff:
            summary_parts.append(f"المدعي: {case.plaintiff}")
        
        if case.defendant:
            summary_parts.append(f"المدعى عليه: {case.defendant}")
        
        if case.status:
            summary_parts.append(f"الحالة: {case.status}")
        
        if case.case_date:
            summary_parts.append(f"تاريخ القضية: {DateUtils.format_arabic_date(case.case_date)}")
        
        return " | ".join(summary_parts)
    
    @staticmethod
    def generate_statistics_summary(stats):
        """Generate statistics summary in Arabic"""
        if not stats:
            return ""
        
        summary_parts = []
        
        if 'total_cases' in stats:
            summary_parts.append(f"إجمالي القضايا: {stats['total_cases']}")
        
        if 'total_judgments' in stats:
            summary_parts.append(f"إجمالي الأحكام: {stats['total_judgments']}")
        
        if 'cases_by_status' in stats:
            for status, count in stats['cases_by_status'].items():
                summary_parts.append(f"{status}: {count}")
        
        return "\n".join(summary_parts)

# Export all utility classes
__all__ = [
    'ArabicTextProcessor',
    'SearchUtils', 
    'FileUtils',
    'DateUtils',
    'ValidationUtils',
    'ReportUtils'
]
