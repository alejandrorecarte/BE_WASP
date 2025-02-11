import logging

from pymongo.mongo_client import MongoClient
from pymongo.database import Database
from pymongo.server_api import ServerApi

import os

from app.databases.client_interface import DBClientInterface


logger = logging.getLogger(__name__)

class MongoDBClient(DBClientInterface):
    _client: MongoClient = None  # Singleton instance
    _database_name: str = None  # Store the database name

    def __init__(self):
        """Initialize with optional database name."""
        db_name = os.getenv("MONGO_DB_NAME")
        logger.info(f"#### Database name: {db_name}")
        self._database_name = db_name

    def connect(self) -> MongoClient:
        """Establish the MongoDB connection (Singleton pattern)."""
        if self._client is None:
            uri = os.getenv("MONGO_URI")
            logger.info(f"#### Database URI: {uri}")
            self._client = MongoClient(uri, server_api=ServerApi('1'))
        return self._client

    def get_database(self) -> Database:
        """Get the specified database from MongoDB connection."""
        return self.connect()[self._database_name]
