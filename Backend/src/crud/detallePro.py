from sqlalchemy.orm import Session
from fastapi import HTTPException 
from src.model.detalle_Proveedor import Detalle_proveedor
from src.schemas.detalle_proveedor import detalleCreate

from datetime import datetime

#Relaciones
from src.model.productos import Producto
from src.model.Proveedor import Proveedor
from src.model.empleado import Empleado


def created_detalle_proveedor(db: Session, data: detalleCreate):

    #Buscamos producto por su id o nombre 
    if isinstance(data.producto, int):
        pro = db.query(Producto).filter(Producto.id == data.producto ).first()

    elif isinstance(data.producto, str):
        pro = db.query(Producto).filter(Producto.nombre == data.producto).first()
    else:
        pro = None

    #Buscamos empleado por nombre
    emp = db.query(Empleado).filter(Empleado.nombre == data.empleado).first()
    if not emp:
         raise HTTPException(status_code=404, detail="Empleado no encontrado")
    prov = db.query(Proveedor).filter(Proveedor.nombre == data.proveedor).first()



    if not pro:
        #Si el producto no existe -> se crea
        Nuevo_Producto = Producto(
            nombre = data.producto, #usamos el texto
            cantidad = data.cantidad,
 
        )
        db.add(Nuevo_Producto)
        db.flush() # Guarda temporalmente en la sesion para obtener su id
        db.refresh(Nuevo_Producto)
        
        producto_id = Nuevo_Producto.id


     #Si el producto ya existe
    else:
        pro.cantidad += data.cantidad

        producto_id = pro.id
    
    

    #Creamos el registro de detalle proveedor
    detalle = Detalle_proveedor(
        producto_id = producto_id,
        proveedor_id = prov.id,
        precio_unit = data.precio_unit,
        cantidad = data.cantidad,
        fecha_ingreso = data.fecha_ingreso or datetime.now(),
        detalle = data.detalle,
        empleado_id = emp.id_empleado
    )
    db.add(detalle)
    db.commit()
    db.refresh(detalle)
    return detalle

