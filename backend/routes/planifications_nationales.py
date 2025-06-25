from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/planifications_nationales", tags=["planifications_nationales"])

@router.post("/", response_model=schemas.PlanificationNationale)
def create_planification(planif: schemas.PlanificationNationaleCreate, db: Session = Depends(get_db)):
    db_planif = models.PlanificationNationale(**planif.dict())
    db.add(db_planif)
    db.commit()
    db.refresh(db_planif)
    return db_planif

@router.get("/", response_model=list[schemas.PlanificationNationale])
def list_planifications(db: Session = Depends(get_db)):
    return db.query(models.PlanificationNationale).all()

@router.get("/{planif_id}", response_model=schemas.PlanificationNationale)
def get_planification(planif_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.PlanificationNationale).filter(models.PlanificationNationale.id == planif_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Planification non trouvée")
    return obj

@router.put("/{planif_id}", response_model=schemas.PlanificationNationale)
def update_planification(planif_id: int, planif: schemas.PlanificationNationaleUpdate, db: Session = Depends(get_db)):
    obj = db.query(models.PlanificationNationale).filter(models.PlanificationNationale.id == planif_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Planification non trouvée")
    for attr, value in planif.dict().items():
        setattr(obj, attr, value)
    db.commit()
    db.refresh(obj)
    return obj

@router.delete("/{planif_id}")
def delete_planification(planif_id: int, db: Session = Depends(get_db)):
    obj = db.query(models.PlanificationNationale).filter(models.PlanificationNationale.id == planif_id).first()
    if not obj:
        raise HTTPException(status_code=404, detail="Planification non trouvée")
    db.delete(obj)
    db.commit()
    return {"ok": True}