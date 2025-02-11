from typing import Optional

from app.databases.handler_interface import DBHandlerInterface
from pymongo.database import Database


class DBHandler(DBHandlerInterface):
    def __init__(self, db: Database, collection_name: str):
        self.collection = db[collection_name]

    def create(self, data: dict) -> str:
        result = self.collection.insert_one(data)
        return str(result.inserted_id)

    def get(self, query: dict) -> Optional[dict]:
        return self.collection.find_one(query)

    def update(self, query: dict, update_data: dict) -> int:
        result = self.collection.update_one(query, {"$set": update_data})
        return result.modified_count

    def delete(self, query: dict) -> int:
        result = self.collection.delete_one(query)
        return result.deleted_count
