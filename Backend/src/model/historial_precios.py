from sqlalchemy import Column, BigInteger, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from src.db.base_class import Base
from datetime import datetime

class Historial_Precios(Base):
    __tablename__ = "historial_precios"
    id = Column(BigInteger, primary_key=True, index=True)
    id_producto = Column(BigInteger, ForeignKey("productos.id"))
    precio_anterior = Column(Float, index=True)
    precio_nuevo = Column(Float, index=True)
    fecha_de_cambio = Column(DateTime, default=datetime.now)


    #relacion
    producto = relationship("Producto", back_populates="historial")