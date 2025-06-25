from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/evenements",
    tags=["evenements"]
)

@router.post("/", response_model=schemas.Evenement)
def create_evenement(evenement: schemas.EvenementCreate, db: Session = Depends(get_db)):
    db_evenement = models.Evenement(**evenement.dict())
    db.add(db_evenement)
    db.commit()
    db.refresh(db_evenement)
    return db_evenement

@router.get("/", response_model=list[schemas.Evenement])
def read_evenements(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Evenement).offset(skip).limit(limit).all()

@router.get("/{evenement_id}", response_model=schemas.Evenement)
def read_evenement(evenement_id: int, db: Session = Depends(get_db)):
    evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id).first()
    if not evenement:
        raise HTTPException(status_code=404, detail="Evenement not found")
    return evenement

@router.put("/{evenement_id}", response_model=schemas.Evenement)
def update_evenement(evenement_id: int, updates: schemas.EvenementUpdate, db: Session = Depends(get_db)):
    db_evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id).first()
    if not db_evenement:
        raise HTTPException(status_code=404, detail="Evenement not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_evenement, key, value)
    db.commit()
    db.refresh(db_evenement)
    return db_evenement

@router.delete("/{evenement_id}", response_model=dict)
def delete_evenement(evenement_id: int, db: Session = Depends(get_db)):
    db_evenement = db.query(models.Evenement).filter(models.Evenement.id == evenement_id).first()
    if not db_evenement:
        raise HTTPException(status_code=404, detail="Evenement not found")
    db.delete(db_evenement)
    db.commit()
    return {"ok": True}