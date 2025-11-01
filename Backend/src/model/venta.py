from sqlalchemy import Column, BigInteger, String, Text,Float, INTEGER,  ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.db.base_class import Base
from datetime import datetime
class Venta(Base):
    __tablename__ ="ventas"
    id = Column(BigInteger, primary_key=True, index=True)
    id_cliente = Column(BigInteger, ForeignKey("clientes.id"))
    id_empleado =Column(BigInteger, ForeignKey("empleados.id_empleado"))
    fecha = Column(DateTime, default=datetime.now )
    total = Column(Float, default = 0.0)



    #Relaciones
    cliente = relationship("Cliente", back_populates="venta")
    empleado = relationship("Empleado", back_populates="venta")
    detalle_venta = relationship("Detalle_venta", back_populates="venta")