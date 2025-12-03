from sqlalchemy import BigInteger, Table, Column, String, ForeignKey, BOOLEAN, Integer
from src.db.base_class import Base
from sqlalchemy.orm import relationship


class Telefono(Base):
    __tablename__ = "telefonos"
    id_telefono = Column(BigInteger, primary_key=True, index=True)
    num = Column(Integer, index=True)
    id_proveedor = Column(BigInteger, ForeignKey("proveedores.id_proveedor"))


    #relaciones
    proveedor = relationship("Proveedor", back_populates="telefono")