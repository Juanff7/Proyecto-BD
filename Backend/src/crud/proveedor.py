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


def get_allProveedor(db: Session):
    return db.query(Proveedor).all()


def get_name(db:Session , getName: str):
    return db.query(Proveedor).filter(Proveedor.nombre == getName).first()

def get_id(db:Session, getid: int):
    return db.query(Proveedor).filter(Proveedor.id == getid).first()
