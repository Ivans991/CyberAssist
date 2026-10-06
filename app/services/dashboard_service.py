from sqlalchemy.orm import Session

from app.repositories import activo_repository, vulnerabilidad_repository
from app.services.vulnerabilidad_service import calcular_riesgo, _normalizar


def obtener_dashboard(db: Session) -> dict:
    activos = activo_repository.obtener_todos(db)
    vulnerabilidades = vulnerabilidad_repository.obtener_todos(db)

    conteo_riesgos = {
        "Critico": 0,
        "Alto": 0,
        "Medio": 0,
        "Bajo": 0,
    }

    for vulnerabilidad in vulnerabilidades:
        if _normalizar(vulnerabilidad.estado) == "Cerrada":
            continue

        riesgo = calcular_riesgo(
            vulnerabilidad.activo.criticidad,
            vulnerabilidad.severidad
        )

        if riesgo in conteo_riesgos:
            conteo_riesgos[riesgo] += 1

    return {
        "total_activos": len(activos),
        "total_vulnerabilidades": len(vulnerabilidades),
        "riesgos_criticos": conteo_riesgos["Critico"],
        "riesgos_altos": conteo_riesgos["Alto"],
        "riesgos_medios": conteo_riesgos["Medio"],
        "riesgos_bajos": conteo_riesgos["Bajo"],
    }