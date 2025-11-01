from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, Union

from .proveedor import proveedorOut
from .producto import ProductoOut
from .empleados import EmpleadoOut


class Detalleproveedor(BaseModel):
    detalle: Optional[str] = None
    precio_unit: float
    cantidad: int 
    fecha_ingreso: Optional[datetime] = None   

class detalleCreate(Detalleproveedor):
    producto: str
    proveedor: str 
    empleado: str

class detalleOut(Detalleproveedor):
    id: int
    total: Optional[float] = None
    producto: Optional[ProductoOut] = None
    proveedor: Optional[proveedorOut] =None 
    empleado: Optional[EmpleadoOut] = None 
    model_config = ConfigDict(from_attributes=True)
 


 



    