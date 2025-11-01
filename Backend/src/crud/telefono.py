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
        proveedor = db.query(Proveedor).filter(Proveedor.id == data.id_proveedor).first()
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
        id_proveedor = proveedor.id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    
    return{
        "id": obj.id,
        "proveedor": proveedor.nombre,
        "num": data.num        
    }


#Obtener todos
def get_telefonos(db: Session):
    #relacion directamente con joined
    telefonos = db.query(Telefono).options(joinedload(Telefono.proveedor)).all()
    return [
        {
            "id": tel.id,
            "proveedor": tel.proveedor.nombre if tel.proveedor else None,
            "num": tel.num
        }
        for tel in telefonos
    ]



   
#Obtener por id
def get_telefono_by_id(db:Session, id: int):
    proveedor = db.query(Proveedor).filter(Proveedor.id == id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    telefono = db.query(Telefono).filter(Telefono.id_proveedor == id).all()

    if not telefono:    
        raise HTTPException(status_code=404, detail="Proveedor no tiene numeros")
    
   
    return {
        "proveedor": proveedor.nombre,
        "telefonos": [{"num": t.num }for t in telefono]
        
    }


#Obtener telefono por nombre del proveedor
def get_telefono_by_nameProv(db:Session, Proveedor_name:str):
    proveedor = db.query(Proveedor).filter(Proveedor.nombre == Proveedor_name).first()
    if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    telefono = db.query(Telefono).filter(Telefono.id_proveedor == proveedor.id).all()
    if not telefono:
            raise HTTPException(status_code=404, detail="Proveedor no tiene numeros")
    
    return {
        "proveedor": proveedor.nombre,
        "telefonos": [{"num": t.num }for t in telefono]
        
    }


    
    
