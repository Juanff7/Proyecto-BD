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

#Actualizar Proveedor
@router.put("/update/{id_proveedor}", response_model=schema_prove.ProveedorCreate)
def update_prov(id_proveedor: int, proveedor: schema_prove.ProveedorCreate, db: Session = Depends(get_db)):
    return crud_prove.Update_proveedor(db, id_Proveedor=id_proveedor, data=proveedor)

#Eliminar Proveedor
@router.delete("/delete/{id_proveedor}")
def delete_prov(id_proveedor: int, db: Session = Depends(get_db)):
    return crud_prove.delete_proveedor(db, id=id_proveedor)

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


@router.get("/ObtenerId", response_model=schema_prove.proveedorOut)
def Get_id(id: int, db: Session = Depends(get_db)):
   proveedor = crud_prove.get_id(db, getid=id)
   if proveedor is None:
        raise HTTPException(status_code=404, detail="Proveedor no encontrado")
   return proveedor

from src.utils.search import buscar_por_nombre_lista
from src.model.Proveedor import Proveedor
@router.get("/autocompletado")
def autocomplete_proveedor(query: str, db: Session = Depends(get_db)):
    proveedores = buscar_por_nombre_lista(db, Proveedor, Proveedor.nombre, query, limite=5)
    return [{"id": p.id_proveedor, "nombre": p.nombre} for p in proveedores]
