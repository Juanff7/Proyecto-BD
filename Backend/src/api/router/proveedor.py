from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from src.api.debs import get_db
from src.crud import proveedor as crud_prove
from src.schemas import proveedor as schema_prove


router = APIRouter()

#Crear un proveedor
@router.post("/create", response_model=schema_prove.ProveedorCreate)
def Create_Prove(Proveedor: schema_prove.ProveedorCreate, db: Session = Depends(get_db)):
    return crud_prove.Created_proveedor(db=db, Data = Proveedor)


#Obtener proveedor
@router.get("/Obtener" ,response_model=List[schema_prove.proveedorOut])
def get(db: Session = Depends(get_db)):
    return crud_prove.get_allProveedor(db)

@router.get("/ObtenerNombre", response_model=schema_prove.proveedorOut)
def get_name(Proveedor: str, db: Session = Depends(get_db)):
    proveedor = crud_prove.get_name(db, getName=Proveedor)
    if proveedor is None: 
         raise HTTPException(status_code=404, detail="Proveedor no encontrado")  
    return proveedor

@router.get("ObtenerId", response_model=schema_prove.proveedorOut)
def Get_id(id: int, db: Session = Depends(get_db)):
   Proveedor = crud_prove.get_id(db, getid=id)
   if Proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor not found")
   return Proveedor
