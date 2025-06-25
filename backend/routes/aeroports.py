from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import models, schemas
from backend.database import get_db  # adapte à ton projet

router = APIRouter(
    prefix="/aeroports",
    tags=["aeroports"],
)

# Create
@router.post("/", response_model=schemas.AeroportOut)
def create_aeroport(aeroport: schemas.AeroportCreate, db: Session = Depends(get_db)):
    db_aeroport = models.Aeroport(**aeroport.dict())
    db.add(db_aeroport)
    db.commit()
    db.refresh(db_aeroport)
    return db_aeroport

# Read all
@router.get("/", response_model=List[schemas.AeroportOut])
def read_aeroports(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Aeroport).offset(skip).limit(limit).all()

# Read one
@router.get("/{aeroport_id}", response_model=schemas.AeroportOut)
def read_aeroport(aeroport_id: int, db: Session = Depends(get_db)):
    aeroport = db.query(models.Aeroport).get(aeroport_id)
    if not aeroport:
        raise HTTPException(status_code=404, detail="Aeroport not found")
    return aeroport

# Update
@router.put("/{aeroport_id}", response_model=schemas.AeroportOut)
def update_aeroport(aeroport_id: int, aeroport: schemas.AeroportUpdate, db: Session = Depends(get_db)):
    db_aeroport = db.query(models.Aeroport).get(aeroport_id)
    if not db_aeroport:
        raise HTTPException(status_code=404, detail="Aeroport not found")
    for k, v in aeroport.dict(exclude_unset=True).items():
        setattr(db_aeroport, k, v)
    db.commit()
    db.refresh(db_aeroport)
    return db_aeroport

# Delete
@router.delete("/{aeroport_id}")
def delete_aeroport(aeroport_id: int, db: Session = Depends(get_db)):
    db_aeroport = db.query(models.Aeroport).get(aeroport_id)
    if not db_aeroport:
        raise HTTPException(status_code=404, detail="Aeroport not found")
    db.delete(db_aeroport)
    db.commit()
    return {"ok": True}