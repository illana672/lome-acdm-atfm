from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/sessions_apoc", tags=["sessions_apoc"])

@router.post("/", response_model=schemas.SessionAPOC)
def create_session_apoc(session: schemas.SessionAPOCCreate, db: Session = Depends(get_db)):
    db_session = models.SessionAPOC(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/", response_model=list[schemas.SessionAPOC])
def read_sessions_apoc(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.SessionAPOC).offset(skip).limit(limit).all()

@router.get("/{session_id}", response_model=schemas.SessionAPOC)
def read_session_apoc(session_id: int, db: Session = Depends(get_db)):
    session = db.query(models.SessionAPOC).filter(models.SessionAPOC.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session APOC non trouvée")
    return session

@router.put("/{session_id}", response_model=schemas.SessionAPOC)
def update_session_apoc(session_id: int, session_data: schemas.SessionAPOCUpdate, db: Session = Depends(get_db)):
    session_db = db.query(models.SessionAPOC).filter(models.SessionAPOC.id == session_id).first()
    if not session_db:
        raise HTTPException(status_code=404, detail="Session APOC non trouvée")
    for key, value in session_data.dict(exclude_unset=True).items():
        setattr(session_db, key, value)
    db.commit()
    db.refresh(session_db)
    return session_db

@router.delete("/{session_id}", response_model=dict)
def delete_session_apoc(session_id: int, db: Session = Depends(get_db)):
    session_db = db.query(models.SessionAPOC).filter(models.SessionAPOC.id == session_id).first()
    if not session_db:
        raise HTTPException(status_code=404, detail="Session APOC non trouvée")
    db.delete(session_db)
    db.commit()
    return {"ok": True}