import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
from typing import Optional

from app.util.constants import Environment
from app.util.logger import logger

# ENV: local, docker, replit, stage, prod
ENVIRONMENT = os.getenv('ENVIRONMENT', 'prod')
logger.info(f"Current environment: {ENVIRONMENT}")

# Load environment variables from the appropriate .env file
if ENVIRONMENT in [Environment.LOCAL.value, Environment.DOCKER.value, Environment.REPLIT.value]:
    env_file = f".env.{ENVIRONMENT}"
    load_dotenv(env_file)
    logger.info(f"Loaded environment variables from {env_file}")

class Settings(BaseModel):
    ENVIRONMENT: Environment = Field(default=ENVIRONMENT)
    SOCRATA_APP_TOKEN: str = Field(default=os.getenv('SOCRATA_APP_TOKEN'))
    GCS_BUCKET_NAME: str = Field(default=os.getenv('GCS_BUCKET_NAME'))
    GCP_PROJECT_ID: str = Field(default=os.getenv('GCP_PROJECT_ID'))
    GOOGLE_CREDENTIALS_FILE: Optional[str] = Field(default=os.getenv('GOOGLE_CREDENTIALS_FILE'))

    class Config:
        env_file = env_file
        env_file_encoding = 'utf-8'
        use_enum_values = True

def get_settings() -> Settings:
    try:
        settings = Settings()
        logger.info("Settings loaded successfully")
        logger.debug(f"Loaded settings: {settings.dict()}")
        return settings
    except ValidationError as e:
        logger.error(f"Error loading settings: {e}")
        for error in e.errors():
            logger.error(f"Field '{error['loc'][0]}': {error['msg']}")
        raise ValueError("Failed to load settings. Check your environment variables.")

settings = get_settings()
logger.info("Configuration initialized")
