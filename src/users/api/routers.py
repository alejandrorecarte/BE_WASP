import logging

from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2AuthorizationCodeBearer

from app.controllers.exceptions.exceptions import ControlledException
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
from users.controllers.constants import (
    GOOGLE_AUTH_URL,
    GOOGLE_CLIENT_ID,
    GOOGLE_REDIRECT_URI,
    GOOGLE_TOKEN_URL,
)
from users.controllers.handler_interface import GoogleLoginHandlerInterface, LoginHandlerInterface
from users.controllers.input_data_models import (
    InputGetMeData,
    InputGoogleLoginData,
    InputLoginData,
    InputRegisterData,
)

logger = logging.getLogger(__name__)

router = APIRouter()

oauth2_scheme = OAuth2AuthorizationCodeBearer(
    authorizationUrl=GOOGLE_AUTH_URL,  # URL de autorización de Google
    tokenUrl=GOOGLE_TOKEN_URL,  # URL para obtener el token de Google
)


@router.get("/google/redirect", status_code=status.HTTP_200_OK)
async def google_redirect():
    """
    Handles the Google OAuth2 redirect.

    This endpoint constructs a redirect URL for Google OAuth2 authentication and redirects the user to it.
    If an error occurs during the process, it logs the error and raises an HTTP 400 Bad Request exception.

    Returns:
        RedirectResponse: A response object that redirects the user to the Google OAuth2 authentication URL.

    Raises:
        HTTPException: If an error occurs during the redirect process, an HTTP 400 Bad Request exception is raised.
    """
    try:
        return RedirectResponse(
            url=(
                f"{GOOGLE_AUTH_URL}?response_type=code&client_id={GOOGLE_CLIENT_ID}"
                f"&redirect_uri={GOOGLE_REDIRECT_URI}&scope=openid%20profile%20email"
                f"&access_type=offline"
            )
        )
    except ControlledException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
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
    """
    Handles Google login requests.

    Args:
        request_data (RequestGoogleLoginData): The data required for Google login.
        response (Response): The response object to be modified.
        handler (GoogleLoginHandlerInterface, optional): The handler for Google login. Defaults to Depends(get_google_login_handler).

    Returns:
        ResponseGoogleLoginData: The response data for Google login.

    Raises:
        HTTPException: If an error occurs during the login process, a 400 BAD REQUEST error is raised.
    """
    try:
        output_google_login = await handler.google_login(
            input_google_login=InputGoogleLoginData(code=request_data.code)
        )
        response = create_token(response=response, user_id=output_google_login.user_id)
        return ResponseGoogleLoginData()
    except ControlledException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
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
    """
    Handle user registration request.

    Args:
        request_data (RequestRegisterData): The data required for user registration.
        response (Response): The response object to be modified.
        handler (LoginHandlerInterface, optional): The login handler dependency. Defaults to Depends(get_login_handler).

    Returns:
        ResponseRegisterData: The response data after successful registration.

    Raises:
        HTTPException: If an error occurs during registration, an HTTP 400 exception is raised with the error details.
    """
    try:
        output_register = handler.register(
            input_register=InputRegisterData.model_validate(request_data.model_dump())
        )
        response = create_token(response=response, user_id=output_register.user_id)
        return ResponseRegisterData()

    except ControlledException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseLoginData)
def post_login(
    request_data: RequestLoginData,
    response: Response,
    handler: LoginHandlerInterface = Depends(get_login_handler),
):
    """
    Handle user login request.
    Args:
        request_data (RequestLoginData): The login request data.
        response (Response): The response object to be modified.
        handler (LoginHandlerInterface, optional): The login handler dependency. Defaults to Depends(get_login_handler).
    Returns:
        ResponseLoginData: The response data after successful login.
    Raises:
        HTTPException: If there is an error during login, an HTTP 400 Bad Request exception is raised.
    """
    try:
        output_login = handler.login(
            input_login=InputLoginData.model_validate(request_data.model_dump())
        )
        response = create_token(response=response, user_id=output_login.user_id)
        return ResponseLoginData()

    except ControlledException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.post("/logout", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseLogoutData)
def post_logout(response: Response):
    """
    Handle user logout by invalidating the authentication token.
    Args:
        response (Response): The response object to be modified.
    Returns:
        ResponseLogoutData: An object indicating successful logout.
    Raises:
        HTTPException: If an error occurs during token invalidation,
                       an HTTP 400 Bad Request exception is raised with the error details.
    """
    try:
        response = invalidate_token(response=response)
        return ResponseLogoutData()

    except ControlledException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
    except Exception as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/me", status_code=status.HTTP_200_OK, response_model=ResponseMeData)
def get_me(
    response: Response,
    handler: LoginHandlerInterface = Depends(get_login_handler),
    token_payload: str = Depends(get_token_from_cookie),
):
    """
    Retrieve the current user's information based on the token payload.

    Args:
        response (Response): The response object.
        handler (LoginHandlerInterface, optional): The login handler dependency. Defaults to Depends(get_login_handler).
        token_payload (str, optional): The token payload extracted from the cookie. Defaults to Depends(get_token_from_cookie).

    Returns:
        ResponseMeData: The response data containing the user ID.

    Raises:
        HTTPException: If there is an HTTP error.
        HTTPException: If there is a general exception, with status code 400 and the error detail.
    """
    try:
        handler.get_me(InputGetMeData(user_id=token_payload["user_id"]))
        return ResponseMeData(user_id=token_payload["user_id"])
    except ControlledException as error:
        raise HTTPException(status_code=error.status_code, detail=error.detail)
    except Exception as error:
        logger.error(str(error))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
