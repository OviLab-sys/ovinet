from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ----------------- USER SCHEMAS -----------------
class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    phone_number: str = Field(..., min_length=10, max_length=15)

class UserCreate(UserBase):
    pin: str = Field(..., min_length=4, max_length=6, description="4-6 digit PIN")

class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ----------------- WALLET SCHEMAS -----------------
class WalletBase(BaseModel):
    balance: float = Field(0.0, description="Current wallet balance")

class WalletResponse(WalletBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True

class WalletTopUp(BaseModel):
    amount: float = Field(..., gt=0, description="Amount to top up")


# ----------------- DATA PACKAGE SCHEMAS -----------------
class DataPackageBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Package name (e.g., '1GB')")
    price: float = Field(..., gt=0, description="Price in KSH")
    data_limit_mb: int = Field(..., gt=0, description="Data limit in megabytes")
    duration_hours: int = Field(..., gt=0, description="Validity duration in hours")

class DataPackageCreate(DataPackageBase):
    pass

class DataPackageResponse(DataPackageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

class DataPackageUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50, description="Updated package name (e.g., '5GB')")
    price: Optional[float] = Field(None, gt=0, description="Updated price in KSH")
    data_limit_mb: Optional[int] = Field(None, gt=0, description="Updated data limit in megabytes")
    duration_hours: Optional[int] = Field(None, gt=0, description="Updated validity duration in hours")


# ----------------- DATA PACKET SCHEMAS -----------------
class DataPacketBase(BaseModel):
    code: str = Field(..., min_length=8, max_length=8, description="Unique 8-character code")
    price: float = Field(..., gt=0, description="Price of the purchased packet")
    expires_at: datetime = Field(..., description="Packet expiration timestamp")

class DataPacketCreate(BaseModel):
    package_id: int = Field(..., gt=0, description="ID of the data package being purchased")

class DataPacketResponse(DataPacketBase):
    id: int
    user_id: int
    package_id: int
    is_active: bool

    class Config:
        from_attributes = True


# ----------------- TRANSACTION SCHEMAS -----------------
class TransactionBase(BaseModel):
    amount: float = Field(..., gt=0, description="Transaction amount")
    transaction_type: str = Field(..., description="Type of transaction ('credit' or 'debit')")
    status: str = Field(..., description="Status ('pending', 'completed', 'failed')")
    description: Optional[str] = Field(None, description="Transaction description")

class TransactionCreate(TransactionBase):
    pass

class TransactionResponse(TransactionBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True

#-----------Payment schemas---------- 

class PaymentResponse(BaseModel):
    status: str = Field(..., description="Payment status (success, pending, failed)")
    txn_id: str = Field(..., description="Transaction ID from the payment gateway")
    message: Optional[str] = Field(None, description="Additional payment information")

    class Config:
        from_attributes = True


class PaymentCreate(BaseModel):
    phone_number: str = Field(..., min_length=10, max_length=15, description="Recipient phone number")
    amount: float = Field(..., gt=0, description="Payment amount in KES")
    transaction_id: str = Field(..., description="Unique transaction ID for tracking")

    class Config:
        from_attributes = True


# ----------------- AUTH SCHEMAS -----------------
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    phone_number: Optional[str] = None


# ----------------- ACTIVE SESSION SCHEMAS -----------------

class ActiveSessionCreate(BaseModel):
    user_id: int
    package_id: int
    ip_address: str
    start_time: datetime
    end_time: datetime
    is_active: bool = True


class SessionCreate(BaseModel):
    user_id: int
    package_id: int
    ip_address: str
    start_time: datetime
    end_time: datetime


class SessionBase(BaseModel):
    user_id: int = Field(..., description="User ID associated with the session")
    package_id: int = Field(..., description="Data package ID")
    ip_address: str = Field(..., description="User's IP address")
    start_time: datetime = Field(..., description="Session start time")
    end_time: datetime = Field(..., description="Session end time")

class SessionResponse(SessionBase):
    id: int
    is_active: bool = Field(..., description="Indicates if the session is currently active")

    class Config:
        from_attributes = True
