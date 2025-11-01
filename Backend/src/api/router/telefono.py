from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from src.api.debs import get_db
from src.crud import telefono as crud_Tel
from src.schemas import telefono as Schema_tel



router = APIRouter()

@router.post("/create", response_model=Schema_tel.telefonoOut)
def create_telefono(telefono: Schema_tel.TelefonoCraate, db: Session = Depends(get_db)):
    return crud_Tel.Created_tel(db=db, data=telefono)

@router.get("/obtener/todos", response_model=List[Schema_tel.telefonoOut])
def get_all_telefonos(db: Session = Depends(get_db)):
    return crud_Tel.get_telefonos(db)

@router.get("/obtener/name", response_model=Schema_tel.TelefonosPorProveedor)
def get_telefono_por_nombre(nombre: str, db: Session = Depends(get_db)):
    return crud_Tel.get_telefono_by_nameProv(db, Proveedor_name=nombre)

@router.get("/obtener/id", response_model=Schema_tel.TelefonosPorProveedor)
def get_telefono_por_id(id: int, db: Session = Depends(get_db)):
    return crud_Tel.get_telefono_by_id(db, id=id)


