from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import crud, schemas
from app.database import get_db  # Changed import from dependencies to database

router = APIRouter()

@router.get("/packages/{name}", response_model=schemas.DataPackage)
def get_package_by_name(name: str, db: Session = Depends(get_db)):
    package = crud.get_package_by_name(db, name)
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")
    return package

@router.post("/packages", response_model=schemas.DataPackage)
def create_package(package: schemas.DataPackageCreate, db: Session = Depends(get_db)):
    return crud.create_data_package(db, package)

@router.get("/", response_model=list[schemas.DataPackageResponse])
def get_all_packages(db: Session = Depends(get_db)):
    """
    Retrieve all available data packages.
    """
    return crud.get_all_data_packages(db)

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