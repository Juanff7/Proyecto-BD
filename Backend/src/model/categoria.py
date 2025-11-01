from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship
from src.db.base_class import Base

class Categoria(Base):
    __tablename__ = "categorias"
    id = Column(BigInteger, primary_key=True, index=True)
    tipo = Column(String, index=True)


    #Relaciones
    producto = relationship("Producto", back_populates="categoria")