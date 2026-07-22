from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/api/transactions", tags=["Transactions"])

@router.post("/")
def add_transaction(transaction: schemas.TransactionCreate, user_id: int, db: Session = Depends(database.get_db)):
    return crud.create_transaction(db, transaction, user_id)

@router.get("/")
def get_all_transactions(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_transactions(db, user_id)