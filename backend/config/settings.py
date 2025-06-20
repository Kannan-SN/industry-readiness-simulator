from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    google_api_key: str
    weaviate_url: str
    weaviate_api_key: str
    cors_origins: str = "http://localhost:5173"
    
    class Config:
        env_file = ".env"

settings = Settings()