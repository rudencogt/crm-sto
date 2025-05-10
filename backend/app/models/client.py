# app/models/client.py

from sqlalchemy import Column, String, Boolean, DateTime
from sqlalchemy.dialects.postgresql import UUID
from app.database_client import BaseClient
import uuid
import datetime

class Client(BaseClient):
    __tablename__ = "clients"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    first_name = Column(String, nullable=False, index=True)
    last_name = Column(String, nullable=False, index=True)
    phone = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=True)
    birthday = Column(DateTime, nullable=True)
    notes = Column(String, nullable=True)

    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    consent_given = Column(Boolean, default=False)
    consent_given_at = Column(DateTime, nullable=True)
