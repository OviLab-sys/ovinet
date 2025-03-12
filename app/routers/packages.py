from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import schemas, crud, database

router = APIRouter(prefix="/packages", tags=["Packages"])

# Dependency to get the database session
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.DataPackageResponse)
def create_package(package_data: schemas.DataPackageCreate, db: Session = Depends(get_db)):
    """
    Create a new data package (e.g., 1GB, 10GB plans).
    """
    existing_package = crud.get_package_by_name(db, package_data.name)
    if existing_package:
        raise HTTPException(status_code=400, detail="Package with this name already exists.")
    
    return crud.create_package(db, package_data)

@router.get("/", response_model=list[schemas.DataPackageResponse])
def get_all_packages(db: Session = Depends(get_db)):
    """
    Retrieve all available data packages.
    """
    return crud.get_all_packages(db)

@router.get("/{package_id}", response_model=schemas.DataPackageResponse)
def get_package_by_id(package_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific data package by ID.
    """
    package = crud.get_package_by_id(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found.")
    return package

@router.put("/{package_id}", response_model=schemas.DataPackageResponse)
def update_package(package_id: int, package_data: schemas.DataPackageUpdate, db: Session = Depends(get_db)):
    """
    Update details of a specific data package.
    """
    package = crud.get_package_by_id(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found.")
    
    return crud.update_package(db, package_id, package_data)

@router.delete("/{package_id}", status_code=204)
def delete_package(package_id: int, db: Session = Depends(get_db)):
    """
    Delete a specific data package by ID.
    """
    package = crud.get_package_by_id(db, package_id)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found.")
    
    crud.delete_package(db, package_id)
    return {"message": "Package deleted successfully"}