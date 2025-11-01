from sqlalchemy.orm import Session
from src.model.empleado import Empleado
from src.schemas.empleados import EmpleadoCreated


#Seguridad de token para el login
from src.core.security import create_access_token
from fastapi import HTTPException, status

#Contraseña encriptada 
import bcrypt

from src.model.cargo import Cargo


#Crear un empleado 
def create_empleado(db: Session, data:EmpleadoCreated) -> Empleado:
    
    #Encriptamos la contraseña para que nadie la vea
    hashed = bcrypt.hashpw(data.contraseña.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    obj= Empleado (
        nombre = data.nombre,
        apellido = data.apellido,
        email = data.email,
        password_hash = hashed,
        id_cargo = data.id_cargo,
        activo = data.activo
    )
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj



#---------------login---------------
def login_empleado(db: Session, email: str, password: str):
    empleado = db.query(Empleado).filter(Empleado.email == email).first()
    if not empleado:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empleado no encontrado")
    if not bcrypt.checkpw(password.encode("utf-8"),empleado.password_hash.encode("utf-8")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Contraseña incorrecta")
    
    token = create_access_token({"sub": str(empleado.id_empleado)})
    return {"access_token" : token, "token_type": "bearer"}

