from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(
    prefix="/audit_logs",
    tags=["audit_logs"]
)

@router.post("/", response_model=schemas.AuditLog)
def create_audit_log(audit_log: schemas.AuditLogCreate, db: Session = Depends(get_db)):
    db_log = models.AuditLog(**audit_log.dict())
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.get("/", response_model=list[schemas.AuditLog])
def read_audit_logs(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.AuditLog).offset(skip).limit(limit).all()

@router.get("/{audit_log_id}", response_model=schemas.AuditLog)
def read_audit_log(audit_log_id: int, db: Session = Depends(get_db)):
    log = db.query(models.AuditLog).filter(models.AuditLog.id == audit_log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    return log

@router.put("/{audit_log_id}", response_model=schemas.AuditLog)
def update_audit_log(audit_log_id: int, update: schemas.AuditLogUpdate, db: Session = Depends(get_db)):
    db_log = db.query(models.AuditLog).filter(models.AuditLog.id == audit_log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    for key, value in update.dict(exclude_unset=True).items():
        setattr(db_log, key, value)
    db.commit()
    db.refresh(db_log)
    return db_log

@router.delete("/{audit_log_id}", response_model=dict)
def delete_audit_log(audit_log_id: int, db: Session = Depends(get_db)):
    db_log = db.query(models.AuditLog).filter(models.AuditLog.id == audit_log_id).first()
    if not db_log:
        raise HTTPException(status_code=404, detail="Audit log not found")
    db.delete(db_log)
    db.commit()
    return {"ok": True}