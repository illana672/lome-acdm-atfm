from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/gestion_droits_utilisateurs",
    tags=["gestion_droits_utilisateurs"]
)

@router.post("/", response_model=schemas.GestionDroitsUtilisateurs)
def create_droit(droit: schemas.GestionDroitsUtilisateursCreate, db: Session = Depends(get_db)):
    # Vérifie si l'utilisateur existe
    if not db.query(models.Utilisateur).filter(models.Utilisateur.id == droit.utilisateur_id).first():
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    db_droit = models.GestionDroitsUtilisateurs(**droit.dict())
    db.add(db_droit)
    db.commit()
    db.refresh(db_droit)
    return db_droit

@router.get("/", response_model=list[schemas.GestionDroitsUtilisateurs])
def read_droits(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.GestionDroitsUtilisateurs).offset(skip).limit(limit).all()

@router.get("/{droit_id}", response_model=schemas.GestionDroitsUtilisateurs)
def read_droit(droit_id: int, db: Session = Depends(get_db)):
    droit = db.query(models.GestionDroitsUtilisateurs).filter(models.GestionDroitsUtilisateurs.id == droit_id).first()
    if not droit:
        raise HTTPException(status_code=404, detail="Droit utilisateur non trouvé")
    return droit

@router.put("/{droit_id}", response_model=schemas.GestionDroitsUtilisateurs)
def update_droit(droit_id: int, updates: schemas.GestionDroitsUtilisateursUpdate, db: Session = Depends(get_db)):
    droit = db.query(models.GestionDroitsUtilisateurs).filter(models.GestionDroitsUtilisateurs.id == droit_id).first()
    if not droit:
        raise HTTPException(status_code=404, detail="Droit utilisateur non trouvé")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(droit, key, value)
    db.commit()
    db.refresh(droit)
    return droit

@router.delete("/{droit_id}")
def delete_droit(droit_id: int, db: Session = Depends(get_db)):
    droit = db.query(models.GestionDroitsUtilisateurs).filter(models.GestionDroitsUtilisateurs.id == droit_id).first()
    if not droit:
        raise HTTPException(status_code=404, detail="Droit utilisateur non trouvé")
    db.delete(droit)
    db.commit()
    return {"ok": True}