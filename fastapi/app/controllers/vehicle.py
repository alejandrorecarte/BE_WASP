from models.vehicle import Vehicle, VehicleType, FuelType
from controllers.queries import create_vehicle_query, check_vehicle_access_query, update_vehicle_query, delete_vehicle_query, get_vehicle_query, get_post_vehicles_query
from database import execute, execute_query
from controllers.post import check_post_access
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)

def check_vehicle_access(user_email: str, license_plate: str, db_connection):
    query = check_vehicle_access_query()
    params = (license_plate)
    
    results = execute_query(query, params, db_connection)
    
    if results:
        if user_email == results[0][0]:
            return
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access not granted for that document"
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Document not found"
    )

def vehicle_formatter(vehicle_nf):

    logger.debug(vehicle_nf)
    
    vehicle = Vehicle(
        license_plate=vehicle_nf[0],
        brand = vehicle_nf[1],
        model = vehicle_nf[2],
        registration_year=vehicle_nf[3],
        price = vehicle_nf[4],
        observations=vehicle_nf[5],
        vehicle_type=VehicleType(vehicle_nf[6]),
        fuel_type=FuelType(vehicle_nf[7]),
        photo=vehicle_nf[8],
        post_id=vehicle_nf[9]
    )
    return vehicle

def create_vehicle(vehicle: Vehicle, user_email, db_connection):
    check_post_access(user_email, vehicle.post_id, db_connection)

    query = create_vehicle_query()
    params = (vehicle.license_plate, vehicle.brand, vehicle.model, vehicle.registration_year, vehicle.price, vehicle.observations, vehicle.vehicle_type, vehicle.fuel_type, vehicle.photo, vehicle.post_id)
    
    execute(query, params, db_connection)
    
    return vehicle

def update_vehicle(vehicle: Vehicle, user_email: str, db_connection):
    check_vehicle_access(user_email, vehicle.license_plate, db_connection)
    
    query = update_vehicle_query()
    params = (vehicle.brand, vehicle.model, vehicle.registration_year, vehicle.price, vehicle.observations, vehicle.vehicle_type, vehicle.fuel_type, vehicle.photo, vehicle.license_plate)
    
    execute(query, params, db_connection)
    
    return vehicle

def delete_vehicle(license_plate: str, user_email: str, db_connection):
    check_vehicle_access(user_email, license_plate, db_connection)
    
    query = delete_vehicle_query()
    
    execute(query, license_plate, db_connection)
    
def get_vehicle(license_plate: str, db_connection):
    
    query = get_vehicle_query()
    
    result = execute_query(query, license_plate, db_connection)
    
    return vehicle_formatter(result[0])
    
def get_post_vehicles(post_id: int, db_connection):

    query = get_post_vehicles_query()
    
    result = execute_query(query, post_id, db_connection)
    
    vehicles = []
    for vehicle_nf in result:
        vehicles.append(vehicle_formatter(vehicle_nf))
        
    return vehicles