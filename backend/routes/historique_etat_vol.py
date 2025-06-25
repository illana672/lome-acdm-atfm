from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/historique_etat_vol", tags=["historique_etat_vol"])

@router.post("/", response_model=schemas.HistoriqueEtatVol)
def create_historique_etat_vol(historique: schemas.HistoriqueEtatVolCreate, db: Session = Depends(get_db)):
    db_histo = models.HistoriqueEtatVol(**historique.dict())
    db.add(db_histo)
    db.commit()
    db.refresh(db_histo)
    return db_histo

@router.get("/", response_model=list[schemas.HistoriqueEtatVol])
def read_historiques_etat_vol(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.HistoriqueEtatVol).offset(skip).limit(limit).all()

@router.get("/{histo_id}", response_model=schemas.HistoriqueEtatVol)
def read_historique_etat_vol(histo_id: int, db: Session = Depends(get_db)):
    histo = db.query(models.HistoriqueEtatVol).filter(models.HistoriqueEtatVol.id == histo_id).first()
    if not histo:
        raise HTTPException(status_code=404, detail="Historique non trouvé")
    return histo

@router.put("/{histo_id}", response_model=schemas.HistoriqueEtatVol)
def update_historique_etat_vol(histo_id: int, historique: schemas.HistoriqueEtatVolUpdate, db: Session = Depends(get_db)):
    db_histo = db.query(models.HistoriqueEtatVol).filter(models.HistoriqueEtatVol.id == histo_id).first()
    if not db_histo:
        raise HTTPException(status_code=404, detail="Historique non trouvé")
    for key, value in historique.dict(exclude_unset=True).items():
        setattr(db_histo, key, value)
    db.commit()
    db.refresh(db_histo)
    return db_histo

@router.delete("/{histo_id}", response_model=dict)
def delete_historique_etat_vol(histo_id: int, db: Session = Depends(get_db)):
    db_histo = db.query(models.HistoriqueEtatVol).filter(models.HistoriqueEtatVol.id == histo_id).first()
    if not db_histo:
        raise HTTPException(status_code=404, detail="Historique non trouvé")
    db.delete(db_histo)
    db.commit()
    return {"ok": True}