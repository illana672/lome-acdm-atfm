from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/affectations_ressources", tags=["affectations_ressources"])

@router.post("/", response_model=schemas.AffectationRessource)
def create_affectation(aff: schemas.AffectationRessourceCreate, db: Session = Depends(get_db)):
    db_aff = models.AffectationRessource(**aff.dict())
    db.add(db_aff)
    db.commit()
    db.refresh(db_aff)
    return db_aff

@router.get("/", response_model=list[schemas.AffectationRessource])
def read_affectations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AffectationRessource).offset(skip).limit(limit).all()

@router.get("/{affectation_id}", response_model=schemas.AffectationRessource)
def read_affectation(affectation_id: int, db: Session = Depends(get_db)):
    aff = db.query(models.AffectationRessource).filter(models.AffectationRessource.id == affectation_id).first()
    if not aff:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    return aff

@router.put("/{affectation_id}", response_model=schemas.AffectationRessource)
def update_affectation(affectation_id: int, update: schemas.AffectationRessourceUpdate, db: Session = Depends(get_db)):
    db_aff = db.query(models.AffectationRessource).filter(models.AffectationRessource.id == affectation_id).first()
    if not db_aff:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_aff, key, value)
    db.commit()
    db.refresh(db_aff)
    return db_aff

@router.delete("/{affectation_id}", response_model=dict)
def delete_affectation(affectation_id: int, db: Session = Depends(get_db)):
    db_aff = db.query(models.AffectationRessource).filter(models.AffectationRessource.id == affectation_id).first()
    if not db_aff:
        raise HTTPException(status_code=404, detail="Affectation non trouvée")
    db.delete(db_aff)
    db.commit()
    return {"ok": True}