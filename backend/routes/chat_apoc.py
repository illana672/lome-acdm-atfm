from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/chat_apoc", tags=["chat_apoc"])

@router.post("/", response_model=schemas.ChatAPOC)
def create_chat_apoc(chat: schemas.ChatAPOCCreate, db: Session = Depends(get_db)):
    db_chat = models.ChatAPOC(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.get("/", response_model=list[schemas.ChatAPOC])
def read_chats_apoc(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ChatAPOC).offset(skip).limit(limit).all()

@router.get("/{chat_id}", response_model=schemas.ChatAPOC)
def read_chat_apoc(chat_id: int, db: Session = Depends(get_db)):
    chat = db.query(models.ChatAPOC).filter(models.ChatAPOC.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Message chat APOC non trouvé")
    return chat

@router.put("/{chat_id}", response_model=schemas.ChatAPOC)
def update_chat_apoc(chat_id: int, chat_data: schemas.ChatAPOCUpdate, db: Session = Depends(get_db)):
    db_chat = db.query(models.ChatAPOC).filter(models.ChatAPOC.id == chat_id).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Message chat APOC non trouvé")
    for key, value in chat_data.dict(exclude_unset=True).items():
        setattr(db_chat, key, value)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@router.delete("/{chat_id}", response_model=dict)
def delete_chat_apoc(chat_id: int, db: Session = Depends(get_db)):
    db_chat = db.query(models.ChatAPOC).filter(models.ChatAPOC.id == chat_id).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Message chat APOC non trouvé")
    db.delete(db_chat)
    db.commit()
    return {"ok": True}