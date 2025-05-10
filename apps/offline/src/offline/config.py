from loguru import logger
from pydantic import Field, field_validator
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

    OPENAI_API_KEY: str = Field(
        description="API key for OpenAI service authentication.",
    )

    OPENAI_MODEL_ID: str = Field(
        default="gpt-4o-mini",
        description="Model ID for OpenAI service.",
    )

    @field_validator("OPENAI_API_KEY")
    @classmethod
    def check_not_empty(cls, value: str, info) -> str:
        if not value or value.strip() == "":
            logger.error(f"{info.field_name} cannot be empty.")
            raise ValueError(f"{info.field_name} cannot be empty.")
        return value

try:
    settings = Settings()
except Exception as e:
    logger.error(f"Failed to load configuration: {e}")
    raise SystemExit(e)