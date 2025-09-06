from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules import accounting_ratios as ar
import logging


def main() -> None:
    logger = get_logger(__name__)
    logger.info("separate log file")
    shared_logger.info("main entry point")
    ar.logger_test()

if __name__ == "__main__":
    main()