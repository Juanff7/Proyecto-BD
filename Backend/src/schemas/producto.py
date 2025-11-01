from pydantic import BaseModel, ConfigDict
from typing import Optional

from .categoria import CategoriaOut


#Producto Base
class ProductoBase(BaseModel):
      nombre: str
      descripcion: Optional[str] = None

class ProductoCreate(ProductoBase):
      categoria: Optional[str] = None 
      costo_venta: float
      imagen_url: Optional[str] = None
      


class ProductoOut(BaseModel):
    id: int
    nombre: str
    descripcion: Optional[str]
    costo_venta: Optional[float] = 0
    cantidad: Optional[int] = 0
    categoria: Optional[CategoriaOut] = None
    imagen_url: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)