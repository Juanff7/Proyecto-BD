from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from src.api.debs import get_db
from src.schemas.reporte_venta import ReporteVentaRequest
from fastapi.responses import FileResponse
from src.crud import venta as crud_venta
from src.schemas.venta import VentaCreate, VentaOut
from src.utils.pdf_generator_venta import generar_pdf_ventas
from datetime import date

router = APIRouter()


@router.post("/create", response_model=VentaOut)
def create_venta(entrada: VentaCreate, db: Session = Depends(get_db)):
    return crud_venta.Create_venta(db=db, data=entrada)

# ================================
#   OBTENER TODAS LAS VENTAS
# ================================
@router.get("/obtener", response_model=List[VentaOut])
def get_ventas(db: Session = Depends(get_db)):
    return crud_venta.get_allventas(db)


# ================================
#   VENTAS POR FECHA ÚNICA
# ================================
@router.get("/buscar_fecha/{fecha}", response_model=List[VentaOut])
def buscar_fecha(fecha: str, db: Session = Depends(get_db)):
    return crud_venta.buscar_por_fecha(db, fecha)



# ================================
#   VENTAS POR RANGO DE FECHAS
#   /rango?inicio=2024-01-01&fin=2024-01-31
# ================================
@router.get("/rango", response_model=List[VentaOut])
def ventas_por_rango(inicio: date, fin: date, db: Session = Depends(get_db)):
    return crud_venta.get_por_rango(db, inicio, fin)


# ================================
#   FACTURA COMPLETA
# ================================
@router.get("/factura/{id_venta}")
def obtener_factura(id_venta: int, db: Session = Depends(get_db)):
    return crud_venta.obtener_factura(db, id_venta)


# ================================
#   REPORTE PDF GENERALIZADO
# ================================
@router.post("/reporte/general")
def generar_reporte_general(data: ReporteVentaRequest):
    path = "src/reports/reporte_ventas.pdf"
    generar_pdf_ventas(path, data.filtros, data.ventas)
    return FileResponse(path, media_type="application/pdf", filename="reporte_ventas.pdf")


from sqlalchemy.orm import joinedload
from src.model.venta import Venta
from fastapi import HTTPException
from src.model.detalle_venta import Detalle_venta




@router.get("/obtener/mes", response_model=List[VentaOut])
def obtener_ventas_mes(db: Session = Depends(get_db)):
    return crud_venta.obtener_ventas_mes(db)
