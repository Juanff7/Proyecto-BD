from sqlalchemy import BigInteger, Column, String, ForeignKey, BOOLEAN
from src.db.base_class import Base
from sqlalchemy.orm import relationship


class Empleado(Base):
    __tablename__ = "empleados"
    id_empleado = Column(BigInteger, primary_key = True)
    nombre = Column(String, index=True)
    apellido = Column(String, index=True)
    email = Column(String, index=True)
    password_hash = Column(String, index=True)
    id_cargo = Column(BigInteger, ForeignKey("cargos.id_cargo"))
    activo = Column(BOOLEAN, index= True)
    


    #relaciones 1:1
    cargo = relationship("Cargo", back_populates="empleado", uselist=False)
    detallesP = relationship("Detalle_proveedor", back_populates="empleado")
    venta = relationship("Venta", back_populates="empleado")
    