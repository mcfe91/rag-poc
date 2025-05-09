from loguru import logger
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    A Pydantic-based settings class for managing application configuration.
    """

    model_config: SettingsConfigDict = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8"
    )

    NOTION_SECRET_KEY: str | None = Field(
        default=None, description="Secret key for Notion API authentication."
    )

try:
    settings = Settings()
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    raise SystemExit(e)