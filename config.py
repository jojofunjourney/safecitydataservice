import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
SOCRATA_APP_TOKEN = os.getenv('SOCRATA_APP_TOKEN')
GOOGLE_APPLICATION_CREDENTIALS = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
GCS_BUCKET_NAME = os.getenv('GCS_BUCKET_NAME')