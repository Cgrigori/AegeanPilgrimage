import os

class Config:
    
    STRIPE_PUBLIC_KEY = os.getenv("STRIPE_PUBLIC_KEY", "")
    STRIPE_SECRET_KEY = os.getenv("STRIPE_SECRET_KEY", "")
    STRIPE_WEBHOOK_SECRET = os.getenv("STRIPE_WEBHOOK_SECRET", "")
    SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY", "")
    FROM_EMAIL = os.getenv("FROM_EMAIL", "no-reply@example.com")
    CONTACT_EMAIL = os.getenv("CONTACT_EMAIL", "info@example.com")    
    SECRET_KEY = os.getenv("SECRET_KEY", "dev")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///local.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Avatar uploads (local dev)
    AVATAR_UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "uploads", "avatars")
    MAX_CONTENT_LENGTH = 3 * 1024 * 1024  # 3 MB limit
