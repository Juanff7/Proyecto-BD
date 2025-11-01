from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List 
from src.api.debs import get_db
from src.crud import producto as Crud_Product
from src.schemas import producto as Schema_Prod

router = APIRouter()


#Actualizar producto
@router.put("/update/name", response_model=Schema_Prod.ProductoBase)
def Update_product(Product_name: str, data: Schema_Prod.ProductoCreate, db : Session = Depends(get_db)):
    product = Crud_Product.get_name(db, Product_Name= Product_name)
    if product is None:
        raise HTTPException(status_code=404, detail="Error")
    return Crud_Product.Update_Producto(db=db, producto_name= Product_name, data=data)


@router.get("/", response_model= List[Schema_Prod.ProductoOut])
def get(db: Session = Depends(get_db)):
    return Crud_Product.get_allproductos(db)



@router.get("/buscar/name", response_model=Schema_Prod.ProductoOut)
def get(product: str, db: Session = Depends(get_db)):
    producto = Crud_Product.get_name(db, Product_Name=product)
    if producto is None:
        raise HTTPException(status_code=404, detail="Producto no encontrado")  
    return producto




@router.get("/{product_id}", response_model= Schema_Prod.ProductoOut)
def get(product_id : int ,db: Session = Depends(get_db)):
    producto = Crud_Product.get_id(db, producto_id=product_id)
    if producto is None:
        raise HTTPException(status_code=404, detail="post not found")
    return producto


