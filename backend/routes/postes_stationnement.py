from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/postes_stationnement",
    tags=["postes_stationnement"]
)

# CREATE
@router.post("/", response_model=schemas.PosteStationnement)
def create_poste_stationnement(poste: schemas.PosteStationnementCreate, db: Session = Depends(get_db)):
    db_poste = models.PosteStationnement(**poste.dict())
    db.add(db_poste)
    db.commit()
    db.refresh(db_poste)
    return db_poste

# READ ALL
@router.get("/", response_model=List[schemas.PosteStationnement])
def get_postes_stationnement(db: Session = Depends(get_db)):
    return db.query(models.PosteStationnement).all()

# READ BY ID
@router.get("/{poste_id}", response_model=schemas.PosteStationnement)
def get_poste_stationnement(poste_id: int, db: Session = Depends(get_db)):
    poste = db.query(models.PosteStationnement).filter(models.PosteStationnement.id == poste_id).first()
    if not poste:
        raise HTTPException(status_code=404, detail="Poste de stationnement non trouvé")
    return poste

# UPDATE
@router.put("/{poste_id}", response_model=schemas.PosteStationnement)
def update_poste_stationnement(poste_id: int, poste_update: schemas.PosteStationnementUpdate, db: Session = Depends(get_db)):
    poste = db.query(models.PosteStationnement).filter(models.PosteStationnement.id == poste_id).first()
    if not poste:
        raise HTTPException(status_code=404, detail="Poste de stationnement non trouvé")
    for key, value in poste_update.dict(exclude_unset=True).items():
        setattr(poste, key, value)
    db.commit()
    db.refresh(poste)
    return poste

# DELETE
@router.delete("/{poste_id}")
def delete_poste_stationnement(poste_id: int, db: Session = Depends(get_db)):
    poste = db.query(models.PosteStationnement).filter(models.PosteStationnement.id == poste_id).first()
    if not poste:
        raise HTTPException(status_code=404, detail="Poste de stationnement non trouvé")
    db.delete(poste)
    db.commit()
    return {"detail": "Poste de stationnement supprimé"}