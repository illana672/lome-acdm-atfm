from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/notifications_websocket",
    tags=["notifications_websocket"]
)

@router.post("/", response_model=schemas.NotificationWebsocketOut, status_code=201)
def create_notification(notification: schemas.NotificationWebsocketCreate, db: Session = Depends(get_db)):
    db_notification = models.NotificationWebsocket(**notification.dict())
    db.add(db_notification)
    db.commit()
    db.refresh(db_notification)
    return db_notification

@router.get("/", response_model=list[schemas.NotificationWebsocketOut])
def read_notifications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.NotificationWebsocket).offset(skip).limit(limit).all()

@router.get("/{notification_id}", response_model=schemas.NotificationWebsocketOut)
def read_notification(notification_id: int, db: Session = Depends(get_db)):
    notif = db.query(models.NotificationWebsocket).filter(models.NotificationWebsocket.id == notification_id).first()
    if not notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    return notif

@router.put("/{notification_id}", response_model=schemas.NotificationWebsocketOut)
def update_notification(notification_id: int, notification: schemas.NotificationWebsocketUpdate, db: Session = Depends(get_db)):
    db_notif = db.query(models.NotificationWebsocket).filter(models.NotificationWebsocket.id == notification_id).first()
    if not db_notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    for key, value in notification.dict(exclude_unset=True).items():
        setattr(db_notif, key, value)
    db.commit()
    db.refresh(db_notif)
    return db_notif

@router.delete("/{notification_id}")
def delete_notification(notification_id: int, db: Session = Depends(get_db)):
    db_notif = db.query(models.NotificationWebsocket).filter(models.NotificationWebsocket.id == notification_id).first()
    if not db_notif:
        raise HTTPException(status_code=404, detail="Notification not found")
    db.delete(db_notif)
    db.commit()
    return {"ok": True}