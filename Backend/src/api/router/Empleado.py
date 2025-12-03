from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.debs import get_db
from src.schemas.empleados import EmpleadoCreate, EmpleadoUpdate, EmpleadoOut
from src.crud import empleado as crud_empleado

router = APIRouter()


# Crear
@router.post("/create", response_model=EmpleadoOut)
def create_empleado(entrada: EmpleadoCreate, db: Session = Depends(get_db)):
    return crud_empleado.create_empleado(db, entrada)


# Obtener todos
@router.get("/obtener_todos", response_model=list[EmpleadoOut])
def obtener_todos(db: Session = Depends(get_db)):
    return crud_empleado.get_all_empleados(db)


# Obtener por ID
@router.get("/obtener/{id_empleado}", response_model=EmpleadoOut)
def obtener_por_id(id_empleado: int, db: Session = Depends(get_db)):
    return crud_empleado.get_empleado(db, id_empleado)


# Actualizar
@router.put("/actualizar/{id_empleado}", response_model=EmpleadoOut)
def actualizar(id_empleado: int, entrada: EmpleadoUpdate, db: Session = Depends(get_db)):
    return crud_empleado.update_empleado(db, id_empleado, entrada)


# Eliminar
@router.delete("/eliminar/{id_empleado}")
def eliminar(id_empleado: int, db: Session = Depends(get_db)):
    return crud_empleado.delete_empleado(db, id_empleado)


from src.utils.search import buscar_por_nombre_lista
from src.model.empleado import Empleado
@router.get("/autocompletado")
def autocomplete_empleado(query: str, db: Session = Depends(get_db)):
    empleados = buscar_por_nombre_lista(db, Empleado, Empleado.nombre, query, limite=5)
    return [{"id": e.id_empleado, "nombre": e.nombre} for e in empleados]
