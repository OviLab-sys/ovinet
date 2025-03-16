from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Import List from typing
from app import crud, schemas
from app.database import get_db  # Changed import from dependencies to database

router = APIRouter()

@router.post("/sessions", response_model=schemas.ActiveSession)
def create_session(session: schemas.ActiveSessionCreate, db: Session = Depends(get_db)):
    return crud.create_active_session(db, session)

@router.get("/sessions/{user_id}", response_model=List[schemas.ActiveSession])
def get_sessions(user_id: int, db: Session = Depends(get_db)):
    sessions = crud.get_sessions_by_user_id(db, user_id)
    if not sessions:
        raise HTTPException(status_code=404, detail="Sessions not found")
    return sessions