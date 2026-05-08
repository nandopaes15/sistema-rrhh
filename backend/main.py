from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers.usuarios import router as usuarios_router
from routers.roles import router as roles_router
from routers.auditoria import router as auditoria_router
from routers.empleados import router as empleados_router
from routers.cargos_dependencias import cargos_router, dependencias_router
from routers.asistencias import router as asistencias_router
from routers.nominas import router as nominas_router

app = FastAPI(
    title="Sistema de Seguridad y RRHH",
    description="API REST – Grupo 2 · Ingeniería de Software III",
    version="1.0.0"
)

# Permitir peticiones desde el frontend (cualquier origen en desarrollo)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(usuarios_router,     prefix="/api")
app.include_router(roles_router,        prefix="/api")
app.include_router(auditoria_router,    prefix="/api")
app.include_router(empleados_router,    prefix="/api")
app.include_router(cargos_router,       prefix="/api")
app.include_router(dependencias_router, prefix="/api")
app.include_router(asistencias_router,  prefix="/api")
app.include_router(nominas_router,      prefix="/api")


@app.get("/")
def root():
    return {"mensaje": "API funcionando ✓", "docs": "/docs"}
