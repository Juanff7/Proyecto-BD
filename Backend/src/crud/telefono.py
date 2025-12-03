from sqlalchemy.orm import Session
from src.model.Telefono import Telefono
from src.schemas.telefono import TelefonoCraate
from fastapi import HTTPException

#carga las relaciones automaticamente provedor -> telefono
from sqlalchemy.orm import joinedload

from src.model.Proveedor import Proveedor



#Crear un telfono
def Created_tel(db: Session, data: TelefonoCraate):
    #si manda id proveedor, lo usamos directamente
    if data.id_proveedor:
        proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == data.id_proveedor).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor con ese ID no existe")
    elif data.proveedor:
        proveedor = db.query(Proveedor).filter(Proveedor.nombre == data.proveedor).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor con ese nombre no existe")
        
    else:
           raise HTTPException(status_code=400, detail="Debes enviar nombre o ID del proveedor")


    obj = Telefono(
        num= data.num,
        id_proveedor = proveedor.id_proveedor
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    
    return{
        "id": obj.id_telefono,
        "proveedor": proveedor.nombre,
        "num": data.num        
    }


#Obtener todos
def get_telefonos(db: Session):
    telefonos = db.query(Telefono).options(joinedload(Telefono.proveedor)).all()

    return [
        {
            "id": t.id_telefono,
            "num": t.num,
            "proveedor": t.proveedor.nombre if t.proveedor else None
        }
        for t in telefonos
    ]


   
#Obtener por id
def get_telefono_by_id(db: Session, id: int):
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    telefonos = db.query(Telefono).filter(Telefono.id_proveedor == id).all()

    return {
        "proveedor": proveedor.nombre,
        "telefonos": [t.num for t in telefonos]
    }


#Obtener telefono por nombre del proveedor
def get_telefono_by_nameProv(db: Session, Proveedor_name: str):
    proveedor = db.query(Proveedor).filter(Proveedor.nombre == Proveedor_name).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    telefonos = db.query(Telefono).filter(Telefono.id_proveedor == proveedor.id_proveedor).all()

    return {
        "proveedor": proveedor.nombre,
        "telefonos": [t.num for t in telefonos]
    }



    
    
