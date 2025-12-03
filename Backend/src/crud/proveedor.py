from http.client import HTTPException
from sqlalchemy.orm import  Session
from src.model.Proveedor import Proveedor
from src.schemas.proveedor import ProveedorCreate




def Created_proveedor(db:Session, Data: ProveedorCreate ):
    Prov = Proveedor(
        nombre = Data.nombre,
        apellido = Data.apellido,
        usuario_ebay = Data.usuario_ebay,
        pais = Data.pais,
        tipo = Data.tipo
    )
    db.add(Prov)
    db.commit()
    db.refresh(Prov)
    return Prov

def Update_proveedor(db: Session, id_Proveedor: int, data: ProveedorCreate):
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id_Proveedor).first()
    if not proveedor: 
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    proveedor.nombre = data.nombre
    proveedor.apellido = data.apellido  
    proveedor.usuario_ebay = data.usuario_ebay
    proveedor.pais = data.pais
    proveedor.tipo = data.tipo
    db.commit()
    db.refresh(proveedor)
    return proveedor

def delete_proveedor(db:Session, id:int):
    proveedor = db.query(Proveedor).filter(Proveedor.id_proveedor == id).first()
    if not proveedor:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
    db.delete(proveedor)
    db.commit()
    return {"detail": "Proveedor eliminado correctamente"}

def get_allProveedor(db: Session):
    return db.query(Proveedor).all()

def get_name(db:Session , getName: str):
    return db.query(Proveedor).filter(Proveedor.nombre.ilike(getName)).first()

def get_id(db:Session, getid: int):
    return db.query(Proveedor).filter(Proveedor.id_proveedor == getid).first()
