from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Nomina, DetalleNomina
from schemas import NominaCreate, NominaOut, DetalleNominaCreate, DetalleNominaOut
from typing import List
from decimal import Decimal

router = APIRouter(prefix="/nominas", tags=["Nóminas"])


# ── NÓMINAS ────────────────────────────────────────────────────────────────

@router.get("/", response_model=List[NominaOut])
def listar(db: Session = Depends(get_db)):
    return db.query(Nomina).order_by(Nomina.periodo.desc()).all()


@router.get("/{id_nomina}", response_model=NominaOut)
def obtener(id_nomina: int, db: Session = Depends(get_db)):
    n = db.query(Nomina).filter(Nomina.id_nomina == id_nomina).first()
    if not n:
        raise HTTPException(status_code=404, detail="Nómina no encontrada")
    return n


@router.post("/", response_model=NominaOut, status_code=201)
def crear(data: NominaCreate, db: Session = Depends(get_db)):
    n = Nomina(**data.model_dump())
    db.add(n)
    db.commit()
    db.refresh(n)
    return n


@router.delete("/{id_nomina}", status_code=204)
def eliminar(id_nomina: int, db: Session = Depends(get_db)):
    n = db.query(Nomina).filter(Nomina.id_nomina == id_nomina).first()
    if not n:
        raise HTTPException(status_code=404, detail="Nómina no encontrada")
    db.delete(n)
    db.commit()


# ── DETALLE NÓMINA ─────────────────────────────────────────────────────────

@router.get("/{id_nomina}/detalles", response_model=List[DetalleNominaOut])
def listar_detalles(id_nomina: int, db: Session = Depends(get_db)):
    rows = db.query(DetalleNomina).filter(DetalleNomina.id_nomina == id_nomina).all()
    result = []
    for d in rows:
        result.append(DetalleNominaOut(
            id_detalle_nomina=d.id_detalle_nomina, id_nomina=d.id_nomina,
            id_empleado=d.id_empleado, salario_base=d.salario_base,
            descuentos=d.descuentos,
            salario_neto=d.salario_neto or (d.salario_base - d.descuentos),
            empleado_nombre=d.empleado.nombre if d.empleado else None
        ))
    return result


@router.post("/{id_nomina}/detalles", response_model=DetalleNominaOut, status_code=201)
def agregar_detalle(id_nomina: int, data: DetalleNominaCreate, db: Session = Depends(get_db)):
    if not db.query(Nomina).filter(Nomina.id_nomina == id_nomina).first():
        raise HTTPException(status_code=404, detail="Nómina no encontrada")
    salario_neto = data.salario_base - data.descuentos
    d = DetalleNomina(id_nomina=id_nomina, id_empleado=data.id_empleado,
                      salario_base=data.salario_base, descuentos=data.descuentos,
                      salario_neto=salario_neto)
    db.add(d)
    # Actualizar total nómina
    nomina = db.query(Nomina).filter(Nomina.id_nomina == id_nomina).first()
    nomina.total_nomina = (nomina.total_nomina or Decimal("0")) + salario_neto
    db.commit()
    db.refresh(d)
    return DetalleNominaOut(
        id_detalle_nomina=d.id_detalle_nomina, id_nomina=d.id_nomina,
        id_empleado=d.id_empleado, salario_base=d.salario_base,
        descuentos=d.descuentos, salario_neto=salario_neto,
        empleado_nombre=d.empleado.nombre if d.empleado else None
    )


@router.delete("/detalles/{id_detalle}", status_code=204)
def eliminar_detalle(id_detalle: int, db: Session = Depends(get_db)):
    d = db.query(DetalleNomina).filter(DetalleNomina.id_detalle_nomina == id_detalle).first()
    if not d:
        raise HTTPException(status_code=404, detail="Detalle no encontrado")
    db.delete(d)
    db.commit()
