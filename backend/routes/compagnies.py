from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/compagnies")

@router.post("/compagnies/", response_model=schemas.Compagnie)
def create_compagnie(compagnie: schemas.CompagnieCreate, db: Session = Depends(get_db)):
    db_compagnie = models.Compagnie(**compagnie.dict())
    db.add(db_compagnie)
    db.commit()
    db.refresh(db_compagnie)
    return db_compagnie

@router.get("/compagnies/", response_model=list[schemas.Compagnie])
def read_compagnies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Compagnie).offset(skip).limit(limit).all()

@router.get("/compagnies/{compagnie_id}", response_model=schemas.Compagnie)
def read_compagnie(compagnie_id: int, db: Session = Depends(get_db)):
    compagnie = db.query(models.Compagnie).filter(models.Compagnie.id == compagnie_id).first()
    if not compagnie:
        raise HTTPException(status_code=404, detail="Compagnie non trouvée")
    return compagnie

@router.put("/compagnies/{compagnie_id}", response_model=schemas.Compagnie)
def update_compagnie(compagnie_id: int, compagnie: schemas.CompagnieUpdate, db: Session = Depends(get_db)):
    db_compagnie = db.query(models.Compagnie).filter(models.Compagnie.id == compagnie_id).first()
    if not db_compagnie:
        raise HTTPException(status_code=404, detail="Compagnie non trouvée")
    for field, value in compagnie.dict(exclude_unset=True).items():
        setattr(db_compagnie, field, value)
    db.commit()
    db.refresh(db_compagnie)
    return db_compagnie

@router.delete("/compagnies/{compagnie_id}", response_model=schemas.Compagnie)
def delete_compagnie(compagnie_id: int, db: Session = Depends(get_db)):
    db_compagnie = db.query(models.Compagnie).filter(models.Compagnie.id == compagnie_id).first()
    if not db_compagnie:
        raise HTTPException(status_code=404, detail="Compagnie non trouvée")
    db.delete(db_compagnie)
    db.commit()
    return db_compagnie