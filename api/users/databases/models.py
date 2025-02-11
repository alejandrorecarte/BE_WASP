from typing import Optional

import bcrypt
from bson import ObjectId
from pydantic import BaseModel, EmailStr, Field, field_validator, model_validator


# Clase base User
class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id", exclude=False)
    email: EmailStr
    name: str
    last_name: str

    class Config:
        populate_by_name = True
        extra = "ignore"
        from_attributes = True


# Clase derivada para un usuario interno
class InternalUser(User):
    type: str = "internal"  # Asegura que este usuario es interno
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
            values["hashed_password"] = bcrypt.hashpw(
                password.encode("utf-8"), bcrypt.gensalt()
            ).decode("utf-8")
        return values


# Clase derivada para un usuario de Google
class GoogleUser(User):
    type: str = "google"  # Asegura que este usuario es de Google

    class Config:
        populate_by_name = True
        extra = "ignore"
        from_attributes = True
