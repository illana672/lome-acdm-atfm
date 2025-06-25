from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/maintenance", tags=["maintenance"])

@router.post("/", response_model=schemas.Maintenance)
def create_maintenance(maintenance: schemas.MaintenanceCreate, db: Session = Depends(get_db)):
    db_maintenance = models.Maintenance(**maintenance.dict())
    db.add(db_maintenance)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

@router.get("/", response_model=list[schemas.Maintenance])
def read_maintenances(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Maintenance).offset(skip).limit(limit).all()

@router.get("/{maintenance_id}", response_model=schemas.Maintenance)
def read_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    maintenance = db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()
    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance non trouvée")
    return maintenance

@router.put("/{maintenance_id}", response_model=schemas.Maintenance)
def update_maintenance(maintenance_id: int, update: schemas.MaintenanceUpdate, db: Session = Depends(get_db)):
    db_maintenance = db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance non trouvée")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_maintenance, key, value)
    db.commit()
    db.refresh(db_maintenance)
    return db_maintenance

@router.delete("/{maintenance_id}", response_model=dict)
def delete_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    db_maintenance = db.query(models.Maintenance).filter(models.Maintenance.id == maintenance_id).first()
    if not db_maintenance:
        raise HTTPException(status_code=404, detail="Maintenance non trouvée")
    db.delete(db_maintenance)
    db.commit()
    return {"ok": True}