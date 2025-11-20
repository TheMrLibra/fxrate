from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "postgresql://user:password@localhost:5432/fxrate_db"
    secret_key: str = ""
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

