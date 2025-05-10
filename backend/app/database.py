import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

load_dotenv()

AUTH_DB_URL = f"postgresql://{os.getenv('AUTH_DB_USER')}:{os.getenv('AUTH_DB_PASSWORD')}@{os.getenv('AUTH_DB_HOST')}:{os.getenv('AUTH_DB_PORT')}/{os.getenv('AUTH_DB_NAME')}"

engine = create_engine(AUTH_DB_URL)
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)
Base = declarative_base()
