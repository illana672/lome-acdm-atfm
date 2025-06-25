from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/incidents_techniques", tags=["incidents_techniques"])

@router.post("/", response_model=schemas.IncidentTechnique)
def create_incident(incident: schemas.IncidentTechniqueCreate, db: Session = Depends(get_db)):
    db_incident = models.IncidentTechnique(**incident.dict())
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.get("/", response_model=list[schemas.IncidentTechnique])
def read_incidents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.IncidentTechnique).offset(skip).limit(limit).all()

@router.get("/{incident_id}", response_model=schemas.IncidentTechnique)
def read_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(models.IncidentTechnique).filter(models.IncidentTechnique.id == incident_id).first()
    if not incident:
        raise HTTPException(status_code=404, detail="Incident technique non trouvé")
    return incident

@router.put("/{incident_id}", response_model=schemas.IncidentTechnique)
def update_incident(incident_id: int, update: schemas.IncidentTechniqueUpdate, db: Session = Depends(get_db)):
    db_incident = db.query(models.IncidentTechnique).filter(models.IncidentTechnique.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident technique non trouvé")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_incident, key, value)
    db.commit()
    db.refresh(db_incident)
    return db_incident

@router.delete("/{incident_id}", response_model=dict)
def delete_incident(incident_id: int, db: Session = Depends(get_db)):
    db_incident = db.query(models.IncidentTechnique).filter(models.IncidentTechnique.id == incident_id).first()
    if not db_incident:
        raise HTTPException(status_code=404, detail="Incident technique non trouvé")
    db.delete(db_incident)
    db.commit()
    return {"ok": True}