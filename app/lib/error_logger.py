import logging


error_logger = logging.getLogger("error_logger")
error_logger.setLevel(logging.ERROR)

# File handler (logs to a file)
file_handler = logging.FileHandler("error.log", mode="a")
file_handler.setLevel(logging.ERROR)

# Stream handler (logs to the terminal)
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.ERROR)

# Define the log format
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Add handlers to the logger
error_logger.addHandler(file_handler)
error_logger.addHandler(stream_handler)
