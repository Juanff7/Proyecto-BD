from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional


from .cargo import Cargoout


#Empleado base
class EmpleadoBase(BaseModel):
    email: EmailStr
    nombre: str
    apellido: str 

#-------------Crear empleado--------------------
class EmpleadoCreated(EmpleadoBase):
    contraseña: str
    id_cargo: int 
    activo:Optional[bool] = True


#-----------Obtener empleado en pantalla---------
class EmpleadoOut(EmpleadoBase):
    id_empleado : int
    activo: bool
    cargo: Optional[Cargoout] = None
    model_config = ConfigDict(from_attributes=True)


#------------login----------
class EmpleadoLogin(BaseModel):
    email: EmailStr
    contraseña: str
    


    

