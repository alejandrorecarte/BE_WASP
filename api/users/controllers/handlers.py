import logging
import os
from datetime import datetime, timedelta, timezone

import httpx
import jwt
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
from users.databases.models import GoogleUser, InternalUser, User

logger = logging.getLogger(__name__)


class UserHandler(UserHandlerInterface):
    def __init__(self, db_handler: UserDBHandler):
        self.db_handler = db_handler

    # Create JWT Access Token
    def create_access_token(self, user: User) -> str:
        expiration_time = datetime.now(timezone.utc) + timedelta(
            minutes=int(os.getenv("EXPIRATION_MINUTES"))
        )
        payload = {"id": user.id, "user_email": user.email, "exp": expiration_time}
        return jwt.encode(payload, os.getenv("SECRET_KEY"), algorithm="HS256")

    # Verify JWT Access Token
    def verify_access_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, os.getenv("SECRET_KEY"), algorithms=["HS256"])
            exp_timestamp = payload["exp"]
            exp_datetime = datetime.fromtimestamp(exp_timestamp, tz=timezone.utc)
            current_datetime = datetime.now(timezone.utc)
            if current_datetime > exp_datetime:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
                )

            return payload

        except jwt.ExpiredSignatureError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has expired"
            )
        except jwt.InvalidTokenError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate token",
            )

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
            return OutputAuthGoogleCallbackData(access_token=self.create_access_token(user))

    def register(self, input_register: InputRegisterData) -> OutputRegisterData:
        existing_user = self.db_handler.get({"email": input_register.email})
        if existing_user:
            raise ControlledException(status_code=400, detail="User already exists")

        user_data = InternalUser.model_validate(
            input_register.model_dump()
        )  # Convert the Pydantic model to a dictionary
        self.db_handler.create_internal_user(user_data=user_data)  # Insert user data into the DB

        return OutputRegisterData(access_token=self.create_access_token(user_data))

    def login(self, input_login: InputLoginData) -> OutputLoginData:
        return OutputLoginData(access_token=self.create_access_token(""))
