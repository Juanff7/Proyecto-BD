from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import Optional, Union

from .producto import ProductoOut
from .venta import VentaOut

class Detalle_ventaBase(BaseModel):
    cantidad: int
    detalle: Optional[str] = None
    

class Detalle_ventaCreate(Detalle_ventaBase):
    id_venta: int
    id_producto: Optional[int] = None 
    producto: Optional[str] = None 

class detalle_VentaOut(Detalle_ventaBase):
    id_dv: int
    id_venta: int
    venta: Optional[VentaOut] = None
    id_producto: int
    producto: Optional[ProductoOut] = None
    precio_unit: float
    sub_total: float
    model_config = ConfigDict(from_attributes=True)

class detalle_ventaSimple(BaseModel):
    id_dv: int
    producto: str
    cantidad: int
    precio_unit: float
    sub_total: float
    cliente: str
    empleado: str

    model_config = ConfigDict(from_attributes=True)
from src.schemas.producto import ProductoBase
class DetalleVentaResponse(BaseModel):
    id_detalle: int
    cantidad: int
    precio_unit: float
    sub_total: float
    producto: ProductoBase | None = None

    model_config = ConfigDict(from_attributes=True)
    
