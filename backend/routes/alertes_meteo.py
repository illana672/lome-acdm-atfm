from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/alertes_meteo", tags=["alertes_meteo"])

@router.post("/", response_model=schemas.AlerteMeteo)
def create_alerte_meteo(alerte: schemas.AlerteMeteoCreate, db: Session = Depends(get_db)):
    db_alerte = models.AlerteMeteo(**alerte.dict())
    db.add(db_alerte)
    db.commit()
    db.refresh(db_alerte)
    return db_alerte

@router.get("/", response_model=list[schemas.AlerteMeteo])
def read_alertes_meteo(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AlerteMeteo).offset(skip).limit(limit).all()

@router.get("/{alerte_id}", response_model=schemas.AlerteMeteo)
def read_alerte_meteo(alerte_id: int, db: Session = Depends(get_db)):
    alerte = db.query(models.AlerteMeteo).filter(models.AlerteMeteo.id == alerte_id).first()
    if not alerte:
        raise HTTPException(status_code=404, detail="Alerte météo non trouvée")
    return alerte

@router.put("/{alerte_id}", response_model=schemas.AlerteMeteo)
def update_alerte_meteo(alerte_id: int, alerte_data: schemas.AlerteMeteoUpdate, db: Session = Depends(get_db)):
    db_alerte = db.query(models.AlerteMeteo).filter(models.AlerteMeteo.id == alerte_id).first()
    if not db_alerte:
        raise HTTPException(status_code=404, detail="Alerte météo non trouvée")
    for key, value in alerte_data.dict(exclude_unset=True).items():
        setattr(db_alerte, key, value)
    db.commit()
    db.refresh(db_alerte)
    return db_alerte

@router.delete("/{alerte_id}", response_model=dict)
def delete_alerte_meteo(alerte_id: int, db: Session = Depends(get_db)):
    db_alerte = db.query(models.AlerteMeteo).filter(models.AlerteMeteo.id == alerte_id).first()
    if not db_alerte:
        raise HTTPException(status_code=404, detail="Alerte météo non trouvée")
    db.delete(db_alerte)
    db.commit()
    return {"ok": True}