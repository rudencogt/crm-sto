from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from uuid import uuid4

from app.database_client import get_client_db
from app.models.order import Order, OrderActionType  # Импортируем OrderActionType
from app.models.client import Client
from app.models.vehicle import Vehicle
from app.models.user import User
from app.schemas.order import (
    OrderCreate, OrderResponse, OrderDetailed,
    OrderFullCreate
)
from app.dependencies.auth import get_current_user

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)

# Создание нового заказа с добавлением истории
@router.post("/", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_client_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(Client.id == order_data.client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    vehicle = db.query(Vehicle).filter(Vehicle.id == order_data.vehicle_id).first()
    if not vehicle:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    # Создание нового заказа
    new_order = Order(
        id=uuid4(),
        client_id=order_data.client_id,
        vehicle_id=order_data.vehicle_id,
        status=order_data.status,
        payment_method=order_data.payment_method,
        notes=order_data.notes
    )
    db.add(new_order)
    db.flush()  # Выполняем flush, чтобы получить ID

    # Локальный импорт OrderHistory для предотвращения циклического импорта
    from app.models.order import OrderHistory  # Локальный импорт для предотвращения циклического импорта

    # Записываем в историю заказа
    history = OrderHistory(
        order_id=new_order.id,
        user_id=current_user.id,
        action=OrderActionType.status_change,
        comment=f"Order created with status: {order_data.status}"
    )
    db.add(history)
    db.commit()  # Подтверждаем транзакцию
    db.refresh(new_order)  # Получаем обновленную информацию о заказе

    return new_order


# Получение всех заказов
@router.get("/", response_model=List[OrderDetailed])
def get_orders(
    db: Session = Depends(get_client_db),
    current_user: User = Depends(get_current_user)
):
    return db.query(Order).filter(Order.client_id == current_user.id).all()


# Создание заказа с клиентом и автомобилем (включая историю)
@router.post("/full", response_model=OrderResponse)
def create_full_order(
    data: OrderFullCreate,
    db: Session = Depends(get_client_db),
    current_user: User = Depends(get_current_user)
):
    client = db.query(Client).filter(
        (Client.phone == data.client.phone) |
        (Client.email == data.client.email)
    ).first()

    if not client:
        client = Client(
            id=uuid4(),
            first_name=data.client.first_name,
            last_name=data.client.last_name,
            phone=data.client.phone,
            email=data.client.email
        )
        db.add(client)
        db.flush()  # Сгенерировать ID для клиента перед использованием

    vehicle = Vehicle(
        id=uuid4(),
        client_id=client.id,
        make=data.vehicle.make,
        model=data.vehicle.model,
        vin=data.vehicle.vin,
        plate_number=data.vehicle.plate_number
    )
    db.add(vehicle)
    db.flush()  # Сначала генерируем ID для автомобиля

    order = Order(
        id=uuid4(),
        client_id=client.id,
        vehicle_id=vehicle.id,
        status=data.order.status,
        payment_method=data.order.payment_method,
        notes=data.order.notes
    )
    db.add(order)
    db.flush()  # Сначала генерируем ID для заказа

    # Локальный импорт OrderHistory для предотвращения циклического импорта
    from app.models.order import OrderHistory  # Локальный импорт для предотвращения циклического импорта

    # Добавляем запись в историю
    history = OrderHistory(
        order_id=order.id,
        user_id=current_user.id,
        action=OrderActionType.status_change,
        comment=f"Order created with status: {data.order.status}"
    )
    db.add(history)
    db.commit()  # Подтверждаем все изменения
    db.refresh(order)  # Обновляем информацию о заказе

    return order
