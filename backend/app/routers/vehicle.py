from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database_client import get_client_db  # Для работы с базой данных клиентов и автомобилей
from app.models.vehicle import Vehicle  # Модель Vehicle
from app.schemas.vehicle import VehicleIn, VehicleOut  # Для валидации данных
from app.dependencies.auth import get_current_user  # Для проверки авторизованного пользователя
from app.models.user import User  # Модель User
from sqlalchemy.exc import SQLAlchemyError

router = APIRouter()

# Создание нового автомобиля
@router.post("/", response_model=VehicleOut)
def create_vehicle(
    vehicle_data: VehicleIn,  # Данные для нового автомобиля
    db: Session = Depends(get_client_db),  # Сессия для работы с базой данных
    current_user: User = Depends(get_current_user)  # Проверка текущего авторизованного пользователя
):
    if not current_user:
        raise HTTPException(status_code=403, detail="Not authenticated")

    # Создаем новый объект автомобиля с данными из запроса
    new_vehicle = Vehicle(
        make=vehicle_data.make,
        model=vehicle_data.model,
        vin=vehicle_data.vin,
        plate_number=vehicle_data.plate_number,
        engine=vehicle_data.engine,
        fuel_type=vehicle_data.fuel_type,
        engine_volume=vehicle_data.engine_volume,
        year=vehicle_data.year  # Добавляем год выпуска автомобиля
    )

    try:
        # Добавляем новый автомобиль в базу данных
        db.add(new_vehicle)
        db.commit()
        db.refresh(new_vehicle)  # Обновляем информацию о только что созданном объекте
    except SQLAlchemyError:
        db.rollback()  # Откатываем изменения в случае ошибки
        raise HTTPException(status_code=500, detail="Database error occurred while creating vehicle")

    return new_vehicle  # Возвращаем созданный объект автомобиля

# Получение информации об автомобиле по ID
@router.get("/{vehicle_id}", response_model=VehicleOut)
def get_vehicle(
    vehicle_id: str,  # ID автомобиля, который ищем
    db: Session = Depends(get_client_db),  # Используем get_client_db для работы с базой данных
    current_user: User = Depends(get_current_user)  # Проверка, если пользователь авторизован
):
    if not current_user:
        raise HTTPException(status_code=403, detail="Not authenticated")

    # Ищем автомобиль по его ID
    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    # Если автомобиль не найден, выбрасываем ошибку
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    
    return vehicle  # Возвращаем информацию о найденном автомобиле
