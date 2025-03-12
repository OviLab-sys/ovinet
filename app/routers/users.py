from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, crud, database
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends

router = APIRouter(prefix="/users", tags=["Users"])

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered.")
    return crud.create_user(db, user)

@router.post("/token", response_model=schemas.Token)
def login_user(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials.")
    access_token = crud.create_access_token({"sub": user.phone_number})
    return {"access_token": access_token, "token_type": "bearer"}

def get_current_user(phone_number: str, db: Session = Depends(database.get_db)):
    return crud.get_current_user(db, phone_number)

@router.get("/{user_id}/wallet", response_model=schemas.WalletResponse)
def get_user_wallet(user_id: int, db: Session = Depends(get_db)):
    return crud.get_wallet_by_user_id(db, user_id)
