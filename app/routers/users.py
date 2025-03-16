from fastapi import APIRouter, Depends, HTTPException # All used
from sqlalchemy.orm import Session  # Used
from app import crud, models, schemas  # All used
from app.database import get_db  # Used
from app.auth import authenticate_user, create_access_token, get_current_user  # All used

router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_phone(db, phone_number=user.phone_number)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered.")
    return crud.create_user(db, user)

@router.post("/token", response_model=schemas.Token)
def login_for_access_token(form_data: schemas.LoginForm, db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Incorrect username or password")
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=schemas.User)
def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.get("/users/{user_id}/wallet", response_model=schemas.Wallet)
def get_wallet(user_id: int, db: Session = Depends(get_db)):
    wallet = crud.get_wallet_by_user_id(db, user_id)
    if wallet is None:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet
