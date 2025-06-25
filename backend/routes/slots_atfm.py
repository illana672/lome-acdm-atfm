from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/slots_atfm",
    tags=["slots_atfm"]
)

@router.post("/", response_model=schemas.SlotATFM)
def create_slot_atfm(slot: schemas.SlotATFMCreate, db: Session = Depends(get_db)):
    db_slot = models.SlotATFM(**slot.dict())
    db.add(db_slot)
    db.commit()
    db.refresh(db_slot)
    return db_slot

@router.get("/", response_model=list[schemas.SlotATFM])
def read_slots(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SlotATFM).offset(skip).limit(limit).all()

@router.get("/{slot_id}", response_model=schemas.SlotATFM)
def read_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(models.SlotATFM).filter(models.SlotATFM.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot ATFM not found")
    return slot

@router.put("/{slot_id}", response_model=schemas.SlotATFM)
def update_slot(slot_id: int, slot_update: schemas.SlotATFMUpdate, db: Session = Depends(get_db)):
    slot = db.query(models.SlotATFM).filter(models.SlotATFM.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot ATFM not found")
    for key, value in slot_update.dict(exclude_unset=True).items():
        setattr(slot, key, value)
    db.commit()
    db.refresh(slot)
    return slot

@router.delete("/{slot_id}")
def delete_slot(slot_id: int, db: Session = Depends(get_db)):
    slot = db.query(models.SlotATFM).filter(models.SlotATFM.id == slot_id).first()
    if not slot:
        raise HTTPException(status_code=404, detail="Slot ATFM not found")
    db.delete(slot)
    db.commit()
    return {"ok": True}