from pydantic import BaseModel, ConfigDict


class CategoriaBase(BaseModel):
    tipo: str

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaOut(CategoriaBase):
    id_categoria: int 
    model_config = ConfigDict(from_attributes=True)