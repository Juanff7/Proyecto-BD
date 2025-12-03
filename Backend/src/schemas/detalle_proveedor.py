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
    id_dp: int
    producto: Optional[ProductoOut]
    proveedor: Optional[proveedorOut]
    empleado: Optional[EmpleadoOut]
    precio_unit: float
    cantidad: int
    fecha_ingreso: datetime
    detalle: Optional[str]
    model_config = ConfigDict(from_attributes=True)

from typing import List, Optional

class EntradaSimple(BaseModel):
    id_dp: int
    producto: str
    proveedor: str
    empleado: str
    cantidad: int
    precio_unit: float
    fecha_ingreso: str
    detalle: Optional[str]

class ReporteFiltros(BaseModel):
    search: Optional[str] = None
    fecha: Optional[str] = None
    inicio: Optional[str] = None
    fin: Optional[str] = None

class ReporteEntradaRequest(BaseModel):
    filtros: ReporteFiltros
    entradas: List[EntradaSimple]


 



    