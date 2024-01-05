from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class BaseConfig(BaseSettings):
    ENV_STATE: str | None = None
    model_config: dict = SettingsConfigDict(env_file=".env", extra="ignore")


class GlobalConfig(BaseConfig):
    DATABASE_URL: str | None = None
    DB_FORCE_ROLL_BACK: bool = False


class DevConfig(GlobalConfig):
    model_config: dict = SettingsConfigDict(env_prefix="DEV_")


class TestConfig(GlobalConfig):
    DATABASE_URL: str = "sqlite:///test.db"
    DB_FORCE_ROLL_BACK: bool = True


class ProdConfig(GlobalConfig):
    model_config: dict = SettingsConfigDict(env_prefix="PROD_")


@lru_cache()
def get_config(env_state: str) -> GlobalConfig:
    configurations: dict[str, type(GlobalConfig)] = {"dev": DevConfig, "test": TestConfig, "prod": ProdConfig}
    return configurations[env_state]()


config: GlobalConfig = get_config(BaseConfig().ENV_STATE)
