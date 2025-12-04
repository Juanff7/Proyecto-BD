from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from src.api.debs import get_db
from src.crud import detallePro as Crud_det
from src.schemas import detalle_proveedor as Schema_Det
from datetime import date
from src.utils.pdf_generator import generar_pdf_entradas
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


from src.model.detalle_Proveedor import Detalle_proveedor
from src.model.Proveedor import Proveedor
from sqlalchemy.orm import joinedload
from src.schemas.detalle_proveedor import ReporteEntradaRequest


@router.post("/reporte/general")
def generar_reporte_general(data: ReporteEntradaRequest, db: Session = Depends(get_db)):

    query = (
        db.query(Detalle_proveedor)
        .options(
            joinedload(Detalle_proveedor.proveedor),
            joinedload(Detalle_proveedor.producto),
            joinedload(Detalle_proveedor.empleado)
        )
    )

    # FILTROS POR FECHAS
    if data.fecha_inicio:
        query = query.filter(Detalle_proveedor.fecha_ingreso >= data.fecha_inicio)

    if data.fecha_fin:
        query = query.filter(Detalle_proveedor.fecha_ingreso <= data.fecha_fin)

    # FILTRO POR PROVEEDOR
    if data.proveedor:
        query = query.join(Proveedor).filter(Proveedor.nombre.ilike(f"%{data.proveedor}%"))

    detalles = query.all()

    # Convertir datos
    data_list = [
        {
            "id_entrada": d.id_dp,
            "proveedor": d.proveedor.nombre if d.proveedor else "Proveedor eliminado",
            "fecha": d.fecha_ingreso.strftime("%Y-%m-%d"),
            "producto": d.producto.nombre if d.producto else "Producto eliminado",
            "cantidad": d.cantidad,
            "costo_unit": d.precio_unit,
            "sub_total": d.precio_unit * d.cantidad,
        }
        for d in detalles
    ]

    ruta_pdf = generar_pdf_entradas(data_list)

    return FileResponse(
        ruta_pdf,
        media_type="application/pdf",
        filename="reporte_entradas.pdf"
    )


# Eliminar
@router.delete("/eliminar/{id_dp}")
def eliminar_entrada(id_dp: int, db: Session = Depends(get_db)):
    return Crud_det.delete_detalle_proveedor(db, id_dp=id_dp)