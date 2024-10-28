import logging
import logging.config
import os

# Define the logging configuration
logging.basicConfig(
      level=logging.DEBUG,
      format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
      handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(os.path.dirname(__file__), 'app.log'), mode='a')
      ]
)

# Get the logger
logger = logging.getLogger(__name__)