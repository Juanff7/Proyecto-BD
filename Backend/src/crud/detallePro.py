from sqlalchemy.orm import Session
from fastapi import HTTPException 
from src.model.detalle_Proveedor import Detalle_proveedor
from src.schemas.detalle_proveedor import detalleCreate

from datetime import datetime
from datetime import datetime, date
#Relaciones
from src.model.productos import Producto
from src.model.Proveedor import Proveedor
from src.model.empleado import Empleado


from sqlalchemy import func
from fastapi import HTTPException
from datetime import datetime
from src.model.productos import Producto
from src.model.Proveedor import Proveedor
from src.model.empleado import Empleado
from src.model.detalle_Proveedor import Detalle_proveedor



# funcion de busqueda
from src.utils.search import buscar_por_nombre_uno

def created_detalle_proveedor(db: Session, data: detalleCreate):

    producto  = buscar_por_nombre_uno(db, Producto, Producto.nombre, data.producto)
    if not producto:
         raise HTTPException(400, "Producto no existe en el inventario, añadir en registro de productos")
    
    emp = buscar_por_nombre_uno(db, Empleado, Empleado.nombre, data.empleado)
    if not emp:
         raise HTTPException(400, "Empleado no reconocido")
    pro = buscar_por_nombre_uno(db, Proveedor, Proveedor.nombre, data.proveedor)
    if not pro:
         raise HTTPException(400, "Proveedor no reconocido no reconocido")
    

    if data.precio_unit < 0:
        raise HTTPException(404, "el precio no es valido")


    producto.cantidad += data.cantidad

    db.add(producto)
    db.flush()
    db.refresh(producto)
        
    # ---------- CREAR DETALLE ----------
    detalle = Detalle_proveedor(
        id_producto=producto.id_producto,
        id_proveedor=pro.id_proveedor,
        id_empleado=emp.id_empleado,
        precio_unit=data.precio_unit,
        cantidad=data.cantidad,
        fecha_ingreso=data.fecha_ingreso or datetime.now(),
        detalle=data.detalle
    )

    db.add(detalle)
    db.commit()
    db.refresh(detalle)

    return detalle



from sqlalchemy.orm import joinedload
# -------------------------------------------------------
#  OBTENER TODO EL HISTORIAL (TABLA COMPLETA)
# -------------------------------------------------------
def get_historial(db: Session):
    return (
        db.query(Detalle_proveedor)
        .options(
            joinedload(Detalle_proveedor.proveedor),
            joinedload(Detalle_proveedor.empleado),
            joinedload(Detalle_proveedor.producto)
        )
        .order_by(Detalle_proveedor.fecha_ingreso.desc())
        .all()
    )


# -------------------------------------------------------
#  OBTENER POR FECHA EXACTA
# -------------------------------------------------------
def get_fecha(fecha: date, db: Session):
    inicio = datetime.combine(fecha, datetime.min.time())
    fin = datetime.combine(fecha, datetime.max.time())

    return (
        db.query(Detalle_proveedor)
        .filter(Detalle_proveedor.fecha_ingreso >= inicio)
        .filter(Detalle_proveedor.fecha_ingreso <= fin)
        .order_by(Detalle_proveedor.fecha_ingreso.desc())
        .all()
    )


# -------------------------------------------------------
#  OBTENER POR RANGO DE FECHAS
# -------------------------------------------------------
def get_rango_fechas(db: Session, inicio: date, fin: date):
    inicio_dt = datetime.combine(inicio, datetime.min.time())
    fin_dt = datetime.combine(fin, datetime.max.time())

    return (
        db.query(Detalle_proveedor)
        .filter(Detalle_proveedor.fecha_ingreso >= inicio_dt)
        .filter(Detalle_proveedor.fecha_ingreso <= fin_dt)
        .order_by(Detalle_proveedor.fecha_ingreso.desc())
        .all()
    )


# -------------------------------------------------------
#  OBTENER POR PROVEEDOR
# -------------------------------------------------------
def get_por_proveedor(db: Session, proveedor: str):
    pro = buscar_por_nombre_uno(db, Proveedor, Proveedor.nombre, proveedor)
    if not pro:
        raise HTTPException(404, "Proveedor no encontrado")

    return (
        db.query(Detalle_proveedor)
        .filter(Detalle_proveedor.id_proveedor == pro.id_proveedor)
        .options(
            joinedload(Detalle_proveedor.proveedor),
            joinedload(Detalle_proveedor.empleado),
            joinedload(Detalle_proveedor.producto),
        )
        .order_by(Detalle_proveedor.fecha_ingreso.desc())
        .all()
    )


# -------------------------------------------------------
#  OBTENER POR PRODUCTO
# -------------------------------------------------------
def get_por_producto(db: Session, producto_nombre: str):
    pro = buscar_por_nombre_uno(db, Producto, Producto.nombre, producto_nombre)
    if not pro:
        raise HTTPException(404, "Producto no encontrado")

    return (
        db.query(Detalle_proveedor)
        .filter(Detalle_proveedor.id_producto == pro.id_producto)
        .options(
            joinedload(Detalle_proveedor.proveedor),
            joinedload(Detalle_proveedor.empleado),
            joinedload(Detalle_proveedor.producto),
        )
        .order_by(Detalle_proveedor.fecha_ingreso.desc())
        .all()
    )


# -------------------------------------------------------
#  OBTENER POR EMPLEADO
# -------------------------------------------------------
def get_por_empleado(db: Session, empleado_nombre: str):
    emp = buscar_por_nombre_uno(db, Empleado, Empleado.nombre, empleado_nombre)
    if not emp:
        raise HTTPException(404, "Empleado no encontrado")

    return (
        db.query(Detalle_proveedor)
        .filter(Detalle_proveedor.id_empleado == emp.id_empleado)
        .options(
            joinedload(Detalle_proveedor.proveedor),
            joinedload(Detalle_proveedor.empleado),
            joinedload(Detalle_proveedor.producto),
        )
        .order_by(Detalle_proveedor.fecha_ingreso.desc())
        .all()
    )


# -------------------------------------------------------
#  ELIMINAR DETALLE Y RESTAR STOCK
# -------------------------------------------------------
def delete_detalle_proveedor(db: Session, id_dp: int):
    detalle = db.query(Detalle_proveedor).filter(
        Detalle_proveedor.id_dp == id_dp
    ).first()

    if not detalle:
        raise HTTPException(404, "Registro no encontrado")

    producto = db.query(Producto).filter(
        Producto.id_producto == detalle.id_producto
    ).first()

    if producto.cantidad - detalle.cantidad < 0:
        raise HTTPException(
            400,
            f"No se puede eliminar porque el inventario quedaría negativo. Stock actual: {producto.cantidad}"
        )

    # Revertir inventario
    producto.cantidad -= detalle.cantidad

    db.delete(detalle)
    db.commit()

    return {"detail": "Entrada eliminada y stock revertido correctamente"}