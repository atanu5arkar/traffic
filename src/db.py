from pymongo import AsyncMongoClient

from src.constants import DB_NAME, MONGO_URI

mongo = AsyncMongoClient(MONGO_URI)
db = mongo[DB_NAME]
client_configs = db.client_configs

if __name__ == "__main__":
    import asyncio

    asyncio.run(client_configs.create_index("key", unique=True))
