from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/messages_atfm", tags=["messages_atfm"])

@router.post("/", response_model=schemas.MessageATFM)
def create_message(message: schemas.MessageATFMCreate, db: Session = Depends(get_db)):
    db_message = models.MessageATFM(**message.dict())
    db.add(db_message)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.get("/", response_model=list[schemas.MessageATFM])
def read_messages(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.MessageATFM).offset(skip).limit(limit).all()

@router.get("/{message_id}", response_model=schemas.MessageATFM)
def read_message(message_id: int, db: Session = Depends(get_db)):
    msg = db.query(models.MessageATFM).filter(models.MessageATFM.id == message_id).first()
    if not msg:
        raise HTTPException(status_code=404, detail="Message not found")
    return msg

@router.put("/{message_id}", response_model=schemas.MessageATFM)
def update_message(message_id: int, message: schemas.MessageATFMUpdate, db: Session = Depends(get_db)):
    db_message = db.query(models.MessageATFM).filter(models.MessageATFM.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    for key, value in message.dict(exclude_unset=True).items():
        setattr(db_message, key, value)
    db.commit()
    db.refresh(db_message)
    return db_message

@router.delete("/{message_id}", response_model=dict)
def delete_message(message_id: int, db: Session = Depends(get_db)):
    db_message = db.query(models.MessageATFM).filter(models.MessageATFM.id == message_id).first()
    if not db_message:
        raise HTTPException(status_code=404, detail="Message not found")
    db.delete(db_message)
    db.commit()
    return {"ok": True}