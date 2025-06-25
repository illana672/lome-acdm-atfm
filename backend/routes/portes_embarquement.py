from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db
from backend.schemas import PorteEmbarquement, PorteEmbarquementCreate, PorteEmbarquementUpdate

router = APIRouter()

@router.post("/portes_embarquement/", response_model=schemas.PorteEmbarquement)
def create_porte(porte: schemas.PorteEmbarquementCreate, db: Session = Depends(get_db)):
    db_porte = models.PorteEmbarquement(**porte.dict())
    db.add(db_porte)
    db.commit()
    db.refresh(db_porte)
    return db_porte

@router.get("/portes_embarquement/", response_model=list[schemas.PorteEmbarquement])
def read_portes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.PorteEmbarquement).offset(skip).limit(limit).all()

@router.get("/portes_embarquement/{porte_id}", response_model=schemas.PorteEmbarquement)
def read_porte(porte_id: int, db: Session = Depends(get_db)):
    porte = db.query(models.PorteEmbarquement).filter(models.PorteEmbarquement.id == porte_id).first()
    if porte is None:
        raise HTTPException(status_code=404, detail="Porte d'embarquement non trouvée")
    return porte

@router.put("/portes_embarquement/{porte_id}", response_model=schemas.PorteEmbarquement)
def update_porte(porte_id: int, porte_update: schemas.PorteEmbarquementUpdate, db: Session = Depends(get_db)):
    porte = db.query(models.PorteEmbarquement).filter(models.PorteEmbarquement.id == porte_id).first()
    if porte is None:
        raise HTTPException(status_code=404, detail="Porte d'embarquement non trouvée")
    for field, value in porte_update.dict().items():
        setattr(porte, field, value)
    db.commit()
    db.refresh(porte)
    return porte

@router.delete("/portes_embarquement/{porte_id}", response_model=schemas.PorteEmbarquement)
def delete_porte(porte_id: int, db: Session = Depends(get_db)):
    porte = db.query(models.PorteEmbarquement).filter(models.PorteEmbarquement.id == porte_id).first()
    if porte is None:
        raise HTTPException(status_code=404, detail="Porte d'embarquement non trouvée")
    db.delete(porte)
    db.commit()
    return porte