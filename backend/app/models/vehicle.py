from sqlalchemy import Column, String, Float, Enum, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import enum
from app.database_client import BaseClient  # Базовый класс для моделей

# Тип топлива, используемый в классе Vehicle
class FuelType(enum.Enum):
    petrol = "petrol"
    diesel = "diesel"
    gas = "gas"
    lpg = "lpg"

# Модель для таблицы vehicles
class Vehicle(BaseClient):
    __tablename__ = "vehicles"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    make = Column(String, nullable=False)  # Марка автомобиля
    model = Column(String, nullable=False)  # Модель автомобиля
    vin = Column(String, unique=True, nullable=False)  # VIN номер
    plate_number = Column(String, unique=True, nullable=False)  # Номерной знак
    engine = Column(String, nullable=False)  # Тип двигателя
    fuel_type = Column(Enum(FuelType), nullable=False)  # Тип топлива
    engine_volume = Column(Float, nullable=False)  # Объем двигателя
    year = Column(Integer, nullable=True)  # Год выпуска автомобиля (новое поле)

    # owner_id без внешнего ключа на users — users в другой БД
    owner_id = Column(UUID(as_uuid=True), nullable=False)

    # owner-связь можешь временно убрать или оставить как заглушку (не будет работать как relationship без таблицы users)
    # owner = relationship("User", back_populates="vehicles")  # <- отключено для избежания ошибок
