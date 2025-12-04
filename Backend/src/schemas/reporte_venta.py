# src/schemas/reporte_venta.py

from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class ReporteVentaRequest(BaseModel):
    fecha_inicio: Optional[date] = None
    fecha_fin: Optional[date] = None
    cliente: Optional[str] = None
    empleado: Optional[str] = None


class ItemVenta(BaseModel):
    producto: str
    cantidad: int
    precio: float
    subtotal: float


class ReporteVentaResponse(BaseModel):
    id_venta: int
    fecha: date
    cliente: str
    empleado: str
    total: float
    items: Optional[List[ItemVenta]] = None
