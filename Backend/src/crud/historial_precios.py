from sqlalchemy.orm import Session
from fastapi import HTTPException
from datetime import datetime

from src.model.historial_precios import Historial_Precios
from src.model.productos import Producto
from src.schemas.historial_precios import CreateHistorial


def created_historial_precios(db: Session, data: CreateHistorial):

    # Buscar producto por id o nombre
    if isinstance(data.producto, int):
        pro = db.query(Producto).filter(Producto.id_producto == data.producto).first()
    else:
        pro = db.query(Producto).filter(Producto.nombre == data.producto).first()

    if not pro:
        raise HTTPException(404, "Producto no existe")

    # Guardar precio anterior
    precio_anterior = pro.costo_venta

    # Actualizar al nuevo precio
    pro.costo_venta = data.precio_nuevo

    historial = Historial_Precios(
        id_producto=pro.id_producto,
        precio_anterior=precio_anterior,
        precio_nuevo=data.precio_nuevo,
        fecha_de_cambio=data.fecha_de_cambio or datetime.now()
    )

    db.add(historial)
    db.commit()
    db.refresh(historial)
    return historial


from sqlalchemy.orm import joinedload

def get_all_historial(db: Session):
    return (
        db.query(Historial_Precios)
        .options(joinedload(Historial_Precios.producto))
        .order_by(Historial_Precios.fecha_de_cambio.desc())
        .all()
    )


def get_by_id(db: Session, historial_id: int):
    return db.query(Historial_Precios).filter(Historial_Precios.id == historial_id).first()

def get_by_producto(db: Session, producto_id: int):
    return (
        db.query(Historial_Precios)
        .options(joinedload(Historial_Precios.producto))
        .filter(Historial_Precios.id_producto == producto_id)
        .order_by(Historial_Precios.fecha_de_cambio.desc())
        .all()
    )


def get_by_fecha(db: Session, fecha: datetime):
    return db.query(Historial_Precios)\
        .filter(Historial_Precios.fecha_de_cambio.date() == fecha.date())\
        .all()


def get_rango_fechas(db: Session, desde: datetime, hasta: datetime):
    return db.query(Historial_Precios)\
        .filter(Historial_Precios.fecha_de_cambio >= desde)\
        .filter(Historial_Precios.fecha_de_cambio <= hasta)\
        .order_by(Historial_Precios.fecha_de_cambio.asc())\
        .all()
