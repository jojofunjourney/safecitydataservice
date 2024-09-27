import os
import yaml
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
        
    def load_yaml(self):
        with open('env.yaml', 'r') as file:
            self.yaml_data = yaml.safe_load(file)

    def load_variables(self):
        self.SOCRATA_APP_TOKEN = self.yaml_data['SOCRATA_APP_TOKEN']
        self.GCS_BUCKET_NAME = self.yaml_data['GCS_BUCKET_NAME']
        
        # load google credentials file only if environment is local
        if ENVIRONMENT == 'local':
            self.GOOGLE_CREDENTIALS_FILE = self.yaml_data['GOOGLE_CREDENTIALS_FILE']
        else:
            self.GOOGLE_CREDENTIALS_FILE = os.getenv('GOOGLE_CREDENTIALS_FILE')
        
        self.ENVIRONMENT = self.yaml_data['ENVIRONMENT']
        
        # Log the loaded variables for debugging
        logger.debug(f"Loaded SOCRATA_APP_TOKEN: {self.SOCRATA_APP_TOKEN}")
        logger.debug(f"Loaded GOOGLE_CREDENTIALS_FILE: {self.GOOGLE_CREDENTIALS_FILE}")
        logger.debug(f"Loaded GCS_BUCKET_NAME: {self.GCS_BUCKET_NAME}")
        logger.debug(f"Loaded ENVIRONMENT: {self.ENVIRONMENT}")
        

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
        logger.debug(f"GCS_BUCKET_NAME: {self.GCS_BUCKET_NAME}")
        logger.debug(f"GOOGLE_CREDENTIALS_FILE: {'*' * len(self.GOOGLE_CREDENTIALS_FILE) if self.GOOGLE_CREDENTIALS_FILE else 'Not set'}")

# Create a global instance of the config
config = Config()

# You can now import this config object in other files
# from config import config
# Example usage: socrata_token = config.SOCRATA_APP_TOKEN