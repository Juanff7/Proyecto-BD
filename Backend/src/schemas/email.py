from pydantic import BaseModel, ConfigDict, EmailStr
from typing import Optional

from .proveedor import ProveedorBase


#tefono base
class Emailbase(BaseModel):
    email: EmailStr

class EmailCraate(Emailbase):
    proveedor_n: Optional[str] = None
    proveedor_id: Optional[int] = None

class EmailOut(BaseModel):
    id: int
    email: EmailStr
    proveedor: Optional[str] = None  # ← SOLO nombre del proveedor

    model_config = ConfigDict(from_attributes=True)


class EmailPorProveedor(BaseModel):
    proveedor: str
    correos: list[str]
