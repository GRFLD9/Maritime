import os
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()


class Config:
    # ===== Основные настройки =====
    SECRET_KEY = os.getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///instance/default.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # ===== Настройки безопасности =====
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_TOKEN_LOCATION = ["headers"]
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    WTF_CSRF_ENABLED = True

    # ===== Настройки администратора =====
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL')
    ADMIN_INITIAL_PASSWORD = os.getenv('ADMIN_INITIAL_PASSWORD')

    @classmethod
    def validate(cls):
        missing = []
        if not cls.SECRET_KEY:
            missing.append("SECRET_KEY")
        if not cls.JWT_SECRET_KEY:
            missing.append("JWT_SECRET_KEY")
        if missing and os.getenv("FLASK_ENV") == "production":
            raise RuntimeError(f"Missing required environment variables in production: {', '.join(missing)}")


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', 'sqlite:///:memory:')
    WTF_CSRF_ENABLED = False
    PRESERVE_CONTEXT_ON_EXCEPTION = False


class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_pre_ping': True,
        'pool_recycle': 3600
    }


current_env = os.getenv('FLASK_ENV', 'development')
if current_env == 'production':
    ProductionConfig.validate()
elif current_env == 'development':
    DevelopmentConfig.validate()
elif current_env == 'testing':
    TestingConfig.validate()
