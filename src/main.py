from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules import accounting_ratios as ar
import argparse


def main() -> None:

    logger = get_logger(__name__)
    parser = cli()
    args = parser.parse_args()

    
    logger.info("separate log file")
    shared_logger.info("main entry point")
    ar.logger_test()
    

def cli() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="This program is a CLI tool which allows users to fetch the accounting ratios of listed companies when provided the ticker.")
    return parser

if __name__ == "__main__":
    main()