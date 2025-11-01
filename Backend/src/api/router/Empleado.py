from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
#Obtener usuario(login)
from src.api.debs import get_db, get_current_user
from src.crud import empleado as Crud_empleado
from src.schemas import empleados as Schema_empleado


router = APIRouter()


#-----------crear un empleado--------------
@router.post("/Create", response_model=Schema_empleado.EmpleadoOut)
def Create_Empleado(empleado: Schema_empleado.EmpleadoCreated, db: Session= Depends(get_db)):
    return Crud_empleado.create_empleado(db=db, data=empleado)

#-----------logear un empleado-------------
@router.post("/login")
def login_empleado(credenciales: Schema_empleado.EmpleadoLogin, db : Session = Depends(get_db)):
    return Crud_empleado.login_empleado(db, credenciales.email, credenciales.contraseña)



#-----------Obtener empleado logueado-------------
@router.get("/Me", response_model= Schema_empleado.EmpleadoOut)
def Obtener_mi_perfil(current_user: Schema_empleado.EmpleadoOut = Depends(get_current_user)):
    return current_user



from fastapi.security import OAuth2PasswordRequestForm

@router.post("/token")
def login_for_swagger(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # usamos username = email
    return Crud_empleado.login_empleado(db, form_data.username, form_data.password)
