from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload
from src.model.detalle_venta import Detalle_venta
from src.model.productos import Producto
from src.model.venta import Venta
from src.schemas.detalle_venta import Detalle_ventaCreate
from src.utils.search import buscar_por_nombre_uno
from datetime import datetime

def create_detalle_venta(db: Session, data: Detalle_ventaCreate):

    # Buscar venta
    venta = db.query(Venta).filter(
        Venta.id_venta == data.id_venta
    ).first()

    if not venta:
        raise HTTPException(404, "Venta no encontrada")

    # Buscar producto por ID o nombre
    if data.id_producto:
        producto = db.query(Producto).filter(
            Producto.id_producto == data.id_producto
        ).first()
    else:
        producto = buscar_por_nombre_uno(
            db, Producto, Producto.nombre, data.producto
        )

    if not producto:
        raise HTTPException(404, "Producto no encontrado")
    
    if producto.cantidad <= 0:
        raise HTTPException(400, "No hay existencias de este producto")

    if producto.cantidad < data.cantidad:
        raise HTTPException(
            400,
            f"Stock insuficiente. Disponible: {producto.cantidad}, requerido: {data.cantidad}"
        )
    
    producto.cantidad -= data.cantidad
    db.add(producto)


    # Precio desde el inventario
    precio_unit = producto.costo_venta 
    sub_total = precio_unit * data.cantidad

    # Crear detalle
    detalle = Detalle_venta(
        id_venta=data.id_venta,
        id_producto=producto.id_producto,
        cantidad=data.cantidad,
        precio_unit=precio_unit,
        sub_total=sub_total,
        detalle=data.detalle
    )

    db.add(detalle)

    # Actualizar total de la venta
    venta.total += sub_total

    db.commit()
    db.refresh(detalle)

    # Cargar relaciones antes de retornar
    detalle = db.query(Detalle_venta).options(
        joinedload(Detalle_venta.producto),
        joinedload(Detalle_venta.venta)
    ).filter(Detalle_venta.id_dv == detalle.id_dv).first()

    return detalle




# Obtener todos los detalles (para el historial global)
def get_all_detalleVenta(db: Session):
    return (
        db.query(Detalle_venta)
        .options(
            joinedload(Detalle_venta.producto),
            joinedload(Detalle_venta.venta).joinedload("cliente"),
            joinedload(Detalle_venta.venta).joinedload("empleado")
        )
        .order_by(Detalle_venta.id_dv.desc())
        .all()
    )


# Eliminar detalle (y revertir stock + total)
def delete_detalleVenta(db: Session, id_detalle_venta: int):

    detalle = db.query(Detalle_venta).filter(
        Detalle_venta.id_dv == id_detalle_venta
    ).first()

    if not detalle:
        raise HTTPException(404, "Detalle no encontrado")

    producto = db.query(Producto).filter(
        Producto.id_producto == detalle.id_producto
    ).first()

    venta = db.query(Venta).filter(
        Venta.id_venta == detalle.id_venta
    ).first()

    # Revertir
    producto.cantidad += detalle.cantidad
    venta.total -= detalle.sub_total

    db.delete(detalle)
    db.commit()

    return {"detail": "Detalle eliminado y stock revertido"}

    # ==========================
    # 💥 ELIMINAR DETALLE
    # ==========================
    db.delete(detalle)
    db.commit()

    return detalle_info



#generar una factura 
def obtener_factura(db: Session, id_venta: int):
    venta = db.query(Venta).filter(Venta.id_venta == id_venta).first()
    if not venta:
        raise HTTPException(404, "venta no encontrada")
    
    detalles = db.query(Detalle_venta).filter(Detalle_venta.id_venta == id_venta).all()


    lista_detalles = []

    for d in detalles:
        lista_detalles.append({
            "producto": d.producto.nombre,
            "cantidad": d.cantidad,
            "precio_unit": d.precio_unit,
            "sub_total": d.sub_total
        })

    return {
        "venta":{
            "id_venta": venta.id_venta,
            "fecha": venta.fecha,
            "cliente": venta.cliente.nombre,
            "empleado": venta.empleado.nombre,
            "total": venta.total
        },
        "detalle": lista_detalles
    }

