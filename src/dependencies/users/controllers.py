from fastapi import Depends

from app.databases.handler_interface import DBHandlerInterface
from dependencies.users.databases import get_user_db_handler
from users.controllers.handler_interface import GoogleLoginHandlerInterface, LoginHandlerInterface
from users.controllers.handlers import GoogleLoginHandler, LoginHandler


def get_login_handler(
    db_handler: DBHandlerInterface = Depends(get_user_db_handler),
) -> LoginHandlerInterface:
    """Dependency to provide a handler instance"""
    return LoginHandler(db_handler)


def get_google_login_handler(
    db_handler: DBHandlerInterface = Depends(get_user_db_handler),
) -> GoogleLoginHandlerInterface:
    """Dependency to provide a handler instance"""
    return GoogleLoginHandler(db_handler)
