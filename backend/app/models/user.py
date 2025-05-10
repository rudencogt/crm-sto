from sqlalchemy import Column, Integer, String, Boolean, Enum
from app.database_client import BaseAuth
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    mechanic = "mechanic"

class User(BaseAuth):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(Enum(UserRole), nullable=False, default=UserRole.mechanic)
