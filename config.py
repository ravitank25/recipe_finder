import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base directory
BASE_DIR = Path(__file__).resolve().parent

# Database directory
DB_DIR = BASE_DIR / "database"
DB_DIR.mkdir(exist_ok=True)


class Config:
    # Secret Key
    SECRET_KEY = os.getenv(
        "3151191dc311ab61381eb7f50e6effcb1725879440342f762f3554b1872cc520",
        "recipe-finder-secret-key-change-in-production"
    )

    # Database Configuration
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DB_DIR / 'recipe.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Flask Configuration
    FLASK_ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = os.getenv("FLASK_DEBUG", "True").lower() == "true"

    # Session Configuration
    SESSION_COOKIE_SECURE = os.getenv(
        "SESSION_COOKIE_SECURE", "False"
    ).lower() == "true"

    SESSION_COOKIE_HTTPONLY = os.getenv(
        "SESSION_COOKIE_HTTPONLY", "True"
    ).lower() == "true"

    SESSION_COOKIE_SAMESITE = os.getenv(
        "SESSION_COOKIE_SAMESITE", "Lax"
    )