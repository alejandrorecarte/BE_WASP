import logging

import httpx
from app.controllers.exceptions import ControlledException
from fastapi import HTTPException, status
from users.controllers.constants import (
    GOOGLE_CLIENT_ID,
    GOOGLE_CLIENT_SECRET,
    GOOGLE_REDIRECT_URI,
    GOOGLE_TOKEN_URL,
    GOOGLE_USER_INFO_URL,
)
from users.controllers.handler_interface import UserHandlerInterface
from users.controllers.input_data_models import (
    InputAuthGoogleCallbackData,
    InputLoginData,
    InputRegisterData,
)
from users.controllers.output_data_models import (
    OutputAuthGoogleCallbackData,
    OutputLoginData,
    OutputRegisterData,
)
from users.databases.handler import UserDBHandler
from users.databases.models import GoogleUser, InternalUser

from api.auth.utils import create

logger = logging.getLogger(__name__)


class UserHandler(UserHandlerInterface):
    def __init__(self, db_handler: UserDBHandler):
        self.db_handler = db_handler

    async def auth_google_callback(
        self, input_auth_google_callback: InputAuthGoogleCallbackData
    ) -> OutputAuthGoogleCallbackData:
        # Intercambiar el código por un token de acceso
        logger.info(f"Authenticating Google user with code: {input_auth_google_callback.code}")
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                GOOGLE_TOKEN_URL,
                data={
                    "code": input_auth_google_callback.code,  # El código de autorización
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
            user_info_dict = user_info_response.json()["user"]
            user = GoogleUser(
                email=user_info_dict["email"],
                name=user_info_dict["name"],
                last_name=user_info_dict["last_name"],
            )
            self.db_handler.create_google_user(user_data=user)
            logger.info(f"Google user authenticated: {user_info_dict['email']}")
            return OutputAuthGoogleCallbackData(access_token=create(user))

    def register(self, input_register: InputRegisterData) -> OutputRegisterData:
        existing_user = self.db_handler.get({"email": input_register.email})
        if existing_user:
            raise ControlledException(status_code=400, detail="User already exists")

        user_data = InternalUser.model_validate(
            input_register.model_dump()
        )  # Convert the Pydantic model to a dictionary
        self.db_handler.create_internal_user(user_data=user_data)  # Insert user data into the DB

        return OutputRegisterData(access_token=create(user_data))

    def login(self, input_login: InputLoginData) -> OutputLoginData:
        input_user = InternalUser.model_validate(input_login.model_dump())

        user_data = self.db_handler.get({"email": input_user.email})
        if not user_data:
            raise HTTPException(status_code=400, detail="User not found")

        if user_data.password != input_user.hashed_password:
            raise HTTPException(status_code=400, detail="Incorrect password")

        return OutputLoginData(access_token=create(user_data))
