from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models.vulnerabilidad import Vulnerabilidad
from app.schemas.vulnerabilidad import VulnerabilidadCreate, VulnerabilidadUpdate
from app.repositories import vulnerabilidad_repository, activo_repository

def _normalizar(texto: str) -> str:
    equivalencias = {
        "a": "á", "e": "é", "i": "í", "o": "ó", "u": "ú"
    }
    texto = texto.strip().lower()
    for sin_tilde, con_tilde in equivalencias.items():
        texto = texto.replace(con_tilde, sin_tilde)
    return texto.capitalize()

MATRIZ_RIESGO = {
    "Baja":    {"Baja": "Bajo",    "Media": "Medio",   "Alta": "Alto",    "Critica": "Critico"},
    "Media":   {"Baja": "Medio",   "Media": "Medio",   "Alta": "Alto",    "Critica": "Critico"},
    "Alta":    {"Baja": "Alto",    "Media": "Alto",    "Alta": "Critico", "Critica": "Critico"},
    "Critica": {"Baja": "Critico", "Media": "Critico", "Alta": "Critico", "Critica": "Critico"},
}
REGLAS_RECOMENDACION = [
    (
        ["contraseña", "contrasena", "password"],
        "Fortalecer la política de contraseñas y establecer requisitos de complejidad."
    ),
    (
        ["acceso remoto", "anydesk", "teamviewer", "remoto"],
        "Establecer una política para el uso de herramientas de acceso remoto."
    ),
    (
        ["firmware", "router", "switch", "bios", "hardware", "dispositivo", "version"],
        "Verificar y aplicar una versión de firmware soportada y actualizada."
    ),
    (
        ["sistema operativo", "windows", "desactualizado", "actualizacion"],
        "Aplicar las actualizaciones y parches de seguridad disponibles."
    ),
]

RECOMENDACION_POR_RIESGO = {
    "Critico": "Riesgo crítico: revisar y remediar esta vulnerabilidad de forma prioritaria.",
    "Alto":    "Riesgo alto: planificar la remediación en el corto plazo.",
    "Medio":   "Riesgo medio: incluir en el plan de mejora continua de seguridad.",
    "Bajo":    "Riesgo bajo: monitorear y evaluar en revisiones periódicas.",
}


def generar_recomendacion(nombre: str, riesgo: str) -> str:
    nombre_normalizado = _normalizar(nombre).lower()

    for palabras_clave, recomendacion in REGLAS_RECOMENDACION:
        for palabra in palabras_clave:
            if palabra in nombre_normalizado:
                return recomendacion

    return RECOMENDACION_POR_RIESGO.get(
        riesgo,
        "Evaluar la vulnerabilidad y definir un plan de acción."
    )

def calcular_riesgo(criticidad: str, severidad: str) -> str:
    crit = _normalizar(criticidad)
    sev = _normalizar(severidad)

    fila = MATRIZ_RIESGO.get(crit)

    if fila is None:
        return "Desconocido"

    return fila.get(sev, "Desconocido")


def _serializar(vulnerabilidad: Vulnerabilidad) -> dict:
    riesgo = calcular_riesgo(
        vulnerabilidad.activo.criticidad,
        vulnerabilidad.severidad
    )

    return {
        "id": vulnerabilidad.id,
        "activo_id": vulnerabilidad.activo_id,
        "nombre": vulnerabilidad.nombre,
        "descripcion": vulnerabilidad.descripcion,
        "severidad": vulnerabilidad.severidad,
        "evidencia": vulnerabilidad.evidencia,
        "fecha_identificacion": vulnerabilidad.fecha_identificacion,
        "estado": vulnerabilidad.estado,
        "riesgo": riesgo,
        "recomendacion": generar_recomendacion(vulnerabilidad.nombre, riesgo),
    }

def crear_vulnerabilidad(db: Session, datos: VulnerabilidadCreate):

    activo = activo_repository.obtener_por_id(db, datos.activo_id)

    if activo is None:
        raise ValueError(
            f"No existe un activo con id {datos.activo_id}"
        )

    nueva_vulnerabilidad = Vulnerabilidad(
        activo_id=datos.activo_id,
        nombre=datos.nombre,
        descripcion=datos.descripcion,
        severidad=datos.severidad,
        evidencia=datos.evidencia,
        fecha_identificacion=datos.fecha_identificacion,
        estado=datos.estado
    )

    try:
        vulnerabilidad_creada = vulnerabilidad_repository.crear(db, nueva_vulnerabilidad)
        return _serializar(vulnerabilidad_creada)

    except IntegrityError:
            "No se pudo crear la vulnerabilidad por un conflicto de datos."

def obtener_vulnerabilidad(db: Session, vulnerabilidad_id: int):

    vulnerabilidad = vulnerabilidad_repository.obtener_por_id(db, vulnerabilidad_id)

    if vulnerabilidad is None:
        return None

    return _serializar(vulnerabilidad)


def obtener_vulnerabilidades(db: Session):

    vulnerabilidades = vulnerabilidad_repository.obtener_todos(db)

    return [_serializar(v) for v in vulnerabilidades]


def obtener_vulnerabilidades_por_activo(db: Session, activo_id: int):

    vulnerabilidades = vulnerabilidad_repository.obtener_por_activo(db, activo_id)

    return [_serializar(v) for v in vulnerabilidades]

def actualizar_vulnerabilidad(
    db: Session,
    vulnerabilidad_id: int,
    datos: VulnerabilidadUpdate
):

    vulnerabilidad = vulnerabilidad_repository.obtener_por_id(
        db,
        vulnerabilidad_id
    )

    if vulnerabilidad is None:
        return None

    vulnerabilidad.nombre = datos.nombre
    vulnerabilidad.descripcion = datos.descripcion
    vulnerabilidad.severidad = datos.severidad
    vulnerabilidad.evidencia = datos.evidencia
    vulnerabilidad.fecha_identificacion = datos.fecha_identificacion
    vulnerabilidad.estado = datos.estado

    vulnerabilidad_actualizada = vulnerabilidad_repository.actualizar(db, vulnerabilidad)

    return _serializar(vulnerabilidad_actualizada)


def eliminar_vulnerabilidad(db: Session, vulnerabilidad_id: int):

    vulnerabilidad = vulnerabilidad_repository.obtener_por_id(
        db,
        vulnerabilidad_id
    )

    if vulnerabilidad is None:
        return None

    vulnerabilidad_repository.eliminar(db, vulnerabilidad)

    return vulnerabilidad
