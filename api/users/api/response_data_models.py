from typing import Optional

from app.api.response_data_models import ResponseData


class ResponseAuthGoogleCallbackData(ResponseData):
    message: Optional[str] = "Google authentication successful"
    access_token: Optional[str] = None


class ResponseLoginData(ResponseData):
    message: Optional[str] = "Login successful"
    access_token: Optional[str] = None


class ResponseRegisterData(ResponseData):
    message: Optional[str] = "Register successful"
    access_token: Optional[str] = None


class ResponseLogoutData(ResponseData):
    message: Optional[str] = "Logout successful"


class ResponseMeData(ResponseData):
    message: Optional[str] = "User information retrieved"
    user: Optional[dict] = None
