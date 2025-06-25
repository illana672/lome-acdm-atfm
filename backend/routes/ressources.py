from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/ressources", tags=["ressources"])

@router.post("/", response_model=schemas.Ressource)
def create_ressource(ressource: schemas.RessourceCreate, db: Session = Depends(get_db)):
    db_ressource = models.Ressource(**ressource.dict())
    db.add(db_ressource)
    db.commit()
    db.refresh(db_ressource)
    return db_ressource

@router.get("/", response_model=list[schemas.Ressource])
def read_ressources(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Ressource).offset(skip).limit(limit).all()

@router.get("/{ressource_id}", response_model=schemas.Ressource)
def read_ressource(ressource_id: int, db: Session = Depends(get_db)):
    ressource = db.query(models.Ressource).filter(models.Ressource.id == ressource_id).first()
    if not ressource:
        raise HTTPException(status_code=404, detail="Ressource non trouvée")
    return ressource

@router.put("/{ressource_id}", response_model=schemas.Ressource)
def update_ressource(ressource_id: int, update: schemas.RessourceUpdate, db: Session = Depends(get_db)):
    db_ressource = db.query(models.Ressource).filter(models.Ressource.id == ressource_id).first()
    if not db_ressource:
        raise HTTPException(status_code=404, detail="Ressource non trouvée")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_ressource, key, value)
    db.commit()
    db.refresh(db_ressource)
    return db_ressource

@router.delete("/{ressource_id}", response_model=dict)
def delete_ressource(ressource_id: int, db: Session = Depends(get_db)):
    db_ressource = db.query(models.Ressource).filter(models.Ressource.id == ressource_id).first()
    if not db_ressource:
        raise HTTPException(status_code=404, detail="Ressource non trouvée")
    db.delete(db_ressource)
    db.commit()
    return {"ok": True}
