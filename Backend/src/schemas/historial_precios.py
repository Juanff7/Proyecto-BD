from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

#relaciones 
from .producto import ProductoOut

class HistorialBase(BaseModel):
    fecha_de_cambio: Optional[datetime] = None

class CreateHistorial(HistorialBase):
    producto: str
    precio_nuevo: float


class HistorialOut(HistorialBase):
    id: int
    id_producto: int
    precio_anterior: Optional[float] = None 
    precio_nuevo: float
    fecha_de_cambio: datetime



