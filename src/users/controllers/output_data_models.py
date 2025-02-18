from pydantic import BaseModel

from users.databases.models import User


class OutputGoogleLoginData(BaseModel):
    user: User

    class Config:
        extra = "allow"


class OutputRegisterData(BaseModel):
    user: User

    class Config:
        extra = "allow"


class OutputLoginData(BaseModel):
    user: User

    class Config:
        extra = "allow"
