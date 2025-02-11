from typing import Optional

from pydantic import BaseModel


class OutputAuthGoogleCallbackData(BaseModel):
    access_token: Optional[str] = None

    class Config:
        extra = "allow"


class OutputRegisterData(BaseModel):
    access_token: Optional[str] = None

    class Config:
        extra = "allow"


class OutputLoginData(BaseModel):
    access_token: Optional[str] = None

    class Config:
        extra = "allow"
