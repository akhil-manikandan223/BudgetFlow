from pydantic import BaseModel
from datetime import date as date_type

class ExpenseBase(BaseModel):
    amount: float
    category: str
    date: date_type

class ExpenseCreate(ExpenseBase):
    pass

class ExpenseUpdate(BaseModel):
    amount: float | None = None
    category: str | None = None
    date: date_type | None = None

class ExpenseOut(ExpenseBase):
    id: int