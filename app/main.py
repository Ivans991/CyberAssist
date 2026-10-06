from fastapi import FastAPI
from app.routes.home import router
from app.routes.activos import router as activos_router
from app.database import Base, engine
from app.routes.dashboard import router as dashboard_router
from app.models.activo import Activo
from app.routes.reportes import router as reportes_router
from app.models.vulnerabilidad import Vulnerabilidad
from app.routes.paginas import router as paginas_router
from app.routes.vulnerabilidades import router as vulnerabilidades_router
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(router)
app.include_router(activos_router)
app.include_router(vulnerabilidades_router)
app.include_router(dashboard_router)
app.include_router(reportes_router)
app.include_router(paginas_router)