from users.controllers.handler_interface import UserHandlerInterface
from users.controllers.input_data_models import InputRegisterData, InputLoginData
from users.controllers.output_data_models import OutputLoginData


class UserHandler(UserHandlerInterface):

    def register(self, input_register: InputRegisterData) -> bool:
        return True

    def login(self, input_login: InputLoginData) -> OutputLoginData:
        return OutputLoginData()
