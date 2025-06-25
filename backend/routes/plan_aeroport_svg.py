# routes/plan_aeroport_svg.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from backend.models import PlanAeroportSVG, Vol
from backend.schemas import PlanAeroportSVG, PlanAeroportSVGCreate, PlanAeroportSVGUpdate
from backend.database import get_db

router = APIRouter(prefix="/plans", tags=["plan_aeroport_svg"])

@router.post("/", response_model=PlanAeroportSVG)
def create_plan(plan: PlanAeroportSVGCreate, db: Session = Depends(get_db)):
    # Optionnel: vérifier que vol_id existe
    if plan.vol_id is not None:
        vol = db.query(Vol).filter(Vol.id == plan.vol_id).first()
        if not vol:
            raise HTTPException(status_code=404, detail="Vol not found")
    db_plan = PlanAeroportSVG(**plan.dict())
    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.get("/", response_model=List[PlanAeroportSVG])
def read_plans(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return db.query(PlanAeroportSVG).offset(skip).limit(limit).all()

@router.get("/{plan_id}", response_model=PlanAeroportSVG)
def read_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = db.query(PlanAeroportSVG).filter(PlanAeroportSVG.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.put("/{plan_id}", response_model=PlanAeroportSVG)
def update_plan(plan_id: int, plan: PlanAeroportSVGUpdate, db: Session = Depends(get_db)):
    db_plan = db.query(PlanAeroportSVG).filter(PlanAeroportSVG.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    for key, value in plan.dict(exclude_unset=True).items():
        setattr(db_plan, key, value)
    db.commit()
    db.refresh(db_plan)
    return db_plan

@router.delete("/{plan_id}", response_model=dict)
def delete_plan(plan_id: int, db: Session = Depends(get_db)):
    db_plan = db.query(PlanAeroportSVG).filter(PlanAeroportSVG.id == plan_id).first()
    if not db_plan:
        raise HTTPException(status_code=404, detail="Plan not found")
    db.delete(db_plan)
    db.commit()
    return {"ok": True}