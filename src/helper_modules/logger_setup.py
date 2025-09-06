import logging



def get_logger(name: str=__name__) -> logging.Logger:
    """
    used to create custom logs for each module

    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # prevent duplicate handlers
    if not logger.handlers:
        handler = logging.FileHandler(f"logs/{name}.log")
        formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d")
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.propagate = False

    return logger


# configure a shared log which logs the program as a whole
# https://medium.com/@shrimantshubham/basic-example-of-log-into-a-single-log-file-from-several-python-modules-090e57ce8f50
shared_logger = logging.getLogger(__name__)
shared_logger.setLevel(logging.DEBUG)

# prevent duplicate handlers
if not shared_logger.handlers:
    handler = logging.FileHandler("shared_log.log", mode="w")
    formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s - %(lineno)d")
    handler.setFormatter(formatter)
    shared_logger.addHandler(handler)
    shared_logger.propagate = False

