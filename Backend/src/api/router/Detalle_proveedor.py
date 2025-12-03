from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.api.debs import get_db
from src.crud import detallePro as Crud_det
from src.schemas import detalle_proveedor as Schema_Det
from datetime import date
from src.utils.pdf_generator import generar_pdf_general
from fastapi.responses import FileResponse

router = APIRouter()

#Crear un Entrada de productos
@router.post("/Create", response_model=Schema_Det.detalleOut)
def Create_Detealle(Entrada: Schema_Det.detalleCreate, db: Session = Depends(get_db)):
    return Crud_det.created_detalle_proveedor(db=db, data=Entrada)

# Obtener todo
@router.get("/obtener", response_model=List[Schema_Det.detalleOut])
def get_dpro(db: Session = Depends(get_db)):
    return Crud_det.get_historial(db)


# Buscar por fecha
@router.get("/buscar_fecha/{fecha}", response_model=List[Schema_Det.detalleOut])
def buscar_fecha(fecha: date, db: Session = Depends(get_db)):
    return Crud_det.get_fecha(fecha, db)


# Rango de fechas
@router.get("/rango", response_model=List[Schema_Det.detalleOut])
def rango_fechas(inicio: date, fin: date, db: Session = Depends(get_db)):
    return Crud_det.get_rango_fechas(db, inicio, fin)





from src.schemas.detalle_proveedor import ReporteEntradaRequest
# Reporte PDF por proveedor
@router.post("/reporte/general")
def generar_reporte_general(data: ReporteEntradaRequest):
    path = "src/reports/reporte_general.pdf"
    generar_pdf_general(path, data.filtros, data.entradas)
    return FileResponse(path, media_type="application/pdf", filename="reporte_entradas.pdf")





# Eliminar
@router.delete("/eliminar/{id_dp}")
def eliminar_entrada(id_dp: int, db: Session = Depends(get_db)):
    return Crud_det.delete_detalle_proveedor(db, id_dp=id_dp)