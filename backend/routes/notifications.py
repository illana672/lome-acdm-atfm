from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from backend.database import get_db
from backend import models, schemas

router = APIRouter(
    prefix="/notifications",
    tags=["notifications"]
)

@router.post("/", response_model=schemas.Notification)
def create_notification(notification: schemas.NotificationCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == notification.utilisateur_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db_notification = models.Notification(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/", response_model=List[schemas.Notification])
def get_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Notification).offset(skip).limit(limit).all()

@router.get("/{notification_id}", response_model=schemas.Notification)
def get_notification(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    return notif

@router.put("/{notification_id}", response_model=schemas.Notification)
def update_notification(notification_id: int, notification: schemas.NotificationUpdate, db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    for var, value in vars(notification).items():
        if value is not None:
            setattr(notif, var, value)
    db.commit()
    db.refresh(notif)
    return notif

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(models.Notification).filter(models.Notification.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification non trouvée")
    db.delete(notif)
    db.commit()
    return {"ok": True}