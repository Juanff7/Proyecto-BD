from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from src.api.debs import get_db
from src.crud import producto as Crud_Product
from src.schemas import producto as Schema_Prod
import shutil
import os

router = APIRouter()

# Carpeta donde se guardan las imágenes
upload_dir = "src/uploads/"
os.makedirs(upload_dir, exist_ok=True)




#Autocompletado de lista(categorias)
from src.utils.search import buscar_por_nombre_lista
from src.model.productos import Producto
@router.get("/autocompletado")
def autocomplete_producto(query: str, db: Session = Depends(get_db)):
    if not query.strip():
        return []
        
    productos = buscar_por_nombre_lista(
        db, Producto, Producto.nombre, query, limite=5
    )
    
    return [
        {"id_producto": p.id_producto, "nombre": p.nombre}
        for p in productos
    ]


# Subir imagen
@router.post("/upload")
def upload_image(file: UploadFile = File(...)):
    ext = os.path.splitext(file.filename)[1]
    if ext.lower() not in [".jpg", ".jpeg", ".png", ".gif"]:
        raise HTTPException(status_code=400, detail="Extensión de archivo inválida")

    file_path = os.path.join(upload_dir, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"url": f"http://localhost:8000/uploads/{file.filename}"}


#Crear un producto
@router.post("/create", response_model = Schema_Prod.ProductoOut)
def crear_producto(data: Schema_Prod.ProductoCreate, db: Session = Depends(get_db)):
    return Crud_Product.create_producto(db, data)



@router.put("/update/id/{producto_id}", response_model=Schema_Prod.ProductoOut)
def update_product_by_id(producto_id: int, data: Schema_Prod.ProductoCreate, db: Session = Depends(get_db)):
    return Crud_Product.update_producto_por_id(db, producto_id, data)

@router.delete("/delete/{id}")
def eliminar_producto(id: int, db: Session = Depends(get_db)):
    return Crud_Product.delete_producto(db, producto_id=id)



#Obtener todos los productos
@router.get("/", response_model=List[Schema_Prod.ProductoOut])
def get_all(db: Session = Depends(get_db)):
    productos = Crud_Product.get_allproductos(db)
    if not productos:
        raise HTTPException(status_code=404, detail="No hay productos registrados")
    return productos




# Buscar producto por ID
@router.get("/{id}", response_model=Schema_Prod.ProductoOut)
def get_by_id(id: int, db: Session = Depends(get_db)):
    producto = Crud_Product.get_id(db, producto_id= id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto

