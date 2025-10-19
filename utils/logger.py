import logging
from logging.handlers import RotatingFileHandler
import os

# Create logs directory if it doesn't exist
if not os.path.exists("logs"):
    os.makedirs("logs")

# Logger configuration
logger = logging.getLogger("task_logger")
logger.setLevel(logging.INFO)  # or DEBUG for more details

# Rotating file handler
file_handler = RotatingFileHandler("logs/app.log", maxBytes=5*1024*1024, backupCount=3)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
