from pydantic import BaseModel, ConfigDict

class CargoBase(BaseModel):
    tipo: str

class CargoCreate(CargoBase):
    pass 

class Cargoout(CargoBase):
    id_cargo: int
    model_config = ConfigDict(from_attributes=True)

    
    