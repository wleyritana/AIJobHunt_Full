import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    NOTIFY_PROVIDER = os.getenv("NOTIFY_PROVIDER", "console")
    NOTIFY_EMAIL_FROM = os.getenv("NOTIFY_EMAIL_FROM", "no-reply@example.com")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
