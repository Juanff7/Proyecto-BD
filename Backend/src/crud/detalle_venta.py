from fastapi import HTTPException
from sqlalchemy.orm import Session
from src.model.detalle_venta import Detalle_venta
from src.schemas.detalle_venta import Detalle_ventaCreate

#Relaciones
from src.model.productos import Producto
from src.model.venta import Venta



#Crear un detalle de venta
def Create_detalleVenta(db: Session, data: Detalle_ventaCreate):
    #Buscamos la venta
    venta = db.query(Venta).filter(Venta.id == data.id_venta).first()
    if not venta:
        raise HTTPException(status_code=404, detail="Venta no encontrada")
    
    #buscamos el producto
    if data.id_producto:
        producto = db.query(Producto).filter(Producto.id == data.id_producto).first()
    elif data.producto:
        producto = db.query(Producto).filter(Producto.nombre == data.producto).first()
    else:
        raise HTTPException(status_code=404, detail="Debes enviar el id del producto o nombre del producto")
    

    if producto.cantidad <= 0:
        raise HTTPException(status_code=404, detail="Producto sin stock disponible")
    elif producto.cantidad < data.cantidad:
        raise HTTPException(status_code=404, detail="Solo hay {producto.Cantidad} de este producto")
    

    
    #Calcular sub total
    subtotal = data.cantidad * data.precio_unit

    #Reduccion de inventario sobre el producto que se esta comprando
    producto.cantidad -= data.cantidad

    #Creamos el detalle
    detalle_venta = Detalle_venta(
        id_venta = data.id_venta,
        id_producto = data.id_producto,
        cantidad = data.cantidad,
        precio_unit = data.precio_unit,
        sub_total = subtotal,
        detalle = data.detalle
    )

    db.add(detalle_venta)
    venta.total = (venta.total or 0) + subtotal

    db.commit()
    db.refresh(detalle_venta)
    return detalle_venta


