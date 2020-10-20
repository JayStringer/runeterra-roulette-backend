"""Backend componenet of Runeterra Roulette web app project"""

import logging
import os
import sys

logging.basicConfig(stream=sys.stdout, level=os.getenv("LOG_LEVEL", "INFO"))
