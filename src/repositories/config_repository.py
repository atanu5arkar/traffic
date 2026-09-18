from src.db import client_configs
from src.models.client_config import ClientConfig, ShortClientConfig


class ConfigRepository:
    async def add(self, config: ClientConfig):
        return await client_configs.update_one(
            {"key": config.key}, {"$set": config.model_dump()}, upsert=True
        )

    async def get(self, key: str):
        conf = await client_configs.find_one({"key": key}, {"_id": 0, "created_at": 0})
        if not conf:
            return None
        return ShortClientConfig(burst_size=conf["burst_size"], rps=conf["rps"])


config_repo = ConfigRepository()
