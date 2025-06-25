from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import schemas, models
from backend.database import get_db

router = APIRouter()

# Create alerte
@router.post("/alertes/", response_model=schemas.Alerte)
def create_alerte(alerte: schemas.AlerteCreate, db: Session = Depends(get_db)):
    db_alerte = models.Alerte(**alerte.dict())
    db.add(db_alerte)
    db.commit()
    db.refresh(db_alerte)
    return db_alerte

# Read all alertes
@router.get("/alertes/", response_model=list[schemas.Alerte])
def read_alertes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Alerte).offset(skip).limit(limit).all()

# Read one alerte
@router.get("/alertes/{alerte_id}", response_model=schemas.Alerte)
def read_alerte(alerte_id: int, db: Session = Depends(get_db)):
    alerte = db.query(models.Alerte).filter(models.Alerte.id == alerte_id).first()
    if not alerte:
        raise HTTPException(status_code=404, detail="Alerte not found")
    return alerte

# Update alerte
@router.put("/alertes/{alerte_id}", response_model=schemas.Alerte)
def update_alerte(alerte_id: int, alerte: schemas.AlerteUpdate, db: Session = Depends(get_db)):
    db_alerte = db.query(models.Alerte).filter(models.Alerte.id == alerte_id).first()
    if not db_alerte:
        raise HTTPException(status_code=404, detail="Alerte not found")
    for key, value in alerte.dict(exclude_unset=True).items():
        setattr(db_alerte, key, value)
    db.commit()
    db.refresh(db_alerte)
    return db_alerte

# Delete alerte
@router.delete("/alertes/{alerte_id}", response_model=dict)
def delete_alerte(alerte_id: int, db: Session = Depends(get_db)):
    db_alerte = db.query(models.Alerte).filter(models.Alerte.id == alerte_id).first()
    if not db_alerte:
        raise HTTPException(status_code=404, detail="Alerte not found")
    db.delete(db_alerte)
    db.commit()
    return {"ok": True}