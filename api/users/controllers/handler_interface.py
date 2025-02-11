from abc import ABC, abstractmethod

from users.controllers.input_data_models import InputRegisterData, InputLoginData
from users.controllers.output_data_models import OutputLoginData


class UserHandlerInterface(ABC):

    @abstractmethod
    def register(self, input_register: InputRegisterData) -> bool:
        pass

    @abstractmethod
    def login(self, input_login: InputLoginData) -> OutputLoginData:
        pass
