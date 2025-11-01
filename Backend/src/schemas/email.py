from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

from .proveedor import ProveedorBase


#tefono base
class Emailbase(BaseModel):
    email: EmailStr

class EmailCraate(Emailbase):
    proveedor_n: Optional[str] = None
    proveedor_id: Optional[str] = None

class EmailOut(Emailbase):
    id: int
    proveedor: Optional[ProveedorBase] = None
    model_config = ConfigDict(from_attributes=True)

class EmailPorProveedor(BaseModel):
    proveedor: str 
    email: list[dict[str,int]] #Lista los correos