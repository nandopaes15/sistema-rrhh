from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime, time
from decimal import Decimal


# ── AUTH ───────────────────────────────────────────────────────────────────

class LoginRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
    nombre_completo: str
    roles: List[str]


# ── ROLES ──────────────────────────────────────────────────────────────────

class RolBase(BaseModel):
    nombre_rol: str
    descripcion: Optional[str] = None

class RolCreate(RolBase): pass

class RolOut(RolBase):
    id_rol: int
    class Config: from_attributes = True


# ── USUARIOS ───────────────────────────────────────────────────────────────

class UsuarioCreate(BaseModel):
    username: str
    password: str
    nombre_completo: str
    email: EmailStr
    estado: Optional[str] = "activo"
    roles: Optional[List[int]] = []

class UsuarioUpdate(BaseModel):
    username: Optional[str] = None
    nombre_completo: Optional[str] = None
    email: Optional[EmailStr] = None
    estado: Optional[str] = None
    roles: Optional[List[int]] = None

class UsuarioOut(BaseModel):
    id_usuario: int
    username: str
    nombre_completo: str
    email: str
    estado: str
    fecha_creacion: datetime
    roles: List[str] = []
    class Config: from_attributes = True


# ── AUDITORÍA ──────────────────────────────────────────────────────────────

class AuditoriaOut(BaseModel):
    id_log: int
    id_usuario: Optional[int]
    accion: str
    descripcion: Optional[str]
    tabla_afectada: Optional[str]
    id_registro: Optional[int]
    fecha: datetime
    ip: Optional[str]
    username: Optional[str] = None
    class Config: from_attributes = True


# ── CARGOS ─────────────────────────────────────────────────────────────────

class CargoBase(BaseModel):
    descripcion: str

class CargoCreate(CargoBase): pass

class CargoOut(CargoBase):
    id_cargo: int
    class Config: from_attributes = True


# ── DEPENDENCIAS ───────────────────────────────────────────────────────────

class DependenciaBase(BaseModel):
    descripcion: str

class DependenciaCreate(DependenciaBase): pass

class DependenciaOut(DependenciaBase):
    id_dependencia: int
    class Config: from_attributes = True


# ── EMPLEADOS ──────────────────────────────────────────────────────────────

class EmpleadoCreate(BaseModel):
    cedula: str
    nombre: str
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    id_dependencia: Optional[int] = None
    id_cargo: Optional[int] = None
    salario_base: Decimal = Decimal("0")
    fecha_ingreso: date
    estado: Optional[str] = "activo"

class EmpleadoUpdate(BaseModel):
    cedula: Optional[str] = None
    nombre: Optional[str] = None
    direccion: Optional[str] = None
    telefono: Optional[str] = None
    id_dependencia: Optional[int] = None
    id_cargo: Optional[int] = None
    salario_base: Optional[Decimal] = None
    fecha_ingreso: Optional[date] = None
    estado: Optional[str] = None

class EmpleadoOut(BaseModel):
    id_empleado: int
    cedula: str
    nombre: str
    direccion: Optional[str]
    telefono: Optional[str]
    id_dependencia: Optional[int]
    id_cargo: Optional[int]
    salario_base: Decimal
    fecha_ingreso: date
    estado: str
    cargo_nombre: Optional[str] = None
    dependencia_nombre: Optional[str] = None
    class Config: from_attributes = True


# ── ASISTENCIAS ────────────────────────────────────────────────────────────

class AsistenciaCreate(BaseModel):
    id_empleado: int
    fecha: date
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None

class AsistenciaUpdate(BaseModel):
    hora_entrada: Optional[time] = None
    hora_salida: Optional[time] = None

class AsistenciaOut(BaseModel):
    id_asistencia: int
    id_empleado: int
    fecha: date
    hora_entrada: Optional[time]
    hora_salida: Optional[time]
    empleado_nombre: Optional[str] = None
    class Config: from_attributes = True


# ── NÓMINAS ────────────────────────────────────────────────────────────────

class NominaCreate(BaseModel):
    periodo: str
    fecha_generacion: date
    total_nomina: Decimal = Decimal("0")

class NominaOut(BaseModel):
    id_nomina: int
    periodo: str
    fecha_generacion: date
    total_nomina: Decimal
    class Config: from_attributes = True


# ── DETALLE NÓMINA ─────────────────────────────────────────────────────────

class DetalleNominaCreate(BaseModel):
    id_nomina: int
    id_empleado: int
    salario_base: Decimal
    descuentos: Decimal = Decimal("0")

class DetalleNominaOut(BaseModel):
    id_detalle_nomina: int
    id_nomina: int
    id_empleado: int
    salario_base: Decimal
    descuentos: Decimal
    salario_neto: Optional[Decimal]
    empleado_nombre: Optional[str] = None
    class Config: from_attributes = True
