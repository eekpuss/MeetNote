# backend/config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///database/meetnote.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = os.environ.get('DEBUG') or True
    
    # Konfigurasi JWT yang diperlukan
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-dev-secret'
    JWT_ACCESS_TOKEN_EXPIRES = 86400  # 24 jam
    JWT_TOKEN_LOCATION = ['headers']  # Lokasi token (headers)
    JWT_HEADER_NAME = 'Authorization'
    JWT_HEADER_TYPE = 'Bearer'
    
    # Konfigurasi email
    MAIL_SERVER = os.environ.get('MAIL_SERVER') or 'smtp.gmail.com'
    MAIL_PORT = os.environ.get('MAIL_PORT') or 587
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME') or 'your-email@gmail.com'
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD') or 'your-password'
    MAIL_USE_TLS = True
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER') or 'your-email@gmail.com'