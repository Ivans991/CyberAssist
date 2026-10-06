from pydantic import BaseModel

class ActivoCreate(BaseModel):
    codigo: str
    tipo: str
    clasificacion: str
    nombre: str
    marca_modelo: str | None = None
    ubicacion: str
    responsable: str
    funcion: str
    sistema_operativo: str | None = None
    informacion_procesada: str | None = None
    direccion_ip: str | None = None
    criticidad: str
    observaciones: str | None = None
    estado: str

class ActivoUpdate(BaseModel):

    codigo: str
    tipo: str
    clasificacion: str
    nombre: str
    marca_modelo: str | None = None
    ubicacion: str
    responsable: str
    funcion: str
    sistema_operativo: str | None = None
    informacion_procesada: str | None = None
    direccion_ip: str | None = None
    criticidad: str
    observaciones: str | None = None
    estado: str
