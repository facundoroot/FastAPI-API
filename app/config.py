# Pydantic
from pydantic import BaseSettings


# validate env variables
class Settings(BaseSettings):
    # validate and optional values
    database_hostname: str
    database_port: int
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config():
        env_file = ".env"


settings = Settings()
