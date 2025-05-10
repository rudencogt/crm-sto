from sqlalchemy import Column, String, DateTime, ForeignKey, Text, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database_client import BaseClient
import uuid
import datetime
import enum

class OrderActionType(str, enum.Enum):
    status_change = "status_change"
    comment = "comment"
    assign = "assign"

class OrderHistory(BaseClient):
    __tablename__ = "order_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=False)
    
    # Убрали ForeignKey на users.id, так как users в другой базе
    user_id = Column(UUID(as_uuid=True), nullable=True)

    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    action = Column(Enum(OrderActionType), nullable=False)
    comment = Column(Text, nullable=True)

    order = relationship("Order", backref="history")
