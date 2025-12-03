from sqlalchemy import Column, BigInteger, String, Text, INTEGER, Float, ForeignKey
from sqlalchemy.orm import relationship
from src.db.base_class import Base



class Detalle_venta(Base):
    __tablename__ = "detalles_venta"
    id_dv = Column(BigInteger, primary_key=True, index=True )
    id_venta = Column(BigInteger, ForeignKey("ventas.id_venta"))
    id_producto = Column(BigInteger, ForeignKey("productos.id_producto"))
    cantidad = Column(INTEGER, index=True)
    precio_unit = Column(Float, index=True )
    sub_total = Column(Float, index  = True)
    detalle = Column(Text, index=True)
    




    venta = relationship("Venta", back_populates="detalle_venta")
    producto = relationship("Producto", back_populates="detalle_venta")
