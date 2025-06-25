from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/integration_systemes_externes",
    tags=["integration_systemes_externes"]
)

@router.post("/", response_model=schemas.IntegrationSystemesExternes)
def create_integration(integration: schemas.IntegrationSystemesExternesCreate, db: Session = Depends(get_db)):
    db_integration = models.IntegrationSystemesExternes(**integration.dict())
    db.add(db_integration)
    db.commit()
    db.refresh(db_integration)
    return db_integration

@router.get("/", response_model=list[schemas.IntegrationSystemesExternes])
def read_integrations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.IntegrationSystemesExternes).offset(skip).limit(limit).all()

@router.get("/{integration_id}", response_model=schemas.IntegrationSystemesExternes)
def read_integration(integration_id: int, db: Session = Depends(get_db)):
    item = db.query(models.IntegrationSystemesExternes).filter(models.IntegrationSystemesExternes.id == integration_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Integration systeme externe non trouvée")
    return item

@router.put("/{integration_id}", response_model=schemas.IntegrationSystemesExternes)
def update_integration(integration_id: int, integration_update: schemas.IntegrationSystemesExternesUpdate, db: Session = Depends(get_db)):
    item = db.query(models.IntegrationSystemesExternes).filter(models.IntegrationSystemesExternes.id == integration_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Integration systeme externe non trouvée")
    for key, value in integration_update.dict(exclude_unset=True).items():
        setattr(item, key, value)
    db.commit()
    db.refresh(item)
    return item

@router.delete("/{integration_id}")
def delete_integration(integration_id: int, db: Session = Depends(get_db)):
    item = db.query(models.IntegrationSystemesExternes).filter(models.IntegrationSystemesExternes.id == integration_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Integration systeme externe non trouvée")
    db.delete(item)
    db.commit()
    return {"ok": True}