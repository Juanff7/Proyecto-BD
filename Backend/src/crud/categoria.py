from sqlalchemy.orm import Session
from src.model.categoria import Categoria
from src.schemas.categoria import CategoriaCreate



#Crear categoria 
def Created_category(db:Session, categoria: CategoriaCreate):
    Data = Categoria(
           tipo = categoria.tipo
    )
    db.add(Data)
    db.commit()
    db.refresh(Data)
    return Data

