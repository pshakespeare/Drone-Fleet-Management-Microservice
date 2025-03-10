import os
from datetime import timedelta

class Config:
    """Base configuration."""
    
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    CORS_ORIGIN_WHITELIST = [
        'http://localhost:5000',
        'http://localhost:3000',
    ]

class ProductionConfig(Config):
    """Production configuration."""
    
    ENV = 'production'
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    
class DevelopmentConfig(Config):
    """Development configuration."""
    
    ENV = 'development'
    DEBUG = True
    DB_NAME = 'drone_db_dev'
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASS', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

class TestingConfig(Config):
    """Testing configuration."""
    
    TESTING = True
    DEBUG = True
    DB_NAME = 'drone_db_test'
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASS = os.getenv('DB_PASS', 'postgres')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', 5432)
    SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 