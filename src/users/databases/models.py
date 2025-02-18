from typing import Optional

from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator

from security.cryptography import hash


class UserType:
    INTERNAL = "internal"
    GOOGLE = "google"


# Clase base User
class User(BaseModel):
    type: str
    id: Optional[str] = Field(None, alias="_id", exclude=False)
    email: EmailStr
    name: str
    last_name: str
    password: Optional[str] = Field(None, exclude=True)
    hashed_password: Optional[str] = None

    # Convertir ObjectId a string para el campo `id`
    @field_validator("id", mode="before")
    def convert_objectid_to_str(cls, v):
        if v is not None and isinstance(v, ObjectId):
            return str(v)
        return v

    # Hashear la contraseña
    @model_validator(mode="before")
    def hash_password(cls, values):
        password = values.get("password")
        if password and not values.get("hashed_password"):
            values["hashed_password"] = hash(password)
        return values

    class Config:
        populate_by_name = True
        extra = "ignore"
        from_attributes = True
