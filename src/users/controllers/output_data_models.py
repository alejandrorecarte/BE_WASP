from pydantic import BaseModel


class OutputGoogleLoginData(BaseModel):
    user_id: str

    class Config:
        extra = "allow"


class OutputRegisterData(BaseModel):
    user_id: str

    class Config:
        extra = "allow"


class OutputLoginData(BaseModel):
    user_id: str

    class Config:
        extra = "allow"
