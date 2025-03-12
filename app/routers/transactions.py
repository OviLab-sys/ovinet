from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database, intasend_service

router = APIRouter(prefix="/transactions", tags=["Transactions"])

def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

intasend = intasend_service.IntaSendService()

@router.post("/initiate", response_model=schemas.PaymentResponse)
def initiate_payment(payment_data: schemas.PaymentCreate, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, payment_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    transaction = crud.create_transaction(db, payment_data)
    payment_response = intasend.initiate_payment(user.phone_number, payment_data.amount)
    return {"transaction_id": transaction.id, "payment_status": payment_response["status"]}

@router.get("/{user_id}", response_model=list[schemas.TransactionResponse])
def get_user_transactions(user_id: int, db: Session = Depends(get_db)):
    return crud.get_transactions_by_user_id(db, user_id)