from sqlalchemy.orm import Session
from fastapi import HTTPException
from src.model.productos import Producto
from src.model.categoria import Categoria
from src.schemas.producto import ProductoCreate
from src.utils.search import buscar_por_nombre_uno, buscar_por_nombre_lista
from sqlalchemy import func 

#Crear un producto nuevo
def create_producto(db: Session, data: ProductoCreate):
    existente = buscar_por_nombre_uno(db, Producto, Producto.nombre, data.nombre)
    if existente:
         raise HTTPException(400, "Ya existe un producto con ese nombre")
    
    Categoria_id = None 
    if data.categoria:
      categoria = buscar_por_nombre_uno(db, Categoria, Categoria.tipo, data.categoria)
      if not categoria: 
          raise HTTPException(404, "categoria no encontrada")
      Categoria_id =  categoria.id_categoria
      
    nuevo =  Producto(
        nombre = data.nombre.strip().title(),
        descripcion = data.descripcion,
        id_categoria = Categoria_id,
        costo_venta = data.costo_venta,
        cantidad = 0,
        imagen_url = data.imagen_url
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo 


def update_producto_por_id(db: Session, producto_id: int, data: ProductoCreate):
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(404, "Producto no encontrado")

    # Categoría
    categoria_id = None
    if data.categoria:
        categoria = buscar_por_nombre_uno(db, Categoria, Categoria.tipo, data.categoria)
        if not categoria:
            raise HTTPException(404, f"Categoría '{data.categoria}' no existe")
        categoria_id = categoria.id_categoria

    # Validar precio
    if data.costo_venta <= 0:
        raise HTTPException(400, "El costo de venta debe ser mayor a 0")
    
    producto.nombre = data.nombre
    producto.descripcion = data.descripcion
    producto.id_categoria = categoria_id
    producto.costo_venta = data.costo_venta

    if data.imagen_url:
        producto.imagen_url = data.imagen_url

    db.commit()
    db.refresh(producto)
    return producto



def delete_producto(db: Session, producto_id: int):
    producto = db.query(Producto).filter(Producto.id_producto == producto_id).first()
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    db.delete(producto)
    db.commit()

    return {"detail": "Producto eliminado"}

#Obtener Todos
def get_allproductos(db: Session):
    return db.query(Producto).all()



#Obtener por id un producto
def get_id(db: Session, producto_id: int):
    return db.query(Producto).filter(Producto.id_producto == producto_id).first()

#Busqueda por nombre parcial de una categoria y de un producto
def buscar_productos(db: Session, search: str, categoria:str = None, limit: int = 10):
   query = db.query(Producto)

   #FILTRADO DE NOMBRE SEPARADO POR PALABRAS
   if search:
       palabras = search.lower().split()
       for palabra in palabras:
           query = query.filter(func.lower(Producto.nombre).ilike(f"%{palabra}%"))

   #Filtrado por categoria
   if categoria:
       cat = buscar_por_nombre_uno(db, Categoria, Categoria.tipo, categoria)
       if cat: 
           query = query.filter(Producto.id_categoria == cat.id_categoria)

   return query.limit(limit).all()