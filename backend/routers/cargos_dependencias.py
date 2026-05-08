from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Cargo, Dependencia
from schemas import CargoCreate, CargoOut, DependenciaCreate, DependenciaOut
from typing import List

# ── CARGOS ─────────────────────────────────────────────────────────────────
cargos_router = APIRouter(prefix="/cargos", tags=["Cargos"])

@cargos_router.get("/", response_model=List[CargoOut])
def listar_cargos(db: Session = Depends(get_db)):
    return db.query(Cargo).all()

@cargos_router.post("/", response_model=CargoOut, status_code=201)
def crear_cargo(data: CargoCreate, db: Session = Depends(get_db)):
    c = Cargo(**data.model_dump())
    db.add(c)
    db.commit()
    db.refresh(c)
    return c

@cargos_router.put("/{id_cargo}", response_model=CargoOut)
def actualizar_cargo(id_cargo: int, data: CargoCreate, db: Session = Depends(get_db)):
    c = db.query(Cargo).filter(Cargo.id_cargo == id_cargo).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    c.descripcion = data.descripcion
    db.commit()
    db.refresh(c)
    return c

@cargos_router.delete("/{id_cargo}", status_code=204)
def eliminar_cargo(id_cargo: int, db: Session = Depends(get_db)):
    c = db.query(Cargo).filter(Cargo.id_cargo == id_cargo).first()
    if not c:
        raise HTTPException(status_code=404, detail="Cargo no encontrado")
    db.delete(c)
    db.commit()


# ── DEPENDENCIAS ───────────────────────────────────────────────────────────
dependencias_router = APIRouter(prefix="/dependencias", tags=["Dependencias"])

@dependencias_router.get("/", response_model=List[DependenciaOut])
def listar_dep(db: Session = Depends(get_db)):
    return db.query(Dependencia).all()

@dependencias_router.post("/", response_model=DependenciaOut, status_code=201)
def crear_dep(data: DependenciaCreate, db: Session = Depends(get_db)):
    d = Dependencia(**data.model_dump())
    db.add(d)
    db.commit()
    db.refresh(d)
    return d

@dependencias_router.put("/{id_dependencia}", response_model=DependenciaOut)
def actualizar_dep(id_dependencia: int, data: DependenciaCreate, db: Session = Depends(get_db)):
    d = db.query(Dependencia).filter(Dependencia.id_dependencia == id_dependencia).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dependencia no encontrada")
    d.descripcion = data.descripcion
    db.commit()
    db.refresh(d)
    return d

@dependencias_router.delete("/{id_dependencia}", status_code=204)
def eliminar_dep(id_dependencia: int, db: Session = Depends(get_db)):
    d = db.query(Dependencia).filter(Dependencia.id_dependencia == id_dependencia).first()
    if not d:
        raise HTTPException(status_code=404, detail="Dependencia no encontrada")
    db.delete(d)
    db.commit()
