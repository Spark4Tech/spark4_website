# config.py

import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'AA00BB00CC'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    CSRF_ENABLED = True
    SESSION_COOKIE_NAME = 'website_session'
    SESSION_COOKIE_SECURE = True 
    SESSION_COOKIE_HTTPONLY = True 
    SESSION_COOKIE_SAMESITE = 'Lax' 
    PERMANENT_SESSION_LIFETIME = timedelta(hours=24) 
    WTF_CSRF_ENABLED = True 
    WTF_CSRF_TIME_LIMIT = 7200
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB limit
    
    POSTMARK_API_KEY = os.getenv('POSTMARK_API_KEY')
    POSTMARK_SENDER_EMAIL = os.getenv('POSTMARK_SENDER_EMAIL')
    POSTMARK_NOTIFY_EMAIL = os.getenv('POSTMARK_NOTIFY_EMAIL')
    # POSTMARK_ACCOUNT_TOKEN = os.getenv('POSTMARK_ACCOUNT_TOKEN')

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # In-memory database for testing
    WTF_CSRF_ENABLED = False  # Disable CSRF for testing purposes
    DEBUG = False