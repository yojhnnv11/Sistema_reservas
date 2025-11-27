from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import get_db
from app.models.models import Usuario as UsuarioModel
from app.schemas.schemas import Usuario as UsuarioSchema, UsuarioCreate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=list[UsuarioSchema])
def listar(db: Session = Depends(get_db)):
    return db.query(UsuarioModel).all()

@router.post("/", response_model=UsuarioSchema)
def crear(data: UsuarioCreate, db: Session = Depends(get_db)):
    u = UsuarioModel(**data.dict())
    db.add(u)
    db.commit()
    db.refresh(u)
    return u

@router.put("/{id}", response_model=UsuarioSchema)
def actualizar(id: int, data: UsuarioCreate, db: Session = Depends(get_db)):
    u = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    for key, value in data.dict().items():
        setattr(u, key, value)
    db.commit()
    db.refresh(u)
    return u

@router.delete("/{id}")
def eliminar(id: int, db: Session = Depends(get_db)):
    u = db.query(UsuarioModel).filter(UsuarioModel.id == id).first()
    if not u:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db.delete(u)
    db.commit()
    return {"detail": "Usuario eliminado"}  