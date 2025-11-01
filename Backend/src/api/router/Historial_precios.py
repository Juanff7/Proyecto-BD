from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List 

from src.api.debs import get_db
from src.crud import historial_precios as historial_crud
from src.schemas import historial_precios as Schema_historial


router = APIRouter()

#Crear un cambio de precios 
@router.post("/Create", response_model=Schema_historial.HistorialOut)
def created_historial(Entrada: Schema_historial.CreateHistorial, db: Session = Depends(get_db)):
    return historial_crud.created_historial_precios(db=db, data=Entrada)


#obtener historiales 

@router.get("/", response_model= List[Schema_historial.HistorialOut])
def get(db: Session = Depends(get_db)):
    return historial_crud.get_allHistorial(db)



@router.get("/{product_id}", response_model= Schema_historial.HistorialOut)
def get(historial: int ,db: Session = Depends(get_db)):
    historial = historial_crud.get_id(db, Historial=historial)
    if historial is None:
        raise HTTPException(status_code=404, detail="post not found")
    return historial
