from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.activo import Activo


def crear(db: Session, activo: Activo):

    try:
        db.add(activo)
        db.commit()
        db.refresh(activo)

        return activo

    except IntegrityError:
        db.rollback()
        raise


def obtener_por_id(db: Session, activo_id: int):

    return (
        db.query(Activo)
        .filter(Activo.id == activo_id)
        .first()
    )


def obtener_todos(
    db: Session,
    id: int = None,
    codigo: str = None,
    nombre: str = None,
    ubicacion: str = None,
    tipo: str = None,
    estado: str = None
):

    query = db.query(Activo)

    if id is not None:
        query = query.filter(Activo.id == id)

    if codigo:
        query = query.filter(Activo.codigo.ilike(f"%{codigo.strip()}%"))

    if nombre:
        query = query.filter(Activo.nombre.ilike(f"%{nombre.strip()}%"))

    if ubicacion:
        query = query.filter(Activo.ubicacion.ilike(f"%{ubicacion.strip()}%"))

    if tipo:
        query = query.filter(Activo.tipo.ilike(f"%{tipo.strip()}%"))

    if estado:
        query = query.filter(Activo.estado.ilike(f"%{estado.strip()}%"))

    return query.all()


def actualizar(db: Session, activo: Activo):

    db.commit()
    db.refresh(activo)

    return activo


def eliminar(db: Session, activo: Activo):

    db.delete(activo)
    db.commit()