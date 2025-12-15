from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    google_api_key: str
    anthropic_api_key: str
    gemini_model: str
    embedding_model: str
    collection_name: str
    chroma_host: str
    api_host: str

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()  # type: ignore[call-arg]
