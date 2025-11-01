from sqlalchemy import BigInteger, Table, Column, String, ForeignKey, BOOLEAN
from src.db.base_class import Base
from sqlalchemy.orm import relationship


class Cargo(Base):
    __tablename__ = "cargos"
    id_cargo = Column(BigInteger, primary_key = True)
    tipo = Column(String, index =True)


    #Relacion 
    empleado = relationship("Empleado", back_populates="cargo", uselist=False)