from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List 

from src.api.debs import get_db
from src.crud import cliente as Cliente_crud
from src.schemas import Cliente as Cliente_schema

router = APIRouter()

#Crear un cliente 
@router.post("/Create", response_model= Cliente_schema.ClienteBase)
def Create_Cliente(Cliente: Cliente_schema.ClienteBase, db: Session = Depends(get_db)):
    return Cliente_crud.Created_Cliente(db = db, data=Cliente)

#Actualizar un cliente
@router.put("/update", response_model=Cliente_schema.ClienteBase)
def Update_cliente(id : int, data: Cliente_schema.ClienteBase, db: Session = Depends(get_db)):
      cliente = Cliente_crud.get_id(db, id = id)
      if cliente is None: 
        raise HTTPException(status_code=404, detail="cliente no encontrado")
      return Cliente_crud.Update_Cliente(db = db, id= id, data = data)

    

#Obtener clientes
@router.get("/Obtener", response_model=List[Cliente_schema.ClienteOut])
def get_clientes(db: Session = Depends(get_db)):
    return Cliente_crud.get_allCLiente(db)

@router.get("/Obtener/name", response_model=Cliente_schema.ClienteOut)
def get_name(name: str, db : Session = Depends(get_db)):
   cliente = Cliente_crud.get_name(db, name = name)
   if cliente is None: 
       raise HTTPException(status_code=404, detail="cliente no encontrado")
   return cliente


@router.get("/Obtener/id", response_model=Cliente_schema.ClienteOut)
def get_name(id: int, db : Session = Depends(get_db)):
   cliente = Cliente_crud.get_id(db, id = id)
   if cliente is None: 
       raise HTTPException(status_code=404, detail="cliente no encontrado")
   return cliente
