import logging
import os

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from users.api.routers import router as users_router

# Leer las variables de entorno sin asignarles valores en el código
CONNECTION_TRIES = os.getenv("CONNECTION_TRIES")  # Lee el número de intentos de conexión
EXPIRATION_MINUTES = os.getenv("EXPIRATION_MINUTES")  # Lee el tiempo de expiración
SECRET_KEY = os.getenv("SECRET_KEY")  # Lee la clave secreta para el JWT
PAGE_SIZE = os.getenv("PAGE_SIZE")  # Lee el tamaño de página para la paginación
MAX_IMAGE_SIZE = os.getenv("MAX_IMAGE_SIZE")  # Lee el tamaño máximo de la imagen

# Leer las variables de conexión a la base de datos desde las variables de entorno
DB_HOST = os.getenv("DB_HOST")  # Nombre del contenedor de la base de datos
DB_PORT = os.getenv("DB_PORT")  # Puerto de la base de datos
DB_USER = os.getenv("DB_USER")  # Usuario de la base de datos
DB_PASSWORD = os.getenv("DB_PASSWORD")  # Contraseña de la base de datos
DB_NAME = os.getenv("DB_NAME")  # Nombre de la base de datos

app = FastAPI(
    docs_url="/api/docs",  # Custom Swagger UI URL
    redoc_url="/api/redoc",  # Custom ReDoc URL
    openapi_url="/api/openapi.json",  # OpenAPI schema path
)

# Incluir los routers para los diferentes endpoints
app.include_router(users_router, prefix="/users", tags=["Users"])

# Agregar middleware para CORS (Compartir recursos entre orígenes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todos los orígenes (solo para desarrollo)
    allow_credentials=True,
    allow_methods=["*"],  # Permite todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permite todos los headers
)

# Configuración del logger para registrar mensajes
logging.basicConfig(
    level=logging.DEBUG,
    format="%(levelname)s - %(name)s - %(asctime)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        # logging.FileHandler('app/app.log')  # Guardar los logs en el archivo app.log
    ],
)
