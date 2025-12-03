from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.api.debs import get_db

from src.crud import detalle_venta as crud_Dventa
from src.schemas import detalle_venta as Schema_Dventa


router = APIRouter()

#Crear un detalle
@router.post("/Create", response_model= Schema_Dventa.detalle_VentaOut)
def create_detalle_venta(entrada: Schema_Dventa.Detalle_ventaCreate, db: Session = Depends(get_db)):
    return crud_Dventa.create_detalle_venta(db, data=entrada)


#Obtener todos los detalles de venta
@router.get("/obtener_todos", response_model= list[Schema_Dventa.detalle_ventaSimple])
def obtener_todos_detallesVentas(db: Session = Depends(get_db)):
    return crud_Dventa.get_all_detalleVenta(db)

@router.get("/obtener/{id_detalle_venta}", response_model= Schema_Dventa.detalle_ventaSimple)
def obtener_for_id_detalleventa(id_detalle_venta: int, db: Session = Depends(get_db)):
    return crud_Dventa.get_detalleVenta(db, id_detalle_venta = id_detalle_venta)


@router.delete("/eliminar/{id_detalle_venta}")
def eliminar_detalle_venta(id_detalle_venta: int, db: Session = Depends(get_db)):
    return crud_Dventa.delete_detalleVenta(db, id_detalle_venta)


