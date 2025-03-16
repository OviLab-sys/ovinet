from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import crud, schemas
from app.database import get_db  # Changed import from dependencies to database

router = APIRouter()

@router.post("/packets", response_model=schemas.DataPacket)
def create_packet(packet: schemas.DataPacketCreate, db: Session = Depends(get_db)):
    session = crud.get_session_by_id(db, packet.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return crud.create_data_packet(db, packet)

@router.get("/packets/{user_id}", response_model=List[schemas.DataPacket])
def get_packets(user_id: int, db: Session = Depends(get_db)):
    packets = crud.get_packets_by_user_id(db, user_id)
    if not packets:
        raise HTTPException(status_code=404, detail="Packets not found")
    return packets

@router.get("/packets/{session_id}/usage", response_model=int)
def get_total_data_usage(session_id: int, db: Session = Depends(get_db)):
    session = crud.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return crud.get_total_data_usage(db, session_id)