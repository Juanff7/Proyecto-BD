from pydantic import BaseModel

class EmpleadoBase(BaseModel):
    nombre: str
    apellido: str
    email: str
    id_cargo: int
    activo: bool = True


class EmpleadoCreate(EmpleadoBase):
    pass


class EmpleadoUpdate(EmpleadoBase):
    pass


class EmpleadoOut(EmpleadoBase):
    id_empleado: int

    class Config:
        from_attributes = True
