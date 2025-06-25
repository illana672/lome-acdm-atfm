from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/sources_donnees",
    tags=["sources_donnees"]
)

@router.post("/", response_model=schemas.SourceDonnees)
def create_source_donnees(source: schemas.SourceDonneesCreate, db: Session = Depends(get_db)):
    db_source = models.SourceDonnees(**source.dict())
    db.add(db_source)
    db.commit()
    db.refresh(db_source)
    return db_source

@router.get("/", response_model=list[schemas.SourceDonnees])
def read_sources_donnees(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SourceDonnees).offset(skip).limit(limit).all()

@router.get("/{source_id}", response_model=schemas.SourceDonnees)
def read_source_donnees(source_id: int, db: Session = Depends(get_db)):
    source = db.query(models.SourceDonnees).filter(models.SourceDonnees.id == source_id).first()
    if not source:
        raise HTTPException(status_code=404, detail="SourceDonnees not found")
    return source

@router.put("/{source_id}", response_model=schemas.SourceDonnees)
def update_source_donnees(source_id: int, updates: schemas.SourceDonneesUpdate, db: Session = Depends(get_db)):
    db_source = db.query(models.SourceDonnees).filter(models.SourceDonnees.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="SourceDonnees not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_source, key, value)
    db.commit()
    db.refresh(db_source)
    return db_source

@router.delete("/{source_id}", response_model=dict)
def delete_source_donnees(source_id: int, db: Session = Depends(get_db)):
    db_source = db.query(models.SourceDonnees).filter(models.SourceDonnees.id == source_id).first()
    if not db_source:
        raise HTTPException(status_code=404, detail="SourceDonnees not found")
    db.delete(db_source)
    db.commit()
    return {"ok": True}