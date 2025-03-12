from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get database credentials from environment variables
MYSQL_USER = os.getenv("MYSQL_USER")  # Key is "MYSQL_USER"
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")  # Key is "MYSQL_PASSWORD"
MYSQL_DB = os.getenv("MYSQL_DB")  # Key is "MYSQL_DB"

# Construct the database URL
DATABASE_URL = f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@localhost/{MYSQL_DB}"

# Print the database URL for debugging
print(f"Database URL: {DATABASE_URL}")

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create a configured Session class
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# Create a base class for declarative models
Base = declarative_base()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()