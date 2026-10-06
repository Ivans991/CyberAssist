from fastapi import APIRouter, Depends
from fastapi.responses import Response
from sqlalchemy.orm import Session
from app.security import verificar_credenciales
from app.database import get_db
from app.services import reporte_service


router = APIRouter(
    prefix="/reportes",
    tags=["Reportes"],
    dependencies=[Depends(verificar_credenciales)]
)


@router.get("/pdf")
def descargar_reporte_pdf(
    db: Session = Depends(get_db)
):
    pdf_bytes = reporte_service.generar_reporte_pdf(db)

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": "attachment; filename=informe_cyberassist.pdf"
        }
    )