from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from src.schemas.producto import ProductoOut
# -------------------------
# ENTRADA (para crear)
# -------------------------
class CreateHistorial(BaseModel):
    producto: int   # id del producto
    precio_nuevo: float
    fecha_de_cambio: Optional[datetime] = None


# -------------------------
# SALIDA (para responder)
# -------------------------
class HistorialOut(BaseModel):
    id_historial: int
    id_producto: int
    precio_anterior: Optional[float]
    precio_nuevo: float
    fecha_de_cambio: datetime
    producto: Optional[ProductoOut] = None 

    class Config:
        from_attributes = True
