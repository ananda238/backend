from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models, schemas
from datetime import datetime, date, timedelta
import hashlib
import jwt
import os
from dotenv import load_dotenv

load_dotenv()
JWT_SECRET = os.getenv("JWT_SECRET")

# ---------- AUTH using SHA256 (simple, untuk development) ----------
def hash_password(password: str):
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain, hashed):
    return hashlib.sha256(plain.encode()).hexdigest() == hashed

def create_user(db: Session, user: schemas.UserCreate):
    hashed = hash_password(user.password)
    db_user = models.User(name=user.name, email=user.email, password=hashed)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user or not verify_password(password, user.password):
        return None
    return user

def create_jwt(user_id: int):
    payload = {"sub": str(user_id), "exp": datetime.utcnow() + timedelta(days=1)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

# ---------- TRANSACTIONS ----------
def get_transactions(db: Session, user_id: int):
    return db.query(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.date.desc()).all()

def create_transaction(db: Session, transaction: schemas.TransactionCreate, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise Exception("User tidak ditemukan")
    
    category = db.query(models.Category).filter(models.Category.id == transaction.category_id).first()
    if not category:
        raise Exception("Kategori tidak ditemukan")
    
    db_trans = models.Transaction(
        user_id=user_id,
        type=transaction.type,
        category_id=transaction.category_id,
        amount=transaction.amount,
        date=transaction.date,
        note=transaction.note
    )
    db.add(db_trans)
    db.commit()
    db.refresh(db_trans)
    return db_trans

def get_dashboard(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise Exception("User tidak ditemukan")
    
    today = date.today()
    start_of_month = today.replace(day=1)
    if today.month == 12:
        end_of_month = today.replace(year=today.year+1, month=1, day=1)
    else:
        end_of_month = today.replace(month=today.month+1, day=1)
    
    total_income = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.type == models.TransactionType.INCOME,
        models.Transaction.date >= start_of_month,
        models.Transaction.date < end_of_month
    ).scalar() or 0.0
    
    total_expense = db.query(func.sum(models.Transaction.amount)).filter(
        models.Transaction.user_id == user_id,
        models.Transaction.type == models.TransactionType.EXPENSE,
        models.Transaction.date >= start_of_month,
        models.Transaction.date < end_of_month
    ).scalar() or 0.0
    
    balance = total_income - total_expense
    
    recent = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).order_by(models.Transaction.date.desc()).limit(5).all()
    
    recent_list = []
    for t in recent:
        recent_list.append({
            "id": t.id,
            "type": t.type.value if hasattr(t.type, 'value') else str(t.type),
            "category": {"id": t.category.id, "name": t.category.name},
            "amount": t.amount,
            "date": t.date.isoformat(),
            "note": t.note
        })
    
    return {
        "total_income": total_income,
        "total_expense": total_expense,
        "balance": balance,
        "recent_transactions": recent_list
    }