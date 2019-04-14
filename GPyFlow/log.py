import logging
import sys
import uuid

format_string = '[%(asctime)s][%(levelname)s]:%(message)s'
datefmt_string = '%Y-%m-%d %H:%M:%S'

LEVEL_DICT = {
    "CRITICAL": logging.CRITICAL,
    "ERROR": logging.ERROR,
    "WARNING": logging.WARNING,
    "INFO": logging.INFO,
    "DEBUG": logging.DEBUG
}


def getlogger(name, file=None, level="INFO"):
    logger = logging.getLogger(name + uuid.uuid4())
    if file:
        handler = logging.FileHandler(file)
    else:
        handler = logging.StreamHandler(sys.stdout)

    formatter = logging.Formatter(format_string, datefmt=datefmt_string)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    if LEVEL_DICT.get(level):
        logger.setLevel(LEVEL_DICT.get(level))
    else:
        logger.setLevel(LEVEL_DICT.get("INFO"))
    return logger
