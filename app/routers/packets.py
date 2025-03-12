from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/packets", tags=["Packets"])

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.DataPackageResponse)
def create_packet(packet_data: schemas.DataPacketCreate, db: Session = Depends(get_db)):
    """
    Create a new data packet for tracking user data consumption.
    """
    user = crud.get_user_by_id(db, packet_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    session = crud.get_session_by_id(db, packet_data.session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    packet = crud.create_packet(db, packet_data)
    return packet

@router.get("/{user_id}", response_model=list[schemas.DataPacketResponse])
def get_user_packets(user_id: int, db: Session = Depends(get_db)):
    """
    Retrieve all data packets for a specific user.
    """
    user = crud.get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found.")
    
    return crud.get_packets_by_user_id(db, user_id)

@router.get("/{session_id}/usage", response_model=int)
def get_session_usage(session_id: int, db: Session = Depends(get_db)):
    """
    Get total data usage for a specific session.
    """
    session = crud.get_session_by_id(db, session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found.")
    
    total_usage = crud.get_total_data_usage(db, session_id)
    return total_usage