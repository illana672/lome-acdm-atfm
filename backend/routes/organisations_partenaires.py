from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/organisations_partenaires",
    tags=["organisations_partenaires"]
)

@router.post("/", response_model=schemas.OrganisationPartenaire)
def create_organisation(org: schemas.OrganisationPartenaireCreate, db: Session = Depends(get_db)):
    db_org = models.OrganisationPartenaire(**org.dict())
    db.add(db_org)
    db.commit()
    db.refresh(db_org)
    return db_org

@router.get("/", response_model=list[schemas.OrganisationPartenaire])
def read_organisations(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.OrganisationPartenaire).offset(skip).limit(limit).all()

@router.get("/{org_id}", response_model=schemas.OrganisationPartenaire)
def read_organisation(org_id: int, db: Session = Depends(get_db)):
    org = db.query(models.OrganisationPartenaire).filter(models.OrganisationPartenaire.id == org_id).first()
    if not org:
        raise HTTPException(status_code=404, detail="OrganisationPartenaire not found")
    return org

@router.put("/{org_id}", response_model=schemas.OrganisationPartenaire)
def update_organisation(org_id: int, updates: schemas.OrganisationPartenaireUpdate, db: Session = Depends(get_db)):
    db_org = db.query(models.OrganisationPartenaire).filter(models.OrganisationPartenaire.id == org_id).first()
    if not db_org:
        raise HTTPException(status_code=404, detail="OrganisationPartenaire not found")
    for key, value in updates.dict(exclude_unset=True).items():
        setattr(db_org, key, value)
    db.commit()
    db.refresh(db_org)
    return db_org

@router.delete("/{org_id}", response_model=dict)
def delete_organisation(org_id: int, db: Session = Depends(get_db)):
    db_org = db.query(models.OrganisationPartenaire).filter(models.OrganisationPartenaire.id == org_id).first()
    if not db_org:
        raise HTTPException(status_code=404, detail="OrganisationPartenaire not found")
    db.delete(db_org)
    db.commit()
    return {"ok": True}