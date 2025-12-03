from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from src.api.debs import get_db
from src.crud import categoria as crud_cate
from src.schemas import categoria as schema_cate


router = APIRouter()


#Crear Categoria
@router.post("/Create", response_model=schema_cate.CategoriaBase)
def CreateCategory(category: schema_cate.CategoriaCreate, db: Session = Depends(get_db)):
    return crud_cate.Created_category(db=db, categoria=category)


#autocompletado
from src.utils.search import buscar_por_nombre_lista
from src.model.categoria import Categoria
@router.get("/autocompletado")
def autocomplete_categori(query:str, db: Session = Depends(get_db)):
    categorias = buscar_por_nombre_lista(db, Categoria, Categoria.tipo, query, limite=5)
    return [{"id": c.id_categoria, "tipo": c.tipo} for c in categorias]



@router.get("/all")
def get_all_categories(db: Session = Depends(get_db)):
    categorias = db.query(Categoria).all()
    return [{"id": c.id_categoria, "tipo": c.tipo} for c in categorias]
