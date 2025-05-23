import os
from dotenv import load_dotenv

load_dotenv()

def load_config():
    return {
        "SQLALCHEMY_DATABASE_URI": f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "JWT_SECRET_KEY": os.getenv("JWT_SECRET_KEY", "default_secret"),
        "JWT_ACCESS_TOKEN_EXPIRES": int(os.getenv("JWT_ACCESS_TOKEN_EXPIRES", 3600)),
        "DEBUG": os.getenv("FLASK_ENV") == "development"
    }
