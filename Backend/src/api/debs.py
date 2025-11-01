from typing import Generator
from src.db.session import SessionLocal

#Seguridad dependencias(get_current_user)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from src.core.security import SECRET_KEY, ALGORITHM
from src.model.empleado import Empleado
from jose import JWTError, jwt

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/Empleado/token",
    scheme_name="JWT"
)

def get_db() -> Generator:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se puede validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception  

    # 👇 Conversión a entero para evitar error de tipo
    user = db.query(Empleado).filter(Empleado.id_empleado == int(user_id)).first()

    if user is None:
        raise credentials_exception

    return user