from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from dotenv import load_dotenv
import os

load_dotenv()

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)

    db_host: str = Field()
    db_port: int = Field()
    db_name: str = Field()
    db_user: str = Field()
    db_pass: str = Field()

    SECRET_KEY: str = Field()
    ALGORITHM: str = Field()
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field()


settings = Settings()