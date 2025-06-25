from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/milestones",
    tags=["milestones"]
)

@router.post("/", response_model=schemas.Milestone)
def create_milestone(milestone: schemas.MilestoneCreate, db: Session = Depends(get_db)):
    db_milestone = models.Milestone(**milestone.dict())
    db.add(db_milestone)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.get("/", response_model=list[schemas.Milestone])
def read_milestones(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Milestone).offset(skip).limit(limit).all()

@router.get("/{milestone_id}", response_model=schemas.Milestone)
def read_milestone(milestone_id: int, db: Session = Depends(get_db)):
    milestone = db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()
    if not milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    return milestone

@router.put("/{milestone_id}", response_model=schemas.Milestone)
def update_milestone(milestone_id: int, updates: schemas.MilestoneUpdate, db: Session = Depends(get_db)):
    db_milestone = db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_milestone, key, value)
    db.commit()
    db.refresh(db_milestone)
    return db_milestone

@router.delete("/{milestone_id}", response_model=dict)
def delete_milestone(milestone_id: int, db: Session = Depends(get_db)):
    db_milestone = db.query(models.Milestone).filter(models.Milestone.id == milestone_id).first()
    if not db_milestone:
        raise HTTPException(status_code=404, detail="Milestone not found")
    db.delete(db_milestone)
    db.commit()
    return {"ok": True}