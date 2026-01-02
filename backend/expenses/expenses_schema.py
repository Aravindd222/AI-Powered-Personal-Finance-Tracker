# expenses/expenses_schema.py
from pydantic import BaseModel
from datetime import date
from typing import Optional
from uuid import UUID
# Schema for creating a manual expense

class ManualExpenseCreate(BaseModel):
    amount: float
    category: str
    date: date


class ExpenseResponse(BaseModel):
    id: UUID
    amount: float
    category: str
    subcategory: Optional[str]
    date: date
    source: str

    class Config:
        from_attributes = True
