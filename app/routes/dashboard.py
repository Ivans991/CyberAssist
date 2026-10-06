from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.security import verificar_credenciales
from app.database import get_db
from app.services import dashboard_service


router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
    dependencies=[Depends(verificar_credenciales)]
)


@router.get("/")
def obtener_dashboard(
    db: Session = Depends(get_db)
):
    return dashboard_service.obtener_dashboard(db)