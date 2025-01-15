import logging
import os
import json
from api.app.utils.config import Config

config = Config()

def setup_logger(name, log_file='app.log'):
    """Sets up a logger with file and stream handlers."""
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

    # Create a logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
      os.makedirs(log_dir, exist_ok=True)

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    if config.DEBUG:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    return logger