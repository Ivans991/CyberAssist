from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.database import Base


class Activo(Base):
    __tablename__ = "activos"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, nullable=False, index=True)
    tipo = Column(String, nullable=False)
    clasificacion = Column(String, nullable=False)
    nombre = Column(String, nullable=False)
    marca_modelo = Column(String, nullable=True)
    ubicacion = Column(String, nullable=False)
    responsable = Column(String, nullable=False)
    funcion = Column(String, nullable=False)
    sistema_operativo = Column(String, nullable=True)
    informacion_procesada = Column(String, nullable=True)
    direccion_ip = Column(String, nullable=True)
    criticidad = Column(String, nullable=False)
    observaciones = Column(String, nullable=True)
    estado = Column(String, nullable=False)
    vulnerabilidades = relationship("Vulnerabilidad", back_populates="activo")