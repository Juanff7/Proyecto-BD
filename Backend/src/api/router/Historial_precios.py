from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from src.api.debs import get_db
from src.crud import historial_precios as crud
from src.schemas import historial_precios as SchemaHist

router = APIRouter()


@router.post("/create", response_model=SchemaHist.HistorialOut)
def crear(entrada: SchemaHist.CreateHistorial, db: Session = Depends(get_db)):
    return crud.created_historial_precios(db, entrada)


@router.get("/", response_model=List[SchemaHist.HistorialOut])
def obtener_todos(db: Session = Depends(get_db)):
    return crud.get_all_historial(db)


@router.get("/id/{historial_id}", response_model=SchemaHist.HistorialOut)
def obtener_por_id(historial_id: int, db: Session = Depends(get_db)):
    hist = crud.get_by_id(db, historial_id)
    if not hist:
        raise HTTPException(404, "Historial no encontrado")
    return hist


@router.get("/producto/{producto_id}", response_model=List[SchemaHist.HistorialOut])
def obtener_por_producto(producto_id: int, db: Session = Depends(get_db)):
    return crud.get_by_producto(db, producto_id)


@router.get("/fecha/{fecha}", response_model=List[SchemaHist.HistorialOut])
def obtener_por_fecha(fecha: str, db: Session = Depends(get_db)):
    fecha_dt = datetime.fromisoformat(fecha)
    return crud.get_by_fecha(db, fecha_dt)


@router.get("/rango/", response_model=List[SchemaHist.HistorialOut])
def obtener_rango(desde: str, hasta: str, db: Session = Depends(get_db)):
    desde_dt = datetime.fromisoformat(desde)
    hasta_dt = datetime.fromisoformat(hasta)
    return crud.get_rango_fechas(db, desde_dt, hasta_dt)
