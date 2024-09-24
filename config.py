import os
from dotenv import load_dotenv
import json
from util.logger import logger

# Load environment variables from .env file
load_dotenv()

# Access environment variables
SOCRATA_APP_TOKEN = os.getenv('SOCRATA_APP_TOKEN')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', '')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')

# Debugging: Print the value of GOOGLE_APPLICATION_CREDENTIALS
# Parse the JSON string for Google Application Credentials
try:
    GOOGLE_APPLICATION_CREDENTIALS_JSON = json.loads(GOOGLE_APPLICATION_CREDENTIALS)
except json.JSONDecodeError as e:
    print(f"Error parsing GOOGLE_APPLICATION_CREDENTIALS: {e}")
    print("Please ensure the JSON string is properly formatted and escaped.")
    GOOGLE_APPLICATION_CREDENTIALS_JSON = None
