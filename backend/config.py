import os
import urllib.parse
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE_DIR, '..'))
UPLOAD_FOLDER = os.path.join(PROJECT_ROOT, 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'karigar-ai-secret-key-2026-tech4bharat')
    
    # MySQL Database credentials provided by user
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASS = os.getenv('DB_PASS', 'rajkumar@123')
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_PORT = os.getenv('DB_PORT', '3306')
    DB_NAME = os.getenv('DB_NAME', 'Karigar_Ai')
    
    # URL-encode password to safely handle special characters like '@'
    ENCODED_PASS = urllib.parse.quote_plus(DB_PASS)
    MYSQL_URI = f"mysql+pymysql://{DB_USER}:{ENCODED_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"
    SQLITE_URI = f"sqlite:///{os.path.join(BASE_DIR, 'karigar_fallback.db')}"
    
    # Default to MySQL as configured
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', MYSQL_URI)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    UPLOAD_FOLDER = UPLOAD_FOLDER
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    
    # AI/ML Provider Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', '')
    AI_PROVIDER = os.getenv('AI_PROVIDER', 'deterministic_demo') # 'openai' or 'deterministic_demo'
