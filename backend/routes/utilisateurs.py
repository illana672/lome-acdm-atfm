from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from backend.database import get_db
from backend import models, schemas

router = APIRouter(
    prefix="/utilisateurs",
    tags=["utilisateurs"]
)

@router.post("/", response_model=schemas.Utilisateur)
def create_utilisateur(utilisateur: schemas.UtilisateurCreate, db: Session = Depends(get_db)):
    # Vérifier si l'email existe déjà
    db_user = db.query(models.Utilisateur).filter(models.Utilisateur.email == utilisateur.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé")
    db_utilisateur = models.Utilisateur(**utilisateur.dict())
    db.add(db_utilisateur)
    db.commit()
    db.refresh(db_utilisateur)
    return db_utilisateur

@router.get("/", response_model=List[schemas.Utilisateur])
def get_utilisateurs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Utilisateur).offset(skip).limit(limit).all()

@router.get("/{utilisateur_id}", response_model=schemas.Utilisateur)
def get_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    return utilisateur

@router.put("/{utilisateur_id}", response_model=schemas.Utilisateur)
def update_utilisateur(utilisateur_id: int, utilisateur_update: schemas.UtilisateurUpdate, db: Session = Depends(get_db)):
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    for var, value in utilisateur_update.dict(exclude_unset=True).items():
        setattr(utilisateur, var, value)
    db.commit()
    db.refresh(utilisateur)
    return utilisateur

@router.delete("/{utilisateur_id}")
def delete_utilisateur(utilisateur_id: int, db: Session = Depends(get_db)):
    utilisateur = db.query(models.Utilisateur).filter(models.Utilisateur.id == utilisateur_id).first()
    if not utilisateur:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db.delete(utilisateur)
    db.commit()
    return {"ok": True}