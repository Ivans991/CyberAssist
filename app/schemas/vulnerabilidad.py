from datetime import date
from pydantic import BaseModel


class VulnerabilidadCreate(BaseModel):
    activo_id: int
    nombre: str
    descripcion: str | None = None
    severidad: str
    evidencia: str | None = None
    fecha_identificacion: date
    estado: str = "Abierta"


class VulnerabilidadUpdate(BaseModel):
    nombre: str
    descripcion: str | None = None
    severidad: str
    evidencia: str | None = None
    fecha_identificacion: date
    estado: str