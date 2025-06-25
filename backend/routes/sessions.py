from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession
from backend.database import get_db
from backend import models, schemas

router = APIRouter(
    prefix="/sessions",
    tags=["sessions"]
)

@router.post("/", response_model=schemas.SessionOut, status_code=201)
def create_session(session: schemas.SessionCreate, db: DBSession = Depends(get_db)):
    # Vérification unicité jeton
    if db.query(models.Session).filter(models.Session.jeton_session == session.jeton_session).first():
        raise HTTPException(status_code=400, detail="Jeton déjà existant")
    db_session = models.Session(**session.dict())
    db.add(db_session)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.get("/", response_model=list[schemas.SessionOut])
def read_sessions(skip: int = 0, limit: int = 100, db: DBSession = Depends(get_db)):
    return db.query(models.Session).offset(skip).limit(limit).all()

@router.get("/{session_id}", response_model=schemas.SessionOut)
def read_session(session_id: int, db: DBSession = Depends(get_db)):
    session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    return session

@router.put("/{session_id}", response_model=schemas.SessionOut)
def update_session(session_id: int, update: schemas.SessionUpdate, db: DBSession = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_session, key, value)
    db.commit()
    db.refresh(db_session)
    return db_session

@router.delete("/{session_id}")
def delete_session(session_id: int, db: DBSession = Depends(get_db)):
    db_session = db.query(models.Session).filter(models.Session.id == session_id).first()
    if not db_session:
        raise HTTPException(status_code=404, detail="Session non trouvée")
    db.delete(db_session)
    db.commit()
    return {"ok": True}