import enum
from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Integer, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database_client import BaseClient
import uuid
import datetime

# Определяем типы статусов для заказа
class OrderStatus(str, enum.Enum):
    new = "new"
    diagnostics = "diagnostics"
    in_progress = "in_progress"
    waiting_parts = "waiting_parts"
    done = "done"

# Определяем методы оплаты
class PaymentMethod(str, enum.Enum):
    cash = "cash"
    card = "card"
    blik = "blik"
    ukr = "ukr"

# Добавляем OrderActionType для различных типов действий с заказом
class OrderActionType(str, enum.Enum):
    status_change = "status_change"
    comment = "comment"
    assign = "assign"

# Модель для заказов
class Order(BaseClient):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)
    vehicle_id = Column(UUID(as_uuid=True), ForeignKey("vehicles.id"), nullable=False)

    status = Column(Enum(OrderStatus), default=OrderStatus.new, nullable=False)
    start_date = Column(DateTime, default=datetime.datetime.utcnow)
    end_date = Column(DateTime, nullable=True)
    work_days = Column(Integer, nullable=True)

    payment_method = Column(Enum(PaymentMethod), nullable=True)
    notes = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    client = relationship("Client", backref="orders")
    vehicle = relationship("Vehicle", backref="orders")

    # История заказов с строковой аннотацией для предотвращения циклических импортов
    history = relationship("OrderHistory", backref="order", lazy="dynamic")
