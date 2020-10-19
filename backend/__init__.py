import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))
