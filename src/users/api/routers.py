import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer

from dependencies.users.controllers import get_google_login_handler, get_login_handler
from security.authentication import create_token, get_token_from_cookie, invalidate_token
from users.api.request_data_models import (
    RequestGoogleLoginData,
    RequestLoginData,
    RequestRegisterData,
)
from users.api.response_data_models import (
    ResponseGoogleLoginData,
    ResponseLoginData,
    ResponseLogoutData,
    ResponseMeData,
    ResponseRegisterData,
)
from users.controllers.constants import GOOGLE_AUTH_URL, GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI
from users.controllers.handler_interface import GoogleLoginHandlerInterface, LoginHandlerInterface
from users.controllers.input_data_models import (
    InputGoogleLoginData,
    InputLoginData,
    InputRegisterData,
)

logger = logging.getLogger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",  # URL de autorización de Google
    tokenUrl="https://oauth2.googleapis.com/token",  # URL para obtener el token de Google
)


@router.get("/google/redirect", status_code=status.HTTP_200_OK)
async def google_redirect():
    try:
        return RedirectResponse(
            url=(
                f"{GOOGLE_AUTH_URL}?response_type=code&client_id={GOOGLE_CLIENT_ID}"
                f"&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email"
                f"&access_type=offline"
            )
        )
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post(
    "/google/login",
    status_code=status.HTTP_200_OK,
    response_model=ResponseGoogleLoginData,
)
async def google_login(
    request_data: RequestGoogleLoginData,
    response: Response,
    handler: GoogleLoginHandlerInterface = Depends(get_google_login_handler),
):
    try:
        await handler.google_login(input_google_login=InputGoogleLoginData(code=request_data.code))
        return ResponseGoogleLoginData()
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post(
    "/register",
    status_code=status.HTTP_201_CREATED,
    response_model=ResponseRegisterData,
)
def post_register(
    request_data: RequestRegisterData,
    response: Response,
    handler: LoginHandlerInterface = Depends(get_login_handler),
):
    try:
        output_register = handler.register(
            input_register=InputRegisterData.model_validate(request_data.model_dump())
        )
        response = create_token(response=response, user_id=output_register.user_id)
        return ResponseRegisterData()
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseLoginData)
def post_login(
    request_data: RequestLoginData,
    response: Response,
    handler: LoginHandlerInterface = Depends(get_login_handler),
):
    try:
        output_login = handler.login(
            input_login=InputLoginData.model_validate(request_data.model_dump())
        )
        response = create_token(response=response, user_id=output_login.user_id)
        return ResponseLoginData()

    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/logout", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseLogoutData)
def post_logout(response: Response):
    try:
        response = invalidate_token(response=response)
        return ResponseLogoutData()

    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/me", status_code=status.HTTP_200_OK, response_model=ResponseMeData)
def get_me(
    response: Response,
    handler: LoginHandlerInterface = Depends(get_login_handler),
    access_token: str = Depends(get_token_from_cookie),
):
    try:
        user = handler.get_me()
        return ResponseMeData(user=user)
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
