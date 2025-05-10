from app.database_client import get_auth_db
from app.models.user import User, UserRole
from passlib.context import CryptContext
from sqlalchemy.orm import Session

# Настройка хеширования пароля
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)

def create_admin(db: Session):
    admin = User(
        full_name="Admin",
        email="io.rudenko@gmail.com",
        hashed_password=get_password_hash("master123"),  # можно заменить
        role=UserRole.admin,
        is_active=True
    )
    db.add(admin)
    db.commit()
    db.refresh(admin)
    print(f"✅ Админ создан: {admin.email} (id={admin.id})")

if __name__ == "__main__":
    for db in get_auth_db():
        create_admin(db)
