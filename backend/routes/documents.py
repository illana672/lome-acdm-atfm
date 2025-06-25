from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend import models, schemas
from backend.database import get_db

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/", response_model=schemas.Document)
def create_document(document: schemas.DocumentCreate, db: Session = Depends(get_db)):
    db_doc = models.Document(**document.dict())
    db.add(db_doc)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.get("/", response_model=list[schemas.Document])
def read_documents(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(models.Document).offset(skip).limit(limit).all()

@router.get("/{doc_id}", response_model=schemas.Document)
def read_document(doc_id: int, db: Session = Depends(get_db)):
    doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    return doc

@router.put("/{doc_id}", response_model=schemas.Document)
def update_document(doc_id: int, document: schemas.DocumentUpdate, db: Session = Depends(get_db)):
    db_doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    for key, value in document.dict(exclude_unset=True).items():
        setattr(db_doc, key, value)
    db.commit()
    db.refresh(db_doc)
    return db_doc

@router.delete("/{doc_id}", response_model=dict)
def delete_document(doc_id: int, db: Session = Depends(get_db)):
    db_doc = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not db_doc:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    db.delete(db_doc)
    db.commit()
    return {"ok": True}