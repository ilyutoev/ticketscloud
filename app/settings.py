from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = "localhost"
    port: int = 8080

    mongo_host: str = "localhost"
    mongo_port: int = 27017


settings = Settings()
