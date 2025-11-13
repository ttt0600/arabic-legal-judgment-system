import os
from datetime import timedelta

class Config:
    # Basic Flask configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here-change-in-production'
    
    # Database configuration - Optimized for large datasets
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'localhost'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'root'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'arabic_legal_system'
    
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}/{MYSQL_DB}?charset=utf8mb4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Database connection pool settings - Optimized for large datasets
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 20,              # Increased from default 5
        'pool_recycle': 3600,         # Recycle connections every hour
        'pool_pre_ping': True,        # Verify connections before using
        'pool_timeout': 30,           # Connection timeout
        'max_overflow': 40,           # Max additional connections beyond pool_size
        'echo': False,                # Set to True for SQL debugging
        'connect_args': {
            'connect_timeout': 10,
            'read_timeout': 30,
            'write_timeout': 30,
            'max_allowed_packet': 64 * 1024 * 1024,  # 64MB for large content
        }
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-string'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_ALGORITHM = 'HS256'
    
    # File upload configuration - Increased limits for large files
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER') or 'uploads'
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size (increased from 16MB)
    ALLOWED_EXTENSIONS = {'pdf', 'doc', 'docx', 'txt', 'jpg', 'jpeg', 'png', 'zip', 'rar'}
    
    # Arabic language configuration
    LANGUAGE = 'ar'
    TIMEZONE = 'Asia/Riyadh'
    
    # Pagination - Optimized for large datasets
    POSTS_PER_PAGE = 50  # Increased from 20
    MAX_SEARCH_RESULTS = 1000  # Increased from 100
    
    # Caching configuration - Important for large datasets
    CACHE_TYPE = 'redis' if os.environ.get('REDIS_URL') else 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_KEY_PREFIX = 'legal_system_'
    
    # Email configuration (for notifications)
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = int(os.environ.get('MAIL_PORT') or 587)
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() in ['true', 'on', '1']
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Redis configuration (for caching and background tasks)
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # Elasticsearch configuration (for advanced search with large datasets)
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL') or 'http://localhost:9200'
    ELASTICSEARCH_INDEX_PREFIX = 'legal_system_'
    
    # Security settings
    BCRYPT_LOG_ROUNDS = 12
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # API Rate limiting - Adjusted for large dataset operations
    RATELIMIT_STORAGE_URL = REDIS_URL
    RATELIMIT_DEFAULT = "2000 per hour"  # Increased from 1000
    RATELIMIT_HEADERS_ENABLED = True
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL') or 'INFO'
    LOG_FILE = os.environ.get('LOG_FILE') or 'logs/app.log'
    LOG_MAX_BYTES = 10 * 1024 * 1024  # 10MB
    LOG_BACKUP_COUNT = 5
    
    # Backup settings
    BACKUP_FOLDER = os.environ.get('BACKUP_FOLDER') or 'backups'
    AUTO_BACKUP_ENABLED = os.environ.get('AUTO_BACKUP_ENABLED', 'true').lower() in ['true', 'on', '1']
    BACKUP_RETENTION_DAYS = int(os.environ.get('BACKUP_RETENTION_DAYS') or 30)
    
    # Large dataset optimization settings
    ENABLE_QUERY_CACHING = True
    ENABLE_LAZY_LOADING = True
    ENABLE_BATCH_PROCESSING = True
    BATCH_SIZE = 1000  # Number of records to process at once
    
    # Search optimization
    FULLTEXT_SEARCH_ENABLED = True
    SEARCH_CACHE_TIMEOUT = 600  # 10 minutes
    
    # Performance monitoring
    ENABLE_QUERY_PROFILING = os.environ.get('ENABLE_QUERY_PROFILING', 'false').lower() in ['true', 'on', '1']
    SLOW_QUERY_THRESHOLD = 1.0  # seconds

class DevelopmentConfig(Config):
    DEBUG = True
    TESTING = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_recycle': 3600,
        'pool_pre_ping': True,
        'echo': True,  # Show SQL queries in development
    }

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    
    # Production-specific optimizations
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 30,              # More connections in production
        'pool_recycle': 1800,         # Recycle more frequently
        'pool_pre_ping': True,
        'pool_timeout': 30,
        'max_overflow': 60,
        'echo': False,
        'connect_args': {
            'connect_timeout': 10,
            'read_timeout': 60,       # Longer timeouts for large queries
            'write_timeout': 60,
            'max_allowed_packet': 128 * 1024 * 1024,  # 128MB in production
        }
    }
    
    # Production rate limiting
    RATELIMIT_DEFAULT = "5000 per hour"
    
    # Enable all caching in production
    ENABLE_QUERY_CACHING = True
    CACHE_DEFAULT_TIMEOUT = 600  # 10 minutes in production

class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(seconds=1)
    WTF_CSRF_ENABLED = False

# Configuration dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

# MySQL optimization queries (run these manually for large datasets)
MYSQL_OPTIMIZATION_QUERIES = """
-- Increase MySQL buffer pool size (add to my.cnf or my.ini)
-- innodb_buffer_pool_size = 2G  (adjust based on available RAM)

-- Enable query cache
-- query_cache_type = 1
-- query_cache_size = 256M

-- Increase max connections
-- max_connections = 500

-- Optimize for InnoDB
-- innodb_flush_log_at_trx_commit = 2
-- innodb_log_file_size = 256M

-- For full-text search optimization
-- ft_min_word_len = 2  (for Arabic text)

-- Add FULLTEXT indexes for search (run in MySQL):
ALTER TABLE cases ADD FULLTEXT INDEX idx_cases_fulltext (title, description, plaintiff, defendant);
ALTER TABLE judgments ADD FULLTEXT INDEX idx_judgments_fulltext (title, content, keywords);
ALTER TABLE search_indexes ADD FULLTEXT INDEX idx_search_fulltext (normalized_content);
"""
