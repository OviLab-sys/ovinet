from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List  # Import List from typing
from app import crud, schemas
from app.intasend_service import IntaSendService

router = APIRouter()

@router.post("/transactions", response_model=schemas.Transaction)
def create_transaction(payment: schemas.PaymentCreate, db: Session = Depends(get_db)):
    transaction = crud.create_transaction(db, schemas.TransactionCreate(**payment.dict()))
    if not transaction:
        raise HTTPException(status_code=400, detail="Transaction creation failed")
    intasend_service = IntaSendService()
    intasend_service.initiate_mpesa_payment(payment.phone_number, payment.amount, transaction.transaction_id)
    return transaction

@router.get("/transactions/{user_id}", response_model=List[schemas.Transaction])
def get_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = crud.get_transactions_by_user_id(db, user_id)
    if not transactions:
        raise HTTPException(status_code=404, detail="Transactions not found")
    return transactions