from src.helper_modules.logger_setup import get_logger, shared_logger
from pathlib import Path

logger = get_logger(__name__)

def main():
    file_path = get_path()
    print(file_path)

def get_path() -> Path:
    """
    prompts user continuously for the desired file path for the excel output 
    
    """

    while True:
        try:
            file_path = Path(input("Please provide desired output file path, must be a directory: ").strip("\" "))
            if not file_path.is_dir():
                print("Please ensure that the provided file path is a directory")
                logger.warning("Invalid file path provided")
                shared_logger.warning("Invalid file path provided")
                continue
            elif str(file_path) == ".":
                print("Please provide a file path")
                logger.warning("File path not provided")
                shared_logger.warning("File path not provided")
                continue
            else:
                print("File path successfully provided")
                logger.info(f"File path successfully provided: {file_path}")
                shared_logger.info(f"File path successfully provided: {file_path}")
                return file_path
        except Exception as e:
            print(e)
            logger.warning("Invalid file path provided")
            shared_logger.warning("Invalid file path provided")
            continue

if __name__ == "__main__":
    main()