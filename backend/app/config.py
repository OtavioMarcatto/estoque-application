from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Estoque"
    debug: bool = False
    database_url: str = "sqlite+aiosqlite:///./estoque.db"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
