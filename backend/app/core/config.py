from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    jwt_secret: str = "changeme"
    debug: bool = True

    class Config:
        env_file = ".env"

settings = Settings()

