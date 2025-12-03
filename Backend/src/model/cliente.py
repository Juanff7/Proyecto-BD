from sqlalchemy import Column, BigInteger, String, Text, INTEGER,  ForeignKey
from sqlalchemy.orm import relationship
from src.db.base_class import Base


class Cliente(Base):
    __tablename__ = "clientes"
    id_cliente = Column(BigInteger,primary_key=True, index=True)
    nombre = Column(String, index=True)
    direccion = Column(Text,index=True)
    telefono = Column(INTEGER, index= True)

    #Relaciones
    venta = relationship("Venta", back_populates="cliente")
    
