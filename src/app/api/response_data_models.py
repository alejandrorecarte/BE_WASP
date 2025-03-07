from typing import Optional

from pydantic import BaseModel


class ResponseData(BaseModel):
    message: Optional[str] = None
    success: Optional[bool] = True

    class Config:
        extra = "allow"
