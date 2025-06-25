from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/communication_interne",
    tags=["communication_interne"]
)

@router.post("/", response_model=schemas.CommunicationInterne)
def create_communication_interne(data: schemas.CommunicationInterneCreate, db: Session = Depends(get_db)):
    db_comm = models.CommunicationInterne(**data.dict())
    db.add(db_comm)
    db.commit()
    db.refresh(db_comm)
    return db_comm

@router.get("/", response_model=list[schemas.CommunicationInterne])
def read_communications(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.CommunicationInterne).offset(skip).limit(limit).all()

@router.get("/{comm_id}", response_model=schemas.CommunicationInterne)
def read_communication(comm_id: int, db: Session = Depends(get_db)):
    comm = db.query(models.CommunicationInterne).filter(models.CommunicationInterne.id == comm_id).first()
    if not comm:
        raise HTTPException(status_code=404, detail="CommunicationInterne not found")
    return comm

@router.put("/{comm_id}", response_model=schemas.CommunicationInterne)
def update_communication(comm_id: int, updates: schemas.CommunicationInterneUpdate, db: Session = Depends(get_db)):
    db_comm = db.query(models.CommunicationInterne).filter(models.CommunicationInterne.id == comm_id).first()
    if not db_comm:
        raise HTTPException(status_code=404, detail="CommunicationInterne not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_comm, key, value)
    db.commit()
    db.refresh(db_comm)
    return db_comm

@router.delete("/{comm_id}", response_model=dict)
def delete_communication(comm_id: int, db: Session = Depends(get_db)):
    db_comm = db.query(models.CommunicationInterne).filter(models.CommunicationInterne.id == comm_id).first()
    if not db_comm:
        raise HTTPException(status_code=404, detail="CommunicationInterne not found")
    db.delete(db_comm)
    db.commit()
    return {"ok": True}