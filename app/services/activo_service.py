from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.repositories import activo_repository, vulnerabilidad_repository
from app.models.activo import Activo
from app.schemas.activo import ActivoCreate, ActivoUpdate
from app.repositories import activo_repository


def crear_activo(db: Session, datos: ActivoCreate):

    nuevo_activo = Activo(
        codigo=datos.codigo.strip().upper(),
        tipo=datos.tipo,
        clasificacion=datos.clasificacion,
        nombre=datos.nombre,
        marca_modelo=datos.marca_modelo,
        ubicacion=datos.ubicacion,
        responsable=datos.responsable,
        funcion=datos.funcion,
        sistema_operativo=datos.sistema_operativo,
        informacion_procesada=datos.informacion_procesada,
        direccion_ip=datos.direccion_ip,
        criticidad=datos.criticidad,
        observaciones=datos.observaciones,
        estado=datos.estado
    )

    try:
        return activo_repository.crear(db, nuevo_activo)

    except IntegrityError:
        raise ValueError(
            f"Ya existe un activo con el código {datos.codigo}"
        )

def obtener_activo(db: Session, activo_id: int):

    return activo_repository.obtener_por_id(db, activo_id)


def obtener_activos(
    db: Session,
    id: int = None,
    codigo: str = None,
    nombre: str = None,
    ubicacion: str = None,
    tipo: str = None,
    estado: str = None
):

    return activo_repository.obtener_todos(
        db,
        id=id,
        codigo=codigo,
        nombre=nombre,
        ubicacion=ubicacion,
        tipo=tipo,
        estado=estado
    )


def actualizar_activo(
    db: Session,
    activo_id: int,
    datos: ActivoUpdate
):

    activo = activo_repository.obtener_por_id(
        db,
        activo_id
    )

    if activo is None:
        return None

    activo.codigo = datos.codigo.strip().upper()
    activo.tipo = datos.tipo
    activo.clasificacion = datos.clasificacion
    activo.nombre = datos.nombre
    activo.marca_modelo = datos.marca_modelo
    activo.ubicacion = datos.ubicacion
    activo.responsable = datos.responsable
    activo.funcion = datos.funcion
    activo.sistema_operativo = datos.sistema_operativo
    activo.informacion_procesada = datos.informacion_procesada
    activo.direccion_ip = datos.direccion_ip
    activo.criticidad = datos.criticidad
    activo.observaciones = datos.observaciones
    activo.estado = datos.estado

    return activo_repository.actualizar(db, activo)


def eliminar_activo(db: Session, activo_id: int):

    activo = activo_repository.obtener_por_id(
        db,
        activo_id
    )

    if activo is None:
        return None

    vulnerabilidades_asociadas = vulnerabilidad_repository.obtener_por_activo(db, activo_id)

    if len(vulnerabilidades_asociadas) > 0:
        raise ValueError(
            f"No se puede eliminar el activo {activo.codigo} "
            f"porque tiene {len(vulnerabilidades_asociadas)} vulnerabilidad(es) asociada(s)."
        )

    activo_repository.eliminar(db, activo)

    return activo
