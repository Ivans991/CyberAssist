from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.schemas.activo import ActivoCreate, ActivoUpdate
from app.services import activo_service
from app.security import verificar_credenciales

router = APIRouter(
    prefix="/activos",
    tags=["Activos"],
    dependencies=[Depends(verificar_credenciales)]
)


@router.post("/")
def crear_activo(
    activo: ActivoCreate,
    db: Session = Depends(get_db)
):
    try:
        return activo_service.crear_activo(
            db,
            activo
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error)
        )


@router.get("/")
def listar_activos(
    id: Optional[int] = None,
    codigo: Optional[str] = None,
    nombre: Optional[str] = None,
    ubicacion: Optional[str] = None,
    tipo: Optional[str] = None,
    estado: Optional[str] = None,
    db: Session = Depends(get_db)
):
    return activo_service.obtener_activos(
        db,
        id=id,
        codigo=codigo,
        nombre=nombre,
        ubicacion=ubicacion,
        tipo=tipo,
        estado=estado
    )


@router.get("/{activo_id}")
def obtener_activo(
    activo_id: int,
    db: Session = Depends(get_db)
):
    activo = activo_service.obtener_activo(
        db,
        activo_id
    )

    if activo is None:
        raise HTTPException(
            status_code=404,
            detail="Activo no encontrado"
        )

    return activo


@router.put("/{activo_id}")
def actualizar_activo(
    activo_id: int,
    datos: ActivoUpdate,
    db: Session = Depends(get_db)
):
    activo = activo_service.actualizar_activo(
        db,
        activo_id,
        datos
    )

    if activo is None:
        raise HTTPException(
            status_code=404,
            detail="Activo no encontrado"
        )

    return activo


@router.delete("/{activo_id}")
def eliminar_activo(
    activo_id: int,
    db: Session = Depends(get_db)
):
    try:
        activo = activo_service.eliminar_activo(
            db,
            activo_id
        )
    except ValueError as error:
        raise HTTPException(status_code=409, detail=str(error))


    if activo is None:
        raise HTTPException(
            status_code=404,
            detail="Activo no encontrado"
        )

    return {
        "mensaje": "Activo eliminado correctamente"
    }
