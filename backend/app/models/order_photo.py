from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database_client import BaseClient
import uuid
import datetime

class OrderPhoto(BaseClient):
    __tablename__ = "order_photos"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)

    filename = Column(String, nullable=False)
    filepath = Column(String, nullable=False)
    label = Column(String, nullable=True)  # например: 'до ремонта', 'VIN', 'после ремонта'

    uploaded_at = Column(DateTime, default=datetime.datetime.utcnow)
