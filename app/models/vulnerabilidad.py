from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base


class Vulnerabilidad(Base):
    __tablename__ = "vulnerabilidades"

    id = Column(Integer, primary_key=True, index=True)
    activo_id = Column(Integer, ForeignKey("activos.id"), nullable=False)
    nombre = Column(String, nullable=False)
    descripcion = Column(String, nullable=True)
    severidad = Column(String, nullable=False)
    evidencia = Column(String, nullable=True)
    fecha_identificacion = Column(Date, nullable=False)
    estado = Column(String, nullable=False, default="Abierta")



    activo = relationship("Activo", back_populates="vulnerabilidades")
