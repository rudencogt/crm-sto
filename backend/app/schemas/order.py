from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from enum import Enum

# --- ENUMs ---
class OrderStatus(str, Enum):
    new = "new"
    diagnostics = "diagnostics"
    in_progress = "in_progress"
    waiting_parts = "waiting_parts"
    done = "done"

class PaymentMethod(str, Enum):
    cash = "cash"
    card = "card"
    blik = "blik"
    ukr = "ukr"

# --- OrderCreate (POST /orders) ---
class OrderCreate(BaseModel):
    client_id: UUID4
    vehicle_id: UUID4
    status: Optional[OrderStatus] = OrderStatus.new
    payment_method: Optional[PaymentMethod] = None
    notes: Optional[str] = None

# --- OrderResponse ---
class OrderResponse(OrderCreate):
    id: UUID4
    start_date: datetime
    end_date: Optional[datetime] = None
    work_days: Optional[int] = None
    created_at: datetime

    class Config:
        orm_mode = True

# --- GET /orders ---
class ClientShort(BaseModel):
    id: UUID4
    first_name: str
    last_name: str
    phone: str

    class Config:
        orm_mode = True

class VehicleShort(BaseModel):
    id: UUID4
    make: str
    model: str
    plate_number: Optional[str] = None

    class Config:
        orm_mode = True

class OrderDetailed(BaseModel):
    id: UUID4
    status: OrderStatus
    payment_method: Optional[PaymentMethod]
    start_date: datetime
    end_date: Optional[datetime]
    notes: Optional[str]
    client: ClientShort
    vehicle: VehicleShort

    class Config:
        orm_mode = True

# --- OrderFullCreate (POST /orders/full) ---
class ClientIn(BaseModel):
    first_name: str
    last_name: str
    phone: str
    email: Optional[str] = None

class VehicleIn(BaseModel):
    make: str
    model: str
    vin: Optional[str]
    plate_number: Optional[str]

class OrderData(BaseModel):
    status: OrderStatus = OrderStatus.new
    payment_method: Optional[PaymentMethod]
    notes: Optional[str] = None

class OrderFullCreate(BaseModel):
    client: ClientIn
    vehicle: VehicleIn
    order: OrderData
