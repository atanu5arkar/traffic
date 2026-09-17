from src.models.client_config import ShortClientConfig


class ConfigRepository:
    def add(self, key: str):
        return

    def get(self, key: str):
        return ShortClientConfig(burst_size=30, rps=2)

config_repo = ConfigRepository()