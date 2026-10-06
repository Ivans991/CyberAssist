from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse

from app.security import verificar_credenciales

router = APIRouter(
    dependencies=[Depends(verificar_credenciales)]
)

@router.get("/inicio")
def pagina_inicio():
    return FileResponse("templates/index.html")


@router.get("/activos")
def pagina_activos():
    return FileResponse("templates/activos.html")

@router.get("/vulnerabilidades")
def pagina_vulnerabilidades():
    return FileResponse("templates/vulnerabilidades.html")

@router.get("/dashboard-view")
def pagina_dashboard():
    return FileResponse("templates/dashboard.html")