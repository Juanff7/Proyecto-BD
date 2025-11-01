from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.api.debs import get_db
from src.crud import venta as crud_venta
from src.schemas import venta as Schema_venta

router = APIRouter()

#Crear una venta(registro)
@router.post("/create", response_model=Schema_venta.ventaOut)
def Create_venta(entrada: Schema_venta.VentaCreate, db:Session = Depends(get_db)):
    return crud_venta.Create_venta(db=db, data=entrada)


