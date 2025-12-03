from pydantic import BaseModel
from datetime import datetime
from typing import Optional

# ---------------------------------------------------------
# SUBSCHEMAS PARA RELACIONES
# ---------------------------------------------------------
class ClienteMini(BaseModel):
    nombre: str
    class Config:
        orm_mode = True

class EmpleadoMini(BaseModel):
    nombre: str
    class Config:
        orm_mode = True


# ---------------------------------------------------------
# CREATE
# ---------------------------------------------------------
class VentaCreate(BaseModel):
    cliente: str
    empleado: str
    fecha: Optional[datetime] = None


# ---------------------------------------------------------
# OUTPUT
# ---------------------------------------------------------
class VentaOut(BaseModel):
    id_venta: int
    fecha: datetime
    total: float

    cliente: ClienteMini
    empleado: EmpleadoMini

    class Config:
        orm_mode = True
