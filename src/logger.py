import logging
from logging.handlers import RotatingFileHandler
import os
from datetime import datetime

# Define the log directory and ensure it exists
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Format the current datetime for the log file name
formatted_datetime = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
file_name = os.path.join(log_dir, f"app_{formatted_datetime}.log")

def get_logger():
    """
    Creates and returns a logger instance.
    Ensures that only one instance of the logger is created.
    """
    logger = logging.getLogger('MyAppLogger')
    if not logger.hasHandlers():
        logger.setLevel(logging.INFO)
        
        # Set up the RotatingFileHandler
        handler = RotatingFileHandler(
            filename=file_name, 
            mode='a', 
            maxBytes=5*1024*1024,
            backupCount=2,
            encoding=None, 
            delay=0
        )
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        
        logger.addHandler(handler)
    
    return logger


