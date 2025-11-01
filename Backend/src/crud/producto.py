from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.model.productos import Producto
from src.model.categoria import Categoria
from src.schemas.producto import ProductoCreate


def Update_Producto(db: Session, producto_name: str, data: ProductoCreate):
    producto = db.query(Producto).filter(Producto.nombre == producto_name).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")


    categoria_id = None
    if data.categoria:
        categoria = db.query(Categoria).filter(Categoria.tipo == data.categoria).first()
        if not categoria:
            raise HTTPException(status_code=404, detail=f"Categoría '{data.categoria}' no existe")
        categoria_id = categoria.id

    producto.categoria_id = categoria_id
    producto.costo_venta = data.costo_venta
    producto.descripcion = data.descripcion
    producto.imagen_url = data.imagen_url

    db.commit()
    db.refresh(producto)
    db.refresh(producto.categoria)
    return producto


def get_allproductos(db: Session):
    return db.query(Producto).all()


def get_name(db: Session, Product_Name: str):
    return db.query(Producto).filter(Producto.nombre == Product_Name).first()


def get_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id == producto_id).first()
