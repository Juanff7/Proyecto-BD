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



