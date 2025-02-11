import logging

from dependencies.users.controllers import get_user_handler
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer
from users.api.request_data_models import (
    RequestAuthGoogleCallbackData,
    RequestLoginData,
    RequestRegisterData,
)
from users.api.response_data_models import (
    ResponseAuthGoogleCallbackData,
    ResponseLoginData,
    ResponseLogoutData,
    ResponseRegisterData,
)
from users.controllers.constants import GOOGLE_AUTH_URL, GOOGLE_CLIENT_ID, GOOGLE_REDIRECT_URI
from users.controllers.handler_interface import UserHandlerInterface
from users.controllers.input_data_models import (
    InputAuthGoogleCallbackData,
    InputLoginData,
    InputRegisterData,
)

logger = logging.getLogger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl="https://accounts.google.com/o/oauth2/auth",  # URL de autorización de Google
    tokenUrl="https://oauth2.googleapis.com/token",  # URL para obtener el token de Google
)


# TODO: Implementar la ruta de autenticación con Google
@router.get("/auth/google")
async def login_google():
    return RedirectResponse(
        url=(
            f"{GOOGLE_AUTH_URL}?response_type=code&client_id={GOOGLE_CLIENT_ID}"
            f"&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email"
            f"&access_type=offline"
        )
    )


@router.post(
    "/auth/google/callback",
    status_code=status.HTTP_200_OK,
    response_model=ResponseAuthGoogleCallbackData,
)
async def auth_google_callback(
    request_data: RequestAuthGoogleCallbackData,
    response: Response,
    handler: UserHandlerInterface = Depends(get_user_handler),
):  # Aquí se recibe el `code`
    try:
        output_auth_google_callback = handler.auth_google_callback(
            input_auth_google_callback=InputAuthGoogleCallbackData(code=request_data.code)
        )
        response.set_cookie(
            key="access_token",
            value=output_auth_google_callback.access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
        )
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
    handler: UserHandlerInterface = Depends(get_user_handler),
):
    try:
        handler.register(input_register=InputRegisterData.model_validate(request_data.model_dump()))
        output_login = handler.login(
            input_login=InputLoginData.model_validate(request_data.model_dump())
        )
        response.set_cookie(
            key="access_token",
            value=output_login.access_token,
            httponly=True,
            secure=True,
            samesite="Strict",
        )
        return ResponseRegisterData.model_validate(output_login.model_dump())
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


# TODO: Implementar la funcionalidad de login
@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseLoginData)
def post_login(
    request_data: RequestLoginData,
    response: Response,
    handler: UserHandlerInterface = Depends(get_user_handler),
):
    try:
        output_login = handler.login(input_login=InputLoginData.model_validate(request_data))
        if access_token := output_login.access_token:
            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                secure=True,
                samesite="Strict",
            )
            return ResponseLoginData.model_validate(output_login)
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials"
            )
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/logout", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseLogoutData)
def post_logout(response: Response):
    try:
        response.set_cookie(
            key="access_token",
            max_age=-1,
            httponly=True,
            secure=True,
            samesite="Strict",
        )

        return ResponseLogoutData()

    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
