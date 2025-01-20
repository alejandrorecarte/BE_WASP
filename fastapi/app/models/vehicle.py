from enum import Enum
from pydantic import BaseModel
from typing import Optional
import base64

class FuelType(Enum):
    GASOLINE = "GASOLINE"
    DIESEL = "DIESEL"
    ELECTRIC = "ELECTRIC"
    HYBRID = "HYBRID"

class VehicleType(Enum):
    CAR = "CAR"
    TRUCK = "TRUCK"
    MOTORCYCLE = "MOTORCYCLE"
    BUS = "BUS"
    FORK_LIFT = "FORK_LIFT"
    CRANE_TRUCK = "CRANE_TRUCK"
    CEMENT_TRUCK = "CEMENT_TRUCK"
    TBM = "TBM"

# Modelo de vehículo con Pydantic
class Vehicle(BaseModel):
    license_plate: str
    brand: str
    model: str
    registration_year: int
    price: float
    observations: str
    vehicle_type: VehicleType
    fuel_type: FuelType
    photo: Optional[bytes]
    post_id: int

    class Config:
        # Esto asegura que los valores del Enum sean convertidos a cadenas en las respuestas JSON
        use_enum_values = True
