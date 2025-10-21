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

    file_name = f"output_{date.today()}.xlsx"

    # make a list of sheet names and zip to match sheet name to financial statement
    sheet_names = ["balance_sheet", "income_statement", "cash_flows"]

    try:
        with pd.ExcelWriter(file / file_name) as writer:
            # iterate through all the provided dfs and use their name as the sheet name
            for df, sheet_name in zip(dfs, sheet_names):
                df.to_excel(writer, sheet_name=sheet_name, header=False)
                logger.info(f"{df} successfully added to excel sheet")
                shared_logger.info(f"{df} successfully added to excel sheet")

            print(f"Excel output successfully created: {file_name}")
    except Exception as e:
        print(e)
        logger.warning(f"{e}")
        shared_logger.warning(f"{e}")