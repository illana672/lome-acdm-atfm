from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/meteo", tags=["meteo"])

@router.post("/", response_model=schemas.Meteo)
def create_meteo(meteo: schemas.MeteoCreate, db: Session = Depends(get_db)):
    db_meteo = models.Meteo(**meteo.dict())
    db.add(db_meteo)
    db.commit()
    db.refresh(db_meteo)
    return db_meteo

@router.get("/", response_model=list[schemas.Meteo])
def read_meteos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Meteo).offset(skip).limit(limit).all()

@router.get("/{meteo_id}", response_model=schemas.Meteo)
def read_meteo(meteo_id: int, db: Session = Depends(get_db)):
    meteo = db.query(models.Meteo).filter(models.Meteo.id == meteo_id).first()
    if not meteo:
        raise HTTPException(status_code=404, detail="Meteo not found")
    return meteo

@router.put("/{meteo_id}", response_model=schemas.Meteo)
def update_meteo(meteo_id: int, meteo: schemas.MeteoUpdate, db: Session = Depends(get_db)):
    db_meteo = db.query(models.Meteo).filter(models.Meteo.id == meteo_id).first()
    if not db_meteo:
        raise HTTPException(status_code=404, detail="Meteo not found")
    for key, value in meteo.dict(exclude_unset=True).items():
        setattr(db_meteo, key, value)
    db.commit()
    db.refresh(db_meteo)
    return db_meteo

@router.delete("/{meteo_id}", response_model=dict)
def delete_meteo(meteo_id: int, db: Session = Depends(get_db)):
    db_meteo = db.query(models.Meteo).filter(models.Meteo.id == meteo_id).first()
    if not db_meteo:
        raise HTTPException(status_code=404, detail="Meteo not found")
    db.delete(db_meteo)
    db.commit()
    return {"ok": True}