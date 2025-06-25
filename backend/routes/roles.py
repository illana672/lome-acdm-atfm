from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/roles", tags=["roles"])

@router.post("/", response_model=schemas.Role)
def create_role(role: schemas.RoleCreate, db: Session = Depends(get_db)):
    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/", response_model=list[schemas.Role])
def read_roles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Role).offset(skip).limit(limit).all()

@router.get("/{role_id}", response_model=schemas.Role)
def read_role(role_id: int, db: Session = Depends(get_db)):
    role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")
    return role

@router.put("/{role_id}", response_model=schemas.Role)
def update_role(role_id: int, role_update: schemas.RoleUpdate, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    for key, value in role_update.dict(exclude_unset=True).items():
        setattr(db_role, key, value)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.delete("/{role_id}", response_model=dict)
def delete_role(role_id: int, db: Session = Depends(get_db)):
    db_role = db.query(models.Role).filter(models.Role.id == role_id).first()
    if not db_role:
        raise HTTPException(status_code=404, detail="Role not found")
    db.delete(db_role)
    db.commit()
    return {"ok": True}