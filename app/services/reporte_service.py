from io import BytesIO
from datetime import datetime
from reportlab.lib.styles import ParagraphStyle
from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet

from app.repositories import activo_repository
from app.services import vulnerabilidad_service, dashboard_service


def generar_reporte_pdf(db: Session) -> bytes:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    estilos = getSampleStyleSheet()
    elementos = []
    estilo_celda = ParagraphStyle(
        "celda",
        parent=estilos["Normal"],
        fontSize=7,
        leading=9,
    )
    # --- Portada / Resumen ejecutivo ---
    elementos.append(Paragraph("Informe Técnico de Seguridad — CyberAssist", estilos["Title"]))
    elementos.append(Paragraph(
        f"Generado el {datetime.now().strftime('%d/%m/%Y %H:%M')}",
        estilos["Normal"]
    ))
    elementos.append(Spacer(1, 20))

    resumen = dashboard_service.obtener_dashboard(db)
    datos_resumen = [
        ["Indicador", "Valor"],
        ["Total de activos", resumen["total_activos"]],
        ["Total de vulnerabilidades", resumen["total_vulnerabilidades"]],
        ["Riesgos críticos", resumen["riesgos_criticos"]],
        ["Riesgos altos", resumen["riesgos_altos"]],
        ["Riesgos medios", resumen["riesgos_medios"]],
        ["Riesgos bajos", resumen["riesgos_bajos"]],
    ]
    tabla_resumen = Table(datos_resumen, hAlign="LEFT")
    tabla_resumen.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elementos.append(tabla_resumen)
    elementos.append(PageBreak())

    # --- Inventario de activos ---
    elementos.append(Paragraph("Inventario de Activos", estilos["Heading1"]))
    elementos.append(Spacer(1, 10))

    activos = activo_repository.obtener_todos(db)
    datos_activos = [["Código", "Nombre", "Tipo", "Criticidad", "Estado"]]
    for activo in activos:
        datos_activos.append([
            activo.codigo, activo.nombre, activo.tipo,
            activo.criticidad, activo.estado
        ])

    tabla_activos = Table(datos_activos, hAlign="LEFT")
    tabla_activos.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 8),
    ]))
    elementos.append(tabla_activos)
    elementos.append(PageBreak())

    # --- Vulnerabilidades, riesgo y recomendaciones ---
    elementos.append(Paragraph("Vulnerabilidades, Riesgo y Recomendaciones", estilos["Heading1"]))
    elementos.append(Spacer(1, 10))

    vulnerabilidades = vulnerabilidad_service.obtener_vulnerabilidades(db)
    datos_vulns = [["Activo ID", "Nombre", "Severidad", "Riesgo", "Recomendación"]]
    for v in vulnerabilidades:
        datos_vulns.append([
            str(v["activo_id"]),
            Paragraph(v["nombre"], estilo_celda),
            v["severidad"],
            v["riesgo"],
            Paragraph(v["recomendacion"], estilo_celda),
        ])

    tabla_vulns = Table(datos_vulns, hAlign="LEFT", colWidths=[50, 90, 60, 50, 200])
    tabla_vulns.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#2c3e50")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    elementos.append(tabla_vulns)

    doc.build(elementos)
    buffer.seek(0)
    return buffer.getvalue()