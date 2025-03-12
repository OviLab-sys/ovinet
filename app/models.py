from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DECIMAL, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from app.database import Base

# User Model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    phone_number = Column(String(15), unique=True, index=True)
    password = Column(String(255))

# Data Package Model (E.g., 1GB, 5GB, etc.)
class DataPackage(Base):
    __tablename__ = "data_packages"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, index=True)
    price = Column(DECIMAL(10, 2))
    data_limit_mb = Column(Integer)

# Data Packet Model (Tracks individual data units consumed)
class DataPacket(Base):
    __tablename__ = "data_packets"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("active_sessions.id"))
    data_used_mb = Column(Integer)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

# Active User Session (Tracks ongoing data consumption)
class ActiveSession(Base):
    __tablename__ = "active_sessions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    package_id = Column(Integer, ForeignKey("data_packages.id"))
    data_used_mb = Column(Integer, default=0)
    is_active = Column(Boolean, default=True)
    start_time = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    package = relationship("DataPackage")

# Transaction History (MPESA Payments)
class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    package_id = Column(Integer, ForeignKey("data_packages.id"))
    amount = Column(DECIMAL(10, 2))
    transaction_id = Column(String(100), unique=True, index=True)
    status = Column(String(20), default="pending")
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship("User")
    package = relationship("DataPackage")