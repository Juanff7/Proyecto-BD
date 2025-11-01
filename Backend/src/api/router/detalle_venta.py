from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.debs import get_db

from src.crud import detalle_venta as crud_Dventa
from src.schemas import detalle_venta as Schema_Dventa


router = APIRouter()

#Crear un detalle
@router.post("/Create", response_model= Schema_Dventa.detalle_VentaOut)
def create_detalle_venta(entrada: Schema_Dventa.Detalle_ventaCreate, db: Session = Depends(get_db)):
    return crud_Dventa.Create_detalleVenta(db, data=entrada)