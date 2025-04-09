from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str
    DB_DRIVER: str

    CACHE_HOST: str
    CACHE_PORT: int
    CACHE_DB: int

    model_config = SettingsConfigDict(env_file=".env")

    @property
    def get_database_url(self):
        return f"{self.DB_DRIVER}://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
