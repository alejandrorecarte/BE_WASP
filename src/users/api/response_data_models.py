from typing import Optional

from app.api.response_data_models import ResponseData


class ResponseGoogleLoginData(ResponseData):
    message: Optional[str] = "Google authentication successful"


class ResponseLoginData(ResponseData):
    message: Optional[str] = "Login successful"


class ResponseRegisterData(ResponseData):
    message: Optional[str] = "Register successful"


class ResponseLogoutData(ResponseData):
    message: Optional[str] = "Logout successful"


class ResponseMeData(ResponseData):
    message: Optional[str] = "User information retrieved"
    user: Optional[dict] = None
