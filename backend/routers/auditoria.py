from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from models import AuditoriaLog, Usuario
from schemas import AuditoriaOut
from typing import List

router = APIRouter(prefix="/auditoria", tags=["Auditoría"])


@router.get("/", response_model=List[AuditoriaOut])
def listar(db: Session = Depends(get_db)):
    logs = db.query(AuditoriaLog).order_by(AuditoriaLog.fecha.desc()).all()
    result = []
    for log in logs:
        u = db.query(Usuario).filter(Usuario.id_usuario == log.id_usuario).first()
        out = AuditoriaOut(
            id_log=log.id_log, id_usuario=log.id_usuario,
            accion=log.accion, descripcion=log.descripcion,
            tabla_afectada=log.tabla_afectada, id_registro=log.id_registro,
            fecha=log.fecha, ip=log.ip,
            username=u.username if u else None
        )
        result.append(out)
    return result
