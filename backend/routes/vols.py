
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter()

@router.post("/vols/", response_model=schemas.Vol)
def create_vol(vol: schemas.VolCreate, db: Session = Depends(get_db)):
    db_vol = models.Vol(**vol.dict())
    db.add(db_vol)
    db.commit()
    db.refresh(db_vol)
    return db_vol

@router.get("/vols/", response_model=list[schemas.Vol])
def read_vols(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Vol).offset(skip).limit(limit).all()

@router.get("/vols/{vol_id}", response_model=schemas.Vol)
def read_vol(vol_id: int, db: Session = Depends(get_db)):
    vol = db.query(models.Vol).filter(models.Vol.id == vol_id).first()
    if not vol:
        raise HTTPException(status_code=404, detail="Vol non trouvé")
    return vol

@router.put("/vols/{vol_id}", response_model=schemas.Vol)
def update_vol(vol_id: int, vol_update: schemas.VolUpdate, db: Session = Depends(get_db)):
    db_vol = db.query(models.Vol).filter(models.Vol.id == vol_id).first()
    if not db_vol:
        raise HTTPException(status_code=404, detail="Vol non trouvé")
    for field, value in vol_update.dict(exclude_unset=True).items():
        setattr(db_vol, field, value)
    db.commit()
    db.refresh(db_vol)
    return db_vol

@router.delete("/vols/{vol_id}", response_model=schemas.Vol)
def delete_vol(vol_id: int, db: Session = Depends(get_db)):
    db_vol = db.query(models.Vol).filter(models.Vol.id == vol_id).first()
    if not db_vol:
        raise HTTPException(status_code=404, detail="Vol non trouvé")
    db.delete(db_vol)
    db.commit()
    return db_vol