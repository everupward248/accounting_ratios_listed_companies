import logging
from src.helper_modules.logger_setup import get_logger, shared_logger


def logger_test():
    shared_logger.info("this is a test")
    logger = get_logger(__name__)
    logger.warning("separate log test")
    shared_logger.debug("another test")