from sqlalchemy.orm import Session
from src.model.cargo import Cargo
from src.schemas.cargo import CargoCreate

#Crear un Cargo
def Created_cargo(db:Session, data: CargoCreate) -> Cargo:
    obj = Cargo(
      tipo= data.tipo
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj 
