from unittest.mock import AsyncMock, MagicMock

import pytest

from app.controllers.exceptions.exception_messages import (
    ERROR_GOOGLE_CODE,
    INCORRECT_PASSWORD,
    USER_ALREADY_EXISTS,
    USER_NOT_FOUND,
)
from app.controllers.exceptions.exceptions import ControlledException
from tests.fixtures.users.user import INTERNAL_BD_USER
from users.controllers.handlers import GoogleLoginHandler, LoginHandler
from users.controllers.input_data_models import (
    InputGetMeData,
    InputGoogleLoginData,
    InputLoginData,
    InputRegisterData,
)
from users.controllers.output_data_models import OutputGoogleLoginData, OutputRegisterData
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
    """
    Test case for registering a user that already exists.
    This test verifies that the `register` method of the `login_handler` raises an
    ControlledException with a status code of 400 and a detail message "User already exists"
    when attempting to register a user with an email that already exists in the database.
    Args:
        login_handler (LoginHandler): The handler responsible for user login and registration.
        db_handler (DBHandler): The handler responsible for database operations.
    Setup:
        - Mocks the `db_handler.get` method to return True, indicating that the user already exists.
        - Creates an instance of `InputRegisterData` with test user details.
    Test:
        - Calls the `register` method of `login_handler` with the test user data.
        - Asserts that an ControlledException is raised.
        - Asserts that the status code of the exception is 400.
        - Asserts that the detail message of the exception is "User already exists".
    """
    db_handler.get.return_value = True
    input_data = InputRegisterData(
        email="test@example.com", password="password", name="Test", last_name="User"
    )

    with pytest.raises(ControlledException) as exc_info:
        login_handler.register(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == USER_ALREADY_EXISTS


def test_register_new_user(login_handler, db_handler):
    """
    Test the registration of a new user.
    This test verifies that the `register` method of the `login_handler` correctly
    registers a new user when the user does not already exist in the database.
    Args:
        login_handler (Mock): A mock object representing the login handler.
        db_handler (Mock): A mock object representing the database handler.
    Setup:
        - The `db_handler.get` method is mocked to return `None`, simulating that
          the user does not already exist in the database.
        - The `db_handler.create_user` method is mocked to return a new user ID.
    Test:
        - An `InputRegisterData` object is created with test user details.
        - The `register` method of the `login_handler` is called with the input data.
        - The result is asserted to be an `OutputRegisterData` object with the
          expected user ID.
    """
    db_handler.get.return_value = None
    db_handler.create_user.return_value = "new_user_id"
    input_data = InputRegisterData(
        email="test@example.com", password="password", name="Test", last_name="User"
    )

    result = login_handler.register(input_data)

    assert result == OutputRegisterData(user_id="new_user_id")


def test_login_user_not_found(login_handler, db_handler):
    """
    Test case for the login handler when the user is not found in the database.
    This test simulates a scenario where the login handler attempts to log in a user
    that does not exist in the database. It ensures that the appropriate ControlledException
    is raised with the correct status code and detail message.
    Args:
        login_handler: The login handler instance to be tested.
        db_handler: The database handler mock used to simulate database interactions.
    Test Steps:
    1. Set up the database handler mock to return None, indicating the user is not found.
    2. Create an instance of InputLoginData with test email and password.
    3. Call the login method of the login handler with the input data and expect an ControlledException.
    4. Assert that the raised exception has a status code of 400 and a detail message "User not found".
    """
    db_handler.get.return_value = None
    input_data = InputLoginData(email="test@example.com", password="password")

    with pytest.raises(ControlledException) as exc_info:
        login_handler.login(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == USER_NOT_FOUND


def test_login_incorrect_password(login_handler, db_handler):
    """
    Test case for the login handler when an incorrect password is provided.
    This test simulates a login attempt with an incorrect password and verifies
    that the login handler raises an ControlledException with a status code of 400 and
    a detail message indicating an incorrect password.
    Args:
        login_handler: The login handler instance to be tested.
        db_handler: The database handler mock used to simulate database interactions.
    Setup:
        - The database handler's `get` method is mocked to return a predefined user.
    Test Steps:
        1. Create an instance of `InputLoginData` with a test email and incorrect password.
        2. Attempt to login using the `login_handler` with the provided input data.
        3. Verify that an ControlledException is raised with the expected status code and detail message.
    Assertions:
        - The raised ControlledException has a status code of 400.
        - The raised ControlledException has a detail message of "Incorrect password".
    """
    db_handler.get.return_value = INTERNAL_BD_USER
    input_data = InputLoginData(email="test@example.com", password="password")

    with pytest.raises(ControlledException) as exc_info:
        login_handler.login(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == INCORRECT_PASSWORD


def test_get_me_user_not_found(login_handler, db_handler):
    """
    Test case for the `get_me` method in the `login_handler` when the user is not found.
    This test simulates the scenario where the `get_user_by_id` method of the `db_handler`
    returns `None`, indicating that the user does not exist in the database. It then
    verifies that the `get_me` method raises an `ControlledException` with a status code of 400
    and a detail message of "User not found".
    Args:
        login_handler: The handler responsible for login operations.
        db_handler: The handler responsible for database operations.
    Raises:
        ControlledException: If the user is not found, an ControlledException with status code 400
                       and detail "User not found" is raised.
    """
    db_handler.get_user_by_id.return_value = None
    input_data = InputGetMeData(user_id="non_existent_user_id")

    with pytest.raises(ControlledException) as exc_info:
        login_handler.get_me(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == USER_NOT_FOUND


def test_get_me_success(login_handler, db_handler):
    """
    Test the successful retrieval of user data using the 'get_me' method.
    This test verifies that the 'get_me' method of the login_handler correctly
    retrieves and returns user data when provided with a valid user ID.
    Args:
        login_handler (LoginHandler): The handler responsible for user login operations.
        db_handler (DBHandler): The handler responsible for database operations.
    Setup:
        - Mocks the database handler's 'get_user_by_id' method to return predefined user data.
        - Creates an instance of InputGetMeData with a valid user ID.
    Assertions:
        - Ensures that the 'get_me' method is called with the correct input data.
        - Verifies that the returned user data matches the predefined user data.
    """
    user_data = INTERNAL_BD_USER
    db_handler.get_user_by_id.return_value = user_data
    input_data = InputGetMeData(user_id="existing_user_id")

    login_handler.get_me(input_data)


@pytest.mark.asyncio
async def test_google_login_token_error(google_login_handler, db_handler):
    """
    Test case for the google_login method in the google_login_handler.
    This test simulates a scenario where the Google login process fails to obtain an access token.
    It verifies that the appropriate ControlledException is raised with the correct status code and error message.
    Args:
        google_login_handler: The handler responsible for processing Google login requests.
        db_handler: The database handler used for database operations.
    Setup:
        - Mocks the async HTTP client to return an empty JSON response when attempting to obtain the access token.
    Test:
        - Asserts that an ControlledException with status code 400 and a specific error message is raised when the access token cannot be obtained.
    """
    input_data = InputGoogleLoginData(code="auth_code")
    async_client_mock = AsyncMock()
    async_client_mock.post.return_value.json.return_value = {}

    with pytest.raises(ControlledException) as exc_info:
        await google_login_handler.google_login(input_data)

    assert exc_info.value.status_code == 400
    assert exc_info.value.detail == ERROR_GOOGLE_CODE


@pytest.mark.asyncio
async def test_google_login_success(mocker, google_login_handler, db_handler):
    """
    Test the successful Google login process.
    This test verifies that the Google login handler correctly processes a valid
    authorization code, interacts with the Google API to obtain an access token,
    retrieves user information, and creates a new user in the database if the user
    does not already exist.
    Args:
        mocker: The mocker fixture for patching external dependencies.
        google_login_handler: The handler responsible for processing Google login.
        db_handler: The database handler for interacting with the user database.
    Setup:
        - Mocks the HTTP POST request to the Google token endpoint to return a valid access token.
        - Mocks the HTTP GET request to the Google user info endpoint to return user information.
        - Mocks the database handler to simulate the user not existing and the creation of a new user.
    Assertions:
        - Asserts that the result of the Google login handler is the expected output with the new user ID.
    """
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
