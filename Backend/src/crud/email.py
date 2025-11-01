from sqlalchemy.orm import Session
from src.model.Email import Email
from src.schemas.email import EmailCraate
from fastapi import HTTPException

from src.model.Proveedor import Proveedor 

#relacion directamente
from sqlalchemy.orm import joinedload


#Crear un email
def created_email(db:Session, data: EmailCraate):
    #usando el id del proveedor directamente
    if data.proveedor_id:
        proveedor = db.query(Proveedor).filter(Proveedor.id == data.proveedor_id).first()
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    elif data.proveedor_n:
        proveedor = db.query(Proveedor).filter(Proveedor.nombre == data.proveedor_n).first
        if not proveedor:
            raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    else: 
            raise HTTPException(status_code=404, detail="debes enviar un id o un nombre")
    obj = Email(
        email = data.email,
        id_proveedor = proveedor.id
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return{
        "id": obj.id,
        "proveedor": proveedor.nombre,
        "correo": data.email        
    }   

def get_correo(db:Session):
      #relacion con joined
      correo = db.query(Email).options(joinedload(Email.proveedor)).all()
      return [
            {
            "id": Ema.id,
            "proveedor": Ema.proveedor.nombre if Ema.proveedor else None,
            "Correo": Ema.email 
        }
        for Ema in correo
    ]


#Obtener por nombre 
def get_email_by_name(db: Session, nombre: str):
     proveedor = db.query(Proveedor).filter(Proveedor.nombre == nombre).first()
     if not proveedor:
             raise HTTPException(status_code=404, detail="Proveedor no encontrado")
     email = db.query(Email).filter(Email.id_proveedor == proveedor.id).first()
     return {
          "proveedor": proveedor.nombre,
          "Correos": [{"correo": m.email } for m in email]
     }



#Obtener por id
def get_email_by_id(db:Session, id: int):
     proveedor = db.query(Proveedor).filter(Proveedor.id == id).first()
     if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
     email = db.query(Email).filter(Email.id_proveedor == id)
     if not email:
             raise HTTPException(status_code=404, detail="Proveedor no encontrado")
     return{
          "proveedor": proveedor.nombre,
          "Correos": [{"correo": m.email}for m in email]
     } 

          