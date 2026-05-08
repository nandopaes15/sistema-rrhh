from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Asistencia, Empleado
from schemas import AsistenciaCreate, AsistenciaUpdate, AsistenciaOut
from typing import List

router = APIRouter(prefix="/asistencias", tags=["Asistencias"])


def _to_out(a: Asistencia) -> AsistenciaOut:
    return AsistenciaOut(
        id_asistencia=a.id_asistencia, id_empleado=a.id_empleado,
        fecha=a.fecha, hora_entrada=a.hora_entrada, hora_salida=a.hora_salida,
        empleado_nombre=a.empleado.nombre if a.empleado else None
    )


@router.get("/", response_model=List[AsistenciaOut])
def listar(db: Session = Depends(get_db)):
    return [_to_out(a) for a in db.query(Asistencia).order_by(Asistencia.fecha.desc()).all()]


@router.get("/empleado/{id_empleado}", response_model=List[AsistenciaOut])
def por_empleado(id_empleado: int, db: Session = Depends(get_db)):
    rows = db.query(Asistencia).filter(Asistencia.id_empleado == id_empleado).all()
    return [_to_out(a) for a in rows]


@router.post("/", response_model=AsistenciaOut, status_code=201)
def crear(data: AsistenciaCreate, db: Session = Depends(get_db)):
    existe = db.query(Asistencia).filter(
        Asistencia.id_empleado == data.id_empleado,
        Asistencia.fecha == data.fecha
    ).first()
    if existe:
        raise HTTPException(status_code=400, detail="Ya existe registro para ese empleado en esa fecha")
    a = Asistencia(**data.model_dump())
    db.add(a)
    db.commit()
    db.refresh(a)
    return _to_out(a)


@router.put("/{id_asistencia}", response_model=AsistenciaOut)
def actualizar(id_asistencia: int, data: AsistenciaUpdate, db: Session = Depends(get_db)):
    a = db.query(Asistencia).filter(Asistencia.id_asistencia == id_asistencia).first()
    if not a:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    for field, val in data.model_dump(exclude_unset=True).items():
        setattr(a, field, val)
    db.commit()
    db.refresh(a)
    return _to_out(a)


@router.delete("/{id_asistencia}", status_code=204)
def eliminar(id_asistencia: int, db: Session = Depends(get_db)):
    a = db.query(Asistencia).filter(Asistencia.id_asistencia == id_asistencia).first()
    if not a:
        raise HTTPException(status_code=404, detail="Asistencia no encontrada")
    db.delete(a)
    db.commit()
