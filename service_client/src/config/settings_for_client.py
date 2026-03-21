from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    JWT_TOKEN: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str

    KAFKA_BOOTSTRAP_SERVER: str
    KAFKA_TOPIC: str

    model_config = SettingsConfigDict(env_file="service_client/.env")


settings = Settings()
