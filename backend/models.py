import uuid
from sqlalchemy import Column, String, Date, Float, Text, TIMESTAMP, ForeignKey , Numeric
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())


class Expense(Base):
    __tablename__ = "expenses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    amount = Column(Numeric(10, 2), nullable=False)
    category = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)

    source = Column(String(10), nullable=False)  # manual | ocr
    raw_text = Column(Text)
    confidence = Column(Numeric(4, 2))

    created_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())
