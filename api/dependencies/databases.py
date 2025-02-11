from app.databases.mongo.client import MongoDBClient


def get_db():
    """Dependency to get MongoDB database connection."""
    mongo_client = MongoDBClient()
    return mongo_client.get_database()
