from fastapi import HTTPException
from sqlalchemy.orm import Session

from src.model.empleado import Empleado
from src.schemas.empleados import EmpleadoCreate, EmpleadoUpdate


# Crear empleado
def create_empleado(db: Session, data: EmpleadoCreate):
    empleado = Empleado(
        nombre=data.nombre,
        apellido=data.apellido,
        email=data.email,
        id_cargo=data.id_cargo,
        activo=data.activo
    )
    db.add(empleado)
    db.commit()
    db.refresh(empleado)
    return empleado


# Obtener todos
def get_all_empleados(db: Session):
    return db.query(Empleado).all()


# Obtener uno por ID
def get_empleado(db: Session, id_empleado: int):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    return empleado


# Actualizar empleado
def update_empleado(db: Session, id_empleado: int, data: EmpleadoUpdate):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")
    
    empleado.nombre = data.nombre
    empleado.apellido = data.apellido
    empleado.email = data.email
    empleado.id_cargo = data.id_cargo
    empleado.activo = data.activo

    db.commit()
    db.refresh(empleado)
    return empleado


# Eliminar empleado
def delete_empleado(db: Session, id_empleado: int):
    empleado = db.query(Empleado).filter(Empleado.id_empleado == id_empleado).first()
    if not empleado:
        raise HTTPException(status_code=404, detail="Empleado no encontrado")

    db.delete(empleado)
    db.commit()
    return {"detail": "Empleado eliminado correctamente"}
