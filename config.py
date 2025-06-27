from pydantic_settings import BaseSettings
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    db_host: str = Field(env="DB_HOST")
    db_port: int = Field(env="DB_PORT")
    db_name: str = Field(env="DB_NAME")
    db_user: str = Field(env="DB_USER")
    db_pass: str = Field(env="DB_PASS")

    class Config:
        env_file = ".env"


settings = Settings()