from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from datetime import datetime

from src.model.productos import Producto
from src.model.detalle_venta import Detalle_venta
from src.model.detalle_Proveedor import Detalle_proveedor
from src.model.venta import Venta
from src.model.historial_precios import Historial_Precios


# ================================
# PRODUCTOS MÁS VENDIDOS
# ================================
def top_productos_vendidos(db: Session, limit=5):
    return (
        db.query(
            Producto.nombre.label("producto"),
            func.sum(Detalle_venta.cantidad).label("cantidad_vendida")
        )
        .join(Detalle_venta, Producto.id_producto == Detalle_venta.id_producto)
        .group_by(Producto.nombre)
        .order_by(func.sum(Detalle_venta.cantidad).desc())
        .limit(limit)
        .all()
    )


# ================================
# PRODUCTOS MÁS COMPRADOS
# ================================
def top_productos_comprados(db: Session, limit=5):
    return (
        db.query(
            Producto.nombre.label("producto"),
            func.sum(Detalle_proveedor.cantidad).label("cantidad_comprada")
        )
        .join(Detalle_proveedor, Producto.id_producto == Detalle_proveedor.id_producto)
        .group_by(Producto.nombre)
        .order_by(func.sum(Detalle_proveedor.cantidad).desc())
        .limit(limit)
        .all()
    )


# ================================
# PROMEDIO Y TOTAL DE VENTAS POR MES
# ================================
def ventas_por_mes(db: Session):
    return (
        db.query(
            extract('month', Venta.fecha).label("mes"),
            func.sum(Venta.total).label("total_mes")
        )
        .group_by(extract('month', Venta.fecha))
        .order_by(extract('month', Venta.fecha))
        .all()
    )


# ================================
# VENTAS DEL MES ACTUAL
# ================================
def ventas_mes_actual(db: Session):
    hoy = datetime.now()
    inicio_mes = datetime(hoy.year, hoy.month, 1)

    total = (
        db.query(func.sum(Venta.total))
        .filter(Venta.fecha >= inicio_mes)
        .scalar()
    )

    return total or 0.0


# ================================
# ESTADÍSTICAS DE PRECIOS
# ================================
def estadisticas_precios(db: Session):
    total = db.query(Historial_Precios).count()

    subidas = (
        db.query(Historial_Precios)
        .filter(Historial_Precios.precio_nuevo > Historial_Precios.precio_anterior)
        .count()
    )

    bajadas = (
        db.query(Historial_Precios)
        .filter(Historial_Precios.precio_nuevo < Historial_Precios.precio_anterior)
        .count()
    )

    return {
        "total": total,
        "subidas": subidas,
        "bajadas": bajadas
    }


# ================================
# ENDPOINT ÚNICO PARA EL DASHBOARD
# ================================
def get_dashboard_data(db: Session):

    # Obtener datos crudos
    top_v = top_productos_vendidos(db)                # [('Dudley', 16), ...]
    top_c = top_productos_comprados(db)               # [('Dudley', 59), ...]
    ventas_m = ventas_por_mes(db)                     # [(Decimal('11'), 4035.0), ...]

    # Convertir datos a formato JSON-friendly
    top_v_json = [{"nombre": t[0], "cantidad": t[1]} for t in top_v]
    top_c_json = [{"nombre": t[0], "cantidad": t[1]} for t in top_c]
    ventas_m_json = [{"mes": int(t[0]), "total": float(t[1])} for t in ventas_m]

    # DEBUG PARA VER YA TRANSFORMADO
    print("\n=== DEBUG TRANSFORMADO ===")
    print("top_vendidos_json:", top_v_json)
    print("top_comprados_json:", top_c_json)
    print("ventas_por_mes_json:", ventas_m_json)
    print("==========================\n")

    return {
        "ventas_mes_actual": ventas_mes_actual(db),
        "producto_mas_vendido": producto_mas_vendido(db),
        "producto_mas_comprado": producto_mas_comprado(db),
        "movimientos_precios": movimientos_precios(db),
        "subidas": subidas_precios(db),
        "bajadas": bajadas_precios(db),

        # Versiones corregidas
        "ventas_por_mes": ventas_m_json,
        "top_vendidos": top_v_json,
        "top_comprados": top_c_json,
    }




# ================================
# PRODUCTO MÁS VENDIDO
# ================================
def producto_mas_vendido(db: Session):
    result = (
        db.query(
            Producto.nombre.label("producto"),
            func.sum(Detalle_venta.cantidad).label("cantidad_vendida")
        )
        .join(Detalle_venta, Producto.id_producto == Detalle_venta.id_producto)
        .group_by(Producto.nombre)
        .order_by(func.sum(Detalle_venta.cantidad).desc())
        .first()
    )

    if not result:
        return {"nombre": "Sin datos", "cantidad": 0}

    return {"nombre": result[0], "cantidad": result[1]}


# ================================
# PRODUCTO MÁS COMPRADO A PROVEEDOR
# ================================
def producto_mas_comprado(db: Session):
    result = (
        db.query(
            Producto.nombre.label("producto"),
            func.sum(Detalle_proveedor.cantidad).label("cantidad_comprada")
        )
        .join(Detalle_proveedor, Producto.id_producto == Detalle_proveedor.id_producto)
        .group_by(Producto.nombre)
        .order_by(func.sum(Detalle_proveedor.cantidad).desc())
        .first()
    )

    if not result:
        return {"nombre": "Sin datos", "cantidad": 0}

    return {"nombre": result[0], "cantidad": result[1]}


# ================================
# SUBIDAS, BAJADAS Y MOVIMIENTOS DE PRECIOS
# ================================
def movimientos_precios(db: Session):
    return db.query(Historial_Precios).count()

def subidas_precios(db: Session):
    return (
        db.query(Historial_Precios)
        .filter(Historial_Precios.precio_nuevo > Historial_Precios.precio_anterior)
        .count()
    )

def bajadas_precios(db: Session):
    return (
        db.query(Historial_Precios)
        .filter(Historial_Precios.precio_nuevo < Historial_Precios.precio_anterior)
        .count()
    )
