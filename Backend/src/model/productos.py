from sqlalchemy import Column, BigInteger, String, Text, INTEGER, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base_class import Base


class Producto(Base):
    __tablename__ = "productos"
    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, index=True)
    descripcion = Column(Text, index=True)
    categoria_id = Column(BigInteger, ForeignKey("categorias.id"))
    costo_venta = Column(INTEGER, index=True)
    cantidad = Column(INTEGER, index=True)
    imagen_url = Column(String, nullable=True)

    #relacion
    categoria =  relationship("Categoria", back_populates="producto")
    detallesProveedores = relationship("Detalle_proveedor", back_populates="producto")
    historial = relationship("Historial_Precios", back_populates="producto")
    detalle_venta = relationship("Detalle_venta", back_populates="producto")