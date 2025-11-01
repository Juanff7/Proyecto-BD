from sqlalchemy.orm import Session
from fastapi import HTTPException 
from src.model.historial_precios import Historial_Precios
from src.schemas.historial_precios import CreateHistorial

from datetime import datetime

from src.model.productos import Producto

def created_historial_precios(db: Session, data: CreateHistorial):

    if isinstance(data.producto, int):
        pro = db.query(Producto).filter(Producto.id == data.producto).first()
    elif isinstance(data.producto, str):
        pro = db.query(Producto).filter(Producto.nombre == data.producto).first()
    else: 
        pro = None
 
    if not pro:
        raise HTTPException(status_code=404, detail="Producto no existe")
    #Guardar precio anterior
    precio_anterior = pro.costo_venta

    #Actualizar precio nuevo
    pro.costo_venta = data.precio_nuevo

    historial = Historial_Precios(
        id_producto = pro.id,
        precio_nuevo = data.precio_nuevo,
        fecha_de_cambio = data.fecha_de_cambio or datetime.now()

    )
    
    db.add(historial)
    db.commit()
    db.refresh(historial)
    return historial
    


def get_allHistorial(db: Session):
    return db.query(Historial_Precios).all()


def get_id(db: Session, Historial: int):
    return db.query(Historial_Precios).filter(Historial_Precios.id == Historial).first()