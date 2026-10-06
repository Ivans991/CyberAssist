from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.security import verificar_credenciales
from app.database import get_db
from app.schemas.vulnerabilidad import VulnerabilidadCreate, VulnerabilidadUpdate
from app.services import vulnerabilidad_service


router = APIRouter(
    prefix="/vulnerabilidades",
    tags=["Vulnerabilidades"],
    dependencies=[Depends(verificar_credenciales)]
)


@router.post("/")
def crear_vulnerabilidad(
    vulnerabilidad: VulnerabilidadCreate,
    db: Session = Depends(get_db)
):
    try:
        return vulnerabilidad_service.crear_vulnerabilidad(
            db,
            vulnerabilidad
        )

    except ValueError as error:
        mensaje = str(error)

        if "No existe un activo" in mensaje:
            raise HTTPException(status_code=404, detail=mensaje)

        raise HTTPException(status_code=409, detail=mensaje)


@router.get("/")
def listar_vulnerabilidades(
    db: Session = Depends(get_db)
):
    return vulnerabilidad_service.obtener_vulnerabilidades(db)


@router.get("/{vulnerabilidad_id}")
def obtener_vulnerabilidad(
    vulnerabilidad_id: int,
    db: Session = Depends(get_db)
):
    vulnerabilidad = vulnerabilidad_service.obtener_vulnerabilidad(
        db,
        vulnerabilidad_id
    )

    if vulnerabilidad is None:
        raise HTTPException(
            status_code=404,
            detail="Vulnerabilidad no encontrada"
        )

    return vulnerabilidad


@router.get("/activo/{activo_id}")
def listar_vulnerabilidades_por_activo(
    activo_id: int,
    db: Session = Depends(get_db)
):
    return vulnerabilidad_service.obtener_vulnerabilidades_por_activo(
        db,
        activo_id
    )


@router.put("/{vulnerabilidad_id}")
def actualizar_vulnerabilidad(
    vulnerabilidad_id: int,
    datos: VulnerabilidadUpdate,
    db: Session = Depends(get_db)
):
    vulnerabilidad = vulnerabilidad_service.actualizar_vulnerabilidad(
        db,
        vulnerabilidad_id,
        datos
    )

    if vulnerabilidad is None:
        raise HTTPException(
            status_code=404,
            detail="Vulnerabilidad no encontrada"
        )

    return vulnerabilidad


@router.delete("/{vulnerabilidad_id}")
def eliminar_vulnerabilidad(
    vulnerabilidad_id: int,
    db: Session = Depends(get_db)
):
    vulnerabilidad = vulnerabilidad_service.eliminar_vulnerabilidad(
        db,
        vulnerabilidad_id
    )

    if vulnerabilidad is None:
        raise HTTPException(
            status_code=404,
            detail="Vulnerabilidad no encontrada"
        )

    return {
        "mensaje": "Vulnerabilidad eliminada correctamente"
    }