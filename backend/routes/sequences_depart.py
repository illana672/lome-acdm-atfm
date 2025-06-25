from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/sequences_depart",
    tags=["sequences_depart"]
)

@router.post("/", response_model=schemas.SequenceDepart)
def create_sequence_depart(sequence: schemas.SequenceDepartCreate, db: Session = Depends(get_db)):
    db_seq = models.SequenceDepart(**sequence.dict())
    db.add(db_seq)
    db.commit()
    db.refresh(db_seq)
    return db_seq

@router.get("/", response_model=list[schemas.SequenceDepart])
def read_sequences_depart(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SequenceDepart).offset(skip).limit(limit).all()

@router.get("/{seq_id}", response_model=schemas.SequenceDepart)
def read_sequence_depart(seq_id: int, db: Session = Depends(get_db)):
    seq = db.query(models.SequenceDepart).filter(models.SequenceDepart.id == seq_id).first()
    if not seq:
        raise HTTPException(status_code=404, detail="SequenceDepart not found")
    return seq

@router.put("/{seq_id}", response_model=schemas.SequenceDepart)
def update_sequence_depart(seq_id: int, updates: schemas.SequenceDepartUpdate, db: Session = Depends(get_db)):
    db_seq = db.query(models.SequenceDepart).filter(models.SequenceDepart.id == seq_id).first()
    if not db_seq:
        raise HTTPException(status_code=404, detail="SequenceDepart not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_seq, key, value)
    db.commit()
    db.refresh(db_seq)
    return db_seq

@router.delete("/{seq_id}", response_model=dict)
def delete_sequence_depart(seq_id: int, db: Session = Depends(get_db)):
    db_seq = db.query(models.SequenceDepart).filter(models.SequenceDepart.id == seq_id).first()
    if not db_seq:
        raise HTTPException(status_code=404, detail="SequenceDepart not found")
    db.delete(db_seq)
    db.commit()
    return {"ok": True}