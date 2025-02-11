from pydantic import BaseModel


class RequestAuthGoogleCallbackData(BaseModel):
    code: str


class RequestRegisterData(BaseModel):
    email: str
    name: str
    last_name: str
    password: str


class RequestLoginData(BaseModel):
    email: str
    password: str
