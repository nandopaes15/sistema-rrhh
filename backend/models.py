from sqlalchemy import (Column, Integer, String, Enum, DateTime, Date, Time,
                        Numeric, Text, ForeignKey, UniqueConstraint)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base


# ── SEGURIDAD ──────────────────────────────────────────────────────────────

class Rol(Base):
    __tablename__ = "roles"
    id_rol      = Column(Integer, primary_key=True, index=True)
    nombre_rol  = Column(String(50), unique=True, nullable=False)
    descripcion = Column(String(255))
    usuarios    = relationship("UsuarioRol", back_populates="rol")


class Usuario(Base):
    __tablename__ = "usuarios"
    id_usuario      = Column(Integer, primary_key=True, index=True)
    username        = Column(String(50), unique=True, nullable=False)
    password        = Column(String(255), nullable=False)
    nombre_completo = Column(String(100), nullable=False)
    email           = Column(String(100), unique=True, nullable=False)
    estado          = Column(Enum("activo", "inactivo"), default="activo")
    fecha_creacion  = Column(DateTime, default=func.now())
    roles           = relationship("UsuarioRol", back_populates="usuario")
    logs            = relationship("AuditoriaLog", back_populates="usuario")


class UsuarioRol(Base):
    __tablename__ = "usuario_roles"
    id_usuario  = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="CASCADE"), primary_key=True)
    id_rol      = Column(Integer, ForeignKey("roles.id_rol",     ondelete="CASCADE"), primary_key=True)
    usuario     = relationship("Usuario", back_populates="roles")
    rol         = relationship("Rol",     back_populates="usuarios")


class AuditoriaLog(Base):
    __tablename__ = "auditoria_log"
    id_log         = Column(Integer, primary_key=True, index=True)
    id_usuario     = Column(Integer, ForeignKey("usuarios.id_usuario", ondelete="SET NULL"), nullable=True)
    accion         = Column(String(50), nullable=False)
    descripcion    = Column(Text)
    tabla_afectada = Column(String(50))
    id_registro    = Column(Integer)
    fecha          = Column(DateTime, default=func.now())
    ip             = Column(String(45))
    usuario        = relationship("Usuario", back_populates="logs")


# ── RECURSOS HUMANOS ───────────────────────────────────────────────────────

class Cargo(Base):
    __tablename__ = "cargos"
    id_cargo    = Column(Integer, primary_key=True, index=True)
    descripcion = Column(String(100), nullable=False)
    empleados   = relationship("Empleado", back_populates="cargo")


class Dependencia(Base):
    __tablename__ = "dependencias"
    id_dependencia = Column(Integer, primary_key=True, index=True)
    descripcion    = Column(String(100), nullable=False)
    empleados      = relationship("Empleado", back_populates="dependencia")


class Empleado(Base):
    __tablename__ = "empleados"
    id_empleado    = Column(Integer, primary_key=True, index=True)
    cedula         = Column(String(20), unique=True, nullable=False)
    nombre         = Column(String(100), nullable=False)
    direccion      = Column(String(200))
    telefono       = Column(String(20))
    id_dependencia = Column(Integer, ForeignKey("dependencias.id_dependencia", ondelete="SET NULL"), nullable=True)
    id_cargo       = Column(Integer, ForeignKey("cargos.id_cargo",             ondelete="SET NULL"), nullable=True)
    salario_base   = Column(Numeric(12, 2), default=0)
    fecha_ingreso  = Column(Date, nullable=False)
    estado         = Column(Enum("activo", "inactivo"), default="activo")
    dependencia    = relationship("Dependencia", back_populates="empleados")
    cargo          = relationship("Cargo",       back_populates="empleados")
    asistencias    = relationship("Asistencia",   back_populates="empleado")
    detalles       = relationship("DetalleNomina", back_populates="empleado")


class Asistencia(Base):
    __tablename__ = "asistencias"
    __table_args__ = (UniqueConstraint("id_empleado", "fecha"),)
    id_asistencia = Column(Integer, primary_key=True, index=True)
    id_empleado   = Column(Integer, ForeignKey("empleados.id_empleado", ondelete="CASCADE"), nullable=False)
    fecha         = Column(Date, nullable=False)
    hora_entrada  = Column(Time)
    hora_salida   = Column(Time)
    empleado      = relationship("Empleado", back_populates="asistencias")


class Nomina(Base):
    __tablename__ = "nominas"
    id_nomina        = Column(Integer, primary_key=True, index=True)
    periodo          = Column(String(20), nullable=False)
    fecha_generacion = Column(Date, nullable=False)
    total_nomina     = Column(Numeric(14, 2), default=0)
    detalles         = relationship("DetalleNomina", back_populates="nomina")


class DetalleNomina(Base):
    __tablename__ = "detalle_nomina"
    id_detalle_nomina = Column(Integer, primary_key=True, index=True)
    id_nomina         = Column(Integer, ForeignKey("nominas.id_nomina",       ondelete="CASCADE"), nullable=False)
    id_empleado       = Column(Integer, ForeignKey("empleados.id_empleado",   ondelete="CASCADE"), nullable=False)
    salario_base      = Column(Numeric(12, 2), nullable=False)
    descuentos        = Column(Numeric(12, 2), default=0)
    salario_neto      = Column(Numeric(12, 2))
    nomina            = relationship("Nomina",   back_populates="detalles")
    empleado          = relationship("Empleado", back_populates="detalles")
