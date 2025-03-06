from typing import Optional

from pymongo.database import Database

from app.databases.mongo.handler import DBHandler
from users.databases.models import User


class UserDBHandler(DBHandler):
    def __init__(self, db: Database):
        super().__init__(db, "users")

    def create_user(self, user_data: User) -> str:
        user_dict = user_data.model_dump(
            by_alias=True, exclude={"id", "password"}
        )  # Exclude 'id' and 'password'
        user_id = self.create(user_dict)
        return user_id

    def get_user_by_email(self, email: str) -> Optional[User]:
        user_data = self.get({"email": email})
        if user_data:
            user_data["id"] = str(user_data["_id"])
            return User(**user_data)
        return None
