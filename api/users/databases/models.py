from typing import Optional
from pydantic import BaseModel, root_validator, EmailStr, Field, validator
from bson import ObjectId
from app.utils import hash


class User(BaseModel):
    id: Optional[str] = Field(None, alias="_id", exclude=False)
    email: EmailStr
    name: str
    last_name: str
    password: Optional[str] = Field(None, exclude=True)  # Exclude when saving to DB
    hashed_password: Optional[str] = None

    # Convert ObjectId to string
    @validator("id", pre=True, always=True)
    def convert_objectid_to_str(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        return v

    # Hash the password before saving
    @root_validator(pre=True)
    def hash_password(cls, values):
        password = values.get('password')
        if password and not values.get('hashed_password'):
            values["hashed_password"] = hash(password)
        return values

    class Config:
        populate_by_name = True
        extra = "ignore"
        orm_mode = True
