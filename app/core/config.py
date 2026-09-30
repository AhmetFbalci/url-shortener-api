from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_URL: str

    model_config = SettingsConfigDict(
        env_file="/home/ahmet/Desktop/python_/Url-Shortener-Api/.env",
        extra="ignore"
    )


settings = Settings()