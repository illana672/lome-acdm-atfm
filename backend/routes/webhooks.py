from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/", response_model=schemas.Webhook)
def create_webhook(webhook: schemas.WebhookCreate, db: Session = Depends(get_db)):
    db_webhook = models.Webhook(**webhook.dict())
    db.add(db_webhook)
    db.commit()
    db.refresh(db_webhook)
    return db_webhook

@router.get("/", response_model=list[schemas.Webhook])
def read_webhooks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Webhook).offset(skip).limit(limit).all()

@router.get("/{webhook_id}", response_model=schemas.Webhook)
def read_webhook(webhook_id: int, db: Session = Depends(get_db)):
    webhook = db.query(models.Webhook).filter(models.Webhook.id == webhook_id).first()
    if not webhook:
        raise HTTPException(status_code=404, detail="Webhook non trouvé")
    return webhook

@router.put("/{webhook_id}", response_model=schemas.Webhook)
def update_webhook(webhook_id: int, webhook: schemas.WebhookUpdate, db: Session = Depends(get_db)):
    db_webhook = db.query(models.Webhook).filter(models.Webhook.id == webhook_id).first()
    if not db_webhook:
        raise HTTPException(status_code=404, detail="Webhook non trouvé")
    for key, value in webhook.dict(exclude_unset=True).items():
        setattr(db_webhook, key, value)
    db.commit()
    db.refresh(db_webhook)
    return db_webhook

@router.delete("/{webhook_id}", response_model=dict)
def delete_webhook(webhook_id: int, db: Session = Depends(get_db)):
    db_webhook = db.query(models.Webhook).filter(models.Webhook.id == webhook_id).first()
    if not db_webhook:
        raise HTTPException(status_code=404, detail="Webhook non trouvé")
    db.delete(db_webhook)
    db.commit()
    return {"ok": True}