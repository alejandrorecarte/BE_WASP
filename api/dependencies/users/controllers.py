from app.databases.handler_interface import DBHandlerInterface
from dependencies.users.databases import get_user_db_handler
from fastapi import Depends
from users.controllers.handler_interface import UserHandlerInterface
from users.controllers.handlers import UserHandler


def get_user_handler(
    db_handler: DBHandlerInterface = Depends(get_user_db_handler),
) -> UserHandlerInterface:
    """Dependency to provide a handler instance"""
    return UserHandler(db_handler)
