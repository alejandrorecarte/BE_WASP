from users.controllers.handler_interface import UserHandlerInterface
from users.controllers.handlers import UserHandler


def get_user_handler() -> UserHandlerInterface:
    """Dependency to provide a handler instance"""
    return UserHandler()
