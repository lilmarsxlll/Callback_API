from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RESERVATION_API_URL: str
    ACCESS_TOKEN: str

    KAFKA_BOOTSTRAP_SERVERS: str
    KAFKA_TOPIC: str

    model_config = SettingsConfigDict(env_file="service_client/.env")


settings = Settings()
