import logging

import httpx
from fastapi import HTTPException, status

from app.controllers.exceptions import ControlledException
from users.controllers.constants import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    GOOGLE_TOKEN_URL,
    GOOGLE_USER_INFO_URL,
)
from users.controllers.handler_interface import GoogleLoginHandlerInterface, LoginHandlerInterface
from users.controllers.input_data_models import (
    InputGoogleLoginData,
    InputLoginData,
    InputRegisterData,
)
from users.controllers.output_data_models import (
    OutputGoogleLoginData,
    OutputLoginData,
    OutputRegisterData,
)
from users.databases.handler import UserDBHandler
from users.databases.models import User, UserType

logger = logging.getLogger(__name__)


class LoginHandler(LoginHandlerInterface):
    def __init__(self, db_handler: UserDBHandler):
        self.db_handler = db_handler

    def register(self, input_register: InputRegisterData) -> OutputRegisterData:
        existing_user = self.db_handler.get({"email": input_register.email})
        if existing_user:
            raise ControlledException(status_code=400, detail="User already exists")

        user_data = User.model_validate({**input_register.model_dump(), "type": UserType.INTERNAL})
        user_id = self.db_handler.create_user(user_data=user_data)  # Insert user data into the DB

        return OutputRegisterData(user_id=user_id)

    def login(self, input_login: InputLoginData) -> OutputLoginData:
        input_user = User.model_validate({**input_login.model_dump(), "type": UserType.INTERNAL})

        user_data = self.db_handler.get({"email": input_user.email})
        if not user_data:
            raise HTTPException(status_code=400, detail="User not found")

        if user_data["hashed_password"] != input_user.hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect password")

        return OutputLoginData(user_id=str(user_data["_id"]))


class GoogleLoginHandler(GoogleLoginHandlerInterface):
    def __init__(self, db_handler: UserDBHandler):
        self.db_handler = db_handler

    async def google_login(self, input_google_login: InputGoogleLoginData) -> OutputGoogleLoginData:
        # Intercambiar el código por un token de acceso
        logger.info(f"Authenticating Google user with code: {input_google_login.code}")
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": input_google_login.code,  # El código de autorización
                    "client_id": GOOGLE_CLIENT_ID,
                    "client_secret": GOOGLE_CLIENT_SECRET,
                    "redirect_uri": GOOGLE_REDIRECT_URI,
                    "grant_type": "authorization_code",  # Tipo de concesión
                },
            )
            token_data = token_response.json()

            # Verificar si se obtuvo el token de acceso
            if "access_token" not in token_data:
                logger.error(f"Could not get access token: {token_data}")
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="No se pudo obtener el token de acceso",
                )

            # Obtener la información del usuario desde Google
            user_info_response = await client.get(
                GOOGLE_USER_INFO_URL,
                headers={"Authorization": f"Bearer {token_data['access_token']}"},
            )

            logger.debug(f"Google user info response: {user_info_response.json()}")
            user_info_dict = user_info_response.json()

            # Verificar si el usuario ya existe en la base de datos
            if user := self.db_handler.get_user_by_email(email=user_info_dict["email"]):
                return OutputGoogleLoginData(user_id=user.id)

            user = User(
                type=UserType.GOOGLE,
                email=user_info_dict["email"],
                name=user_info_dict["given_name"],
                last_name=user_info_dict["family_name"],
            )
            user_id = self.db_handler.create_user(user_data=user)
            logger.info(f"Google user authenticated: {user_info_dict['email']}")
            return OutputGoogleLoginData(user_id=user_id)
