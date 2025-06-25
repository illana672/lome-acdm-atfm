from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/logs_systeme", tags=["logs_systeme"])

@router.post("/", response_model=schemas.LogSysteme)
def create_log_systeme(log: schemas.LogSystemeCreate, db: Session = Depends(get_db)):
    db_log = models.LogSysteme(**log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/", response_model=list[schemas.LogSysteme])
def read_logs_systeme(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.LogSysteme).offset(skip).limit(limit).all()

@router.get("/{log_id}", response_model=schemas.LogSysteme)
def read_log_systeme(log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.LogSysteme).filter(models.LogSysteme.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log non trouvé")
    return log

@router.put("/{log_id}", response_model=schemas.LogSysteme)
def update_log_systeme(log_id: int, update: schemas.LogSystemeUpdate, db: Session = Depends(get_db)):
    db_log = db.query(models.LogSysteme).filter(models.LogSysteme.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log non trouvé")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/{log_id}", response_model=dict)
def delete_log_systeme(log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(models.LogSysteme).filter(models.LogSysteme.id == log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Log non trouvé")
    db.delete(db_log)
    db.commit()
    return {"ok": True}