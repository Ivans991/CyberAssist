from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.vulnerabilidad import Vulnerabilidad


def crear(db: Session, vulnerabilidad: Vulnerabilidad):

    try:
        db.add(vulnerabilidad)
        db.commit()
        db.refresh(vulnerabilidad)

        return vulnerabilidad

    except IntegrityError:
        db.rollback()
        raise


def obtener_por_id(db: Session, vulnerabilidad_id: int):

    return (
        db.query(Vulnerabilidad)
        .filter(Vulnerabilidad.id == vulnerabilidad_id)
        .first()
    )


def obtener_todos(db: Session):

    return db.query(Vulnerabilidad).all()


def obtener_por_activo(db: Session, activo_id: int):

    return (
        db.query(Vulnerabilidad)
        .filter(Vulnerabilidad.activo_id == activo_id)
        .all()
    )


def actualizar(db: Session, vulnerabilidad: Vulnerabilidad):

    db.commit()
    db.refresh(vulnerabilidad)

    return vulnerabilidad


def eliminar(db: Session, vulnerabilidad: Vulnerabilidad):

    db.delete(vulnerabilidad)
    db.commit()