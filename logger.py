import logging

# Get a logger instance
logger = logging.getLogger(__name__)

# Set the logging level (e.g., to capture all messages from DEBUG and above)
logger.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# Create and set a formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(formatter)

# Attach handler
logger.addHandler(ch)
