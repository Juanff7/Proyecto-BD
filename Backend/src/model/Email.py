from sqlalchemy import BigInteger, Table, Column, String, ForeignKey, BOOLEAN, Integer
from src.db.base_class import Base
from sqlalchemy.orm import relationship


class Email(Base):
    __tablename__ = "emails"
    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, index=True)
    id_proveedor = Column(BigInteger, ForeignKey("proveedores.id"))


    #relaciones
    proveedor =relationship("Proveedor", back_populates="email")