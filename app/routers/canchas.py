from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import Cancha as CanchaModel
from app.schemas.schemas import Cancha as CanchaSchema, CanchaCreate

router = APIRouter(prefix="/canchas", tags=["Canchas"])

@router.get("/", response_model=list[CanchaSchema])
def listar(db: Session = Depends(get_db)):
    return db.query(CanchaModel).all()

@router.post("/", response_model=CanchaSchema)
def crear(data: CanchaCreate, db: Session = Depends(get_db)):
    c = CanchaModel(**data.dict())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@router.put("/{id}", response_model=CanchaSchema)
def actualizar(id: int, data: CanchaCreate, db: Session = Depends(get_db)):
    c = db.query(CanchaModel).filter(CanchaModel.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    for key, value in data.dict().items():
        setattr(c, key, value)
    db.commit()
    db.refresh(c)
    return c

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    c = db.query(CanchaModel).filter(CanchaModel.id == id).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cancha no encontrada")
    db.delete(c)
    db.commit()
    return {"detail": "Cancha eliminada"}