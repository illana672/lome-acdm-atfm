from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/taches", tags=["taches"])

@router.post("/", response_model=schemas.Tache)
def create_tache(tache: schemas.TacheCreate, db: Session = Depends(get_db)):
    db_tache = models.Tache(**tache.dict())
    db.add(db_tache)
    db.commit()
    db.refresh(db_tache)
    return db_tache

@router.get("/", response_model=list[schemas.Tache])
def read_taches(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Tache).offset(skip).limit(limit).all()

@router.get("/{tache_id}", response_model=schemas.Tache)
def read_tache(tache_id: int, db: Session = Depends(get_db)):
    tache = db.query(models.Tache).filter(models.Tache.id == tache_id).first()
    if not tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    return tache

@router.put("/{tache_id}", response_model=schemas.Tache)
def update_tache(tache_id: int, tache: schemas.TacheUpdate, db: Session = Depends(get_db)):
    db_tache = db.query(models.Tache).filter(models.Tache.id == tache_id).first()
    if not db_tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    for key, value in tache.dict(exclude_unset=True).items():
        setattr(db_tache, key, value)
    db.commit()
    db.refresh(db_tache)
    return db_tache

@router.delete("/{tache_id}", response_model=dict)
def delete_tache(tache_id: int, db: Session = Depends(get_db)):
    db_tache = db.query(models.Tache).filter(models.Tache.id == tache_id).first()
    if not db_tache:
        raise HTTPException(status_code=404, detail="Tâche non trouvée")
    db.delete(db_tache)
    db.commit()
    return {"ok": True}