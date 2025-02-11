from abc import ABC, abstractmethod

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


class UserHandlerInterface(ABC):
    @abstractmethod
    def auth_google_callback(
        self, input_auth_google_callback: InputAuthGoogleCallbackData
    ) -> OutputAuthGoogleCallbackData:
        pass

    @abstractmethod
    def register(self, input_register: InputRegisterData) -> OutputRegisterData:
        pass

    @abstractmethod
    def login(self, input_login: InputLoginData) -> OutputLoginData:
        pass
