from sqlalchemy import Column, BigInteger, String, Text, INTEGER, Float, ForeignKey,  DateTime
from sqlalchemy.orm import relationship
from src.db.base_class import Base
from datetime import datetime


class Detalle_proveedor(Base):
    __tablename__ = "detalles_proveedor"

    id = Column(BigInteger, primary_key=True, index=True)
    producto_id = Column(BigInteger, ForeignKey("productos.id"))
    proveedor_id = Column(BigInteger, ForeignKey("proveedores.id"))  # ✅ corregido
    precio_unit = Column(Float, index=True)
    cantidad = Column(INTEGER, index=True)
    fecha_ingreso = Column(DateTime, default=datetime.now)
    detalle = Column(String, index=True)
    empleado_id = Column(BigInteger, ForeignKey("empleados.id_empleado"))

    # Relaciones
    producto = relationship("Producto", back_populates="detallesProveedores")
    proveedor = relationship("Proveedor", back_populates="detalle_proveedor")
    empleado = relationship("Empleado", back_populates="detallesP")
