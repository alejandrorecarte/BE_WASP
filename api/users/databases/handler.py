from typing import Optional

from app.databases.mongo.handler import DBHandler
from pymongo.database import Database
from users.databases.models import GoogleUser, InternalUser, User


class UserDBHandler(DBHandler):
    def __init__(self, db: Database):
        super().__init__(db, "users")

    def create_google_user(self, user_data: GoogleUser) -> GoogleUser:
        user_dict = user_data.model_dump(by_alias=True, exclude={"id"})  # Exclude 'id'
        user_id = self.create(user_dict)
        return GoogleUser(**user_dict, id=user_id)

    def create_internal_user(self, user_data: InternalUser) -> InternalUser:
        user_dict = user_data.model_dump(
            by_alias=True, exclude={"id", "password"}
        )  # Exclude 'id' and 'password'
        user_id = self.create(user_dict)
        return InternalUser(**user_dict, id=user_id)

    def get_user_by_email(self, email: str) -> Optional[User]:
        user_data = self.get({"email": email})
        if user_data:
            user_data["id"] = str(user_data["_id"])
            return User(**user_data)
        return None
