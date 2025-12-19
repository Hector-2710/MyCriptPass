from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_NAME: str
    DATABASE_URL: str  
    SECRET_KEY: str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRE_MINUTES : int
    DATABASE_TEST: str

    class Config:
        env_file = ".env"

settings = Settings()