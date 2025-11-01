from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.model.venta import Venta
from src.schemas.venta import VentaCreate

from datetime import datetime

#Relaciones
from src.model.cliente import Cliente 
from src.model.empleado import Empleado




def Create_venta(db: Session, data: VentaCreate):
    #Buscamos cliente por su id o nombre
    if data.id_cliente:
        client = db.query(Cliente).filter(Cliente.id == data.id_cliente).first()
    elif data.cliente:
        client = db.query(Cliente).filter(Cliente.nombre == data.cliente).first()
    else: 
         raise HTTPException(status_code=400, detail="Debes enviar id_cliente o nombre del cliente")

    if not client:
        raise HTTPException(status_code=404, detail="Cliente no encontrado")
    
    #Buscar empleado por su id o nombre
    if data.id_empleado:
        emp = db.query(Empleado).filter(Empleado.id_empleado == data.id_empleado).first()
    elif data.empleado:
        emp = db.query(Empleado).filter(Empleado.nombre == data.empleado).first()
    else: 
         raise HTTPException(status_code=400, detail="Debes enviar id_cliente o nombre del cliente")

    if not emp:
        raise HTTPException(status_code=404, detail="empleado no encontrado")
    
    #Cramos el registro
    venta_registro = Venta(
        id_cliente = client.id,
        id_empleado = emp.id_empleado,
        fecha = data.fecha or datetime.now(),
        total = 0.0
    )
    db.add(venta_registro)
    db.commit()
    db.refresh(venta_registro)
    return venta_registro