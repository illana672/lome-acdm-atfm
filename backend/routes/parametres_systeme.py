from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/parametres_systeme",
    tags=["parametres_systeme"]
)

@router.post("/", response_model=schemas.ParametreSysteme)
def create_parametre(parametre: schemas.ParametreSystemeCreate, db: Session = Depends(get_db)):
    db_param = models.ParametreSysteme(**parametre.dict())
    db.add(db_param)
    db.commit()
    db.refresh(db_param)
    return db_param

@router.get("/", response_model=list[schemas.ParametreSysteme])
def read_parametres(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.ParametreSysteme).offset(skip).limit(limit).all()

@router.get("/{param_id}", response_model=schemas.ParametreSysteme)
def read_parametre(param_id: int, db: Session = Depends(get_db)):
    param = db.query(models.ParametreSysteme).filter(models.ParametreSysteme.id == param_id).first()
    if not param:
        raise HTTPException(status_code=404, detail="ParametreSysteme not found")
    return param

@router.put("/{param_id}", response_model=schemas.ParametreSysteme)
def update_parametre(param_id: int, updates: schemas.ParametreSystemeUpdate, db: Session = Depends(get_db)):
    db_param = db.query(models.ParametreSysteme).filter(models.ParametreSysteme.id == param_id).first()
    if not db_param:
        raise HTTPException(status_code=404, detail="ParametreSysteme not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_param, key, value)
    db.commit()
    db.refresh(db_param)
    return db_param

@router.delete("/{param_id}", response_model=dict)
def delete_parametre(param_id: int, db: Session = Depends(get_db)):
    db_param = db.query(models.ParametreSysteme).filter(models.ParametreSysteme.id == param_id).first()
    if not db_param:
        raise HTTPException(status_code=404, detail="ParametreSysteme not found")
    db.delete(db_param)
    db.commit()
    return {"ok": True}