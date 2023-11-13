from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    assistant_name: str = "jean-michel"

    model_config = SettingsConfigDict(
        env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )


class OpenAiSettings(BaseSettings):
    api_key: str
    model: str = "gpt-3.5-turbo"
    max_tokens: int = 500
    temperature: float = 0.7

    model_config = SettingsConfigDict(
        env_prefix="openai_", env_file=".env", extra="ignore", env_file_encoding="utf-8"
    )
