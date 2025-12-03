from fastapi import APIRouter, Depends , HTTPException
from sqlalchemy.orm import Session
from typing import List 

from src.api.debs import get_db
from src.crud import cliente as Cliente_crud
from src.schemas import Cliente as Cliente_schema

router = APIRouter()

# Crear cliente
@router.post("/Create", response_model=Cliente_schema.ClienteOut)
def Create_Cliente(Cliente: Cliente_schema.ClienteBase, db: Session = Depends(get_db)):
    return Cliente_crud.Created_Cliente(db=db, data=Cliente)

# Actualizar cliente
@router.put("/update/{id_cliente}", response_model=Cliente_schema.ClienteOut)
def Update_cliente(id_cliente: int, data: Cliente_schema.ClienteUpdate, db: Session = Depends(get_db)):
    cliente = Cliente_crud.get_id(db, id=id_cliente)
    if cliente is None:
        raise HTTPException(status_code=404, detail="cliente no encontrado")
    return Cliente_crud.Update_Cliente(db=db, id=id_cliente, data=data)

# Eliminar cliente
@router.delete("/delete/{id_cliente}")
def delete_cliente(id_cliente: int, db: Session = Depends(get_db)):
    return Cliente_crud.delete_cliente(db=db, id=id_cliente)

# Obtener todos
@router.get("/Obtener", response_model=List[Cliente_schema.ClienteOut])
def get_clientes(db: Session = Depends(get_db)):
    return Cliente_crud.get_allCLiente(db)

# Obtener por nombre
@router.get("/Obtener/name", response_model=Cliente_schema.ClienteOut)
def get_name(name: str, db: Session = Depends(get_db)):
    cliente = Cliente_crud.get_name(db, name=name)
    if cliente is None:
        raise HTTPException(status_code=404, detail="cliente no encontrado")
    return cliente

# Obtener por ID
@router.get("/Obtener/{id_cliente}", response_model=Cliente_schema.ClienteOut)
def get_cliente_id(id_cliente: int, db: Session = Depends(get_db)):
    cliente = Cliente_crud.get_id(db, id=id_cliente)
    if cliente is None:
        raise HTTPException(status_code=404, detail="cliente no encontrado")
    return cliente

from src.utils.search import buscar_por_nombre_lista
from src.model.cliente import Cliente
@router.get("/autocompletado")
def autocomplete_Cliente(query: str, db: Session = Depends(get_db)):
    cliente = buscar_por_nombre_lista(db, Cliente, Cliente.nombre, query, limite=5)
    return [{"nombre": p.nombre} for p in cliente]
