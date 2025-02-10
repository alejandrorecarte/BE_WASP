from fastapi import APIRouter, HTTPException, status, Response, Depends
import logging

from dependencies.users.controllers.handlers import get_user_handler
from users.api.request_data_models import RequestLoginData, RequestRegisterData
from users.api.response_data_models import ResponseRegisterData, ResponseLoginData, ResponseLogoutData
from users.controllers.handler_interface import UserHandlerInterface
from users.controllers.input_data_models import InputRegisterData, InputLoginData

logger = logging.getLogger(__name__)

router = APIRouter()


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=ResponseRegisterData)
def post_register(
    request_data: RequestRegisterData,
    response: Response,
    handler: UserHandlerInterface = Depends(get_user_handler)
):
    try:
        handler.register(input_register=InputRegisterData.model_validate(request_data))
        output_login = handler.login(input_login=InputLoginData.model_validate(request_data))
        response.set_cookie(key="access_token", value=output_login.access_token, httponly=True, secure=True, samesite='Strict')
        return ResponseRegisterData.model_validate(output_login)
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.post("/login", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseLoginData)
def post_login(
    request_data: RequestLoginData,
    response: Response,
    handler: UserHandlerInterface = Depends(get_user_handler)
):
    try:
        output_login = handler.login(input_login=InputLoginData.model_validate(request_data))
        if access_token := output_login.access_token:
            response.set_cookie(key="access_token", value=access_token, httponly=True, secure=True, samesite='Strict')
            return ResponseLoginData.model_validate(output_login)
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )


@router.post("/logout", status_code=status.HTTP_202_ACCEPTED, response_model=ResponseLogoutData)
def post_logout(response: Response):
    try:
        response.set_cookie(key="access_token", max_age=-1, httponly=True, secure=True, samesite="Strict")

        return ResponseLogoutData()

    except Exception as error:
        logger.warning(str(error))
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
