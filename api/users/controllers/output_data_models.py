from typing import Optional

from pydantic import BaseModel


class OutputLoginData(BaseModel):
    access_token: Optional[str] = None

    class Config:
        extra = "allow"

