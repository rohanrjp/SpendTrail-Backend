from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SECRET_KEY:str
    ALGORITHM:str
    ACCESS_TOKEN_EXPIRE_MINUTES:int
    DATABASE_URL:str
    environment:str
    GEMINI_API_KEY:str

    model_config = SettingsConfigDict(
        env_file=".env", 
        extra="ignore"
    )

Config = Settings()