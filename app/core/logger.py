import logging
import sys
from pathlib import Path
from app.core.config import settings

def setup_logging():
    """
    Configures the root logger for the application.
    """
    # Define the format for log messages
    log_format = "%(asctime)s - %(levelname)-5.5s - [%(name)s] - %(message)s"
    formatter = logging.Formatter(log_format)

    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.LOG_LEVEL.upper())

    # Remove any existing handlers to avoid duplicates
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Add a handler to output logs to the console (stderr)
    console_handler = logging.StreamHandler(sys.stderr)
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # Ensure the directory for the log file exists
    log_file_path = Path(settings.LOG_FILE)
    log_file_path.parent.mkdir(parents=True, exist_ok=True)

    # Add a handler to output logs to a file
    file_handler = logging.FileHandler(str(log_file_path), mode='a')
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)

    logging.info("Logging configured successfully.")
