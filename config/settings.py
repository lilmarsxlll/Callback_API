from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_NAME: str
    DB_HOST: str
    DB_PASS: str
    DB_USER: str

    model_config = SettingsConfigDict(env_file=".env")

    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@"
            f"{self.DB_HOST}/{self.DB_NAME}"
        )


settings = Settings()
