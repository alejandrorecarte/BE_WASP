from pydantic import BaseModel


class InputAuthGoogleCallbackData(BaseModel):
    code: str

    class Config:
        extra = "allow"


class InputRegisterData(BaseModel):
    email: str
    name: str
    last_name: str
    password: str

    class Config:
        extra = "allow"


class InputLoginData(BaseModel):
    email: str
    password: str

    class Config:
        extra = "allow"
