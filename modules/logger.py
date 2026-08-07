"""
logger.py
BeursSimulator
"""

import logging
from config.instellingen import LOGS

# Zorg dat de map bestaat
LOGS.mkdir(exist_ok=True)

LOGBESTAND = LOGS / "simulator.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-8s | %(message)s",
    datefmt="%d/%m/%Y %H:%M:%S",
    handlers=[
        logging.FileHandler(LOGBESTAND, encoding="utf-8"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger("BeursSimulator")