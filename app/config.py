import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev_secret")
    SQLALCHEMY_DATABASE_URI = "sqlite:///db.sqlite3"  # SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    STRIPE_API_KEY = os.environ.get("STRIPE_API_KEY", "test_stripe_key")  # Placeholder
