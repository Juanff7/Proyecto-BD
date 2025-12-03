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
    proveedor = None
    if data.proveedor_id:
          proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == data.proveedor_id).first()
    elif data.proveedor_n:
          proveedor = db.query(Proveedor).filter(Proveedor.nombre == data.proveedor_n).first()
    
    if not proveedor:
          raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    
    nuevo_email = Email(
          email = data.email,
          id_proveedor = proveedor.id_proveedor
    )
    db.add(nuevo_email)
    db.commit()
    db.refresh(nuevo_email)

    return {
            "id": nuevo_email.id_email,
            "email": nuevo_email.email,
            "id_proveedor": {
                    "id": proveedor.id_proveedor,
                    "nombre": proveedor.nombre
            }
    }
def get_correo(db: Session):
    correos = db.query(Email).options(joinedload(Email.proveedor)).all()

    return [
        {
            "id": c.id_email,
            "email": c.email,
            "proveedor": c.proveedor.nombre if c.proveedor else None
        }
        for c in correos
    ]


#Obtener por nombre 
def get_email_by_name(db: Session, nombre: str):
    proveedor = db.query(Proveedor).filter(Proveedor.nombre == nombre).first()
    
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    emails = db.query(Email).filter(Email.id_proveedor == proveedor.id_proveedor).all()

    return {
        "proveedor": proveedor.nombre,
        "Correos": [{"correo": m.email} for m in emails]
    }


def get_email_by_id(db:Session, id: int):
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
    
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")

    emails = db.query(Email).filter(Email.id_proveedor == id).all()

    if not emails:
        raise HTTPException(status_code=404, detail="Proveedor no tiene emails")

    return {
        "proveedor": proveedor.nombre,
        "Correos": [{"correo": m.email} for m in emails]
    }
