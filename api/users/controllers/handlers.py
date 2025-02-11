from users.controllers.handler_interface import UserHandlerInterface
from users.controllers.input_data_models import InputRegisterData, InputLoginData
from users.controllers.output_data_models import OutputLoginData

from app.controllers.exceptions import ControlledException

from users.databases.handler import UserDBHandler

from users.databases.models import User


class UserHandler(UserHandlerInterface):

    def __init__(self, db_handler: UserDBHandler):
        self.db_handler = db_handler

    def register(self, input_register: InputRegisterData) -> bool:
        existing_user = self.db_handler.get({"email": input_register.email})
        if existing_user:
            raise ControlledException(status_code=400, detail="User already exists")

        user_data = User.model_validate(input_register.model_dump())  # Convert the Pydantic model to a dictionary
        self.db_handler.create_user(user_data=user_data)  # Insert user data into the DB

        return True  # Return a success flag

    def login(self, input_login: InputLoginData) -> OutputLoginData:
        return OutputLoginData()
