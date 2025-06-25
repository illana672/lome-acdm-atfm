from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/groupes_communication",
    tags=["groupes_communication"]
)

@router.post("/", response_model=schemas.GroupeCommunication)
def create_groupe_communication(groupe: schemas.GroupeCommunicationCreate, db: Session = Depends(get_db)):
    db_groupe = models.GroupeCommunication(**groupe.dict())
    db.add(db_groupe)
    db.commit()
    db.refresh(db_groupe)
    return db_groupe

@router.get("/", response_model=list[schemas.GroupeCommunication])
def read_groupes_communication(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GroupeCommunication).offset(skip).limit(limit).all()

@router.get("/{groupe_id}", response_model=schemas.GroupeCommunication)
def read_groupe_communication(groupe_id: int, db: Session = Depends(get_db)):
    groupe = db.query(models.GroupeCommunication).filter(models.GroupeCommunication.id == groupe_id).first()
    if not groupe:
        raise HTTPException(status_code=404, detail="GroupeCommunication not found")
    return groupe

@router.put("/{groupe_id}", response_model=schemas.GroupeCommunication)
def update_groupe_communication(groupe_id: int, updates: schemas.GroupeCommunicationUpdate, db: Session = Depends(get_db)):
    db_groupe = db.query(models.GroupeCommunication).filter(models.GroupeCommunication.id == groupe_id).first()
    if not db_groupe:
        raise HTTPException(status_code=404, detail="GroupeCommunication not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_groupe, key, value)
    db.commit()
    db.refresh(db_groupe)
    return db_groupe

@router.delete("/{groupe_id}", response_model=dict)
def delete_groupe_communication(groupe_id: int, db: Session = Depends(get_db)):
    db_groupe = db.query(models.GroupeCommunication).filter(models.GroupeCommunication.id == groupe_id).first()
    if not db_groupe:
        raise HTTPException(status_code=404, detail="GroupeCommunication not found")
    db.delete(db_groupe)
    db.commit()
    return {"ok": True}