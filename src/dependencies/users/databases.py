from fastapi import Depends
from pymongo.database import Database

from dependencies.databases import get_db
from users.databases.handler import UserDBHandler


def get_user_db_handler(db: Database = Depends(get_db)) -> UserDBHandler:
    """Dependency to provide the DBHandler instance"""
    return UserDBHandler(db)
