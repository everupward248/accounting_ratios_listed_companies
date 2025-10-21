from src.helper_modules.logger_setup import get_logger, shared_logger
from src.helper_modules.file import get_path
from pathlib import Path
import pandas as pd 
from datetime import date

logger = get_logger(__name__)

def convert_to_excel(file: Path, *dfs: pd.DataFrame) -> None:
    """
    takes the file path provided by the user and creates an excel document with all the financial data of a listed company
    
    """

    try:
        with pd.ExcelWriter(file / f"output{date.today()}") as writer:
            # iterate through all the provided dfs and use their name as the sheet name
            for df in dfs:
                df.to_excel(writer, sheet_name=f"{df}")
                logger.info(f"{df} successfully added to excel sheet")
                shared_logger.info(f"{df} successfully added to excel sheet")
    except Exception as e:
        print(e)
        logger.info(f"{e}")
        shared_logger.info(f"{e}")