from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProveedorBase(BaseModel):
    nombre: str
    apellido: Optional[str] = None
    usuario_ebay: Optional[str] = None
    pais: Optional[str] = None 
    tipo: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    model_config = ConfigDict(from_attributes=True)

class proveedorOut(ProveedorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
