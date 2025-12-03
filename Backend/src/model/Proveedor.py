from sqlalchemy import BigInteger, Table, Column, String, ForeignKey, BOOLEAN
from src.db.base_class import Base
from sqlalchemy.orm import relationship

class Proveedor(Base):
    __tablename__ = "proveedores"
    id_proveedor = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    usuario_ebay = Column(String, index= True)
    pais = Column(String, index = True)
    tipo = Column(String, index = True)

    #Relaciones
    detalle_proveedor = relationship("Detalle_proveedor", back_populates="proveedor")
    email = relationship("Email", back_populates="proveedor")
    telefono = relationship("Telefono", back_populates="proveedor")