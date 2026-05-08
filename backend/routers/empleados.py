from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Empleado
from schemas import EmpleadoCreate, EmpleadoUpdate, EmpleadoOut
from typing import List

router = APIRouter(prefix="/empleados", tags=["Empleados"])


def _to_out(e: Empleado) -> EmpleadoOut:
    return EmpleadoOut(
        id_empleado=e.id_empleado, cedula=e.cedula, nombre=e.nombre,
        direccion=e.direccion, telefono=e.telefono,
        id_dependencia=e.id_dependencia, id_cargo=e.id_cargo,
        salario_base=e.salario_base, fecha_ingreso=e.fecha_ingreso,
        estado=e.estado,
        cargo_nombre=e.cargo.descripcion if e.cargo else None,
        dependencia_nombre=e.dependencia.descripcion if e.dependencia else None,
    )


@router.get("/", response_model=List[EmpleadoOut])
def listar(db: Session = Depends(get_db)):
    return [_to_out(e) for e in db.query(Empleado).all()]


@router.get("/{id_empleado}", response_model=EmpleadoOut)
def obtener(id_empleado: int, db: Session = Depends(get_db)):
    e = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not e:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return _to_out(e)


@router.post("/", response_model=EmpleadoOut, status_code=201)
def crear(data: EmpleadoCreate, db: Session = Depends(get_db)):
    if db.query(Empleado).filter(Empleado.cedula == data.cedula).first():
        raise HTTPException(status_code=400, detail="Cédula ya registrada")
    e = Empleado(**data.model_dump())
    db.add(e)
    db.commit()
    db.refresh(e)
    return _to_out(e)


@router.put("/{id_empleado}", response_model=EmpleadoOut)
def actualizar(id_empleado: int, data: EmpleadoUpdate, db: Session = Depends(get_db)):
    e = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not e:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    for field, val in data.model_dump(exclude_unset=True).items():
        setattr(e, field, val)
    db.commit()
    db.refresh(e)
    return _to_out(e)


@router.delete("/{id_empleado}", status_code=204)
def eliminar(id_empleado: int, db: Session = Depends(get_db)):
    e = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not e:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    db.delete(e)
    db.commit()
