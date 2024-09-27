import os
from dotenv import load_dotenv
from pydantic import BaseModel, Field, validator
from typing import Optional
from util.logger import logger
from constants import Environment, EnvironmentVariable

# Load environment variables from .env file
load_dotenv()

# Get the environment from the environment variable
ENVIRONMENT = Environment(os.getenv(EnvironmentVariable.ENVIRONMENT.value, Environment.LOCAL.value))

class ConfigModel(BaseModel):
    ENVIRONMENT: Environment = Field(default=ENVIRONMENT)
    SOCRATA_APP_TOKEN: str
    GCS_BUCKET_NAME: str
    GOOGLE_CREDENTIALS_FILE: Optional[str] = None
    GOOGLE_CREDENTIALS_FILE_LOCAL: Optional[str] = None

    @validator('GOOGLE_CREDENTIALS_FILE', always=True)
    def validate_google_credentials(cls, v, values):
        env = values.get('ENVIRONMENT')
        if env in [Environment.LOCAL, Environment.DOCKER, Environment.REPLIT]:
            if not v:
                raise ValueError(f"GOOGLE_CREDENTIALS_FILE is required for {env} environment")
        return v

    class Config:
        use_enum_values = True

class Config:
    def __init__(self):
        self.load_variables()
        self.validate_config()
        self.log_config()
        
    def load_variables(self):
        env_vars = {
            'ENVIRONMENT': ENVIRONMENT,
            'SOCRATA_APP_TOKEN': os.getenv(EnvironmentVariable.SOCRATA_APP_TOKEN.value),
            'GCS_BUCKET_NAME': os.getenv(EnvironmentVariable.GCS_BUCKET_NAME.value),
        }

        if ENVIRONMENT == Environment.LOCAL:
            env_vars['GOOGLE_CREDENTIALS_FILE'] = os.getenv(EnvironmentVariable.GOOGLE_CREDENTIALS_FILE_LOCAL.value)
        elif ENVIRONMENT in [Environment.DOCKER, Environment.REPLIT]:
            env_vars['GOOGLE_CREDENTIALS_FILE'] = os.getenv(EnvironmentVariable.GOOGLE_CREDENTIALS_FILE.value)

        self.config_model = ConfigModel(**env_vars)
        
    def validate_config(self):
        # Pydantic will automatically validate the config when we create the model
        # If validation fails, it will raise a ValidationError
        pass

    def log_config(self):
        logger.info("Configuration loaded successfully")
        logger.debug(f"Loaded configuration: {self.config_model.dict()}")

    def __getattr__(self, name):
        """
        This method is a Python magic method that's called when an attribute 
        lookup has not found the attribute in the usual places (i.e., it's not 
        an instance attribute or class attribute).

        It delegates attribute access to the self.config_model instance. This allows
        users of the Config class to access the attributes of the Pydantic ConfigModel
        directly through the Config instance, without having to go through 
        config.config_model.ATTRIBUTE_NAME.

        For example, when you do:
            config = Config()
            print(config.SOCRATA_APP_TOKEN)
        
        It's actually accessing config.config_model.SOCRATA_APP_TOKEN behind the scenes,
        but in a more convenient way.

        Args:
            name (str): The name of the attribute being accessed.

        Returns:
            The value of the attribute from the config_model.

        Raises:
            AttributeError: If the attribute is not found in config_model.
        """
        return getattr(self.config_model, name)

# Create a global instance of the config
config = Config()

# You can now import this config object in other files
# from config import config
# Example usage: socrata_token = config.SOCRATA_APP_TOKEN