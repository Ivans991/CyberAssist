from fastapi import APIRouter, Depends
from app.security import verificar_credenciales

router = APIRouter(
    dependencies=[Depends(verificar_credenciales)]
)

@router.get("/")
def inicio():
    return {"mensaje": "Bienvenido a CyberAssist"}


@router.get("/about")
def about():
    return {
        "proyecto": "CyberAssist",
        "descripcion": "Aplicación web para la gestión de activos, vulnerabilidades y riesgos de seguridad"
    }