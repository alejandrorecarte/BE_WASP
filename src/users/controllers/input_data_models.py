from pydantic import BaseModel


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


class InputGetMeData(BaseModel):
    user_id: str

    class Config:
        extra = "allow"


class InputGoogleLoginData(BaseModel):
    code: str

    class Config:
        extra = "allow"
