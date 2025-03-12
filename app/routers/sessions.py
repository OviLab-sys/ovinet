from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/sessions", tags=["Sessions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.SessionResponse)
def start_session(session_data: schemas.SessionCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, session_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    return crud.create_session(db, session_data)

@router.get("/{user_id}", response_model=list[schemas.SessionResponse])
def get_user_sessions(user_id: int, db: Session = Depends(get_db)):
    return crud.get_sessions_by_user_id(db, user_id)