import sys
import logging


def create_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    log_format = '%(asctime)s %(name)s %(levelname)-8s %(message)s'
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(log_format))
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    return logger
