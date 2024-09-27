import os
from dotenv import load_dotenv
from util.logger import logger

# Get the environment from the environment variable
ENVIRONMENT = os.getenv('ENVIRONMENT', 'local')

class Config:
    def __init__(self):
        self.load_environment()
        self.load_variables()
        self.validate_config()
        self.log_config()

    def load_environment(self):
        # Determine which .env file to load based on an environment variable
        env_file = f'.env.{ENVIRONMENT}'
        
        if os.path.exists(env_file):
            load_dotenv(env_file)
            logger.info(f"Configuration loaded from {env_file}")
        else:
            logger.warning(f"{env_file} not found, using environment variables")

    def load_variables(self):
        self.SOCRATA_APP_TOKEN = os.getenv('SOCRATA_APP_TOKEN')
        self.GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')
        
        # load google credentials file only if environment is local
        if ENVIRONMENT == 'local':
            self.GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE')
        else:
            self.GOOGLE_CREDENTIALS_FILE = None
        
        self.ENVIRONMENT = os.getenv('ENVIRONMENT')
        
        # Log the loaded variables for debugging
        logger.debug(f"Loaded SOCRATA_APP_TOKEN: {self.SOCRATA_APP_TOKEN}")
        logger.debug(f"Loaded GOOGLE_CREDENTIALS_FILE: {self.GOOGLE_CREDENTIALS_FILE}")
        logger.debug(f"Loaded GCS_BUCKET_NAME: {self.GCS_BUCKET_NAME}")
        logger.debug(f"Loaded ENVIRONMENT: {self.ENVIRONMENT}")
        
        # Add any other configuration variables here

    def validate_config(self):
        required_vars_local = ['SOCRATA_APP_TOKEN', 'GCS_BUCKET_NAME', 'GOOGLE_CREDENTIALS_FILE']
        required_vars_non_local = ['SOCRATA_APP_TOKEN', 'GCS_BUCKET_NAME']
        
        if ENVIRONMENT == 'local':
            required_vars = required_vars_local
        else:
            required_vars = required_vars_non_local
            
        missing_vars = [var for var in required_vars if not getattr(self, var)]
        
        if missing_vars:
            raise EnvironmentError(f"Missing required environment variables: {', '.join(missing_vars)}")

    def log_config(self):
        logger.info("Configuration loaded successfully")
        logger.debug(f"SOCRATA_APP_TOKEN: {'*' * len(self.SOCRATA_APP_TOKEN) if self.SOCRATA_APP_TOKEN else 'Not set'}")
        logger.debug(f"GOOGLE_CREDENTIALS_FILE: {'*' * len(self.GOOGLE_CREDENTIALS_FILE) if self.GOOGLE_CREDENTIALS_FILE else 'Not set'}")
        logger.debug(f"GCS_BUCKET_NAME: {self.GCS_BUCKET_NAME}")

# Create a global instance of the config
config = Config()

# You can now import this config object in other files
# from config import config
# Example usage: socrata_token = config.SOCRATA_APP_TOKEN