from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum

class TransactionType(str, Enum):
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"

class TransactionCreate(BaseModel):
    type: TransactionType
    category_id: int
    amount: float
    date: date
    note: Optional[str] = None

class UserCreate(BaseModel):
    name: str
    email: str
    password: str

class UserLogin(BaseModel):
    email: str
    password: str