from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/gantt_sequencement",
    tags=["gantt_sequencement"]
)

@router.post("/", response_model=schemas.GanttSequencement)
def create_gantt_seq(seq: schemas.GanttSequencementCreate, db: Session = Depends(get_db)):
    # Vérifier que le vol existe
    if not db.query(models.Vol).filter(models.Vol.id == seq.vol_id).first():
        raise HTTPException(status_code=404, detail="Vol non trouvé")
    db_seq = models.GanttSequencement(**seq.dict())
    db.add(db_seq)
    db.commit()
    db.refresh(db_seq)
    return db_seq

@router.get("/", response_model=list[schemas.GanttSequencement])
def read_gantt_seq_list(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GanttSequencement).offset(skip).limit(limit).all()

@router.get("/{seq_id}", response_model=schemas.GanttSequencement)
def read_gantt_seq(seq_id: int, db: Session = Depends(get_db)):
    seq = db.query(models.GanttSequencement).filter(models.GanttSequencement.id == seq_id).first()
    if not seq:
        raise HTTPException(status_code=404, detail="Gantt Sequencement non trouvé")
    return seq

@router.put("/{seq_id}", response_model=schemas.GanttSequencement)
def update_gantt_seq(seq_id: int, updates: schemas.GanttSequencementUpdate, db: Session = Depends(get_db)):
    seq = db.query(models.GanttSequencement).filter(models.GanttSequencement.id == seq_id).first()
    if not seq:
        raise HTTPException(status_code=404, detail="Gantt Sequencement non trouvé")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(seq, key, value)
    db.commit()
    db.refresh(seq)
    return seq

@router.delete("/{seq_id}")
def delete_gantt_seq(seq_id: int, db: Session = Depends(get_db)):
    seq = db.query(models.GanttSequencement).filter(models.GanttSequencement.id == seq_id).first()
    if not seq:
        raise HTTPException(status_code=404, detail="Gantt Sequencement non trouvé")
    db.delete(seq)
    db.commit()
    return {"ok": True}
