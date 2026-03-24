from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    RESERVATION_API_URL: str
    KAFKA_BOOTSTRAP_SERVER: str
    KAFKA_TOPIC: str

    SERVICE_CLIENT_USERNAME: str
    SERVICE_CLIENT_PASSWORD: str

    model_config = SettingsConfigDict(env_file="service_client/.env")


settings = Settings()
