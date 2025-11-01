from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, Union

from .producto import ProductoOut
from .venta import ventaOut

class Detalle_ventaBase(BaseModel):
    cantidad: int
    precio_unit: float
    detalle: Optional[str] = None
    

class Detalle_ventaCreate(Detalle_ventaBase):
    id_venta: int
    id_producto: int
    producto: str

class detalle_VentaOut(Detalle_ventaBase):
    id: int
    id_venta: int
    id_producto: int
    sub_total: float
    model_config = ConfigDict(from_attributes=True)
