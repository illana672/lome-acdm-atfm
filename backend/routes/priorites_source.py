from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/priorites_source", tags=["priorites_source"])

@router.post("/", response_model=schemas.PrioriteSource)
def create_priorite_source(priorite: schemas.PrioriteSourceCreate, db: Session = Depends(get_db)):
    db_priorite = models.PrioriteSource(**priorite.dict())
    db.add(db_priorite)
    try:
        db.commit()
        db.refresh(db_priorite)
        return db_priorite
    except Exception:
        db.rollback()
        raise HTTPException(status_code=400, detail="Source déjà existante")

@router.get("/", response_model=list[schemas.PrioriteSource])
def list_priorites_source(db: Session = Depends(get_db)):
    return db.query(models.PrioriteSource).all()

@router.get("/{priorite_id}", response_model=schemas.PrioriteSource)
def get_priorite_source(priorite_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.PrioriteSource).filter(models.PrioriteSource.id == priorite_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Priorité non trouvée")
    return obj

@router.put("/{priorite_id}", response_model=schemas.PrioriteSource)
def update_priorite_source(priorite_id: int, priorite: schemas.PrioriteSourceUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.PrioriteSource).filter(models.PrioriteSource.id == priorite_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Priorité non trouvée")
    for attr, value in priorite.dict().items():
        setattr(obj, attr, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{priorite_id}")
def delete_priorite_source(priorite_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.PrioriteSource).filter(models.PrioriteSource.id == priorite_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Priorité non trouvée")
    db.delete(obj)
    db.commit()
    return {"ok": True}