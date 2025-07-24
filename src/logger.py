import logging
import sys

class MaxLevelFilter(logging.Filter):
    def __init__(self, max_level):
        super().__init__()
        self.max_level = max_level
    def filter(self, record):
        return record.levelno <= self.max_level

logger = logging.getLogger()
fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

logger.setLevel(logging.DEBUG)



# stdout handler: DEBUG & INFO
stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(MaxLevelFilter(logging.INFO))
stdout_handler.setFormatter(logging.Formatter(fmt))

# stderr handler: WARNING and above
stderr_handler = logging.StreamHandler(sys.stderr)
stderr_handler.setLevel(logging.WARNING)
stderr_handler.setFormatter(logging.Formatter(fmt))

logger.handlers = []
logger.addHandler(stdout_handler)
logger.addHandler(stderr_handler)