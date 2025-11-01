from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional

from .Cliente import ClienteOut
from .empleados import EmpleadoOut

class VentaBase(BaseModel):
    fecha: Optional[datetime] = None

class VentaCreate(VentaBase):
    id_cliente: Optional[int] = None
    cliente: Optional[str] = None    
    id_empleado: Optional[int] = None
    empleado: Optional[str] = None

class ventaOut(VentaBase):
    id: int
    
    total: Optional[float] = None

    id_cliente: int
    id_empleado: int
    
    cliente: Optional[ClienteOut] = None 
    empleado: Optional[EmpleadoOut] = None
    
    model_config = ConfigDict(from_attributes=True)

