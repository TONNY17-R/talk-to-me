import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Security
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-change-in-production'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-change'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'mysql+pymysql://root:password@localhost/talk_to_me'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Redis
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://localhost:6379/0'
    
    # AI Services
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY', '')
    GOOGLE_AI_KEY = os.environ.get('GOOGLE_AI_KEY', '')
    HUGGINGFACE_TOKEN = os.environ.get('HUGGINGFACE_TOKEN', '')
    
    # SMS Gateway (Africa's Talking)
    AT_API_KEY = os.environ.get('AFRICASTALKING_API_KEY', '')
    AT_USERNAME = os.environ.get('AFRICASTALKING_USERNAME', 'sandbox')
    
    # File Uploads
    UPLOAD_FOLDER = 'uploads'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'mp3', 'wav', 'mp4'}
    
    # Email
    MAIL_SERVER = os.environ.get('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.environ.get('MAIL_PORT', 587))
    MAIL_USE_TLS = os.environ.get('MAIL_USE_TLS', 'true').lower() == 'true'
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    
    # Payment (Flutterwave)
    FLW_PUBLIC_KEY = os.environ.get('FLW_PUBLIC_KEY', '')
    FLW_SECRET_KEY = os.environ.get('FLW_SECRET_KEY', '')
    
    # App Settings
    APP_NAME = "Talk to Me Uganda"
    SUPPORT_EMAIL = "support@talktome.ug"
    EMERGENCY_NUMBER = "0800-123-456"
    
    # CORS
    CORS_ORIGINS = [origin.strip() for origin in os.environ.get('CORS_ORIGINS', 'http://localhost:3000').split(',') if origin.strip()]
    
    # Analytics
    SENTRY_DSN = os.environ.get('SENTRY_DSN', '')

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True

class ProductionConfig(Config):
    DEBUG = False
    # Force HTTPS in production
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}