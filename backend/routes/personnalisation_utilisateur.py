from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/personnalisation_utilisateur", tags=["personnalisation_utilisateur"])

@router.post("/", response_model=schemas.PersonnalisationUtilisateur)
def create_personnalisation(personnalisation: schemas.PersonnalisationUtilisateurCreate, db: Session = Depends(get_db)):
    db_personnalisation = models.PersonnalisationUtilisateur(**personnalisation.dict())
    db.add(db_personnalisation)
    db.commit()
    db.refresh(db_personnalisation)
    return db_personnalisation

@router.get("/", response_model=list[schemas.PersonnalisationUtilisateur])
def read_personnalisations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.PersonnalisationUtilisateur).offset(skip).limit(limit).all()

@router.get("/{personnalisation_id}", response_model=schemas.PersonnalisationUtilisateur)
def read_personnalisation(personnalisation_id: int, db: Session = Depends(get_db)):
    p = db.query(models.PersonnalisationUtilisateur).filter(models.PersonnalisationUtilisateur.id == personnalisation_id).first()
    if not p:
        raise HTTPException(status_code=404, detail="Personnalisation non trouvée")
    return p

@router.put("/{personnalisation_id}", response_model=schemas.PersonnalisationUtilisateur)
def update_personnalisation(personnalisation_id: int, update: schemas.PersonnalisationUtilisateurUpdate, db: Session = Depends(get_db)):
    db_p = db.query(models.PersonnalisationUtilisateur).filter(models.PersonnalisationUtilisateur.id == personnalisation_id).first()
    if not db_p:
        raise HTTPException(status_code=404, detail="Personnalisation non trouvée")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_p, key, value)
    db.commit()
    db.refresh(db_p)
    return db_p

@router.delete("/{personnalisation_id}", response_model=dict)
def delete_personnalisation(personnalisation_id: int, db: Session = Depends(get_db)):
    db_p = db.query(models.PersonnalisationUtilisateur).filter(models.PersonnalisationUtilisateur.id == personnalisation_id).first()
    if not db_p:
        raise HTTPException(status_code=404, detail="Personnalisation non trouvée")
    db.delete(db_p)
    db.commit()
    return {"ok": True}