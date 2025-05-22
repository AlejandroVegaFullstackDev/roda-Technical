from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config.settings import load_config

settings = load_config()

engine = create_engine(settings['SQLALCHEMY_DATABASE_URI'])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
