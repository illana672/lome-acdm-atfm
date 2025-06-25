from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend import models, schemas
from backend.database import get_db
from datetime import datetime

router = APIRouter(
    prefix="/historiques_vols",
    tags=["historiques_vols"]
)

@router.post("/", response_model=schemas.HistoriqueVolOut)
def create_historique_vol(hv: schemas.HistoriqueVolCreate, db: Session = Depends(get_db)):
    db_hv = models.HistoriqueVol(**hv.dict(), enregistrement_date=datetime.utcnow())
    db.add(db_hv)
    db.commit()
    db.refresh(db_hv)
    return db_hv

@router.get("/", response_model=List[schemas.HistoriqueVolOut])
def read_historiques_vols(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.HistoriqueVol).offset(skip).limit(limit).all()

@router.get("/{hv_id}", response_model=schemas.HistoriqueVolOut)
def read_historique_vol(hv_id: int, db: Session = Depends(get_db)):
    hv = db.query(models.HistoriqueVol).get(hv_id)
    if not hv:
        raise HTTPException(status_code=404, detail="HistoriqueVol non trouvé")
    return hv

@router.put("/{hv_id}", response_model=schemas.HistoriqueVolOut)
def update_historique_vol(hv_id: int, hv: schemas.HistoriqueVolUpdate, db: Session = Depends(get_db)):
    db_hv = db.query(models.HistoriqueVol).get(hv_id)
    if not db_hv:
        raise HTTPException(status_code=404, detail="HistoriqueVol non trouvé")
    for k, v in hv.dict(exclude_unset=True).items():
        setattr(db_hv, k, v)
    db.commit()
    db.refresh(db_hv)
    return db_hv

@router.delete("/{hv_id}")
def delete_historique_vol(hv_id: int, db: Session = Depends(get_db)):
    db_hv = db.query(models.HistoriqueVol).get(hv_id)
    if not db_hv:
        raise HTTPException(status_code=404, detail="HistoriqueVol non trouvé")
    db.delete(db_hv)
    db.commit()
    return {"ok": True}