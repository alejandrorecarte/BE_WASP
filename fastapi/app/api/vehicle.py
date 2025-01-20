from fastapi import APIRouter, HTTPException, status, Depends, UploadFile, File, Form, Request
from pydantic import BaseModel
from models.vehicle import Vehicle, VehicleType, FuelType
from database import get_db_connection
import logging
from controllers.vehicle import create_vehicle, update_vehicle, delete_vehicle, get_vehicle, get_post_vehicles
from utils import get_token_from_cookie
from fastapi.responses import JSONResponse
import os
import base64

MAX_IMAGE_SIZE = int(os.getenv("MAX_IMAGE_SIZE", 5)) * 1024 * 1024

router = APIRouter()

def vehicle_getter(vehicle: Vehicle):
    vehicle_data = vehicle.model_dump()
    
    # Si el vehículo tiene una imagen, convertirla a base64
    if vehicle_data.get("photo"):
        # Decodificar la imagen de base64 (si la base de datos almacena la imagen como base64)
        photo_base64 = base64.b64encode(vehicle.photo).decode('utf-8')
        vehicle_data['photo'] = photo_base64  # Añadir la imagen codificada en base64 a la respuesta
    
    return vehicle_data


class CreateVehicleRequest(BaseModel):
    license_plate: str
    brand: str
    model: str
    registration_year: int
    price: float
    observations: str
    vehicle_type: VehicleType
    fuel_type: FuelType
    post_id: int
    photo: UploadFile = File(...)

router = APIRouter()

logger = logging.getLogger(__name__)

MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5 MB, por ejemplo

class CreateVehicleRequest(BaseModel):
    license_plate: str
    brand: str
    model: str
    registration_year: int
    price: float
    observations: str
    vehicle_type: VehicleType
    fuel_type: FuelType
    post_id: int


@router.post("/create", status_code=status.HTTP_201_CREATED)
def post_create_vehicle(
    license_plate: str = Form(...),
    brand: str = Form(...),
    model: str = Form(...),
    registration_year: int = Form(...),
    price: float = Form(...),
    observations: str = Form(...),
    vehicle_type: VehicleType = Form(...), 
    fuel_type: FuelType = Form(...),
    post_id: int = Form(...),
    photo: UploadFile = File(...),  # Este es el archivo que se sube
    token: str = Depends(get_token_from_cookie),
    db_connection=Depends(get_db_connection)
):
    user_email = token["user_email"]
    
    try:
        # Verificar el tamaño del archivo
        photo_size = len(photo.file.read())  # Leer el archivo para obtener su tamaño
        if photo_size > MAX_IMAGE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Image size exceeds the {MAX_IMAGE_SIZE} byte limit"
            )
        
        # Reposicionar el puntero del archivo después de leerlo
        photo.file.seek(0)

        # Leer el archivo en bytes
        photo_bytes = photo.file.read()
        photo_base64 = None
        if photo_bytes:
            photo_base64 = base64.b64encode(photo_bytes).decode("utf-8")
        
        # Crear el vehículo
        vehicle = Vehicle(
            license_plate=license_plate,
            brand=brand,
            model=model,
            registration_year=registration_year,
            price=price,
            observations=observations,
            vehicle_type=vehicle_type,
            fuel_type=fuel_type,
            post_id=post_id,
            photo=photo_base64
        )
        
        # Llamar a la función que maneja la creación del vehículo
        vehicle = create_vehicle(vehicle, user_email, db_connection)
        
        return {"vehicle": vehicle_getter(vehicle)}

    except HTTPException as error:
        logger.warning(str(error.detail))
        raise HTTPException(
            status_code=error.status_code,
            detail=error.detail
        )
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

class UpdateVehicleRequest(BaseModel):
    vehicle: Vehicle

@router.post("/update", status_code=status.HTTP_200_OK)
def post_update_vehicle(body: UpdateVehicleRequest , request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    user_email = token["user_email"]
    try:
        vehicle = update_vehicle(body.vehicle, user_email, db_connection)
        return {"vehicle": vehicle_getter(vehicle)}
    except HTTPException as error:
        logger.warning(str(error.detail))
        raise HTTPException(
                    status_code=error.status_code,
                    detail=error.detail 
                )
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(error)
                )

class DeleteVehicleRequest(BaseModel):
    license_plate: str

@router.post("/delete", status_code=status.HTTP_200_OK)
def post_delete_vehicle(body: DeleteVehicleRequest, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    user_email = token["user_email"]
    try:
        delete_vehicle(body.license_plate, user_email, db_connection)
        return {}
    except HTTPException as error:
        logger.warning(str(error.detail))
        raise HTTPException(
                    status_code=error.status_code,
                    detail=error.detail 
                )
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=str(error)
                )

@router.get("/get", status_code=status.HTTP_200_OK)
def get_vehicle_by_license_plate(license_plate: str, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    try:
        vehicle = get_vehicle(license_plate, db_connection)
        return JSONResponse(content={"vehicle": vehicle_getter(vehicle)})
    
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )

@router.get("/post", status_code=status.HTTP_200_OK)
def get_vehicle_by_post_id(post_id: int, request: Request, token: str = Depends(get_token_from_cookie), db_connection=Depends(get_db_connection)):
    try:
        # Obtener los vehículos relacionados con el post_id
        vehicles = get_post_vehicles(post_id, db_connection)

        # Convertir cada vehículo a un diccionario y manejar las imágenes
        vehicles_json = []
        for vehicle in vehicles:
            vehicles_json.append(vehicle_getter(vehicle))
        
        return {"vehicles": vehicles_json}

    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
    