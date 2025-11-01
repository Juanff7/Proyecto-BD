from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.api.debs import get_db
from src.crud import email as crud_em
from src.schemas import email as schema_em


router = APIRouter()

#Crear correo de empleado
@router.post("/Craar", response_model=schema_em.EmailOut)
def Create(Email: schema_em.EmailOut, db: Session = Depends(get_db)):
    return crud_em.created_email(db=db, data=Email)

@router.get("/Obtener", response_model=List[schema_em.EmailOut])
def get_email(db:Session =Depends(get_db)):
    return crud_em.get_correo(db)


@router.get("/Obtener/name", response_model=schema_em.EmailPorProveedor)
def get_name(nombre: str, db: Session = Depends(get_db)):
    return crud_em.get_email_by_name(db, nombre = nombre )

@router.get("/obtener/id", response_model=schema_em.EmailPorProveedor)
def get_id(id: int, db: Session = Depends(get_db)):
    return crud_em.get_email_by_id(db, id=id )

