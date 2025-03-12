from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from datetime import datetime, timezone
from app import models, schemas

# ----------------- USER CRUD OPERATIONS -----------------
def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = user.password  # Hashing should be implemented
    db_user = models.User(username=user.username, phone_number=user.phone_number, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_phone(db: Session, phone_number: str):
    return db.query(models.User).filter(models.User.phone_number == phone_number).first()

# ----------------- DATA PACKAGE CRUD OPERATIONS -----------------
def create_data_package(db: Session, package: schemas.DataPackageCreate):
    db_package = models.DataPackage(name=package.name, price=package.price, data_limit_mb=package.data_limit_mb)
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    return db_package

def get_data_package(db: Session, package_id: int):
    return db.query(models.DataPackage).filter(models.DataPackage.id == package_id).first()

def get_all_data_packages(db: Session):
    return db.query(models.DataPackage).all()

# ----------------- TRANSACTION CRUD OPERATIONS -----------------
def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    db_transaction = models.Transaction(
        user_id=transaction.user_id,
        package_id=transaction.package_id,
        amount=transaction.amount,
        transaction_id=transaction.transaction_id,
        status="pending",
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_transaction)
    try:
        db.commit()
        db.refresh(db_transaction)
        return db_transaction
    except IntegrityError:
        db.rollback()
        return None  # Handle duplicate transaction IDs

def update_transaction_status(db: Session, transaction_id: str, status: str):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()
    if db_transaction:
        db_transaction.status = status
        db.commit()
        db.refresh(db_transaction)
    return db_transaction

def get_transaction_by_id(db: Session, transaction_id: str):
    return db.query(models.Transaction).filter(models.Transaction.transaction_id == transaction_id).first()

# ----------------- ACTIVE SESSION CRUD OPERATIONS -----------------
def create_active_session(db: Session, session: schemas.ActiveSessionCreate):
    db_session = models.ActiveSession(
        user_id=session.user_id,
        package_id=session.package_id,
        start_time=datetime.now(timezone.utc),
        is_active=True
    )
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

def get_active_session(db: Session, user_id: int):
    return db.query(models.ActiveSession).filter(models.ActiveSession.user_id == user_id, models.ActiveSession.is_active == True).first()

def update_session_data_usage(db: Session, session_id: int, data_used_mb: int):
    db_session = db.query(models.ActiveSession).filter(models.ActiveSession.id == session_id).first()
    if db_session:
        db_session.data_used_mb += data_used_mb
        db.commit()
        db.refresh(db_session)
    return db_session

def deactivate_session(db: Session, session_id: int):
    db_session = db.query(models.ActiveSession).filter(models.ActiveSession.id == session_id).first()
    if db_session:
        db_session.is_active = False
        db.commit()
        db.refresh(db_session)
    return db_session

# ----------------- DATA PACKET CRUD OPERATIONS -----------------
def create_data_packet(db: Session, packet: schemas.DataPacketCreate):
    db_packet = models.DataPacket(
        session_id=packet.session_id,
        data_used_mb=packet.data_used_mb,
        created_at=datetime.now(timezone.utc)
    )
    db.add(db_packet)
    db.commit()
    db.refresh(db_packet)
    return db_packet

def get_data_packets_by_session(db: Session, session_id: int):
    return db.query(models.DataPacket).filter(models.DataPacket.session_id == session_id).all()