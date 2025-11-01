
from pydantic_settings import BaseSettings

#Se mandan a llamar las url que se utilizan y etiquetas del proyecto(siempre ver bien que hay en .env)
class Settings(BaseSettings):
    PROJECT_NAME: str = "InventarioSportcity"
    PROJECT_VERSION: str = "1.0.0"
    DATABASE_URL: str
    FRONTEND_URL: str

    class Config:
        env_file = ".env"


settings = Settings()