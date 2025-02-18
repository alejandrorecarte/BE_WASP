from abc import ABC, abstractmethod

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


class UserHandlerInterface(ABC):
    @abstractmethod
    def google_login(self, input_google_login: InputGoogleLoginData) -> OutputGoogleLoginData:
        pass

    @abstractmethod
    def register(self, input_register: InputRegisterData) -> OutputRegisterData:
        pass

    @abstractmethod
    def login(self, input_login: InputLoginData) -> OutputLoginData:
        pass
