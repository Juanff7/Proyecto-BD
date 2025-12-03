from pydantic import BaseModel, ConfigDict
from typing import Optional

from .proveedor import ProveedorBase


#tefono base
class Telefonobase(BaseModel):
    num: int

class TelefonoCraate(Telefonobase):
    proveedor: Optional[str] = None  
    id_proveedor: Optional[int] = None


class telefonoOut(Telefonobase):
    id: int
    proveedor: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)
    
class TelefonosPorProveedor(BaseModel):
    proveedor: str
    telefonos: list[dict[str, int]]
