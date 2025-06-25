from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from backend.database import get_db
from backend import models, schemas

router = APIRouter(
    prefix="/pays",
    tags=["pays"]
)

@router.post("/", response_model=schemas.PaysOut, status_code=201)
def create_pays(pays: schemas.PaysCreate, db: DBSession = Depends(get_db)):
    if db.query(models.Pays).filter(models.Pays.code_iso == pays.code_iso).first():
        raise HTTPException(status_code=400, detail="Code ISO déjà utilisé")
    db_pays = models.Pays(**pays.dict())
    db.add(db_pays)
    db.commit()
    db.refresh(db_pays)
    return db_pays

@router.get("/", response_model=list[schemas.PaysOut])
def read_pays(skip: int = 0, limit: int = 100, db: DBSession = Depends(get_db)):
    return db.query(models.Pays).offset(skip).limit(limit).all()

@router.get("/{pays_id}", response_model=schemas.PaysOut)
def read_one_pays(pays_id: int, db: DBSession = Depends(get_db)):
    pays = db.query(models.Pays).filter(models.Pays.id == pays_id).first()
    if not pays:
        raise HTTPException(status_code=404, detail="Pays non trouvé")
    return pays

@router.put("/{pays_id}", response_model=schemas.PaysOut)
def update_pays(pays_id: int, update: schemas.PaysUpdate, db: DBSession = Depends(get_db)):
    db_pays = db.query(models.Pays).filter(models.Pays.id == pays_id).first()
    if not db_pays:
        raise HTTPException(status_code=404, detail="Pays non trouvé")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_pays, key, value)
    db.commit()
    db.refresh(db_pays)
    return db_pays

@router.delete("/{pays_id}")
def delete_pays(pays_id: int, db: DBSession = Depends(get_db)):
    db_pays = db.query(models.Pays).filter(models.Pays.id == pays_id).first()
    if not db_pays:
        raise HTTPException(status_code=404, detail="Pays non trouvé")
    db.delete(db_pays)
    db.commit()
    return {"ok": True}