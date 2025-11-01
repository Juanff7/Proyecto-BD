from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.api.debs import get_db
from src.crud import detallePro as Crud_det
from src.schemas import detalle_proveedor as Schema_Det



router = APIRouter()

#Crear un Entrada de productos
@router.post("/Create", response_model=Schema_Det.detalleOut)
def Create_Detealle(Entrada: Schema_Det.detalleCreate, db: Session = Depends(get_db)):
    return Crud_det.created_detalle_proveedor(db=db, data=Entrada)

