from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Rol, UsuarioRol
from schemas import RolCreate, RolOut
from typing import List

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.get("/", response_model=List[RolOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Rol).all()


@router.get("/{id_rol}", response_model=RolOut)
def obtener(id_rol: int, db: Session = Depends(get_db)):
    r = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return r


@router.post("/", response_model=RolOut, status_code=201)
def crear(data: RolCreate, db: Session = Depends(get_db)):
    if db.query(Rol).filter(Rol.nombre_rol == data.nombre_rol).first():
        raise HTTPException(status_code=400, detail="Nombre de rol ya existe")
    r = Rol(**data.model_dump())
    db.add(r)
    db.commit()
    db.refresh(r)
    return r


@router.put("/{id_rol}", response_model=RolOut)
def actualizar(id_rol: int, data: RolCreate, db: Session = Depends(get_db)):
    r = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    r.nombre_rol  = data.nombre_rol
    r.descripcion = data.descripcion
    db.commit()
    db.refresh(r)
    return r


@router.delete("/{id_rol}", status_code=204)
def eliminar(id_rol: int, db: Session = Depends(get_db)):
    r = db.query(Rol).filter(Rol.id_rol == id_rol).first()
    if not r:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    # Eliminar primero las asignaciones usuario_roles para evitar error de FK
    db.query(UsuarioRol).filter(UsuarioRol.id_rol == id_rol).delete()
    db.delete(r)
    db.commit()
