from fastapi import FastAPI
from src.core.config import settings
#Peticiones al backend
from fastapi.middleware.cors import CORSMiddleware

from decouple import config


from src.api.router import Cargo
from src.api.router import Empleado
from src.api.router import Producto
from src.api.router import categoria
from src.api.router import proveedor
from src.api.router import telefono
from src.api.router import email
from src.api.router import Detalle_proveedor
from src.api.router import cliente
from src.api.router import Historial_precios
from src.api.router import venta
from src.api.router import detalle_venta


from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/Empleado/token")




app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)

origins = [settings.FRONTEND_URL]

# Que se le permite conectar con el backend?
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ['*'],
    allow_headers=['*']


)


app.openapi_schema = None  # Forzar regeneración de esquema con auth


from fastapi.openapi.utils import get_openapi

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version=settings.PROJECT_VERSION,
        description="Documentación de API con autenticación JWT",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


#-------------Ruta CARGO------------------
app.include_router(Cargo.router, prefix="/Cargo", tags=['etiqueta cargos'])
#-------------Ruta Empleado----------------
app.include_router(Empleado.router,prefix="/Empleado", tags=['etiqueta empleado'])
#-------------ruta Producto----------------
app.include_router(Producto.router, prefix="/Producto", tags=['etiqueta producto'])
#------------Ruta Categoria---------------
app.include_router(categoria.router, prefix="/categoria", tags=['etiqueta categoria'])
#-----------Ruta Proveedor--------------------
app.include_router(proveedor.router, prefix="/Proveedor", tags=['Etiqueta Proveedor'])
#----------Ruta telefonoProveedor-------------------
app.include_router(telefono.router, prefix="/TelefonoP", tags=['Etiqueta Telefono Proveedor'])
#----------Ruta EmailProveedor---------------------------
app.include_router(email.router,prefix="/EmailP", tags=['Etiqueta Email Proveedor'] )
#----------Entrada(Detalle proveedor)---------------------
app.include_router(Detalle_proveedor.router, prefix = "/Entrada",tags=['Etiqueta Detalle proveedor'])
#-----------------Cliente-------------------
app.include_router(cliente.router, prefix= "/Cliente", tags=['Etiquete cliente'])
#----------------historialPrecios--------------------
app.include_router(Historial_precios.router, prefix = "/historial", tags=['etiqueta de historial de precios'])
#---------------venta--------------------------
app.include_router(venta.router, prefix="/venta", tags=['etiqueta de ventas'] )
#--------------detalleventa-----------------------
app.include_router(detalle_venta.router, prefix="/DetalleVenta", tags=['Etiqueta detalle venta'])

