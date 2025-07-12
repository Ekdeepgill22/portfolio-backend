# Environment configuration
from pydantic_settings import BaseSettings
from typing import List
import os


class Settings(BaseSettings):
    # MongoDB Configuration
    mongodb_uri: str = "mongodb+srv://mailekdeep:Ekdeep%4013@cluster0.qls6dn5.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    database_name: str = "portfolio_db"
    
    # CORS Configuration
    cors_origins: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "https://your-portfolio.vercel.app"
    ]
    
    # Environment
    environment: str = "development"
    
    # API Configuration
    api_v1_str: str = "/api/v1"
    project_name: str = "Portfolio Backend"
    
    # Static files configuration
    static_files_path: str = "app/static"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    @property
    def is_development(self) -> bool:
        return self.environment.lower() == "development"


# Global settings instance
settings = Settings()