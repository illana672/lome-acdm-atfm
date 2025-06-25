from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter()

@router.post("/avions/", response_model=schemas.Avion)
def create_avion(avion: schemas.AvionCreate, db: Session = Depends(get_db)):
    db_avion = db.query(models.Avion).filter_by(immatriculation=avion.immatriculation).first()
    if db_avion:
        raise HTTPException(status_code=400, detail="L'avion existe déjà")
    new_avion = models.Avion(**avion.dict())
    db.add(new_avion)
    db.commit()
    db.refresh(new_avion)
    return new_avion

@router.get("/avions/", response_model=list[schemas.Avion])
def read_avions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Avion).offset(skip).limit(limit).all()

@router.get("/avions/{avion_id}", response_model=schemas.Avion)
def read_avion(avion_id: int, db: Session = Depends(get_db)):
    avion = db.query(models.Avion).filter(models.Avion.id == avion_id).first()
    if not avion:
        raise HTTPException(status_code=404, detail="Avion non trouvé")
    return avion

@router.put("/avions/{avion_id}", response_model=schemas.Avion)
def update_avion(avion_id: int, avion_update: schemas.AvionUpdate, db: Session = Depends(get_db)):
    avion = db.query(models.Avion).filter(models.Avion.id == avion_id).first()
    if not avion:
        raise HTTPException(status_code=404, detail="Avion non trouvé")
    for key, value in avion_update.dict(exclude_unset=True).items():
        setattr(avion, key, value)
    db.commit()
    db.refresh(avion)
    return avion

@router.delete("/avions/{avion_id}", response_model=schemas.Avion)
def delete_avion(avion_id: int, db: Session = Depends(get_db)):
    avion = db.query(models.Avion).filter(models.Avion.id == avion_id).first()
    if not avion:
        raise HTTPException(status_code=404, detail="Avion non trouvé")
    db.delete(avion)
    db.commit()
    return avion