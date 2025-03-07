from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import HTTPException

from users.controllers.handlers import GoogleLoginHandler, LoginHandler
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


@pytest.fixture
def db_handler():
    return MagicMock(spec=UserDBHandler)


@pytest.fixture
def login_handler(db_handler):
    return LoginHandler(db_handler=db_handler)


@pytest.fixture
def google_login_handler(db_handler):
    return GoogleLoginHandler(db_handler=db_handler)


def test_register_user_already_exists(login_handler, db_handler):
    db_handler.get.return_value = True
    input_data = InputRegisterData(
        email="test@example.com", password="password", name="Test", last_name="User"
    )

    with pytest.raises(HTTPException) as exc_info:
        login_handler.register(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User already exists"


def test_register_new_user(login_handler, db_handler):
    db_handler.get.return_value = None
    db_handler.create_user.return_value = "new_user_id"
    input_data = InputRegisterData(
        email="test@example.com", password="password", name="Test", last_name="User"
    )

    result = login_handler.register(input_data)

    assert result == OutputRegisterData(user_id="new_user_id")


def test_login_user_not_found(login_handler, db_handler):
    db_handler.get.return_value = None
    input_data = InputLoginData(email="test@example.com", password="password")

    with pytest.raises(HTTPException) as exc_info:
        login_handler.login(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "User not found"


def test_login_incorrect_password(login_handler, db_handler):
    db_handler.get.return_value = {"email": "test@example.com", "hashed_password": "wrong_password"}
    input_data = InputLoginData(email="test@example.com", password="password")

    with pytest.raises(HTTPException) as exc_info:
        login_handler.login(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "Incorrect password"


def test_login_success(login_handler, db_handler):
    db_handler.get.return_value = {
        "_id": "user_id",
        "email": "test@example.com",
        "hashed_password": "$2b$12$dLYqCJjcyVVF5bb4zEEjYe6nA6Q05gv83YMQu/qbkVgmaXtDSNqsS",
    }
    input_data = InputLoginData(email="test@example.com", password="test")

    result = login_handler.login(input_data)

    assert result == OutputLoginData(user_id="user_id")


@pytest.mark.asyncio
async def test_google_login_token_error(google_login_handler, db_handler):
    input_data = InputGoogleLoginData(code="auth_code")
    async_client_mock = AsyncMock()
    async_client_mock.post.return_value.json.return_value = {}

    with pytest.raises(HTTPException) as exc_info:
        await google_login_handler.google_login(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == "No se pudo obtener el token de acceso"


@pytest.mark.asyncio
async def test_google_login_success(mocker, google_login_handler, db_handler):
    # Datos de entrada de la prueba
    input_data = InputGoogleLoginData(code="auth_code")

    # Simulando la respuesta de la obtención del token con un access_token válido usando mocker
    mocker.patch("httpx.AsyncClient.post", return_value=mocked_post_response())
    mocker.patch("httpx.AsyncClient.get", return_value=mocked_get_response())

    # Mock de las funciones de base de datos
    db_handler.get_user_by_email.return_value = None  # El usuario no existe
    db_handler.create_user.return_value = "new_user_id"

    # Ejecutar el login de Google
    result = await google_login_handler.google_login(input_data)

    # Verificar el resultado esperado
    assert result == OutputGoogleLoginData(user_id="new_user_id")


def mocked_post_response():
    # Simulamos una respuesta de post que contiene el access_token
    class MockResponse:
        def json(self):
            return {"access_token": "access_token"}

    return MockResponse()


def mocked_get_response():
    # Simulamos una respuesta de get con los datos del usuario
    class MockResponse:
        def json(self):
            return {"email": "test@example.com", "given_name": "Test", "family_name": "User"}

    return MockResponse()
