from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importing the routers
from app.routers import users, transactions, sessions, packets, packages
from app.database import engine, Base

# Initialize FastAPI app
app = FastAPI(
    title="Wi-Fi Subscription System",
    description="A FastAPI-powered system for managing Wi-Fi subscriptions with MPESA payment, session tracking, and data packets.",
    version="1.0.0"
)

# Set up database tables
Base.metadata.create_all(bind=engine)

# CORS middleware (optional, for cross-origin requests)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict to specific domains later
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allow all headers
)

# Include Routers
app.include_router(users.router)
app.include_router(transactions.router)
app.include_router(sessions.router)
app.include_router(packets.router)
app.include_router(packages.router)

# Root Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Wi-Fi Subscription System!"}

# Health Check Endpoint
@app.get("/health")
def health_check():
    return {"status": "OK"}
