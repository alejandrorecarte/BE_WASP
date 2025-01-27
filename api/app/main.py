import os
from fastapi import FastAPI, Depends, Request
from starlette.middleware.cors import CORSMiddleware
from api.user import router as user_router
from database import close_connection
import logging
from database import get_db_connection
from utils import get_token_from_cookie

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

app = FastAPI()

# Incluir los routers para los diferentes endpoints
app.include_router(user_router, prefix="/users", tags=["Users"])

# Agregar middleware para CORS (Compartir recursos entre orígenes)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],  # Permitir solicitudes desde el frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Configuración del logger para registrar mensajes
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(name)s - %(asctime)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('app.log')  # Guardar los logs en el archivo app.log
    ]
)

# Crear un logger para esta aplicación
logger = logging.getLogger(__name__)

# Evento de inicio de la aplicación
@app.on_event("startup")
async def startup_event():
    """Evento que se ejecuta al iniciar la aplicación"""
    logger.info("Application started")

# Evento de cierre de la aplicación
@app.on_event("shutdown")
async def shutdown_event():
    """Cerrar la conexión a la base de datos al apagar la aplicación"""
    db_connection = await get_db_connection()

    if db_connection:
        close_connection(db_connection)

# Endpoint protegido que obtiene el token desde las cookies
@app.get("/secure-endpoint")
def secure_endpoint(request: Request, token: str = Depends(get_token_from_cookie)):
    """
    Endpoint protegido que requiere el token desde las cookies.
    """
    return {"message": "Access granted", "token": token}
