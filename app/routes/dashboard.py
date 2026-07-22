from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, database

router = APIRouter(prefix="/api", tags=["Dashboard"])

@router.get("/dashboard")
def dashboard(user_id: int, db: Session = Depends(database.get_db)):
    return crud.get_dashboard(db, user_id)