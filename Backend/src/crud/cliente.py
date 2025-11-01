from sqlalchemy.orm import Session
from src.model.cliente import Cliente
from src.schemas.Cliente import ClienteBase, ClienteUpdate
from fastapi import HTTPException



def Created_Cliente(db:Session, data: ClienteBase):
    Client = Cliente(
        nombre = data.nombre,
        direccion = data.direccion,
        telefono = data.telefono

    )
    db.add(Client)
    db.commit()
    db.refresh(Client)
    return Client


def Update_Cliente(db: Session, id: int, data: ClienteUpdate):
    cliente = db.query(Cliente).filter(Cliente.id == id).first()
    if not cliente: 
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    if data.direccion is not None:
        cliente.direccion = data.direccion
    if data.telefono is not None:
        cliente.telefono = data.telefono
    
    
    db.commit()
    db.refresh(cliente)
    return cliente 
    




def get_allCLiente(db:Session):
    return db.query(Cliente).all()


def get_name(db:Session, name: str):
    return db.query(Cliente).filter(Cliente.nombre == name).first()

def get_id(db:Session, id: int):
    return db.query(Cliente).filter(Cliente.id == id).first()


