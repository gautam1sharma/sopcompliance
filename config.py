import os
from datetime import timedelta
from pathlib import Path

class Config:
    """Base configuration class with common settings."""
    
    # Basic Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
    
    # File upload settings
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'pdf', 'docx', 'txt'}
    
    # Session settings
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24)
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; style-src 'self' 'unsafe-inline' https://cdn.jsdelivr.net; font-src 'self' https://cdn.jsdelivr.net;"
    }
    
    # AI Model settings
    SEMANTIC_MODEL_NAME = 'all-roberta-large-v1'
    MODEL_CACHE_DIR = os.path.join(os.getcwd(), '.model_cache')
    SIMILARITY_THRESHOLD = 0.3
    
    # Logging settings
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.path.join(os.getcwd(), 'logs', 'app.log')
    
    # Performance settings
    CACHE_TYPE = 'simple'
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    
    # ISO Standards
    ISO_STANDARDS_PATH = os.path.join(os.getcwd(), 'iso_standards', 'iso27002.json')
    
    @staticmethod
    def init_app(app):
        """Initialize application with config-specific settings."""
        # Ensure required directories exist
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.MODEL_CACHE_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(Config.LOG_FILE), exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False
    SESSION_COOKIE_SECURE = False  # Allow HTTP in development
    
class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    
    # Use environment variables for sensitive settings
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Enhanced security for production
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    
    # Production-specific model settings
    MODEL_CACHE_DIR = '/app/.model_cache'
    LOG_FILE = '/app/logs/app.log'
    
    @staticmethod
    def init_app(app):
        Config.init_app(app)
        
        # Production-specific initialization
        if not os.environ.get('SECRET_KEY'):
            raise RuntimeError("SECRET_KEY environment variable must be set in production")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'test_uploads')
    SESSION_COOKIE_SECURE = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 