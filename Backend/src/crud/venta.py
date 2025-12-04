from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from datetime import datetime
from sqlalchemy import extract

from src.model.venta import Venta
from src.model.cliente import Cliente
from src.model.empleado import Empleado
from datetime import date

from src.utils.search import buscar_por_nombre_uno


# ----------------------------------------------------------------
# CREAR
# ----------------------------------------------------------------
def Create_venta(db: Session, data):

    cliente = buscar_por_nombre_uno(db, Cliente, Cliente.nombre, data.cliente)
    if not cliente:
        raise HTTPException(404, "Cliente no encontrado")

    empleado = buscar_por_nombre_uno(db, Empleado, Empleado.nombre, data.empleado)
    if not empleado:
        raise HTTPException(404, "Empleado no encontrado")

    venta_registro = Venta(
        id_cliente=cliente.id_cliente,
        id_empleado=empleado.id_empleado,
        fecha=data.fecha or datetime.now(),
        total=0.0
    )

    db.add(venta_registro)
    db.commit()
    db.refresh(venta_registro)

    return venta_registro


# Obtener todas las ventas
def get_allventas(db: Session):
    return (
        db.query(Venta)
        .options(joinedload(Venta.cliente), joinedload(Venta.empleado))
        .order_by(Venta.fecha.desc())
        .all()
    )


from sqlalchemy import cast, Date

def buscar_por_fecha(db: Session, fecha: str):
    return (
        db.query(Venta)
        .options(joinedload(Venta.cliente), joinedload(Venta.empleado))
        .filter(cast(Venta.fecha, Date) == fecha)
        .all()
    )

# Obtener ventas por rango
def get_por_rango(db: Session, inicio: date, fin: date):
    inicio_dt = datetime.combine(inicio, datetime.min.time())
    fin_dt = datetime.combine(fin, datetime.max.time())

    return (
        db.query(Venta)
        .filter(Venta.fecha >= inicio_dt, Venta.fecha <= fin_dt)
        .options(joinedload(Venta.cliente), joinedload(Venta.empleado))
        .order_by(Venta.fecha.desc())
        .all()
    )


# Factura (venta + detalles)
from src.model.detalle_venta import Detalle_venta
def obtener_factura(db: Session, id_venta: int):
    venta = (
        db.query(Venta)
        .options(
            joinedload(Venta.cliente),
            joinedload(Venta.empleado),
            joinedload(Venta.detalle_venta).joinedload(Detalle_venta.producto)
        )
        .filter(Venta.id_venta == id_venta)
        .first()
    )

    if not venta:
        raise HTTPException(404, "Venta no encontrada")

    return {
    "id_venta": venta.id_venta,
    "cliente": venta.cliente.nombre,
    "empleado": venta.empleado.nombre,
    "fecha": venta.fecha,
    "total": venta.total,
    "detalles": [
        {
            "id_dv": d.id_dv,
            "producto": d.producto.nombre if d.producto else "Producto eliminado",
            "cantidad": d.cantidad,
            "precio_unit": d.precio_unit,
            "sub_total": d.sub_total
        }
        for d in venta.detalle_venta
    ]
}




from sqlalchemy import and_, extract

def obtener_ventas_mes(db: Session):
    """
    Devuelve las ventas del MES y AÑO actuales.
    Tú ya las limitabas a 4, lo mantengo.
    """
    ahora = datetime.now()
    mes_actual = ahora.month
    año_actual = ahora.year

    ventas = (
        db.query(Venta)
        .options(joinedload(Venta.cliente), joinedload(Venta.empleado))
        .filter(
            extract("month", Venta.fecha) == mes_actual,
            extract("year", Venta.fecha) == año_actual,
        )
        .order_by(Venta.fecha.desc())
        .limit(4)
        .all()
    )

    return ventas