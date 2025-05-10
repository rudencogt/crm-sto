import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.orm import Session

load_dotenv()

# Строки подключения для обеих баз данных
CRM_DB_URL = f"postgresql://{os.getenv('CRM_DB_USER')}:{os.getenv('CRM_DB_PASSWORD')}@{os.getenv('CRM_DB_HOST')}:{os.getenv('CRM_DB_PORT')}/{os.getenv('CRM_DB_NAME')}"
AUTH_DB_URL = f"postgresql://{os.getenv('AUTH_DB_USER')}:{os.getenv('AUTH_DB_PASSWORD')}@{os.getenv('AUTH_DB_HOST')}:{os.getenv('AUTH_DB_PORT')}/{os.getenv('AUTH_DB_NAME')}"

# Создаем engine для обеих баз данных
engine_client = create_engine(CRM_DB_URL)
engine_auth = create_engine(AUTH_DB_URL)

# Создаем сессии для обеих баз данных
SessionLocalClient = sessionmaker(autocommit=False, autoflush=False, bind=engine_client)
SessionLocalAuth = sessionmaker(autocommit=False, autoflush=False, bind=engine_auth)

# Базовые классы для обеих баз данных
BaseClient = declarative_base()
BaseAuth = declarative_base()

# Функции для получения сессий для разных баз данных

# Для базы клиентов и автомобилей
def get_client_db() -> Session:
    db = SessionLocalClient()
    try:
        yield db
    finally:
        db.close()

# Для базы авторизации
def get_auth_db() -> Session:
    db = SessionLocalAuth()
    try:
        yield db
    finally:
        db.close()
