from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import Reserva as ReservaModel
from app.schemas.schemas import Reserva as ReservaSchema, ReservaCreate
from sqlalchemy import and_

router = APIRouter(prefix="/reservas", tags=["Reservas"])

@router.get("/", response_model=list[ReservaSchema])
def listar(db: Session = Depends(get_db)):
    return db.query(ReservaModel).all()

@router.post("/", response_model=ReservaSchema)
def crear(data: ReservaCreate, db: Session = Depends(get_db)):
    # simple overlap check
    if data.cancha_id:
        conflict = db.query(ReservaModel).filter(
            ReservaModel.cancha_id == data.cancha_id,
            ReservaModel.fecha == data.fecha,
            ReservaModel.hora_inicio < data.hora_fin,
            ReservaModel.hora_fin > data.hora_inicio
        ).first()
        if conflict:
            raise HTTPException(400, "Solapamiento con otra reserva")
    r = ReservaModel(**data.dict())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r

@router.put("/{id}", response_model=ReservaSchema)
def actualizar(id: int, data: ReservaCreate, db: Session = Depends(get_db)):
    r = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    # simple overlap check
    if data.cancha_id:
        conflict = db.query(ReservaModel).filter(
            ReservaModel.cancha_id == data.cancha_id,
            ReservaModel.fecha == data.fecha,
            ReservaModel.hora_inicio < data.hora_fin,
            ReservaModel.hora_fin > data.hora_inicio,
            ReservaModel.id != id
        ).first()
        if conflict:
            raise HTTPException(400, "Solapamiento con otra reserva")
    for key, value in data.dict().items():
        setattr(r, key, value)
    db.commit()
    db.refresh(r)
    return r

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    r = db.query(ReservaModel).filter(ReservaModel.id == id).first()
    if not r:
        raise HTTPException(status_code=404, detail="Reserva no encontrada")
    db.delete(r)
    db.commit()
    return {"detail": "Reserva eliminada"}