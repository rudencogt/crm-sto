# backend/init_db.py

from app.database_client import (
    BaseClient, engine_client,
    BaseAuth, engine_auth
)

from app.models.client import Client
from app.models.vehicle import Vehicle
from app.models.order import Order
from app.models.order_history import OrderHistory
from app.models.order_photo import OrderPhoto
from app.models.user import User  # добавили

# Создаём таблицы в базе client_sto_db
BaseClient.metadata.create_all(bind=engine_client)
print("✅ Таблицы clients, vehicles, orders, order_history, order_photos созданы в client_sto_db.")

# Создаём таблицу users в базе crm_sto
BaseAuth.metadata.create_all(bind=engine_auth)
print("✅ Таблица users создана в crm_sto.")
