from pydantic import BaseModel, ConfigDict
from typing import Optional


class ClienteBase(BaseModel):
    nombre: str
    direccion: Optional[str] = None
    telefono: int
    model_config =ConfigDict(from_attributes=True)

class ClienteOut(ClienteBase):
    id: int
    pass

class ClienteUpdate(BaseModel):
    direccion: Optional[str] = None
    telefono: int
    model_config = ConfigDict(from_attributes= True )

