import logging
import os
import sys
from datetime import datetime

LOGS_DIR = "logs"

# Create logs directory if it doesn't exist
os.makedirs(LOGS_DIR, exist_ok=True)

LOG_FILE = os.path.join(LOGS_DIR, f"{datetime.now().strftime('%Y-%m-%d')}.log")

# Configure logging
logging.basicConfig(
    level = logging.INFO,
    format = "%(asctime)s - %(levelname)s - %(message)s",
    handlers = [
        logging.FileHandler(filename=LOG_FILE,mode='a'),  # FileHandler for logging to a file
        logging.StreamHandler(sys.stdout),  # StreamHandler for console output
    ] 
)

logging.getLogger().setLevel(logging.INFO)
logger = logging.getLogger(__name__)