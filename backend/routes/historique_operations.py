from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend import models, schemas

router = APIRouter(
    prefix="/historique_operations",
    tags=["historique_operations"]
)

# --------------------------
# CRUD logé dans le endpoint
# --------------------------

@router.post("/", response_model=schemas.HistoriqueOperation)
def create_historique_operation(
    historique: schemas.HistoriqueOperationCreate,
    db: Session = Depends(get_db)
):
    db_histo = models.HistoriqueOperation(**historique.dict())
    db.add(db_histo)
    db.commit()
    db.refresh(db_histo)
    return db_histo

@router.get("/", response_model=list[schemas.HistoriqueOperation])
def read_historique_operations(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    return db.query(models.HistoriqueOperation).offset(skip).limit(limit).all()

@router.get("/{historique_id}", response_model=schemas.HistoriqueOperation)
def read_historique_operation(
    historique_id: int,
    db: Session = Depends(get_db)
):
    db_histo = db.query(models.HistoriqueOperation).filter(
        models.HistoriqueOperation.id == historique_id
    ).first()
    if not db_histo:
        raise HTTPException(status_code=404, detail="HistoriqueOperation not found")
    return db_histo