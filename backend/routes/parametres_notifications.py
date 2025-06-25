from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, schemas

router = APIRouter(
    prefix="/parametres_notifications",
    tags=["parametres_notifications"]
)

@router.post("/", response_model=schemas.ParametresNotificationsOut, status_code=201)
def create_param_notification(param: schemas.ParametresNotificationsCreate, db: Session = Depends(get_db)):
    db_param = models.ParametresNotifications(**param.dict())
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param

@router.get("/", response_model=list[schemas.ParametresNotificationsOut])
def read_param_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ParametresNotifications).offset(skip).limit(limit).all()

@router.get("/{param_id}", response_model=schemas.ParametresNotificationsOut)
def read_param_notification(param_id: int, db: Session = Depends(get_db)):
    param = db.query(models.ParametresNotifications).filter(models.ParametresNotifications.id == param_id).first()
    if not param:
        raise HTTPException(status_code=404, detail="Paramètre notification non trouvé")
    return param

@router.put("/{param_id}", response_model=schemas.ParametresNotificationsOut)
def update_param_notification(param_id: int, param: schemas.ParametresNotificationsUpdate, db: Session = Depends(get_db)):
    db_param = db.query(models.ParametresNotifications).filter(models.ParametresNotifications.id == param_id).first()
    if not db_param:
        raise HTTPException(status_code=404, detail="Paramètre notification non trouvé")
    for key, value in param.dict(exclude_unset=True).items():
        setattr(db_param, key, value)
    db.commit()
    db.refresh(db_param)
    return db_param

@router.delete("/{param_id}")
def delete_param_notification(param_id: int, db: Session = Depends(get_db)):
    db_param = db.query(models.ParametresNotifications).filter(models.ParametresNotifications.id == param_id).first()
    if not db_param:
        raise HTTPException(status_code=404, detail="Paramètre notification non trouvé")
    db.delete(db_param)
    db.commit()
    return {"ok": True}