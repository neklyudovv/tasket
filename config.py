from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    db_host: str
    db_port: int
    db_name: str
    db_user: str
    db_pass: str

    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    cors_origins: list[str] = []
    cors_methods: list[str] = []
    cors_headers: list[str] = []


settings = Settings()